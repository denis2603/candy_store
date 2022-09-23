from vk_api.utils import get_random_id
from vk_api.vk_api import VkApiGroup
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotMessageEvent, VkBotLongPoll
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from setting import VK_KEY, ID_VK_GROUP, VER_VK_API
from app_store.models import Categories, Product


class BotCandy(VkApiGroup):
    """
    Авторизация с токеном группы, работа с VK от имени сообщества.
    """

    def __init__(self, id_vk_group, *args, **kwargs):
        """
        Инициализация бота, создание меню категорий и меню возврата
        :param id_vk_group: ID сообщества в VK
        """
        super().__init__(*args, **kwargs)
        self.__id_vk_group = id_vk_group
        self._categories = list(Categories.objects.all().values_list('title', flat=True))

        keyboard_menu = VkKeyboard(inline=True)
        for category in self._categories:
            keyboard_menu.add_button(label=category.capitalize(), color=VkKeyboardColor.POSITIVE)

        keyboard_back = VkKeyboard(inline=True)
        keyboard_back.add_button('НАЗАД К МЕНЮ', color=VkKeyboardColor.NEGATIVE)

        self.__keyboard_menu = keyboard_menu.get_keyboard()
        self.__keyboard_back = keyboard_back.get_keyboard()
        del keyboard_menu, keyboard_back

    def start(self, wait=10) -> None:
        """
        Запуск прослушивания сервера VK на получение новых событий в сообществе.
        :param wait: время ожидания
        """
        longpoll = VkBotLongPoll(self, self.__id_vk_group, wait=wait)
        for event in longpoll.listen():
            if isinstance(event, VkBotMessageEvent):
                self.message_event_handling(event)

    def message_event_handling(self, event: VkBotMessageEvent) -> None:
        """
        Обработчик поступившего события с типом сообщение.
        :param event: событие
        """

        user_id = event.message.from_id

        if event.message.text in self._categories:
            category = Categories.objects.get(title=event.message.text)
            self.send_product_from_categories(user_id, category)
        else:
            self.send_menu(user_id)

    def add_foto_to_vk(self, path_to_foto: str) -> str:
        """
        Загрузка фото на сервер VK и получение id загруженного фото
        :param path_to_foto: Абсолютный путь к файлу с фотографией
        :return: id фото на сервере VK
        """

        upload = VkUpload(self)
        result = upload.photo_messages(path_to_foto)
        id_foto = result[0].get('id')
        return id_foto

    def send_menu(self, user_id: str) -> None:
        """
        Отправка меню категорий пользователю от имени сообщества.
        :param user_id: id пользователя.
        """

        values = {
            'user_id': user_id,
            'random_id': get_random_id(),
            'message': 'Выберите категорию для просмотра товаров.',
            'keyboard': self.__keyboard_menu,
        }
        self.method('messages.send', values=values)

    def send_product_from_categories(self, user_id: str, category: Categories) -> None:
        """
        Отправка продуктов из категории пользователю от имени сообщества.
        :param user_id: id пользователя.
        :param category: категория продуктов.
        """

        products = Product.objects.filter(category=category)
        for product in products:
            values = {
                'user_id': user_id,
                'random_id': get_random_id(),
                'message': f'{product.name.upper()}\n{product.description}\n{product.price} руб.',
                'keyboard': VkKeyboard().get_empty_keyboard(),
                'attachment': f'photo-{self.__id_vk_group}_{product.id_foto_vk}',
            }
            self.method('messages.send', values=values)

        values = {
            'user_id': user_id,
            'random_id': get_random_id(),
            'message': f'Это все товары в категории {category.title.upper()}',
            'keyboard': self.__keyboard_back,
        }
        self.method('messages.send', values=values)


bot_candy = BotCandy(token=VK_KEY, api_version=VER_VK_API, id_vk_group=ID_VK_GROUP)
