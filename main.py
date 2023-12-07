import disnake
from disnake.ext import commands
import os
import asyncio

from config import TOKEN

bot = commands.InteractionBot(
    intents=disnake.Intents.all()
)


@bot.listen("on_ready")
async def on_ready():
    print("Ready")
    await bot.change_presence(
        activity=disnake.Activity(
            name="за порядком",
            type=disnake.ActivityType.watching
        ),
        status=disnake.Status.idle
    )


async def main():
    for file in os.listdir("cogs"):
        if (file.endswith(".py")) and (not file.startswith(".")):
            try:
                bot.load_extension(f"cogs.{file[:-3]}")
            except Exception as error:
                print(error)
    await bot.start(token=TOKEN)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
