import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id

from setting import VK_KEY, ID_VK_GROUP, VER_VK_API


bot_candy = vk_api.VkApi(token=VK_KEY, api_version=VER_VK_API)


def start(bot_vk_api):

    longpoll = VkBotLongPoll(bot_vk_api, ID_VK_GROUP)

    for event in longpoll.listen():

        print(event)

        if event.type == VkBotEventType.MESSAGE_NEW:



            values = {
                'user_id': event.message.from_id,
                'random_id': get_random_id(),
                'message': f'Вы написали: {event.message.text}',
            }
            print('*' * 45)
            print(values)
            print('*' * 45)
            bot_candy.method('messages.send', values=values)

