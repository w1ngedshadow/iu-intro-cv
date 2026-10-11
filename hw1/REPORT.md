# ДЗ 1 «Фотолаборатория» — отчёт

**Автор:** Egor Goroshko · **Группа / трек:** B24-MFAI-01 · **Дата подготовки:** 11.10.2026

## 1. Числа

### 1.1. Гамма

`data/dark.jpg`, `--gamma 0.5` и `--gamma 2`.

| γ | среднее | медиана | p1 | p99 | обрезано чёрных, % | обрезано белых, % |
| --- | --- | --- | --- | --- | --- | --- |
| исходник | 13.4 | 13 | 0 | 25 | 2.30 | 0.00 |
| 0.5 | 56.1 | 58 | 0 | 79 | 2.29 | 0.00 |
| 2.0 | 0.9 | 1 | 0 | 3 | 28.48 | 0.00 |

### 1.2. Баланс белого

`data/bright.jpg`, `--method grey-world` и `--method white-patch --percentile 99`. Каналы: B / G / R.

| Метод | усиление B / G / R | средние до | средние после |
| --- | --- | --- | --- |
| grey-world | 1.501 / 0.991 / 0.755 | 78.3 / 118.7 / 155.9 | 117.7 / 117.7 / 117.7 |
| white-patch (p99) | 2.629 / 1.409 / 1.090 | 78.3 / 118.7 / 155.9 | 205.6 / 167.2 / 169.8 |

Grey-world выровнял средние каналов до 117.7 / 117.7 / 117.7 и уменьшил тёплый оттенок.
White-patch дал холодный оттенок: синий усилен в 2.629 раза; яркие цветные участки упаковки и стола не соответствуют белому, поэтому метод ошибся.

### 1.3. EqualizeHist против CLAHE

`data/dark.jpg`, `--clip 2 --tiles 8`.

| Кадр | σ в тенях | среднее в тенях | среднее в светах |
| --- | --- | --- | --- |
| исходный | 2.6 | 3.6 | 19.0 |
| equalizeHist | 17.4 | 27.8 | 231.6 |
| CLAHE | 4.9 | 10.5 | 30.5 |

### 1.4. Хромакей

`data/object.jpg`, фон `data/bg.jpg`, `--sample 800,600,200,200 --open 5 --close 31 --feather 2`.

| Что | Значение |
| --- | --- |
| границы HSV lo / hi | [11, 126, 40] / [33, 249, 255] |
| доля маски | 22.55% |
| компонент до / после морфологии | 216 / 7 |
| дыр в итоговой маске | 0 |
| `ball-lamp.jpg` курса: recall / precision | 94.6% / 99.9% |

### 1.5. Геометрия

| Что | Файл и параметры | Значение |
| --- | --- | --- |
| поворот: размер до → после, пустой холст | `data/poster.jpg --deg 30` | 1500 × 2000 → 2300 × 2483; 47.5% |
| поворот: размер до → после, пустой холст | `data/poster.jpg --deg -137` | 1500 × 2000 → 2462 × 2486; 51.0% |
| PSNR naive / blur / area к Lanczos | `data/text.jpg --scale 0.25 --report` | 25.5 / 31.1 / 33.3 дБ |
| PSNR naive / blur / area к Lanczos | `data/course/iu-building.jpg --scale 0.25 --report` | 27.9 / 36.0 / 37.2 дБ |
| стороны: верх / право / низ / лево | `data/poster.jpg`, углы ниже | 854.2 / 1236.1 / 942.7 / 1316.7 px |
| выпрямление: пропорции и размер | `data/poster.jpg --aspect 0.707` | 943 × 1334; W/H ≈ 0.707 |
| совпадение с `poster-gt.png` | `data/course/poster-angle.jpg --size 640x905`, углы ниже | 99.1% |

Проверка холста при 30°: `W′ = ceil(1500·|cos30°| + 2000·|sin30°|) = 2300`,
`H′ = ceil(1500·|sin30°| + 2000·|cos30°|) = 2483` — размеры совпали с результатом.
При уменьшении ×0.25 тонкие штрихи верхних индексов у D²f и D³f слились и стали хуже различимы.
Углы своего листа: `180,579,1009,373,1396,1547,505,1855`; `aspect=0.707` выбран для листа A4, поскольку 210/297 ≈ 0.707.
Углы плаката курса: `1290,1010,560,330,600,840,1250,220`; совпадение с эталоном считается после перевода в серый и порога 128.

### 1.6. Контактный лист

N = 20, сетка 4 столбца × 5 строк, ячейки 320 × 240, лист 1320 × 1378 — `out/sheet.jpg`.
Файлы и параметры перечислены в команде `sheet` ниже.

## 2. Три вопроса

**2.1. Какое цветовое пространство выбрано для хромакея и почему? Что было бы в RGB?**

Выбрано HSV: оттенок H и насыщенность S отделены от яркости V.
Это позволяет искать цвет при разном освещении; V оставлен в диапазоне 40–255, а маска занимает 22.55% кадра.
В RGB при изменении яркости меняются все три канала, поэтому узкие границы могут потерять тёмные и светлые участки предмета.

**2.2. Что происходит с гистограммой при γ < 1 и при γ > 1? Куда деваются обрезанные пиксели?**

При γ = 0.5 гистограмма сдвигается вправо: среднее выросло с 13.4 до 56.1, p99 — с 25 до 79.
При γ = 2 она сдвигается влево: среднее стало 0.9, p99 — 3, доля чёрных выросла с 2.30% до 28.48%, а p1 остался равен 0.
Положительная гамма не выводит значения за 0–255, но округление сводит разные тёмные значения к нулю.
Если значение выходит за диапазон при другой коррекции, `np.clip` заменяет его на 0 или 255, и потерянные различия уже не восстановить.

**2.3. Почему CLAHE лучше equalizeHist на вашем фото? Если не лучше — что измерили и почему?**

На моём фото CLAHE слабее увеличил контраст теней: σ = 4.9 против 17.4 у equalizeHist.
Среднее в светах — 30.5 против 231.6, поэтому кадр после CLAHE остался тёмным.
Ограничение усиления CLAHE смягчает обработку, а equalizeHist на этом сильном недосвете делает детали и шум заметнее.

## 3. Где сломалось

`chromakey data/object.jpg --sample 800,600,200,200 --close 9` оставил 6 дыр на блике: там снизилась насыщенность, и пиксели не прошли границы HSV.
Увеличение `--close` до 31 убрало дыры; доля маски выросла с 22.41% до 22.55%.

## 4. Команды

Все результаты повторяет `python run_all.py`. Отдельные команды:

```bash
python photolab.py gamma data/dark.jpg --gamma 0.5 -o out/dark_g05.jpg --hist out/dark_g05_hist.png
python photolab.py gamma data/dark.jpg --gamma 2 -o out/dark_g2.jpg --hist out/dark_g2_hist.png
python photolab.py wb data/bright.jpg --method grey-world -o out/bright_gw.jpg
python photolab.py wb data/bright.jpg --method white-patch -o out/bright_wp.jpg
python photolab.py clahe data/dark.jpg --clip 2 --tiles 8 -o out/dark_clahe.jpg --compare out/dark_compare.jpg --hist out/dark_clahe_hist.png
python photolab.py chromakey data/object.jpg --bg data/bg.jpg --sample 800,600,200,200 --close 9 -o out/object_default.jpg --mask out/object_default_mask.png
python photolab.py chromakey data/object.jpg --bg data/bg.jpg --sample 800,600,200,200 --close 31 -o out/object_on_bg.jpg --mask out/object_mask.png
python photolab.py rotate data/poster.jpg --deg 30 -o out/poster_rot30.jpg
python photolab.py rotate data/poster.jpg --deg -137 -o out/poster_rot_minus137.jpg
python photolab.py resize data/text.jpg --scale 0.25 --method naive --report -o out/text_naive.jpg
python photolab.py resize data/text.jpg --scale 0.25 --method blur -o out/text_blur.jpg
python photolab.py resize data/text.jpg --scale 0.25 --method area -o out/text_small.jpg
python photolab.py resize data/text.jpg --scale 2 -o out/text_big.jpg
python photolab.py rectify data/poster.jpg --corners 180,579,1009,373,1396,1547,505,1855 --aspect 0.707 -o out/poster_front.jpg
python photolab.py chromakey data/course/ball-lamp.jpg --bg data/course/road-cam.jpg --lo 140,121,40 --hi 168,230,255 -o out/course_ball.jpg --mask out/course_ball_mask.png
python photolab.py resize data/course/iu-building.jpg --scale 0.25 --report -o out/course_small.jpg
python photolab.py rectify data/course/poster-angle.jpg --corners 1290,1010,560,330,600,840,1250,220 --size 640x905 -o out/course_poster.jpg
python photolab.py sheet data/dark.jpg out/dark_g05.jpg out/dark_g2.jpg out/dark_clahe.jpg data/bright.jpg out/bright_gw.jpg out/bright_wp.jpg data/object.jpg out/object_default.jpg out/object_on_bg.jpg out/object_mask.png data/poster.jpg out/poster_rot30.jpg out/poster_rot_minus137.jpg out/poster_front.jpg data/text.jpg out/text_naive.jpg out/text_blur.jpg out/text_small.jpg out/text_big.jpg --cols 4 -o out/sheet.jpg
python measure.py
```

`measure.py` считает recall/precision мяча и совпадение плаката с эталоном, сохраняет `measurements.json`.
`run_all.py` также записывает вывод команд в `results.json` и список команд в `commands.txt`.

## 5. Инструменты

Python, NumPy, OpenCV, matplotlib и Pillow; основа — [шаблон курса](https://github.com/afanasyspb/iu-intro-cv).
OpenAI Codex помог подготовить отчет + разобраться в сути дз; проверка — 11 тестов, запуск команд и сравнение с эталонами курса.

