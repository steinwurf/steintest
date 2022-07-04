import aiortc
import websockets
import asyncio


async def hello():
    async with websockets.connect("ws://159.89.44.76:8080/") as websocket:

        rtcpeerconnection = aiortc.RTCPeerConnection()

        rtcpeerconnection.createDataChannel("dc")

        await rtcpeerconnection.createOffer()

        rtcpeerconnection.setLocalDescription(localsdp)

        websocket.send(localsdp)


asyncio.run(hello())
