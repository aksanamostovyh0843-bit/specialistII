import numpy as np

class LinearRegression:
    def __init__(self, method='analytical', learning_rate=0.01, n_iters=1000):
        self.method = method  # 'analytical' или 'gradient'
        self.lr = learning_rate
        self.n_iters = n_iters
        self.bias = None
        self.weights = None

    def fit(self, X, y):
        n_samples, n_features = X.shape
        
        # Инициализация параметров
        self.bias = 0
        self.weights = np.zeros(n_features)

        if self.method == 'analytical':
            # Добавляем столбец единиц для смещения
            X_aug = np.c_[np.ones(n_samples), X]
            # Решение нормального уравнения
            theta = np.linalg.inv(X_aug.T.dot(X_aug)).dot(X_aug.T).dot(y)
            self.bias = theta[0]
            self.weights = theta[1:]

        elif self.method == 'gradient':
            # Градиентный спуск
            for _ in range(self.n_iters):
                y_pred = self.bias + np.dot(X, self.weights)
                
                # Вычисление градиентов
                db = (2 / n_samples) * np.sum(y_pred - y)
                dw = (2 / n_samples) * np.dot(X.T, (y_pred - y))
                
                # Обновление параметров
                self.bias -= self.lr * db
                self.weights -= self.lr * dw

    def predict(self, X):
        return self.bias + np.dot(X, self.weights)

# Пример использования
if __name__ == "__main__":
    # Исходные данные
    X = np.array([[1, 2], [2, 4], [3, 1], [4, 3], [5, 5]])
    y = np.array([3, 5, 4, 6, 8])
    
    # Обучение модели
    model = LinearRegression(method='gradient', learning_rate=0.1, n_iters=500)
    model.fit(X, y)
    
    # Параметры модели
    print(f"Смещение (bias): {model.bias:.4f}")
    print(f"Веса (weights): {np.round(model.weights, 4)}")
    
    # Прогнозирование
    X_test = np.array([[2, 3], [6, 2]])
    print("Прогнозы:", np.round(model.predict(X_test), 4))