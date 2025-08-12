import cv2
import numpy as np

def main():
    # Загрузка изображения
    image = cv2.imread('image.jpg')  # Замените 'image.jpg' на путь к вашему изображению
    
    if image is None:
        print("Ошибка: Не удалось загрузить изображение.")
        return
    
    # Создание копии для отображения информации
    original_image = image.copy()
    
    # 1. Преобразование в оттенки серого
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 2. Размытие изображения (сглаживание)
    blurred_image = cv2.GaussianBlur(gray_image, (7, 7), 0)
    
    # 3. Обнаружение краев (детектор Канни)
    edges = cv2.Canny(blurred_image, 50, 150)
    
    # 4. Инвертирование цветов
    inverted_image = cv2.bitwise_not(image)
    
    # 5. Рисование элементов на изображении
    # - Текст
    cv2.putText(image, "OpenCV Demo", (50, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    # - Линия
    cv2.line(image, (0, 0), (image.shape[1], image.shape[0]), (255, 0, 0), 2)
    # - Прямоугольник
    cv2.rectangle(image, (100, 100), (300, 300), (0, 0, 255), 2)
    # - Круг
    cv2.circle(image, (200, 200), 50, (255, 255, 0), 2)
    
    # Создаем мозаику из всех обработанных изображений
    top_row = np.hstack((original_image, inverted_image))
    bottom_row = np.hstack((cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR), image))
    mosaic = np.vstack((top_row, bottom_row))
    
    # Изменение размера мозаики для удобного отображения
    scale_percent = 60  # уменьшаем размер на 40%
    width = int(mosaic.shape[1] * scale_percent / 100)
    height = int(mosaic.shape[0] * scale_percent / 100)
    resized_mosaic = cv2.resize(mosaic, (width, height))
    
    # Отображение результатов
    cv2.imshow('Обработка изображений - OpenCV', resized_mosaic)
    
    # Сохранение результата
    cv2.imwrite('processed_image.jpg', mosaic)
    print("Результат сохранен как 'processed_image.jpg'")
    
    # Ожидание нажатия клавиши и закрытие окон
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()