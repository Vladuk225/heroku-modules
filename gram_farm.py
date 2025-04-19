# meta developer: @Vladislav_225

from .. import loader, utils
import asyncio


class GramFarmMod(loader.Module):
    """Фарм в @valyutaTG_bot"""
    strings = {"name": "GramFarm"}

    def __init__(self):
        self._farm_enabled = False
        self._task = None
        self._bot_username = "@valyutaTG_bot"

    async def client_ready(self, client, db):
        self.client = client

    async def gramfarmoncmd(self, message):
        """Включить фарму"""
        if self._farm_enabled:
            await message.edit("⚠️ Фарм уже включён.")
            return

        self._farm_enabled = True
        self._task = asyncio.create_task(self._farm_loop())
        await message.edit("✅ Фарма включена в @valyutaTG_bot")

    async def gramfarmoffcmd(self, message):
        """Выключить фарму"""
        if not self._farm_enabled:
            await message.edit("⚠️ Фарм уже выключен.")
            return

        self._farm_enabled = False
        if self._task:
            self._task.cancel()
            self._task = None
        await message.edit("❌ Фарм .gram отключён.")

    async def _farm_loop(self):
        while self._farm_enabled:
            try:
                await self.client.send_message(self._bot_username, "бонус")
            except Exception as e:
                print(f"[GramFarm] Ошибка отправки бонуса: {e}")
            await asyncio.sleep(86400)
