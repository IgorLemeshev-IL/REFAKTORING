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

Проект приведён к архитектуре, соответствующей принципам OOP и SOLID,
и готов к расширению без модификации существующего кода.