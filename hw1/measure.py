"""Recall/precision мяча и совпадение выпрямленного плаката с эталоном."""
import json
import os
from pathlib import Path

import cv2
import numpy as np
import photolab as pl

os.chdir(Path(__file__).resolve().parent)

# Эталон мяча — круг с центром (190, 560) и радиусом 58.
ball = pl.imread("data/course/ball-lamp.jpg")
h, w = ball.shape[:2]
y, x = np.mgrid[:h, :w]
target = (x - 190) ** 2 + (y - 560) ** 2 <= 58 ** 2
mask = pl.imread("out/course_ball_mask.png")[:, :, 0] > 0
common = (mask & target).sum()
recall = 100 * common / target.sum()
precision = 100 * common / max(1, mask.sum())

# Сравниваем чернила и фон после одинакового порога 128.
front = pl.imread("out/course_poster.jpg")
reference = pl.imread("data/course/poster-gt.png")
ink_front = cv2.cvtColor(front, cv2.COLOR_BGR2GRAY) < 128
ink_reference = cv2.cvtColor(reference, cv2.COLOR_BGR2GRAY) < 128
match = 100 * (ink_front == ink_reference).mean()

measurements = {
    "course_ball": {"recall_pct": float(recall), "precision_pct": float(precision)},
    "course_poster_match_pct": float(match)
}
Path("out/measurements.json").write_text(
    json.dumps(measurements, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(json.dumps(measurements, ensure_ascii=False, indent=2))
