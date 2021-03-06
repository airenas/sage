import asyncio

import socketio
from aiohttp import web

from sage.api.data import DataType, Data, Sender
from sage.logger import logger


class SocketIO:
    def __init__(self, msg_func, port):
        self.__port = port
        logger.info("Init socket IO")
        self.msg_func = msg_func
        self.sio = socketio.AsyncServer(cors_allowed_origins='*')
        self.sio.on("message", self.message)
        self.sio.on("connect", self.connect)
        self.sio.on("disconnect", self.disconnect)
        self.loop = None

    def start(self):
        logger.info("Starting at %d" % self.__port)
        app = web.Application()
        self.sio.attach(app)
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        server = self.loop.create_server(app.make_handler(), port=self.__port)
        self.loop.run_until_complete(server)
        self.loop.run_forever()

    async def message(self, sid, data):
        if data['type'] == "AUDIO":
            self.msg_func(Data(in_type=DataType.AUDIO, who=Sender.USER, data=data['data']))
        else:
            logger.info("message: %s, %s " % (sid, data))
            self.msg_func(Data(in_type=DataType.TEXT, who=Sender.USER, data=data['data']))

    def process(self, d: Data):
        asyncio.run_coroutine_threadsafe(self.send(d), self.loop)

    async def send(self, d: Data):
        if d.type == DataType.TEXT:
            logger.info("sending msg %s" % d.type)
            await self.sio.emit('message', {"type": "TEXT", "data": str(d.data)})
        elif d.type == DataType.STATUS:
            logger.info("sending msg %s" % d.type)
            await self.sio.emit('message', {"type": "STATUS", "data": str(d.data)})
        elif d.type == DataType.SVG:
            logger.info("sending msg %s" % d.type)
            await self.sio.emit('message', {"type": "SVG", "data": str(d.data)})
        else:
            logger.warning("Don't know what to do with %s data" % d.type)

    async def connect(self, sid, environ):
        logger.info("connect: %s " % sid)
        await self.send(Data(in_type=DataType.TEXT, data="Hi"))
        await self.send(Data(in_type=DataType.STATUS, data="waiting"))

    async def disconnect(self, sid):
        logger.info("disconnect: %s " % sid)
