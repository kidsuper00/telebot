import telebot
from config import keys, TOKEN
from utils import ConvertException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_command(message: telebot.types.Message):
    text = ('Чтобы начать работу введите команду боту в следующем формате:\n'
            '<сокращенное имя валюты> <в какую валюту перевести> <количество переводимой валюты>\n'
            'Увидеть список всех доступных валют: /values')
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['help'])
def help_command(message: telebot.types.Message):
    text = ('Вопросы и предложения по боту пиши @kidsssuper')
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values_command(message: telebot.types.Message):
    currencies = '\n'.join(keys.keys())
    text = f'Доступные валюты:\n{currencies}'
    bot.send_message(message.chat.id, text, parse_mode='HTML')



@bot.message_handler(content_types=['text'])
def convert_command(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertException('Слишком мало или много параметров.\nДля помощи используй команды:\n/start\n/help')

        quote, base, amount = [val.lower() for val in values]
        total_base = CryptoConverter.convert(quote, base, amount)

    except ConvertException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)