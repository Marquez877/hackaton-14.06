import pandas as pd

# Загрузка данных
def load_and_clean_data(file_path):
    """Загружает и очищает данные из CSV."""
    # Укажите правильную кодировку для кириллицы
    data = pd.read_csv(file_path, encoding='utf-8')

    # Переименование столбцов для удобства
    data.columns = [
        'id', 'business', 'investment', 'skills',
        'customers', 'mobility', 'competitors', 'problems'
    ]

    # Удаление пропусков и дубликатов
    data = data.dropna()
    data = data.drop_duplicates()

    return data

# Пример использования
file_path = 'data/opros.csv'
data = load_and_clean_data(file_path)

# Вывод первых строк для проверки
print(data.head())


def add_target_column(data):
    """Добавляет целевую переменную в данные."""
    # Пример: метка успеха на основе условия
    data['success'] = data['investment'].apply(lambda x: 1 if x > 500000 else 0)
    return data
