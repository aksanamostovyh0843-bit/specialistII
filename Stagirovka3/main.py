import telebot
from telebot import types
from request import gpt_request
from config import *
import pickle
import os
from mathgenerator import mathgen
import random
from learn import init_learning_module, start_learning_session,learning_sessions, send_question_gpt

def load_user_data(): #загрузка данных из файла
    if os.path.exists('user_data.pkl'):
        with open('user_data.pkl', 'rb') as f:
            return pickle.load(f)
    return {}

def save_user_data(data):#выгрзука данных в файл
    with open('user_data.pkl','wb') as f:
        pickle.dump(data, f)
    
def is_user_registered(user_id): #проверка, что пользователь зарегестрирован
    user_data = load_user_data()
    if str(user_id) in list(user_data.keys()):
        return True
    else:
        return False

def giga(message):
    bot.send_message(message.chat.id,gpt_request(message.text))
    return


bot = telebot.TeleBot(open('api.txt').read()) #Инициализация бота
init_learning_module(bot)
user_progres = {}
math_levels = [[1,2],[3,4],[5,6]]
questions = []
admin_id = ['5062276224']# через запятую можно перечислить несколько админов

def show_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*main_menu.values())
    bot.send_message(message.from_user.id, "Выберите действие:", reply_markup=markup)

def show_questions(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*question_menu.values())
    bot.send_message(message.from_user.id, "Выберите действие:", reply_markup=markup)

def math_game(message):
    if message.text == 'Меню': # Возврат в меню по желанию пользователя
       show_menu(message)
       return
    user_id = str(message.from_user.id)
    global user_progres
    user_progres[user_id] = [0,0,'']
    markup_line = types.InlineKeyboardMarkup()
    level_math = load_user_data()[user_id]['level_math'] # берем данные уровня математики 
    problem, answer = mathgen.genById(math_levels[level_math][random.randint(0,len(math_levels[level_math])-1)])
    problem = problem.replace(r'\cdot','*').replace('$','')
    answer = answer.replace('$','')
    corr = random.randint(0,3)
    for i in range(4):
        _, fake = mathgen.genById(math_levels[level_math][random.randint(0,len(math_levels[level_math])-1)])
        fake = fake.replace('$','')
        btn = types.InlineKeyboardButton(
            text = f'{answer if i==corr else fake}', # если i и corr равны, пишется answer, иначе fake
            callback_data=f'math_{i}_{corr}_{problem}'
        )
        markup_line.add(btn)
    msg = bot.send_message(user_id, f'Решите пример {problem}', reply_markup=markup_line)
    user_progres[user_id][2] = msg.message_id    

def lesson_selection(message):
    if message.text == 'Меню': #если пользователь нажал меню - возвращаемся
        show_menu(message)
        return
    lesson = message.text #считываем урок, который ползователь выбрал
    lesson_folder = lessons[lesson] #считываем путь к конкретной папке
    try:
        send_materials(message,lesson_folder)
        bot.send_message(message.chat.id, f'Файлы урока {lesson} успешно отправлены')
    except BaseException:
        bot.send_message(message.chat.id, 'Ошибка при отправке файлов')
        show_menu(message)
  
def send_materials(message, folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as file:
                bot.send_message(message.from_user.id, f"Текст урока {file.read()}")
        elif filename.endswith(('.jpg','.jpeg','.png')):
            with open(file_path, 'rb') as photo:
                bot.send_photo(message.from_user.id,photo)
        elif filename.endswith(('.mp4','.mov')):
            with open(file_path, 'rb') as video:
                bot.send_video(message.from_user.id,video)
        elif filename.endswith('.pdf'):
            with open(file_path, 'rb') as pdf:
                bot.send_document(message.from_user.id,pdf, caption='Учебный файл')
        elif filename.endswith('.mp3'):
            with open(file_path, 'rb') as audio:
                bot.send_document(message.from_user.id,audio, caption='Аудио файл')


def test_mode(message):
    if message.text == 'Меню': #если пользователь нажал меню - возвращаемся
        show_menu(message)
        return
    global questions, user_progres
    user_id = str(message.from_user.id)
    user_progres[user_id] = [0,0,'']
    markup = types.ReplyKeyboardMarkup()
    markup.add('Меню')
    lesson_name = list(lessons.keys())[int(message.text)-1]
    bot.send_message(user_id, f"Начинает тест по уроку {lesson_name}",reply_markup=markup)
    try:
        questions = open('test_'+str(message.text)+'.txt','r',encoding='utf-8').readlines()
    except BaseException:
        bot.send_message(user_id,'Ошибка чтения файла')
        show_menu(message)
        return
    send_question(message, questions[user_progres[user_id][0]])

def send_question(message, question):
    markup = types.InlineKeyboardMarkup()
    parts = question.split('_')
    user_id = str(message.from_user.id)
    #Сколько будет 2+2?_1_2_3_4_3
    #В переменной parts получим список ['Сколько..','1','2','3','4','3']
    for i, answer in enumerate(parts[1:-1]):
        btn = types.InlineKeyboardButton(
            text = answer,
            callback_data=f'answer_{user_progres[user_id][0]}_{i}_{parts[-1]}'
        )
        markup.add(btn)
    msg = bot.send_message(user_id, f'{user_progres[user_id][0]+1}. Вопрос {parts[0]}',reply_markup=markup)
    user_progres[user_id][2] = msg.message_id

@bot.callback_query_handler(func=lambda call: call.data.startswith("answer_"))
def handle_answer(message):
    _,ques,answ,corr = message.data.split('_')
    user_id = str(message.from_user.id)
    bot.edit_message_text(
        chat_id=user_id,
        message_id=user_progres[user_id][2],
        text=f'{ques} \nНомер ответа - {int(answ)+1}',
        reply_markup=None
    )
    user_progres[user_id][0]+=1
    if int(answ) == int(corr):
        user_progres[user_id][1]+=1
    if user_progres[user_id][0] != len(questions):
        bot.send_message(user_id, 'Следующий вопрос')
        send_question(message, questions[user_progres[user_id][0]])
    else:
        bot.send_message(user_id, 'Тест завершён!')
        bot.send_message(user_id, f'Ты правильно ответил на {user_progres[user_id][1]}'
                         f' из {len(questions)} вопросов')
        user_data = load_user_data()
        score = round(user_progres[user_id][1]*100/len(questions),2)
        if score >= 60:
            user_data[user_id]['level']+=1
            bot.send_message(user_id, 'Вы прошли тест по этому модулю')
        else:
            bot.send_message(user_id, 'Вы не прошли тест, попробуйте снова')
        save_user_data(user_data)
        show_menu(message)
    
@bot.callback_query_handler(func=lambda call: call.data.startswith('math_'))
# срабатывает когда пользователь отправляет ответ на мат. пример
def math_answer(message):
    _,answ,corr,problem = message.data.split('_')
    user_id = str(message.from_user.id)
    bot.edit_message_text(
        chat_id=user_id,
        message_id=user_progres[user_id][2],
        text=f'Пример {problem}, ваш ответ №{answ}',
        reply_markup=None
    )
    user_data = load_user_data()
    user_id = str(message.from_user.id)
    if corr==answ:
        user_data[user_id]['score_math']+=1
        if user_data[user_id]['score_math']>=5:
            if user_data[user_id]['level_math'] <2:
                user_data[user_id]['level_math']+=1
            user_data[user_id]['score_math']=0 
        save_user_data(user_data)
        bot.send_message(user_id,'Правильно!')
    else:
        bot.send_message(user_id,'Не правильно!')
    msg = bot.send_message(user_id,f'Продолжить? Ваши очки - {user_data[user_id]['score_math']}'
                           f', ваш уровень - {user_data[user_id]['level_math']}')
    bot.register_next_step_handler(msg, math_game)



@bot.message_handler(commands=['start']) #определение реакции бота на /start
def send_wecome(message): #функци реакции на /star
    bot.reply_to(message, "Привет! Я учебный бот") #тело программы
    if is_user_registered(message.from_user.id):
        bot.send_message(message.chat.id, f'Зарегестрирован')
        if str(message.from_user.id) in admin_id:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            markup.add(*admin_menu.values())
            bot.send_message(message.chat.id, "Вы администратор, выберите действие", 
                            reply_markup=markup)
        else:
            show_menu(message)
    else:
        bot.send_message(message.chat.id, 'Не зарегестрирован')
        Register_menu(message)

           
    # bot.send_message(message.chat.id, "Выберите действие:", 
    #                  reply_markup=markup)

@bot.message_handler(commands=['register'])
def Register_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_phone = types.KeyboardButton('Отправить номер телефона', request_contact=True)
    markup.add(btn_phone)
    bot.send_message(message.chat.id, 'Просьба пройти регистрацию.\n\n' 
                     '1. Нажмите на кнопку, чтобы отправить номер телефон\n'
                     '2. Затем введите ФИО', reply_markup=markup)

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
   user_id = str(message.from_user.id)#получение ID пользователя
   phone = message.contact.phone_number #получаем номер телефона из сообщения, которое отправили
   user_data = load_user_data() #загружаем информацию о пользователях, которая уже есть
   if user_id not in user_data: #проверяем, что пользователя с таким ID нет
       user_data[user_id] = {} #если его нет, то добавляем в список пользователей
   user_data[user_id]['phone'] = phone #по ID пользователя добавляем поле номер телефона
   user_data[user_id]['level_math'] = 0  # Уровень в математике
   user_data[user_id]['score_math'] = 0  # Счет в математике
   user_data[user_id]['level'] = 0
   save_user_data(user_data) #сохраняем в файл полученную информацию
   bot.send_message(message.chat.id,'Вы зарегестрированы')
   show_menu(message)
#    msg = bot.send_message(message.chat.id, "Теперь введите ваше ФИО:")
#    bot.register_next_step_handler(msg, process_name_step)
    
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
    elif message.text == 'Игра в математику':
       markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
       markup.add("Меню", "Начать!")
       msg = bot.send_message(
           message.chat.id,
           "Добро пожаловать в математический квиз\nнажмите начать",
           reply_markup=markup
       )
       bot.register_next_step_handler(msg, math_game)
    elif message.text == "Начать обучение":
        user_data = load_user_data()
        user_id = str(message.from_user.id)
        level = user_data[user_id]['level']
        #level = 4 # принудительно вывели все уроки, чтобы набрать уровни строчку нужно удалить
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Меню')
        avalible_lessons = list(lessons.keys())[0:level+1]
        for lesson in avalible_lessons:
            markup.add(types.KeyboardButton(lesson))
        msg = bot.send_message(user_id, 'Выберите урок для изучения',
                                reply_markup=markup)
        bot.register_next_step_handler(msg,lesson_selection)
    elif message.text == 'Начать тестирование':
        user_data = load_user_data()
        user_id = str(message.from_user.id)
        level = user_data[user_id]['level']
        markup = types.ReplyKeyboardMarkup()
        for i in range(level+1):
            markup.add(f'{i+1}')
        markup.add('Меню')
        msg = bot.send_message(user_id,"Выберите тест для прохождения",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, test_mode)
    elif message.text == 'Меню':
        show_menu(message) 
    elif message.text == 'Показать пользователей' and str(message.from_user.id) in admin_id:
        user_data = load_user_data()
        for user in user_data.keys():
            bot.send_message(message.from_user.id,f'Пользователь ID {user}, данные {user_data[user]}')
        bot.send_message(message.from_user.id,f'Всего пользователей - {len(user_data.keys())}')
    elif message.text == 'Удалить всех пользователей' and str(message.from_user.id) in admin_id:
        if os.path.exists('user_data.pkl'):
            os.remove('user_data.pkl')
            bot.send_message(message.from_user.id,f'Файл удалён и создан пустым')
            save_user_data({})
            Register_menu(message)
        else:
            bot.send_message(message.from_user.id,f'Файл отсуствует.')
    elif message.text == 'Изучить тему':
        start_learning_session(message)        

@bot.message_handler(content_types=['photo'])
def photoes(message):
    file_id = message.photo[-1].file_id #из полученного сообщения берём фото. 
    # ИД хранится в последнем элементе с помощью обращения к нему мы получаем file id
    file_info = bot.get_file(file_id) #получение информации о самом файле по его ID
    download_file = bot.download_file(file_info.file_path) #загузка файла в оперативную память
    with open('name_file.jpg', 'wb') as new_f: #сохранение файла
        new_f.write(download_file)
    bot.reply_to(message,'Фото сохранено') #отправка уведомления пользователю

@bot.callback_query_handler(func=lambda call: call.data.startswith("learntest_"))
def handle_learning_test_answer(call):
    """Обработка ответов на вопросы теста"""
    chat_id = str(call.message.chat.id)
    session = learning_sessions.get(chat_id)
    if not session or session['stage'] != 'testing':
        return
    
    # print(call.data)
    _, q_idx, a_idx, c_idx = call.data.split('_')
    # print(q_idx,a_idx, c_idx)
    q_idx, a_idx, c_idx = map(int, (q_idx, a_idx, c_idx))
    question = session['questions'][q_idx]
    
    # Формируем ответ
    response_msg = (
        f"{call.message.text}\n\n"
        f" Ваш ответ: {a_idx+1}. {question['options'][a_idx]}\n"
    )
    
    if a_idx+1 == c_idx:
        session['correct_answers'] += 1
        response_msg += " Верно!"
    else:
        response_msg += (
            f" Неверно.\n"
            f" Правильный ответ: {c_idx}. {question['options'][c_idx-1]}"
        )
    
    # Редактируем сообщение
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=session['last_question_msg'],
        text=response_msg
    )
    
    # Следующий вопрос
    send_question_gpt(chat_id, q_idx + 1)


bot.polling() #отправка "настроек" в бот и его активация. 
# Без него бот неактивен 
