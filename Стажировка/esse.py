# for GigaChat
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat as GigaChatLc
#for diagramm
import re
from collections import Counter
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pymorphy3
import nltk
# Загрузка необходимых ресурсов NLTK
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')
#for report
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# класс для API
# sys_promt - директива для модели, user_esse - текст работы , auth - ключ авторизации
def giga_api(sys_promt, user_esse, auth):
  giga = GigaChatLc(credentials=auth,
                  model='GigaChat:latest',
                  verify_ssl_certs=False
                  )
  sys_promt = SystemMessage(content=sys_promt)
  user_esse = HumanMessage(content=user_esse)
  answer = giga([sys_promt,
                  user_esse])
  #print(answer.content)
  #print(answer.response_metadata)
  return answer

def preprocess_text(text):
    # Приведение к нижнему регистру
    text = text.lower()
    # Удаление пунктуации и цифр
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    # Токенизация
    tokens = word_tokenize(text, language='russian')
    # Удаление стоп-слов
    stop_words = set(stopwords.words('russian'))
    tokens = [word for word in tokens if word not in stop_words and len(word) > 1]
    # Лемматизация с pymorphy2
    morph = pymorphy3.MorphAnalyzer()
    lemmatized = [morph.parse(word)[0].normal_form for word in tokens]

    return lemmatized

def save_word_frequency(words):
    # Подсчет частотности слов
    top_n=20
    word_counts = Counter(words)
    most_common = word_counts.most_common(top_n)
    # Подготовка данных для визуализации
    words, counts = zip(*most_common)
    # Создание диаграммы
    plt.figure(figsize=(12, 8))
    plt.bar(words, counts, color='skyblue')
    plt.xlabel('Слова', fontsize=12)
    plt.ylabel('Частота', fontsize=12)
    plt.title(f'Топ-{top_n} самых частых слов', fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig("plot.png")


# text - строка с текстом для построения диаграммы
def dia_word(text):
  processed_words = preprocess_text(text)
  save_word_frequency(processed_words)


# msg - ответ модели, path_pic -путь к диграмме, path_ttf-путь к шрифту
def my_report(msg, path_pic, path_ttf):
  pdfmetrics.registerFont(TTFont('Arial', path_ttf))  # Укажите путь к файлу шрифта

  # 2. Настраиваем стили с использованием зарегистрированного шрифта
  styles = getSampleStyleSheet()
  styles['Normal'].fontName = 'Arial'  # Указываем шрифт для основного текста
  styles['Title'].fontName = 'Arial'   # И для заголовка

  # 3. Создаём PDF
  doc = SimpleDocTemplate("report.pdf", pagesize=letter)
  story = []

  # Добавляем заголовок (теперь с кириллицей)
  title = Paragraph("<b>Оценка эссе</b>", styles['Title'])
  story.append(title)
  story.append(Spacer(1, 0.5 * inch))

  # Добавляем комментарий эксперта (русский текст)
  expert_comment = msg
  story.append(Paragraph(expert_comment, styles['Normal']))
  story.append(Spacer(1, 0.3 * inch))

  # Добавляем техническую информацию
  tech_info = """
  <b>Технические детали:</b><br/>
  - PDF сгенерирован через reportlab
  """
  story.append(Paragraph(tech_info, styles['Normal']))
  story.append(Spacer(1, 0.3 * inch))

  # Добавляем график
  img = Image(path_pic, width=5*inch, height=3*inch)
  story.append(img)

  # Сохраняем PDF
  doc.build(story)
  print("PDF создан: report.pdf")

# Пример использования
if __name__ == "__main__":

  test_pr = """Ты — профессор литературы
  ## Задача
  Оценивать эссе по 5 критериям
  - Аргументация
  - Раскрытие темы
  - Грамотность
  - Структура
  - Оригинальность
  ## Формат ответа
  Краткое резюме по полученному эссе - не более 5 предложений.
  Дополнительно выставление баллов от 0 до 10 по всем критериям и средним за все (от 0 до 5)
  ## Особые указания
  Сигнализировать если:
  1) эссе менее 250 символов"""

  test_es = """ Каким должен быть воспитатель XXI века? Размышляя над этим вопросом, можно
  сказать, что он ничем не отличается от воспитателя XIX и XX веков. Да, воспитатель
  должен идти в ногу со временем. Безусловно, необходимо, чтобы он владел новейшими
  технологиями, готов и умеет непрерывно учиться, способен к ответственным решениям и
  прогнозированию возможных последствий, умеет общаться и сотрудничать, исполнителен
  и продуктивен в выполнении разного рода задач. Он признаёт свободу и толерантность,
  ответственен за себя, семью, коллектив, страну. Воспитатель физически и психически
  выдержан, умеет отдыхать, ведёт здоровый образ жизни.
  Это так, но в первую очередь воспитатель, как и во все времена должен быть
  образцом духовности, воспитанности, порядочным и честным, добрым и справедливым
  человеком. На мой взгляд, эти главные качества воспитателя были и остаются самыми
  необходимыми.
  Бесспорно, труд воспитателя тяжел. Нелегко быть образцом для подражания,
  эталоном порядочности, советчиком, судьей, наставником, быть творцом детской души!
  Но это приятная радостная тяжесть, потому что в основе ее лежит любовь. На курсах
  повышения квалификации нас учили как работать над собой, не во вред себе, своему
  душевному, психическому здоровью. И говорили: «Нельзя любить сильно своих
  воспитанников, это отразится на вашем здоровье». Задумываясь над этой фразой,
  возникает вопрос: «А как можно работать воспитателем и не любить детей?» Ведь рядом
  со мной дети разные, не похожие друг на друга, веселые и любознательные, робкие и
  застенчивые, дерзкие и неугомонные, «молчуны» и «болтушки». И как приятно слышать,
  когда к тебе подходит ребенок и начинает свой диалог со словами: «Мама…, ой, Ксения
  Сергеевна…», а на душе становится так тепло и радостно. Потому что дети чувствуют, я
  люблю их такими, какие они есть. Детский сад и группа, в которой они воспитываются
  для них как второй дом и семья. Главное – создать благоприятную атмосферу для этого.
  Объясняя малышам простые, но удивительные вещи, рассказываю, как важно быть
  добрым и честным, любить себя и своих близких. Очень важно хвалить ребенка, даже
  тогда, когда его успехи очень скромны. Это воспитывает у детей желание сделать
  следующий шаг.
  Я глубоко убеждена, что я выбрала правильный в жизни путь – профессию
  воспитателя. Работая по зову сердца, я могу сказать – профессии лучше моей нет!  """

  #путь к шрифту, например в одной директори с файлом есть файл TIMES.TTF
  path_ttf = 'TIMES.TTF'
  #путь к изображению
  path_pic = 'plot.png'
  auth = 'ВАШ КЛЮЧ ДЛЯ ДОСТУПА'
  answer = giga_api(test_pr, test_es, auth)
  dia_word(test_es)
  my_report(answer.content,path_pic, path_ttf)