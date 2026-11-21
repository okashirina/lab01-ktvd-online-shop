# Lab 01 · Дополнительное задание КТвД

## Случайные величины в поведении покупателей интернет-магазина

**Выполнила:** Каширина Олеся Сергеевна (ИСУ: 501195)

**Вопрос:** связаны ли количество просмотренных товарных страниц и вероятность покупки?

**Интерактивная страница:** после включения GitHub Pages откроется по адресу
`https://ВАШ_ЛОГИН.github.io/ИМЯ_РЕПОЗИТОРИЯ/`.

**[Читать исследование (Jupyter Notebook)](notebooks/lab01_ktvd_online_shop.ipynb)** — ноутбук с выполненными расчётами и графиками.  
**[Статический HTML-отчёт](docs/report.html)** — тот же отчёт со скрытым кодом (на GitHub исходник HTML может отображаться как файл; для чтения используйте GitHub Pages, адрес `/report.html`).

> **Важно:** GitHub не исполняет HTML прямо внутри README. Чтобы интерактивная страница открывалась по ссылке, нужно один раз включить GitHub Pages из папки `/docs` (инструкция ниже). Сам файл `docs/index.html` уже создан и содержит браузерную версию marimo.

## Результат исследования

В отдельном датасете [Online Shoppers Purchasing Intention](https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset) рассмотрены две случайные величины на одном событии — пользовательской сессии.

| Величина | Столбец | Что измеряет | Тип |
|:--|:--|:--|:--|
| $X$ | `ProductRelated` | Просмотренные страницы товаров, шт. | Дискретная, счётная |
| $Y$ | `Revenue` | Покупка: 0 — нет, 1 — да | Бернулли |

На исходных 12 330 сессиях:

| Показатель | Результат |
|:--|--:|
| Среднее количество просмотренных страниц | 31,73 |
| Медиана просмотренных страниц | 18 |
| Сессии с покупкой | 1 908 (15,47%) |
| Критерий независимости $\chi^2$ | 468,93 (5 степеней свободы) |
| p-value | $4,05\cdot10^{-99}$ |
| V Крамера | 0,195 |

**Вывод:** на уровне значимости 0,05 отвергается гипотеза об отсутствии связи между группами числа просмотров и покупкой. Это статистическая ассоциация, **не доказательство причинного влияния просмотров на покупку**.

## Что выполнено по ТЗ

| Критерий дополнительного задания | Где найти |
|:--|:--|
| Отдельный датасет | `data/online_shoppers_intention.csv` + ссылка и DOI ниже |
| Две случайные величины | Notebook §2 и §3 |
| Строгое математическое обоснование случайных величин | Notebook §2.1 и §3.1, конечное вероятностное пространство и измеримость |
| Эмпирическое обоснование непредсказуемости | Notebook §2.1 и §3.1, условные группы и положительные дисперсии |
| EDA обеих величин | Notebook §2.2, §2.3, §3.2 |
| Проверка гипотезы о зависимости | Notebook §4, таблица сопряжённости, $\chi^2$, p-value, V Крамера |
| Генератор случайной величины | `src/generator.py` + Notebook §6 |
| Математическое обоснование генератора | Notebook §6.1 — квантильное преобразование |
| Сравнение генератора и реальных данных | Notebook §6.2, таблица метрик, CDF и граница DKW |
| Интерактивность | `marimo_app.py` + `docs/index.html` (HTML-WASM) |
| Применение marimo | `marimo_app.py` — реактивные ползунки, выбор графика и результаты |
| Структура, оглавление, якорные ссылки | Notebook, верхнее содержание и разделы |
| Скрытие кода | `docs/report.html` и опубликованный marimo в режиме run |
| Единая визуальная стилистика и единицы | Все графики ноутбука, корректные подписи осей |
| LaTeX-формулы | Markdown-ячейки ноутбука и marimo |
| Выводы и таблица `cat_mark_table` | Notebook §7 |
| Дополнительный материал: выборка и состоятельность | Notebook §5, с/без возвращения |
| Дополнительный материал: автотесты | `tests/test_generator.py` |
| Список литературы | Notebook §8 |

Число **две** выбрано намеренно: это **дополнительное задание КТвД**, а не базовая часть лабораторной для «ИнфоХимии» с тремя величинами.

## Как загрузить на GitHub и открыть страницу

1. Скачайте архив проекта и **распакуйте** его.
2. На [github.com/new](https://github.com/new) создайте **новый публичный репозиторий**, например `lab01-ktvd-online-shop`. При создании можно **не ставить** флажки `Add a README file`, `.gitignore` и `License`: эти файлы/атрибуции уже включены.
3. В пустом репозитории выберите ссылку **uploading an existing file** (или `Add file` → `Upload files`). Перетащите **содержимое папки проекта**, а не сам ZIP. Проверьте, что GitHub видит `README.md`, `marimo_app.py`, папки `data/`, `notebooks/`, `docs/`, `src/` и `tests/`.
4. Нажмите **Commit changes**. Вы не обязаны использовать терминал или git-команды.
5. Откройте **Settings → Pages**. Установите: **Build and deployment → Source: Deploy from a branch → Branch: `main` → Folder: `/docs` → Save**.
6. Через несколько минут на этой же странице появится адрес вида `https://ВАШ_ЛОГИН.github.io/ИМЯ_РЕПОЗИТОРИЯ/`. Это и есть интерактивный генератор. Статический отчёт будет доступен по адресу `https://ВАШ_ЛОГИН.github.io/ИМЯ_РЕПОЗИТОРИЯ/report.html`.
7. По желанию замените в начале README заглушки `ВАШ_ЛОГИН` и `ИМЯ_РЕПОЗИТОРИЯ` реальными значениями и оформите их как Markdown-ссылку на готовую страницу.

**Важно:** браузерной версии marimo для загрузки Python/WebAssembly нужен интернет. После публикации посетителю не нужно устанавливать Python. Если страница запускается не сразу, дождитесь инициализации браузерного окружения.

## Запуск локально (если попросят на защите)

Требуется Python 3.11 или новее.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

python -m pip install -r requirements.txt
python -m marimo run marimo_app.py
```

Откройте адрес, который появится в терминале (обычно `http://localhost:2718`). Для редактирования marimo используйте `python -m marimo edit marimo_app.py`.

Обычный Jupyter Notebook можно открыть командой:

```bash
jupyter notebook notebooks/lab01_ktvd_online_shop.ipynb
```

Сгенерированные выводы и графики уже сохранены внутри `.ipynb`. Если преподаватель просит воспроизвести расчёты, выполните **Run All**. Ноутбук автоматически находит `data/` как из корня проекта, так и из каталога `notebooks/`.

### Проверки и пересборка

```bash
python -m unittest discover -s tests -v
python scripts/embed_reference.py
python -m marimo check marimo_app.py
python -m marimo export html-wasm marimo_app.py --single-file -o docs/index.html --mode run
```

Если нужно заново создать сам ноутбук из исходных Markdown/код-ячеек:

```bash
python scripts/build_notebook.py
python scripts/execute_notebook_inprocess.py
jupyter nbconvert --to html --no-input notebooks/lab01_ktvd_online_shop.ipynb --output report.html --output-dir docs
python scripts/style_report.py
```

Первый шаг пересборки заменяет текущий `.ipynb` новым без результатов, второй повторно заполняет его вычислениями и иллюстрациями.

## Структура проекта

```text
lab01-ktvd-online-shop/
├── README.md
├── requirements.txt
├── data/
│   └── online_shoppers_intention.csv       # исходный датасет UCI
├── notebooks/
│   └── lab01_ktvd_online_shop.ipynb        # исследование с выполненными графиками
├── marimo_app.py                           # интерактивное приложение на Python
├── src/
│   ├── generator.py                       # метод обратной CDF
│   └── stats_utils.py                     # статистические функции
├── tests/
│   └── test_generator.py                  # автотесты
├── scripts/
│   ├── build_notebook.py
│   ├── execute_notebook_inprocess.py
│   └── embed_reference.py
├── docs/
│   ├── index.html                         # интерактивный marimo, GitHub Pages
│   └── report.html                        # полный отчёт без кода
└── .github/workflows/
    └── tests.yml                          # автопроверки после загрузки
```

## Данные, атрибуция и литература

1. Sakar, C. & Kastro, Y. (2018). *Online Shoppers Purchasing Intention Dataset*. UCI Machine Learning Repository. [DOI: 10.24432/C5F88Q](https://doi.org/10.24432/C5F88Q). **Датасет: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)**; источник сохранён без изменения.
2. Devroye, L. (1986). *Non-Uniform Random Variate Generation*. Springer. [Материалы автора](https://luc.devroye.org/rnbookindex.html). Метод инверсии CDF.
3. Python Software Foundation. [`random` и Mersenne Twister](https://docs.python.org/3/library/random.html).
4. [marimo: интерактивные элементы](https://docs.marimo.io/guides/interactivity/) и [HTML-WASM](https://docs.marimo.io/guides/exporting/webassembly_html/).

Проверка воспроизводимости: используется фиксированный `seed=2026`; исходный CSV включён, а частоты, встроенные в опубликованный marimo, пересчитываются скриптом `scripts/embed_reference.py`. **Все выводы ограничены анализом этого набора, не причинной интерпретацией.**

