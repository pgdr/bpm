from statistics import quantiles
from datetime import datetime as dt
import numpy as np
from filterpy.kalman import KalmanFilter

kf = KalmanFilter(dim_x=1, dim_z=1)
kf.x = np.array([[60]])
kf.F = np.array([[1]])
kf.H = np.array([[1]])
kf.alpha = 1.4
kf.P *= 1000.0
kf.R = 0.1
kf.Q = 1e-5


def to_duration(delta):
    out = str(round(delta.total_seconds(), 2)).replace(".", ":")
    m, s = out.split(":")
    m = m.rjust(3)
    s = s.ljust(2, "0")
    return f"{m}:{s}"


BPMs = []

x = input("hit it")
start = prev = dt.now()
out = "  0:00"
while x != "q":
    try:
        x = input(f"{out}")
    except KeyboardInterrupt:
        break
    if x == "q":
        break
    now = dt.now()
    diff = now - prev
    prev = now
    bpm = round(60 / diff.total_seconds())
    BPMs.append(60 / diff.total_seconds())

    kf.update(bpm)
    predicted = kf.predict()

    out = f"{to_duration(now - start)} | {round(kf.x[0, 0])} bpm predicted \t | \t {bpm} exact"


print()
if len(BPMs) < 2:
    exit("Too few taps")
n = min(6, len(BPMs) - 1)
print(" ".join([str(round(x, 2)) for x in quantiles(BPMs, n=n)]))
