from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import ORJSONResponse, HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from kubernetes import client, config, utils
from kubernetes.stream import stream
from urllib.parse import urlencode, urljoin

from utils import kube, consumers

# import logging
from pathlib import Path
import asyncio


app_url = APIRouter()


# html使用
# 获取当前文件所在的目录
current_dir = Path(__file__).resolve().parent
# 获取上一级目录中的模板目录
templates_dir = current_dir.parent / 'html'
# 配置 Jinja2 模板
print(templates_dir)
templates = Jinja2Templates(directory=templates_dir)


@app_url.get("/version", 
                summary="kubernetes version",
                # description="列出docker的版本等基础信息",
                # response_description="返回一个json类型的数据",
                )
async def version():
    return "1.25"

@app_url.get("/websocket/{namespace}/{pod_name}", 
                summary="kubernetes websocket terminal html",
                description="返回一个静态页面,index.html,主要用于容器terminal测试使用",
                response_description="return index.html",
                response_class=HTMLResponse)
async def websocket(request: Request, namespace: str, pod_name: str):
    return templates.TemplateResponse("index.html", {"request": request, "namespace": namespace, "pod_name": pod_name})


@app_url.websocket("/ws/{namespace}/{pod_name}")
async def websocket_endpoint(websocket: WebSocket, namespace: str, pod_name: str):
    await websocket.accept()

    rows_s = 200
    cols_s = 200
    container = 123
    try:
        container_stream = kube.KubeApi().pod_exec(
                                                namespace=namespace,
                                                pod=pod_name, 
                                                container=container, 
                                                rows=rows_s, 
                                                cols=cols_s)
    except Exception as e:
        print(f"Failed to connect to container: {e}")
        await websocket.send_text("Failed to connect to container.")
        await websocket.close()
    
    if container_stream is None:
        await websocket.send_text("\r\n您没有访问该资源的权限，请联系管理员配置权限\r\n")
        await websocket.close()
    else:
        handler = consumers.K8SStreamHandler(websocket, container_stream)
        await handler.handle_stream()



