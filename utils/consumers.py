from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from utils.kube import KubeApi
from websocket._exceptions import WebSocketConnectionClosedException
from threading import Thread
import asyncio
from starlette.websockets import WebSocketState


class K8SStreamHandler():
    def __init__(self, websocket: WebSocket, container_stream):
        Thread.__init__(self)
        self.websocket = websocket
        self.stream = container_stream

    async def stream_to_websocket(self):
        while self.stream.is_open():
            try:
                try:
                    if self.stream.peek_stdout():
                        stdout = self.stream.read_stdout()
                        await self.websocket.send_text(stdout)
                except Exception as stdout_err:
                    print(f"Error reading stdout: {stdout_err}")

                # try:
                #     if self.stream.peek_stderr():
                #         stderr = self.stream.read_stderr()
                #         await self.websocket.send_text(stderr)
                # except Exception as stderr_err:
                #     print(f"Error reading stderr: {stderr_err}")

                await asyncio.sleep(0.1)
            except Exception as e:
                print(f"Exception occurred: {e}")
                break
        else:
            await self.websocket.close()


    async def websocket_to_container(self):
        """
        处理 WebSocket 接收，将收到的数据写入容器的 stdin。
        """
        try:
            while True:
                data = await self.websocket.receive_text()
                
                self.stream.write_stdin(data)
        except Exception as e:
            print(f"websocket disconnect beacuse: {e}")
            self.stream.write_stdin('exit\r')
            await self.websocket.close()

    async def handle_stream(self):
        """
        同时运行 WebSocket 输入处理和容器输出转发。
        """
        results = await asyncio.gather(
            self.websocket_to_container(),  # 处理 WebSocket 输入并发送给容器
            self.stream_to_websocket(),      # 处理容器输出并发送给 WebSocket
            return_exceptions=True
        )

        # 遍历检查哪个协程抛出异常
        for idx, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"Error in task {idx}: {result}")




# class K8SWatchStreamThread(Thread):
#     def __init__(self, websocket: WebSocket, container_stream):
#         Thread.__init__(self)
#         self.websocket = websocket
#         self.stream = container_stream

#     async def stream_logs_to_websocket(self):
#         try:
#             while True:
#                 line = next(self.stream)
#                 await self.websocket.send_text(line)
#                 await self.websocket.send_text("\r\n")
#         except Exception as e:
#             print("您没有访问该资源的权限，请联系管理员")
#             await self.websocket.send_text("\r\n您没有访问该资源的权限，请联系管理员配置权限\r\n")
#         finally:
#             await self.websocket.close()

#     def run(self):
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
#         loop.run_until_complete(self.stream_logs_to_websocket())



