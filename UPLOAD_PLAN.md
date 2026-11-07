# План: озвучка → рендер → бот → сайт (после сброса квот AI Studio ~10:00)

Порядок озвучки — ORDER.json в ветке tts-data (ключи ru_/he_/ar_/en_ID, голос Charon).
Аудио класть: lam/r/public/aud/<low>/<lang>/<ID>.wav (RU: <lang>=ru, в timing_<low>.json поставить audio и dur).
После аудио: `python3 gen_i18n2.py <Comp> <lang> <low>` (подхватит длительности), затем рендер `npx remotion render <Comp>[-lang] out.mp4 --concurrency=2`.

| Ролик | Remotion | low | Страница сайта | Статус текстов |
|---|---|---|---|---|
| Ламинэктомия HE/AR/EN | Lam-he/ar/en | lam | ops/laminectomy.html | ОДОБРЕНО |
| Кифопластика | Kyph(+he/ar/en) | kyph | ops/kyphoplasty.html | ОДОБРЕНО |
| Артроскопия колена | Arth(+…) | arth | ops/knee-arthroscopy.html | ОДОБРЕНО |
| Перелом лодыжки | AnkleFilm(+…) | ankle | ops/ankle-fracture.html | ОДОБРЕНО |
| Грыжа диска и спондилодез | Fusion(+…) | fusion | ops/fusion-discectomy.html | ОДОБРЕНО |
| Эноксапарин дома | Enox(+…) | enox | ops/enoxaparin-injections.html | ОДОБРЕНО |
| Остеосинтез | Osteo(+…) | osteo | ops/osteosynthesis.html | ОДОБРЕНО |
| Тревожные признаки | Postop(+…) | postop | ops/postop.html | ОДОБРЕНО |
| Не терпите боль годами | Wait(+…) | wait | ops/why-wait.html | ОДОБРЕНО |
| В отделении и выписка | Ward(+…) | ward | ops/after-surgery.html | ОДОБРЕНО |
| Операция на шее спереди (ACDF) | Acdf(+…) | acdf | ops/spine-other.html | ОДОБРЕНО 07.11 |
| Ампутация ноги | Amp(+…) | amp | ops/amputation.html | ОДОБРЕНО 07.11 |
| Передний доступ HE/AR/EN | ant (3D-клипы перерендерить) | ant | ops/thr-anterior.html | ОДОБРЕНО 07.11 |
| Перелом плеча у сустава | Shoulder(+…) | shoulder | ops/shoulder-fracture.html | ОДОБРЕНО 07.11 |
| Перелом запястья | Wrist(+…) | wrist | ops/wrist-fracture.html | ОДОБРЕНО 07.11 |
| Делирий (памятка для близких) | Delir(+…) | delir | ops/delirium.html | ОДОБРЕНО 07.11 |
| Как не упасть | Falls(+…) | falls | ops/falls.html | ОДОБРЕНО 07.11 |
| Боль после операции | Pain(+…) | pain | ops/pain.html | ОДОБРЕНО 07.11 |
| Пролежни | Press(+…) | press | ops/pressure-sores.html | ОДОБРЕНО 07.11 |
| Дыхательные упражнения | Breath(+…) | breath | ops/breathing.html | ОДОБРЕНО 07.11 |
| Ходунки | Walker(+…) | walker | ops/walker.html | ОДОБРЕНО 07.11 |
| Отёк ноги | Swell(+…) | swell | ops/swelling.html | ОДОБРЕНО 07.11 |
| Лестница с тростью | clay lestwalk | — | thr/tkr блок «Лестница» | ОДОБРЕНО |

Загрузка: ветка <name>-video → `python3 tools/putvid2.py <page> <vid> '{"ru":..,"he":..,"ar":..,"en":..}'` → raw-ссылка боту Настроцкп → «ОК» → ff-merge в main → чипы языков на главной и в карте сайта.
