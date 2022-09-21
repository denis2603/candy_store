import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from setting import VK_KEY, ID_VK_GROUP

bot_init = vk_api.VkApi(token=VK_KEY)




def start(bot_vk_api):

    longpoll = VkBotLongPoll(bot_vk_api, ID_VK_GROUP)

    for event in longpoll.listen():
        print(event)
