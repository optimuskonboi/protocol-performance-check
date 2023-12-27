import asyncio
import websockets
import cv2
import glob
import time

async def client_program():
    uri = "ws://localhost:8888"  # Replace with the actual server address
    root = "../images"
    filepaths = glob.glob(root+ str("/*"))
    async with websockets.connect(uri, max_size=1024*1024*1024) as websocket:
        for filepath in filepaths:
            img = cv2.imread(filepath)
            print(filepath, img.shape)
            s = time.time()
            # Send an initial message to the server
            await websocket.send(img.tobytes())
            # Receive and print the server's response
            response = await websocket.recv()
            print("t=",time.time() - s)
            print(f"Received from server: {response}")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(client_program())
