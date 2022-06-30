import asyncio

import socketio
from aiohttp import web

from sage.api.data import DataType, Data, Sender
from sage.logger import logger

sio = socketio.AsyncServer(cors_allowed_origins='*')


class SocketIO:
    def __init__(self, msg_func, port):
        self.__port = port
        logger.info("Init socket IO")
        self.msg_func = msg_func
        sio.on("message", self.message)
        sio.on("connect", self.connect)
        sio.on("disconnect", self.disconnect)

    def start(self):
        logger.info("Starting at %d" % self.__port)
        app = web.Application()
        sio.attach(app)
        # web.run_app(app, port=self.__port)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        server = loop.create_server(app.make_handler(), port=self.__port)
        loop.run_until_complete(server)
        loop.run_forever()

    async def message(self, sid, data):
        logger.info("message: %s, %s " % (sid, data))
        self.msg_func(Data(in_type=DataType.TEXT, who=Sender.USER, data=data))

    def process(self, d: Data):
        asyncio.run(self.send(d))

    async def send(self, d: Data):
        if d.type == DataType.TEXT:
            logger.info("sending msg %s" % d.type)
            await sio.emit('message', {"type": "TEXT", "data": str(d.data)})
        elif d.type == DataType.STATUS:
            logger.info("sending msg %s" % d.type)
            await sio.emit('message', {"type": "STATUS", "data": str(d.data)})
        elif d.type == DataType.SVG:
            logger.info("sending msg %s" % d.type)
            await sio.emit('message', {"type": "SVG", "data": str(d.data)})
        else:
            logger.warning("Don't know what to do with %s data" % d.type)

    async def connect(self, sid, environ):
        logger.info("connect: %s " % sid)
        await self.send(Data(in_type=DataType.TEXT, data="Hi"))

    def disconnect(self, sid):
        logger.info("disconnect: %s " % sid)
