import pandas as pd

def load_and_clean_data(file_path):
    """Загружает, очищает и проверяет данные из CSV."""
    try:
        # Загрузка данных
        data = pd.read_csv(file_path, encoding='utf-8', on_bad_lines='skip', sep=',')
        data.columns = [
            'id', 'business', 'investment', 'skills',
            'customers', 'mobility', 'competitors', 'problems'
        ]

        # Удаление пропущенных значений
        data = data.dropna()

        # Проверка типов данных
        if not pd.api.types.is_numeric_dtype(data['investment']):
            raise ValueError("Столбец 'investment' должен быть числовым.")

        # Проверка уникальности идентификаторов
        if not data['id'].is_unique:
            raise ValueError("Столбец 'id' содержит дубликаты.")

        # Проверка диапазона значений
        if (data['investment'] < 0).any():
            raise ValueError("Столбец 'investment' содержит отрицательные значения.")

        # Удаление дубликатов
        data = data.drop_duplicates()

        # Добавление целевой переменной
        data = add_target_column(data)
        return data

    except pd.errors.ParserError as e:
        print(f"Ошибка при чтении CSV: {e}")
        return pd.DataFrame()
    except ValueError as e:
        print(f"Ошибка проверки данных: {e}")
        return pd.DataFrame()

def add_target_column(data):
    """Добавляет целевую переменную в данные."""
    data['success'] = data['investment'].apply(lambda x: 1 if float(x) > 500000 else 0)
    return data