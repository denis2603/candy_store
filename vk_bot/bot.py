from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from setting import VK_KEY, ID_VK_GROUP, VER_VK_API
from vk_api.utils import get_random_id
from vk_api.vk_api import VkApiGroup
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotMessageEvent, VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardButton, VkKeyboardColor
from setting import VK_KEY, ID_VK_GROUP, VER_VK_API
from app_store.models import Categories, Product


class BotCandy(VkApiGroup):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._categories = list(Categories.objects.all().values_list('title', flat=True))

        keyboard_menu = VkKeyboard(inline=True)
        for category in self._categories:
            keyboard_menu.add_button(label=category.capitalize(), color=VkKeyboardColor.POSITIVE)

        keyboard_back = VkKeyboard(inline=True)
        keyboard_back.add_button('НАЗАД К МЕНЮ', color=VkKeyboardColor.NEGATIVE)

        self._keyboard_menu = keyboard_menu.get_keyboard()
        self._keyboard_back = keyboard_back.get_keyboard()
        del keyboard_back, keyboard_menu

    def event_handling(self, event: VkBotEventType):

        if event.type is VkBotEventType.MESSAGE_NEW and event.message.text in self._categories:
            category = Categories.objects.get(title=event.message.text)
            self.send_product_from_categories(event, category)
        else:
            self.send_menu(event)

    def add_foto_to_vk(self, path_to_foto: str) -> str:
        """
        Загрузка фото на сервер VK и получение id загруженного фото
        """
        upload = VkUpload(self)
        result = upload.photo_messages(path_to_foto)
        id_foto = result[0].get('id')
        return id_foto

    def send_menu(self, event: VkBotMessageEvent) -> None:

        message = event.message

        print(f'из send_menu {message = }, \n {type(message) = }')

        message_to_reply = f'Выберите категорию для просмотра товаров.'

        values = {
            'user_id': message.from_id,
            'random_id': get_random_id(),
            'message': message_to_reply,
            'keyboard': self._keyboard_menu,
            'attachment': '',
        }

        self.method('messages.send', values=values)

    def send_product_from_categories(self, event: VkBotMessageEvent, category: Categories) -> None:

        user_id = event.message.from_id

        values = {
            'user_id': user_id,
            'random_id': get_random_id(),
            'message': f'Товары в категории {category.title}',
            'keyboard': VkKeyboard().get_empty_keyboard(),
        }
        self.method('messages.send', values=values)

        products = Product.objects.filter(category=category)

        for product in products:

            values = {
                'user_id': user_id,
                'random_id': get_random_id(),
                'message': f'{product.name} {product.description} {product.price}',
                'keyboard': VkKeyboard().get_empty_keyboard(),
                'attachment': f'photo-{ID_VK_GROUP}_{product.id_foto_vk}',
            }
            self.method('messages.send', values=values)

        values = {
            'user_id': user_id,
            'random_id': get_random_id(),
            'message': f'Это все товары в категории {category.title}',
            'keyboard': self._keyboard_back,
        }
        self.method('messages.send', values=values)


bot_candy = BotCandy(token=VK_KEY, api_version=VER_VK_API)


def start(bot_vk_api: BotCandy):

    longpoll = VkBotLongPoll(bot_vk_api, ID_VK_GROUP, wait=10)
    for event in longpoll.listen():
        bot_candy.event_handling(event)


if __name__ == '__main__':
    start(bot_candy)
