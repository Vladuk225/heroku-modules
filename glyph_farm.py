# meta developer: @Vladislav_225
from telethon.tl.custom import Button
from telethon import events
import asyncio
import random
from .. import utils, loader


@loader.tds
class GlyphBonusMod(loader.Module):
    """Фарм в боте @GlyphGame_bot"""

    strings = {"name": "GlyphFarm"}

    def __init__(self):
        self.farming_enabled = False
        self.task = None

    async def client_ready(self, client, db):
        self.client = client

    async def glyphcmd(self, message):
        """Запустить вручную: .glyph"""
        await self.send_bonus(message)

    async def glyph_farm_oncmd(self, message):
        """Включить забирания бонуса каждые 24 часа."""
        if self.farming_enabled:
            await message.edit("🔄 Автоклик бонуса уже включён.")
            return
        self.farming_enabled = True
        self.task = asyncio.create_task(self.auto_glyph_loop())
        await message.edit("✅ Автоклик бонуса включён. Каждые 24 часа.")

    async def glyph_farm_offcmd(self, message):
        """Выключить забирания бонуса."""
        if not self.farming_enabled:
            await message.edit("⛔️ Автоклик бонуса уже выключен.")
            return
        self.farming_enabled = False
        if self.task:
            self.task.cancel()
            self.task = None
        await message.edit("❌ Автоклик бонуса выключён.")

    async def auto_glyph_loop(self):
        while self.farming_enabled:
            try:
                await self.send_bonus()
            except Exception as e:
                print(f"[GlyphBonus] Ошибка: {e}")
            await asyncio.sleep(86400)  # 24 часа = 86400 секунд

    async def send_bonus(self, manual_message=None):
        bot_username = "@GlyphGame_bot"

        if manual_message:
            await manual_message.edit(f"🔄 Забираю бонус...")
        else:
            await self.client.send_message("me", "🤖 Прошло 24 часа, забираю бонус...")

        msg = await self.client.send_message(bot_username, "бонус")

        try:
            response = await self.client.wait_event(
                events.NewMessage(
                    from_users=bot_username,
                    chats=bot_username,
                    incoming=True
                ),
                timeout=15
            )
        except asyncio.TimeoutError:
            if manual_message:
                await manual_message.edit("⛔️ Бот не ответил.")
            else:
                await self.client.send_message("me", "⛔️ Бот не ответил.")
            return

        if not response.buttons:
            if manual_message:
                await manual_message.edit("❌ Нет кнопок.")
            else:
                await self.client.send_message("me", "❌ Нет кнопок.")
            return

        buttons = sum(response.buttons, [])
        if len(buttons) < 3:
            if manual_message:
                await manual_message.edit("⚠️ Меньше трёх кнопок.")
            else:
                await self.client.send_message("me", "⚠️ Меньше трёх кнопок.")
            return

        choice = random.choice(buttons[:3])
        await response.click(data=choice.data if choice.data else None)

        text = f"✅ Нажал на кнопку: {choice.text}"
        if manual_message:
            await manual_message.edit(text)
        else:
            await self.client.send_message("me", text)
