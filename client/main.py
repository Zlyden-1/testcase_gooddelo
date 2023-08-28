import socket
import string
import random
import asyncio
import json
from typing import List

import httpx


class ClientApp(object):
    SYMBOLS = string.ascii_letters + string.digits
    MIN_NEW_ENTRIES = 10
    MAX_NEW_ENTRIES = 100
    GET_ENTRIES_LIMIT = 10
    PRINT_DELAY = 10
    BASE_URL = "http://server:8000"

    deleted_entries_counter = 0

    def generate_entries(self, number: int):
        entries_texts: List[str] = []
        for i in range(number):
            text = "".join(random.choices(population=self.SYMBOLS, k=16))
            entries_texts.append(text)
        return entries_texts

    async def add_entries(self, client: httpx.AsyncClient):
        while True:
            number = random.randint(self.MIN_NEW_ENTRIES, self.MAX_NEW_ENTRIES)
            texts = self.generate_entries(number)
            for text in texts:
                data = json.dumps({"text": text})
                responce = await client.post(
                    f"{self.BASE_URL}/new",
                    content="application/json",
                    data=data,
                    headers={"accept": "application/json", "Content-Type": "application/json"},
                )
                if not (responce.status_code == 201):
                    print(responce.json())

    async def get_entries(self, client: httpx.AsyncClient):
        responces = await client.get(f"{self.BASE_URL}/entries/{self.GET_ENTRIES_LIMIT}")
        return responces.json()

    async def delete_entries(self, client: httpx.AsyncClient):
        while True:
            entries = await self.get_entries(client)
            for entry in entries:
                await client.delete(f"{self.BASE_URL}/{entry['uuid']}")
                self.deleted_entries_counter += 1

    async def print_deleted_entries_amount(self):
        while True:
            await asyncio.sleep(self.PRINT_DELAY)
            print(self.deleted_entries_counter)


async def run(app: ClientApp, client: httpx.AsyncClient):
    add = asyncio.create_task(app.add_entries(client))
    delete = asyncio.create_task(app.delete_entries(client))
    print_ = asyncio.create_task(app.print_deleted_entries_amount())
    await add
    await delete
    await print_


async def main():
    app = ClientApp()
    async with httpx.AsyncClient() as client:
        await asyncio.create_task(run(app, client))


def is_port_open(host, port) -> bool:
    s = socket.socket()
    try:
        s.connect((host, port))
        s.settimeout(0.2)
    except:
        return False
    else:
        return True


if __name__ == "__main__":
    server_ready = False
    while not server_ready:
        server_ready = is_port_open("server", 8000)
    asyncio.run(main())
