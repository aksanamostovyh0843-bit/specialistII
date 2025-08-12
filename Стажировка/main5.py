import telebot
from telebot import types
from request import gpt_request
from config import *

def giga(message):
    bot.send_message(message.chat.id,gpt_request(message.text))
    return


bot = telebot.TeleBot(open('api.txt').read()) #Инициализация бота

def show_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*main_menu.values())
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

def show_questions(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*question_menu.values())
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

@bot.message_handler(commands=['start']) #определение реакции бота на /start
def send_wecome(message): #функци реакции на /start
    bot.reply_to(message, "Привет! Я учебный бот") #тело программы
    show_menu(message)
    # bot.send_message(message.chat.id, "Выберите действие:", 
    #                  reply_markup=markup)

@bot.message_handler(func=lambda message:True) #блок обработки текстовых сообщений
def handle_buttons(message): #в эту фун-ю добавляем обработку текста через elif
    if message.text == 'Расписание':
        ph = open('raspisanie_23.jpg','rb') #путь к фото, тип чтения. rb - читать файл
        bot.send_photo(message.chat.id,ph,'Раписание')
        url = 'https://sh23-irkutsk-r138.gosweb.gosuslugi.ru/netcat_files/userfiles/2/Moya_papka/raspisanie_23.jpg'
        bot.send_photo(message.chat.id,url,'Раписание')
        # bot.reply_to(message, "Сейчас лето, занятий нет.") 
        # inline_markup = types.InlineKeyboardMarkup() #создание "шаблона" для инлайн копки
        # btn = types.InlineKeyboardButton( #текст и ссылка для кнопки и её инициализация
        #     text="Летние активности",
        #     url="https://leto.mos.ru/"
        # )
        # inline_markup.add(btn) #добавление кнопки в "шаблон" для инлайн кнопок
        # bot.send_message(message.chat.id, "Лучше посмотри летние активности", 
        #                  reply_markup=inline_markup) #отправка сообщения пользователю с кнопкой
    elif message.text == 'ДЗ':
        doc = open('Это домашнее задание.pdf','rb')
        bot.send_document(message.chat.id, doc,caption='ДЗ',
                          visible_file_name='Абракадабра.pdf')
        # bot.reply_to(message, "У вас каникулы, а всё ДЗ у учителей.")
    elif str(message.text).lower() == 'привет':
        bot.reply_to(message, "Привет!")  
    elif message.text == 'Фото':
        try:
            ph = open('name_file.jpg','rb') #путь к фото, тип чтения. rb - читать файл
            bot.send_photo(message.chat.id,ph,'Ваше последнее фото')
        except BaseException:
            bot.reply_to(message, "Фото отсуствует, отправьте новое.")
    elif message.text == 'Вопрос GigaChat':
        msg = bot.reply_to(message, "Напиши текст запроса для языковой модели")
        bot.register_next_step_handler(msg, giga)
    elif message.text == 'F.A.Q.':
        bot.reply_to(message, "Вы попали в раздел ответов на вопросы, выберите один из вопросов.")
        show_questions(message)
        
@bot.message_handler(content_types=['photo'])
def photoes(message):
    file_id = message.photo[-1].file_id #из полученного сообщения берём фото. 
    # ИД хранится в последнем элементе с помощью обращения к нему мы получаем file id
    file_info = bot.get_file(file_id) #получение информации о самом файле по его ID
    download_file = bot.download_file(file_info.file_path) #загузка файла в оперативную память
    with open('name_file.jpg', 'wb') as new_f: #сохранение файла
        new_f.write(download_file)
    bot.reply_to(message,'Фото сохранено') #отправка уведомления пользователю
    
bot.polling() #отправка "настроек" в бот и его активация. 
# Без него бот неактивен 
