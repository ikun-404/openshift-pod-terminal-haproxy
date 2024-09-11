#! /usr/bin/python3
# -*- coding:utf-8 -*-
# @File:main.py
# @Author:zhou jianhang
# @Time:2024/08/22 10:32:31

from fastapi import FastAPI
import uvicorn
from api.urls import app_url
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

# 获取当前文件所在的目录
current_dir = Path(__file__).resolve().parent
# 静态路径拼接
# 对象转换为字符串
current_dir_str = str(current_dir)
# 拼接
static_files_directory = current_dir_str + "/html/static"
print(static_files_directory)
# 挂载静态文件
app.mount("/static", StaticFiles(directory=static_files_directory), name="static")

# 路由
app.include_router(app_url, tags=["kubernetes-websocket开发"])
# app.include_router(shop, prefix="/shop", tags=["商品中心接口"])

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=12811)

