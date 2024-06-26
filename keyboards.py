from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_keyboard(
        *btns: str,
        placeholder: str = None,
        request_contact: int = None,
        request_location: int = None,
        sizes: tuple[int] = (2,),
):

    keyboard = ReplyKeyboardBuilder()

    for index, text in enumerate(btns, start=0):

        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))

        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:

            keyboard.add(KeyboardButton(text=text))

    return keyboard.adjust(*sizes).as_markup(
        resize_keyboard=True, input_field_placeholder=placeholder)


ADMIN_KEYBOARD = get_keyboard(
    "Реакции за всё время",
    "Реакции за день",
    "Реакции за неделю",
    "Выбери период по реакциям",
    "Топ сообщение за всё время",
    "Топ сообщение за день",
    "Топ сообщение за неделю",
    "Выбрать период по сообщениям",
    placeholder="Выберите действие",
    sizes=(2,),
)

# MESSAGES_KB = get_keyboard(
#     "Статистика по сообщениям",
#     placeholder="Выберите действие",
#     sizes=(2,),
# )
