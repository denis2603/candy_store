from candy_store.wsgi import *  # нужно для корректного запуска django
from vk_bot.bot import bot_candy

bot_candy.start()
