"""Повторяет обработку фотографий и сохраняет числа для отчёта."""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
sys.stdout.reconfigure(encoding="utf-8")
Path("out").mkdir(exist_ok=True)

# Каждая строка — обычная команда для photolab.py.
commands = [
    "gamma data/dark.jpg --gamma 0.5 -o out/dark_g05.jpg --hist out/dark_g05_hist.png",
    "gamma data/dark.jpg --gamma 2 -o out/dark_g2.jpg --hist out/dark_g2_hist.png",
    "wb data/bright.jpg --method grey-world -o out/bright_gw.jpg",
    "wb data/bright.jpg --method white-patch -o out/bright_wp.jpg",
    "clahe data/dark.jpg --clip 2 --tiles 8 -o out/dark_clahe.jpg --compare out/dark_compare.jpg --hist out/dark_clahe_hist.png",
    "chromakey data/object.jpg --bg data/bg.jpg --sample 800,600,200,200 --close 9 -o out/object_default.jpg --mask out/object_default_mask.png",
    "chromakey data/object.jpg --bg data/bg.jpg --sample 800,600,200,200 --close 31 -o out/object_on_bg.jpg --mask out/object_mask.png",
    "rotate data/poster.jpg --deg 30 -o out/poster_rot30.jpg",
    "rotate data/poster.jpg --deg -137 -o out/poster_rot_minus137.jpg",
    "resize data/text.jpg --scale 0.25 --method naive --report -o out/text_naive.jpg",
    "resize data/text.jpg --scale 0.25 --method blur -o out/text_blur.jpg",
    "resize data/text.jpg --scale 0.25 --method area -o out/text_small.jpg",
    "resize data/text.jpg --scale 2 -o out/text_big.jpg",
    "rectify data/poster.jpg --corners 180,579,1009,373,1396,1547,505,1855 --aspect 0.707 -o out/poster_front.jpg",
    "chromakey data/course/ball-lamp.jpg --bg data/course/road-cam.jpg --lo 140,121,40 --hi 168,230,255 -o out/course_ball.jpg --mask out/course_ball_mask.png",
    "resize data/course/iu-building.jpg --scale 0.25 --report -o out/course_small.jpg",
    "rectify data/course/poster-angle.jpg --corners 1290,1010,560,330,600,840,1250,220 --size 640x905 -o out/course_poster.jpg",
    "sheet data/dark.jpg out/dark_g05.jpg out/dark_g2.jpg out/dark_clahe.jpg data/bright.jpg out/bright_gw.jpg out/bright_wp.jpg data/object.jpg out/object_default.jpg out/object_on_bg.jpg out/object_mask.png data/poster.jpg out/poster_rot30.jpg out/poster_rot_minus137.jpg out/poster_front.jpg data/text.jpg out/text_naive.jpg out/text_blur.jpg out/text_small.jpg out/text_big.jpg --cols 4 -o out/sheet.jpg",
]

records = []
for command in commands:
    print("python photolab.py " + command, flush=True)
    process = subprocess.run(
        [sys.executable, "photolab.py"] + command.split(),
        capture_output=True, text=True, encoding="utf-8"
    )
    if process.returncode != 0:
        print(process.stderr)
        raise SystemExit(process.returncode)

    result = json.loads(process.stdout)
    records.append({"command": "python photolab.py " + command, "result": result})
    print(process.stdout.strip(), flush=True)

Path("out/commands.txt").write_text(
    "\n".join(record["command"] for record in records) + "\n", encoding="utf-8"
)
Path("out/results.json").write_text(
    json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8"
)

# Дополнительные измерения для кадров с известным эталоном.
process = subprocess.run([sys.executable, "measure.py"])
if process.returncode != 0:
    raise SystemExit(process.returncode)

print("Готово: результаты находятся в out.")