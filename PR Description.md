# 📦 Crypto Analyzer (OOP + SOLID)

## 🧠 Общая идея проекта

Проект — это крипто-анализатор, который:
- получает данные о криптовалютах из API
- анализирует их (рост / падение)
- выводит результат в разных форматах (console / json / csv)

---

## 🏗 Архитектура

```
CLI → Provider → Portfolio → Formatter
```

---

## 📁 Структура проекта

```
analyz/
│
├── main.py                  # точка входа (CLI)
│
├── models/
│   ├── crypto_asset.py      # одна криптовалюта (сущность)
│   └── portfolio.py        # логика анализа списка крипты
│
├── providers/
│   ├── coingecko.py        # API CoinGecko
│   ├── coinmarketcap.py    # API CoinMarketCap
│   └── factory.py          # выбор провайдера
│
├── formatters/
│   ├── console.py          # вывод в терминал
│   ├── json.py             # JSON вывод
│   ├── csv.py              # CSV вывод
│   └── factory.py          # выбор формата
│
└── venv/
```

---

## 🧱 CryptoAsset

Одна криптовалюта.

Поля:
- name
- symbol
- price
- change_24h

---

## 📊 CryptoPortfolio

Анализирует список крипты:

- top_gainers(n)
- top_losers(n)
- filter_positive()
- filter_negative()

---

## 🌐 Providers

Отвечают за получение данных из API:

- CoinGecko
- CoinMarketCap

👉 НЕ делают анализ, только получают данные.

---

## 🖨 Formatters

Отвечают за вывод:

- Console → терминал
- JSON → структурированный вывод
- CSV → файл

---

## ⚙️ main.py

Связывает всё вместе:

1. берёт аргументы CLI
2. выбирает provider
3. получает данные
4. анализирует через portfolio
5. выводит через formatter

---

## 🧩 CLI

```
--source  coingecko / coinmarketcap
--output  console / json / csv
--top     количество монет
```

---

## 🚀 Пример запуска

```
python main.py --source coingecko --output json --top 5
```

---

## 🧠 SOLID

✔ S — каждый класс делает 1 задачу  
✔ O — можно добавлять новые форматы/провайдеры  
✔ D — main зависит от абстракций  

---

## 🏁 Итог

Это мини backend-архитектура:
- API слой
- Domain слой
- Presentation слой


24.04.2026 

## 📦 Что сделано

Добавлены comprehensive unit-тесты для крипто-анализатора. Покрытие кода — **96%**.

## 🆕 Добавленные файлы

| Файл | Назначение |
|------|-----------|
| `decorators.py` | Декоратор `@retry` для повторных попыток при ошибках API |
| `tests/conftest.py` | Общие фикстуры — тестовые данные, моки API, моки HTTP, моки окружения |
| `tests/test_models.py` | Тесты модели `CryptoAsset` — создание, валидация, магические методы, edge cases |
| `tests/test_collection.py` | Тесты `CryptoPortfolio` — top gainers/losers, volume, итерация, доступ по ключу |
| `tests/test_providers.py` | Тесты провайдеров с замокированными HTTP-запросами |
| `tests/test_decorators.py` | Тесты декоратора `@retry` — повторы, лимит попыток, интеграция |
| `tests/test_output_formatters.py` | Тесты форматтеров — Console, JSON, CSV, полиморфизм |
| `tests/test_factory.py` | Тесты фабрик — ProviderFactory, FormatterFactory |

## 🔧 Изменения в существующем коде

| Файл | Что изменено |
|------|-------------|
| `models/crypto_asset.py` | Добавлена **валидация** в `__init__` — проверка на пустые строки и типы |
| `models/portfolio.py` | Добавлены **`__getitem__`** (доступ по индексу) и **`total_volume()`** (объём) |
| `providers/coinmarketcap.py` | Наследование от `CryptoProvider`, декоратор `@retry`, удалён закомментированный код |
| `providers/coingecko.py` | Декоратор `@retry`, удалён закомментированный код |
| `main.py` | Убран костыль приведения типов |

## 🧪 Виды тестов

- **Unit-тесты** — модель данных и коллекция (60+ тестов)
- **Тесты с моками** — API-запросы замокированы, тесты работают без интернета (16 тестов)
- **Параметризованные тесты** — `@pytest.mark.parametrize` для однотипных проверок (20+ параметризаций)
- **Тесты декоратора** — `@retry`, проверка повторов и лимита попыток (15 тестов)
- **Тесты форматтеров** — JSON, CSV, Console через единый интерфейс (29 тестов)
- **Тесты фабрик** — ProviderFactory, FormatterFactory (8 тестов)
- **Тесты полиморфизма** — LSP для провайдеров и форматтеров

**Всего: 130+ тестов, все проходят.**

## 🔍 Edge cases покрыты

- Пустые/некорректные данные — валидация (пустые строки, неверные типы)
- Отсутствие API ключа, некорректные/пустые ответы API, отсутствующие поля в JSON
- Отрицательные и нулевые значения, очень большие/маленькие числа
- Юникод и спецсимволы в названиях
- Сравнение с неподдерживаемыми типами (NotImplemented)
- Все попытки retry неудачны, неподдерживаемые исключения
- Сохранение метаданных функции после декорирования
- Пустые списки во всех компонентах

## 🚀 Запуск тестов

```bash
# Все тесты
pytest -v

# С покрытием
pytest --cov=. --cov-report=term -v

# HTML-отчёт
pytest --cov=. --cov-report=html
