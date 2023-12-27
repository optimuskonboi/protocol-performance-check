import asyncio
import websockets
import numpy as np

async def handler(websocket, path):
    while True:
        data = await websocket.recv()
        data = np.frombuffer(data, dtype=np.uint8)
        reply = f"Data received as: {data.shape}!"
        await websocket.send(reply)

start_server = websockets.serve(handler, "localhost", 8888, max_size=1024*1024*1024)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
