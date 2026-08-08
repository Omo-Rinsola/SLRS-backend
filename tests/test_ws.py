import asyncio
import websockets


async def test():

    async with websockets.connect("ws://localhost:8000/detection/ws") as ws:
        print("Connected!")
        await ws.send("How fa")
        response = await ws.recv()
        print(f"Response: {response}")
asyncio.run(test())
