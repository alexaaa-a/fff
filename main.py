import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State

state_storage = StateMemoryStorage()

bot = telebot.TeleBot("6350172558:AAF6XvbagrURfZZD26WkK6JfA1Za1a_yAm0",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()
    ideas = State()
    questions = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "регистрация"
text_button_1 = "наши контакты"
text_button_2 = "идеи для проекта"
text_button_3 = "обратная связь"

menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'добро пожаловать в мой первый телеграм-бот! с чего начнём?',
        reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, 'отлично! _как тебя зовут?_')
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, 'приятно познакомиться! `сколько тебе лет?`')
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, 'спасибо за регистрацию!', reply_markup=menu_keyboard)
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id,
                     "наши контакты:\n[мы в вк](https://vk.com/)\n[мы в инстаграме](https://instagram.com/)\n[наш ютуб](https://www.youtube.com)",
                     reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "проект *на какую тему* тебя интересует?", reply_markup=menu_keyboard)


@bot.message_handler(state=PollState.ideas)
def ideas(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['ideas'] = message.text
    bot.send_message(message.chat.id,
                     'спасибо! админ обязательно в скором времени вышлет тебе идею для создания проекта по теме',
                     reply_markup=menu_keyboard)
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "появился вопрос? напиши его сюда, чтобы наш модератор смог тебе ответиить!",
                     reply_markup=menu_keyboard)


@bot.message_handler(state=PollState.age)
def questions(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['questions'] = message.text
    bot.send_message(message.chat.id, 'твой вопрос на рассмотрении! ответим *в течение часа*.',
                     reply_markup=menu_keyboard)
    bot.delete_state(message.from_user.id, message.chat.id)


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()
