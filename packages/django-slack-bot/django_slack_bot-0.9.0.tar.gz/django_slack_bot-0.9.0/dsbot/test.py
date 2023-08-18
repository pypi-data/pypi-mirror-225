from asgiref.sync import async_to_sync

from dsbot import client


class TestClient(client.BotClient):
    @async_to_sync
    async def test_input(self, event, data):
        await self._dispatch_event(event=event, data=data)
