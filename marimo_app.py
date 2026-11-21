"""Интерактивный генератор X = количества просмотренных товарных страниц.

Запуск: marimo run marimo_app.py
Публикация: marimo export html-wasm marimo_app.py --single-file -o docs/index.html

Частоты ниже вшиты сборочным скриптом scripts/embed_reference.py: они точно
совпадают с data/online_shoppers_intention.csv, но браузер не загружает CSV.
"""

import marimo

__generated_with = "0.18.0"
app = marimo.App(width="full")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import base64
    import bisect
    import json
    import math
    import random
    import statistics
    import zlib

    return mo, base64, bisect, json, math, random, statistics, zlib


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        <style>
        :root { --canvas:#f8fafc; --ink:#11233a; --blue:#2563eb; --orange:#f97316; }
        .mo-markdown h1 {font-weight:850; letter-spacing:-0.04em; line-height:1.12; color:var(--ink);}
        .mo-markdown h2 {font-weight:770; letter-spacing:-0.025em; color:var(--ink);}
        .mo-markdown p {line-height:1.7;}
        </style>

        # Просмотры страниц и покупка

        **Лабораторная работа 01 · Дополнительное задание КТвД**

        **Выполнила:** Каширина Олеся Сергеевна (ИСУ: 501195)

        В наборе **12 330 сессий** интернет-магазина. Генератор создаёт число просмотренных товарных страниц по фактическим частотам из CSV. Сравните результаты при разных объёмах выборки.

        <span style="color:#64748b">Источник: UCI Online Shoppers Purchasing Intention · Единица X: страницы за сессию, шт.</span>
        """
    )
    return


@app.cell(hide_code=True)
def _(base64, json, zlib):
    # Заменяется командой `python scripts/embed_reference.py` из корня проекта.
    COUNTS_B85 = "c-l2pOO^y72)hsq`6zmpeslk8On}rXB|<<T-M`-wzkl*mIc7kUI2-5^yX+yc0=VH;_ecC4U;-6*#d86lxMuNy&&!}HzM9!^<@MoW_ti&;?F!Z{*3o*zPJg7B6~A7w)s`ow#bXOsRhp^jD;_gk6|=eMEoTc{^)t5UuDb2uqoYzZt3tb?(N|B@`>hL>igGYp<#H3%O5tF(D%HWfDwl(KwFS&tNgd2xp<n6uIfz$%#F8x6P`Q;TOuB?{$>NHT(|((NM@~0AWmgm8Vk(7Cx;uNx>0zksvTu{!cIQ2&RdIV`dWA>&r8^}m@4gb1XFrL`bC&eGk7CM&Hu1+X-NF#>Gp1klo-@mGF#Yz&^gI5|IWeM&OCA5jfGTfd@>NIH;0w{iwxfl`m&tpKruee9sg`Sv{{>(9U+@+01z+ETukv2(QSn^x70<;)I_?s&L&f{n<b67MAI99v>%;SccGOqzcxU1t`QD}dN$>Gm6OV<M#JXy6`orfby5jrT(u=*$=L^=>#k$|e;|EmK2_T|T6+|@n(dtJF4NXQp-$zR84icK`AfeqtBr62e1wcQ;0sV|2CQGTOBcYx#B=Hg-9sKJ+NoPcElLX4?Dj=Lr4&8JP$YwBEE>trHR#~EH)FFUqnmAY_L^EghvqaOFw382_X`T{IqYghr)4UK(`$IHS2vjo;tPrZ1Gy2#_La3$#58HT12-UP7R5SL?Gk)9}llIH=8%**+HO&vzv|p*Fkq?Gy23a3e)BI4)*x%SoHH|v<%LZQ7SE^||w6k%SbwMqCe&i{&G#ZhOd*pen3o4m2dEUGaKjU4Ot*OIS&_4aKb$Fil7?yufi8FXp`swF)iOge*IPW%_KAO$D&6wAixBeO$lm7E=^F`G0_j$KDdFrpAkvz_LpLbiZ{$TyVI4tbkGjH%6!FO!NZN_cp+03&Uw`bn?!<_S>|6!en?>zKR-Y4&qyh+~t{N5n<$1dY8<G4R|>3>=OV;$TR<DS?Xe_uh|#L442d7N{0H6r7b{+zQLc{n#W+I<mcKire}-7_EO;+%(b4j#N`-+d>M@tgPTud{zn{dv;wvR?MV-`vNVJqo@%bmD`18AiL$9tZ0T))mP!`@YxkZ|Y#PKbw2G@8F?-cHjU00rl=r6a"
    _pairs = json.loads(zlib.decompress(base64.b85decode(COUNTS_B85)).decode("utf-8"))
    values = [int(pair[0]) for pair in _pairs]
    counts = [int(pair[1]) for pair in _pairs]
    pop_size = sum(counts)
    assert pop_size == 12330 and values[0] == 0 and values[-1] == 705
    cumulative = []
    _running = 0
    for _c in counts:
        _running += _c
        cumulative.append(_running / pop_size)
    ref_mean = sum(v * c for v, c in zip(values, counts)) / pop_size
    return values, counts, pop_size, cumulative, ref_mean


@app.cell(hide_code=True)
def _(mo):
    n_slider = mo.ui.slider(100, 20000, value=5000, step=100, label="Число сгенерированных сессий")
    seed_slider = mo.ui.slider(0, 9999, value=2026, step=1, label="Seed генератора")
    plot_type = mo.ui.dropdown(
        options={"Частоты по группам": "bars", "Накопленное распределение": "cdf"},
        value="Частоты по группам", label="Тип визуализации"
    )
    mo.vstack([mo.hstack([n_slider, seed_slider], gap=3), plot_type], gap=1)
    return n_slider, seed_slider, plot_type


@app.cell(hide_code=True)
def _(bisect, cumulative, n_slider, random, seed_slider, values, ref_mean, math, mo):
    _rng = random.Random(int(seed_slider.value))
    generated = [values[bisect.bisect_left(cumulative, _rng.random())]
                 for _ in range(int(n_slider.value))]
    generated_mean = sum(generated) / len(generated)
    generated_std = math.sqrt(sum((v-generated_mean)**2 for v in generated)/len(generated))
    _sorted_generated = sorted(generated)
    _ref_diff = max(abs(cumulative[i] - bisect.bisect_right(_sorted_generated, val)/len(generated))
                    for i, val in enumerate(values))
    _dkw = math.sqrt(math.log(2 / 0.05)/(2 * len(generated)))
    mo.md(
        f"""
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(175px,1fr));gap:12px;margin:20px 0 12px">
          <div style="background:#edf4ff;border-radius:14px;padding:18px"><div style="color:#475569;font-size:12px">Реальные: среднее</div><div style="font-size:28px;font-weight:800;color:#1d4ed8">{ref_mean:.2f}</div><div style="font-size:12px;color:#64748b">страниц за сессию</div></div>
          <div style="background:#fff1e6;border-radius:14px;padding:18px"><div style="color:#475569;font-size:12px">Генератор: среднее</div><div style="font-size:28px;font-weight:800;color:#c2410c">{generated_mean:.2f}</div><div style="font-size:12px;color:#64748b">страниц за сессию</div></div>
          <div style="background:#ecfdf5;border-radius:14px;padding:18px"><div style="color:#475569;font-size:12px">Расстояние CDF, D</div><div style="font-size:28px;font-weight:800;color:#047857">{_ref_diff:.4f}</div><div style="font-size:12px;color:#64748b">DKW-граница {_dkw:.4f}</div></div>
          <div style="background:#f1f5f9;border-radius:14px;padding:18px"><div style="color:#475569;font-size:12px">Стандартное отклонение</div><div style="font-size:28px;font-weight:800;color:#334155">{generated_std:.2f}</div><div style="font-size:12px;color:#64748b">страниц · генератор</div></div>
        </div>
        """
    )
    return generated, generated_mean, generated_std


@app.cell(hide_code=True)
def _(mo, generated, counts, values, pop_size, plot_type, bisect):
    _W, _H = 960, 380
    _left, _top, _draw_w, _draw_h = 65, 26, 860, 292
    _parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {_W} {_H}" role="img" aria-label="Сравнение реального и сгенерированного распределений" style="width:100%;height:auto;background:#fff;border:1px solid #e2e8f0;border-radius:14px">']
    if plot_type.value == 'bars':
        _labels = ['0','1–5','6–15','16–30','31–60','61+']
        def bucket(v):
            if v == 0: return 0
            if v <= 5: return 1
            if v <= 15: return 2
            if v <= 30: return 3
            if v <= 60: return 4
            return 5
        _real = [0]*6
        _gen = [0]*6
        for _v, _c in zip(values, counts): _real[bucket(_v)] += _c
        for _v in generated: _gen[bucket(_v)] += 1
        _max_share = max(max(_real)/pop_size, max(_gen)/len(generated))*1.12
    else:
        _max_share = 1.0
    for _t in [0, .25, .5, .75, 1]:
        _yy = _top + (1 - _t)*_draw_h
        _parts.append(f'<line x1="{_left}" x2="{_left+_draw_w}" y1="{_yy}" y2="{_yy}" stroke="#e2e8f0" stroke-dasharray="3 5"/><text x="{_left-12}" y="{_yy+4}" text-anchor="end" font-size="12" fill="#64748b">{_t*_max_share:.0%}</text>')
    if plot_type.value == 'bars':
        _step = _draw_w/6
        for _i, _label in enumerate(_labels):
            _a = _real[_i]/pop_size
            _b = _gen[_i]/len(generated)
            _x0 = _left + _i*_step + 30
            for _offset, _value, _color in [(0,_a,'#2563eb'), (43,_b,'#f97316')]:
                _bar_h = _value/_max_share*_draw_h
                _parts.append(f'<rect x="{_x0+_offset:.1f}" y="{_top+_draw_h-_bar_h:.1f}" width="38" height="{_bar_h:.1f}" rx="4" fill="{_color}"/>')
            _parts.append(f'<text x="{_left+(_i+.5)*_step:.1f}" y="{_top+_draw_h+26}" text-anchor="middle" fill="#475569" font-size="13">{_label}</text>')
        _parts.append(f'<text x="{_left+_draw_w/2}" y="{_H-12}" text-anchor="middle" fill="#475569" font-size="13">Просмотренные товарные страницы, шт.</text>')
    else:
        _xmax = max(values)
        _real_y = 0
        _real = []
        for _v,_c in zip(values,counts):
            _real_y += _c
            _real.append((_v, _real_y/pop_size))
        _sg = sorted(generated)
        _gen = [(val, bisect.bisect_right(_sg, val)/len(_sg)) for val in values]
        for _curve, _color in [(_real,'#2563eb'), (_gen,'#f97316')]:
            _points = ' '.join(f'{_left+_v/_xmax*_draw_w:.1f},{_top+(1-_p)*_draw_h:.1f}' for _v,_p in _curve)
            _parts.append(f'<polyline points="{_points}" fill="none" stroke="{_color}" stroke-width="2.3"/>')
        for _tick in [0, 100, 200, 300, 400, 500, 600, 705]:
            _parts.append(f'<text x="{_left+_tick/_xmax*_draw_w:.1f}" y="{_top+_draw_h+24}" text-anchor="middle" fill="#475569" font-size="12">{_tick}</text>')
        _parts.append(f'<text x="{_left+_draw_w/2}" y="{_H-12}" text-anchor="middle" fill="#475569" font-size="13">Просмотренные товарные страницы, шт.</text>')
    _parts.append('<rect x="740" y="14" width="12" height="12" fill="#2563eb"/><text x="757" y="25" font-size="12" fill="#334155">Реальные</text>')
    _parts.append('<rect x="831" y="14" width="12" height="12" fill="#f97316"/><text x="848" y="25" font-size="12" fill="#334155">Генератор</text>')
    _parts.append('</svg>')
    mo.Html(''.join(_parts))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Как работает алгоритм

        1. Считаем частоты $p_k=n_k/12\,330$ для каждого значения числа страниц.
        2. Строим накопленные вероятности $F(k)=\sum_{j\le k}p_j$.
        3. Генерируем $U\sim\mathrm{Uniform}[0,1)$ и выбираем минимальное $k$ с $F(k)\ge U$.

        $$X^*=F^{-1}(U),\qquad P(X^*\le k)=P(U\le F(k))=F(k).$$

        В отдельной симуляции статистики могут не совпасть точно. При увеличении числа генераций отклонения обычно уменьшаются.

        ### Данные и исследование

        Источник: [UCI Online Shoppers Purchasing Intention](https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset).
        В основном Jupyter Notebook (`notebooks/lab01_ktvd_online_shop.ipynb` в репозитории) приведены EDA обеих величин, математические определения, проверка независимости, моделирование выборок и проверки генератора. [Читать HTML-отчёт](report.html).

        *Примечание:* генератор воспроизводит распределение числа просмотров, но **не** предсказывает результат покупки и не порождает новые уникальные пользовательские траектории. `seed` задаёт воспроизводимую псевдослучайную последовательность.
        """
    )
    return


if __name__ == "__main__":
    app.run()

