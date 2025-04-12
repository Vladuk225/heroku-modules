from .. import loader, utils
import asyncio

@loader.tds
class MatterDiggerMod(loader.Module):
    """Автокопание материи каждые 10 минут в боте @bforgame_bot"""
    strings = {"name": "MatterDigger"}

    def __init__(self):
        self.running = False

    async def client_ready(self, client, db):
        self.me = await client.get_me()
        self.entity = await client.get_entity("@bforgame_bot")

    async def diggermattercmd(self, message):
        """Включить автокопание материи в @bforgame_bot"""
        if self.running:
            await message.edit("⚠️ Уже запущено.")
            return

        self.running = True
        await message.edit("✅ Запущено автокопание в чате @bforgame_bot")

        while self.running:
            for _ in range(12):
                try:
                    await message.client.send_message(self.entity, "Копать материю")
                    await asyncio.sleep(1)
                except Exception as e:
                    await message.client.send_message(message.chat_id, f"Ошибка: {e}")
                    self.running = False
                    return
            await asyncio.sleep(600)  # 10 минут

    async def stopmattercmd(self, message):
        """Остановить автокопание"""
        self.running = False
        await message.edit("⛔️ Автокопание остановлено.")
