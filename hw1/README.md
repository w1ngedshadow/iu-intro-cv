# ДЗ 1 Фотолаборатория

Решение — `photolab.py`, отчёт — `REPORT.md`.
Свои фото и эталоны курса находятся в `data/`, результаты — в `out/`.

## Запуск

Нужен Python 3.11. Для отдельного окружения в Windows:

```powershell
python -m venv .venv
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt
& ".\.venv\Scripts\python.exe" run_all.py
& ".\.venv\Scripts\python.exe" -m pytest tests -q
```

В настроенной папке курса из каталога `work/hw1`:

```powershell
& "..\..\.venv\Scripts\python.exe" run_all.py
& "..\..\.venv\Scripts\python.exe" -m pytest tests -q
```

В Linux/macOS после установки зависимостей:

```bash
python run_all.py
python -m pytest tests -q
```

`run_all.py` выполняет команды ниже, записывает их вывод в `out/results.json`,
а список команд — в `out/commands.txt`.
`measure.py` считает recall/precision мяча и совпадение плаката с эталоном;
числа сохраняются в `out/measurements.json`.
Всего в `out/`: 25 изображений и 3 файла с командами и числами.
Контактный лист — `out/sheet.jpg`: 20 изображений, 4 столбца × 5 строк.

## Команды

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

Кэши и виртуальное окружение в сдачу не входят.

Основа — [шаблон и учебные изображения курса](https://github.com/afanasyspb/iu-intro-cv).
