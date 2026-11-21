"""Оформление HTML после nbconvert без изменения текста, формул и графиков.

Запуск из корня проекта: python scripts/style_report.py
Стили встроены в report.html: для просмотра не требуется отдельный CSS.
"""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "docs" / "report.html"
html = path.read_text(encoding="utf-8")

MARKER = 'data-lab-designed="1"'
if MARKER in html:
    print("HTML-отчёт уже оформлен")
    raise SystemExit(0)

STYLES = r"""
<style id="lab-report-style" data-lab-designed="1">
  :root {
    --paper: #ffffff;
    --canvas: #f2f6fb;
    --ink: #18283f;
    --muted: #64748b;
    --blue: #2563eb;
    --orange: #f97316;
    --line: #dce6f1;
  }
  * { box-sizing: border-box; }
  html { scroll-behavior: smooth; }
  body.jp-Notebook {
    font-family: Inter, "Segoe UI", Arial, sans-serif;
    background: var(--canvas);
    color: var(--ink);
    margin: 0;
    padding: 0;
    line-height: 1.7;
    -webkit-font-smoothing: antialiased;
  }
  body.jp-Notebook a { color: var(--blue); text-underline-offset: 3px; }
  body.jp-Notebook a:hover { color: #1d4ed8; }
  body.jp-Notebook a:focus-visible { outline: 3px solid #ffb86c; outline-offset: 3px; }

  .lab-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    padding: 13px max(24px, calc((100vw - 1080px) / 2));
    color: #eaf1ff;
    background: #0d1930;
    border-bottom: 1px solid rgba(255,255,255,.1);
  }
  .lab-brand { display: flex; align-items: center; gap: 12px; font-weight: 750; font-size: .88rem; }
  .lab-brand-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    height: 30px;
    width: 30px;
    border-radius: 9px;
    background: var(--orange);
    color: #1e293b;
    font-size: 12px;
    font-weight: 850;
  }
  .lab-topbar nav { display: flex; align-items: center; gap: 22px; font-size: .81rem; }
  .lab-topbar nav a { color: #dae7fd; text-decoration: none; font-weight: 600; }
  .lab-topbar nav a:hover { color: #fff; }
  .lab-topbar nav a.lab-nav-button {
    color: #fff;
    padding: 8px 13px;
    border: 1px solid rgba(255,255,255,.28);
    border-radius: 9px;
    background: rgba(255,255,255,.09);
  }

  body.jp-Notebook main {
    width: min(1080px, calc(100% - 36px));
    max-width: 1080px;
    margin: 34px auto 0;
    padding: 0 0 45px;
    border-radius: 24px;
    border: 1px solid #e0e8f1;
    background: var(--paper);
    box-shadow: 0 18px 70px rgba(17, 38, 71, .08);
    overflow: hidden;
  }
  body.jp-Notebook main > .jp-Cell { margin: 0; border: none; }

  body.jp-Notebook main > .jp-Cell:first-child {
    position: relative;
    isolation: isolate;
    padding: 55px 60px 48px;
    color: #fff;
    background:
      radial-gradient(circle at 89% 7%, rgba(91,176,255,.47), transparent 37%),
      linear-gradient(127deg, #101d38 2%, #18376b 76%, #214e82 100%);
  }
  body.jp-Notebook main > .jp-Cell:first-child::after {
    content: "";
    position: absolute;
    width: 330px;
    height: 330px;
    right: -100px;
    top: 25px;
    border: 1px solid rgba(194,222,255,.28);
    border-radius: 50%;
    box-shadow: 0 0 0 64px rgba(177,207,252,.055), 0 0 0 128px rgba(177,207,252,.045);
    pointer-events: none;
    z-index: -1;
  }
  body.jp-Notebook main > .jp-Cell:first-child h1 {
    color: #91c9ff;
    font-size: .8rem;
    text-transform: uppercase;
    letter-spacing: .16em;
    font-weight: 800;
    margin: 0 0 20px;
    line-height: 1.45;
    border: 0;
  }
  body.jp-Notebook main > .jp-Cell:first-child h2 {
    color: #fff;
    font-size: 3rem;
    font-size: clamp(2.15rem, 4vw, 3.25rem);
    letter-spacing: -.045em;
    line-height: 1.16;
    font-weight: 800;
    max-width: 790px;
    margin: 0 0 27px;
    border: 0;
  }
  body.jp-Notebook main > .jp-Cell:first-child p {
    color: #d9e8fa;
    line-height: 1.7;
    max-width: 810px;
    margin: 12px 0;
    font-size: 1.03rem;
  }
  body.jp-Notebook main > .jp-Cell:first-child strong { color: #fff; }
  body.jp-Notebook main > .jp-Cell:first-child a { color: #bde3ff; }
  body.jp-Notebook main > .jp-Cell:first-child p:last-of-type {
    display: inline-block;
    border: 1px solid rgba(255,255,255,.24);
    border-radius: 12px;
    background: rgba(255,255,255,.085);
    padding: 10px 16px;
    margin-top: 21px;
    font-size: .91rem;
    line-height: 1.7;
  }
  body.jp-Notebook main > .jp-Cell:first-child .anchor-link { display: none; }

  body.jp-Notebook main > .jp-Cell:nth-child(2) {
    margin: 30px 46px 22px;
    padding: 24px 26px;
    border: 1px solid #dfe8f3;
    border-radius: 16px;
    background: #f8fbff;
  }
  body.jp-Notebook main > .jp-Cell:nth-child(2) h3 {
    font-size: 1.16rem;
    margin: 0 0 13px;
    color: var(--ink);
  }
  body.jp-Notebook main > .jp-Cell:nth-child(2) ol {
    display: grid;
    grid-template-columns: repeat(2,minmax(0,1fr));
    gap: 9px 24px;
    list-style: none;
    padding: 0;
    margin: 0;
  }
  body.jp-Notebook main > .jp-Cell:nth-child(2) ol > li {
    border-left: 3px solid #93b7f5;
    padding: 5px 0 5px 12px;
    font-size: .91rem;
    line-height: 1.45;
  }
  body.jp-Notebook main > .jp-Cell:nth-child(2) ol > li > a { font-weight: 720; text-decoration: none; }
  body.jp-Notebook main > .jp-Cell:nth-child(2) ul { padding-left: 17px; margin: 7px 0 0; }
  body.jp-Notebook main > .jp-Cell:nth-child(2) ul li { margin-top: 4px; font-size: .86rem; }
  body.jp-Notebook main > .jp-Cell:nth-child(2) p:last-child {
    color: var(--muted);
    font-size: .82rem;
    margin: 17px 0 0;
  }

  body.jp-Notebook main > .jp-MarkdownCell:not(:first-child):not(:nth-child(2)) { padding: 9px 58px 2px; }
  body.jp-Notebook main > .jp-CodeCell { padding: 2px 52px 12px; }
  body.jp-Notebook main .jp-RenderedMarkdown {
    color: var(--ink);
    font-family: inherit;
    font-size: 1rem;
    line-height: 1.75;
  }
  body.jp-Notebook main > .jp-MarkdownCell:not(:first-child):not(:nth-child(2)) h2 {
    margin: 23px 0 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--line);
    color: #12294b;
    font-size: 1.63rem;
    font-weight: 770;
    line-height: 1.3;
    letter-spacing: -.02em;
  }
  body.jp-Notebook main h3 { margin: 22px 0 9px; color: #23477d; font-size: 1.2rem; font-weight: 740; }
  body.jp-Notebook main p { margin: 9px 0 13px; }
  body.jp-Notebook main li { margin: 5px 0; }
  body.jp-Notebook main blockquote {
    margin: 16px 0;
    border-left: 4px solid var(--blue);
    border-radius: 0 10px 10px 0;
    background: #f4f8ff;
    padding: 8px 18px;
    color: #334155;
  }
  body.jp-Notebook main .jp-OutputArea { width: 100%; overflow-x: auto; }
  body.jp-Notebook main .jp-OutputArea-output { max-width: 100%; }
  body.jp-Notebook main .jp-OutputArea-output img {
    display: block;
    max-width: 100%;
    height: auto;
    border: 1px solid #e2eaf4;
    border-radius: 13px;
    background: white;
    margin: 10px auto 16px;
    box-shadow: 0 7px 22px rgba(26, 54, 93, .055);
  }
  body.jp-Notebook main table { border-collapse: separate; border-spacing: 0; width: 100%; font-size: .88rem; margin: 12px 0 21px; }
  body.jp-Notebook main table th {
    color: #184076;
    background: #ecf4ff;
    font-weight: 760;
    padding: 11px 12px;
    border-bottom: 1px solid #cbdced;
    text-align: left;
    white-space: normal;
  }
  body.jp-Notebook main table td { padding: 10px 12px; border-bottom: 1px solid #e7eef7; }
  body.jp-Notebook main table tr:nth-child(even) td { background: #f9fbfe; }
  body.jp-Notebook main table tr:hover td { background: #f2f8ff; }
  body.jp-Notebook main mjx-container[display="true"] {
    display: block;
    padding: 12px 6px;
    overflow-x: auto;
    overflow-y: hidden;
    max-width: 100%;
  }
  body.jp-Notebook main .jp-RenderedMarkdown code {
    background: #f0f4fa;
    color: #224d7f;
    padding: 2px 5px;
    border-radius: 5px;
    font-size: .9em;
  }
  body.jp-Notebook main .anchor-link { opacity: .25; margin-left: 7px; }
  body.jp-Notebook main .anchor-link:hover { opacity: 1; }
  body.jp-Notebook main a[id] { scroll-margin-top: 30px; }
  .lab-footer {
    max-width: 1080px;
    margin: 23px auto 42px;
    padding: 0 18px;
    color: #718096;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    font-size: .79rem;
  }
  .lab-footer a { color: #25559a; text-decoration: none; }

  @media (max-width: 760px) {
    .lab-topbar { padding: 13px 18px; }
    .lab-topbar nav { gap: 12px; }
    .lab-topbar nav a:not(.lab-nav-button) { display: none; }
    body.jp-Notebook main { width: calc(100% - 16px); margin-top: 10px; border-radius: 16px; }
    body.jp-Notebook main > .jp-Cell:first-child { padding: 38px 26px 31px; }
    body.jp-Notebook main > .jp-Cell:first-child h2 { font-size: 2.05rem; }
    body.jp-Notebook main > .jp-Cell:nth-child(2) { margin: 16px; padding: 18px; }
    body.jp-Notebook main > .jp-Cell:nth-child(2) ol { grid-template-columns: 1fr; }
    body.jp-Notebook main > .jp-MarkdownCell:not(:first-child):not(:nth-child(2)) { padding: 7px 21px 0; }
    body.jp-Notebook main > .jp-CodeCell { padding: 2px 14px 10px; }
    body.jp-Notebook main table { font-size: .78rem; }
    body.jp-Notebook main table { display: block; overflow-x: auto; white-space: nowrap; }
    body.jp-Notebook main table th, body.jp-Notebook main table td { padding: 8px 7px; }
    body.jp-Notebook main > .jp-MarkdownCell:not(:first-child):not(:nth-child(2)) h2 { font-size: 1.36rem; }
  }
  @media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }
  @media print {
    body.jp-Notebook { background: white; }
    .lab-topbar, .lab-footer { display: none; }
    body.jp-Notebook main { width: 100%; max-width: none; border: 0; border-radius: 0; margin: 0; box-shadow: none; }
    body.jp-Notebook main > .jp-Cell:first-child { print-color-adjust: exact; -webkit-print-color-adjust: exact; }
    body.jp-Notebook main .jp-OutputArea-output img { box-shadow: none; }
  }
</style>
"""

NAV = """
<header class="lab-topbar" aria-label="Навигация по отчёту">
  <div class="lab-brand"><span class="lab-brand-badge">01</span><span>ПРИКЛАДНАЯ СТАТИСТИКА</span></div>
  <nav aria-label="Разделы">
    <a href="#toc">Содержание</a>
    <a href="#resume">Выводы</a>
    <a class="lab-nav-button" href="index.html">Генератор ↗</a>
  </nav>
</header>
"""

FOOTER = """
<footer class="lab-footer">
  <span>Лабораторная работа 01 · КТвД</span>
  <span>Каширина Олеся Сергеевна · ИСУ 501195</span>
  <a href="#top">Наверх ↑</a>
</footer>
"""

if "</head>" not in html or "</main>" not in html or not re.search(r"<body\b[^>]*>", html):
    raise SystemExit("Не найдена ожидаемая структура nbconvert HTML")

chart_descriptions = [
    "Распределение числа товарных страниц: гистограммы и эмпирическая функция распределения",
    "Доли сессий с покупкой и без покупки, доверительный интервал конверсии",
    "Конверсия по числу просмотренных страниц и распределение исходов по группам",
    "Ошибка оценок для выборок с возвращением и без возвращения",
    "Сравнение исходных и сгенерированных распределений числа товарных страниц",
]
missing_alt = 'alt="No description has been provided for this image"'
if html.count(missing_alt) != len(chart_descriptions):
    raise SystemExit("Число графиков изменилось: проверьте подписи в style_report.py")
for description in chart_descriptions:
    html = html.replace(missing_alt, f'alt="{description}"', 1)

html = html.replace('<html lang="en">', '<html lang="ru">', 1)
html = re.sub(r"<title>[^<]*</title>",
              "<title>Лабораторная 01 · Каширина Олеся · КТвД</title>", html, count=1)
html = html.replace("</head>", STYLES + "\n</head>", 1)
html = re.sub(r"(<body\b[^>]*>)", lambda match: match.group(1) + NAV, html, count=1)
html = html.replace("</main>", "</main>" + FOOTER, 1)
path.write_text(html, encoding="utf-8")
print("HTML-отчёт оформлен: обложка, оглавление, таблицы, графики, адаптивная вёрстка")

