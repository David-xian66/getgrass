# -*- coding: utf-8 -*-
import asyncio
import datetime
import random
import ssl
import json
import time
import uuid
import sys
import os

import websockets


def getTime():
    return datetime.datetime.now().strftime('%y.%m.%d-%H:%M:%S.%f')

def getTime_log():
    return datetime.datetime.now().strftime('%y.%m.%d-%H.%M.%S.%f')


runTime = getTime_log()

def setLogFile(log_file_path):
    file = os.path.join(log_file_path, runTime+'.log')
    if os.path.isfile(file):
        # 避免错误
        os.remove(file)
    return file




class logger_():
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path
    def addLogToFile(self, text):
        newLine = True
        if os.path.isfile(self.log_file_path):
            newLine = False
        with open(self.log_file_path, 'a') as f:
            if newLine:
                f.write(str(text))
            else:
                f.write('\n' + str(text))
    def debug(self, text):
        text = '  DEBUG  ' + str(getTime()) + '  ' + str(text)
        print(text)
        self.addLogToFile(text=text)
    def info(self, text):
        text = '  INFO   ' + str(getTime()) + '  ' + str(text)
        print(text)
        self.addLogToFile(text=text)
    def error(self, text):
        text = '  ERROR  ' + str(getTime()) + '  ' + str(text)
        print(text)
        self.addLogToFile(text=text)


async def connect_to_wss(user_id, logger):
    device_id = str(uuid.uuid4())
    logger.info(device_id)
    while True:
        try:
            await asyncio.sleep(random.randint(1, 10) / 10)
            custom_headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            }
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            uri = "wss://proxy.wynd.network:4650/"
            server_hostname = "proxy.wynd.network"
            async with websockets.connect(uri, ssl=ssl_context, extra_headers=custom_headers,
                                          server_hostname=server_hostname) as websocket:
                async def send_ping():
                    while True:
                        send_message = json.dumps(
                            {"id": str(uuid.uuid4()), "version": "1.0.0", "action": "PING", "data": {}})
                        logger.debug(send_message)
                        await websocket.send(send_message)
                        await asyncio.sleep(20)

                await asyncio.sleep(1)
                asyncio.create_task(send_ping())

                while True:
                    response = await websocket.recv()
                    message = json.loads(response)
                    logger.info(message)
                    if message.get("action") == "AUTH":
                        auth_response = {
                            "id": message["id"],
                            "origin_action": "AUTH",
                            "result": {
                                "browser_id": device_id,
                                "user_id": user_id,
                                "user_agent": custom_headers['User-Agent'],
                                "timestamp": int(time.time()),
                                "device_type": "extension",
                                "version": "4.0.2"
                            }
                        }
                        logger.debug(auth_response)
                        await websocket.send(json.dumps(auth_response))

                    elif message.get("action") == "PONG":
                        pong_response = {"id": message["id"], "origin_action": "PONG"}
                        logger.debug(pong_response)
                        await websocket.send(json.dumps(pong_response))
        except Exception as e:
            logger.error(e)


async def main(logger):
    _user_id = '2gxV6b5xWXwFac55zt55B4TFdJ6'
    await connect_to_wss(_user_id, logger)


if __name__ == '__main__':
    # 运行主函数
    path = os.path.dirname(os.path.abspath(__file__))
    log_file_path = setLogFile(path)
    logger = logger_(log_file_path=log_file_path)
    asyncio.run(main(logger))
