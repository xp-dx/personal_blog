from datetime import datetime

date_object = datetime(2023, 10, 21)  # Создаём объект даты
print(date_object.strftime("%B %-d, %Y"))  # Результат: "Март"
