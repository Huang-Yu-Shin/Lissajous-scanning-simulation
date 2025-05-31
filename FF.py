import numpy as np
import math
import pandas as pd

img_size = 512
sampling_rate = 50_000_000

def generate_lissajous(fx, fy, phase, img_size, sample_rate):
    totalsample = int(sample_rate / math.gcd(int(fx), int(fy)))
    t = np.arange(totalsample) / sample_rate
    x = np.round((img_size / 2) * (1 + np.sin(2 * np.pi * fx * t))).astype(int)
    y = np.round((img_size / 2) * (1 + np.sin(2 * np.pi * fy * t + phase))).astype(int)
    sample_map = np.zeros((img_size, img_size), dtype=np.uint16)
    for i in range(len(x)):
        if 0 <= x[i] < img_size and 0 <= y[i] < img_size:
            sample_map[y[i], x[i]] += 1
    nonzero_pixels = np.count_nonzero(sample_map)
    total_pixels = img_size * img_size
    fill_factor = (nonzero_pixels / total_pixels) * 100
    return fill_factor, sample_map

# Phase list
phase_list = [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi, 5*np.pi/4, 3*np.pi/2, 7*np.pi/4]

# Result container
results = []

# Loop through x values
for x in range(2, 37):
    ratio = int(2160 / x)
    fx = ratio * (x - 1)
    fy = ratio * x

    phase_fill_factors = []
    combined_map = np.zeros((img_size, img_size), dtype=np.uint8)

    for phase in phase_list:
        fill, sample_map = generate_lissajous(fx, fy, phase, img_size, sampling_rate)
        phase_fill_factors.append(round(fill, 2))
        combined_map += (sample_map > 0).astype(np.uint8)

    combined_fill = round(np.count_nonzero(combined_map) / (img_size * img_size) * 100, 2)

    result_entry = {
        "x": x,
        "ratio": ratio,
        "fx": fx,
        "fy": fy,
        "fx:fy": f"{fx}:{fy}",
        "Combined8PhaseFill(%)": combined_fill,
    }

    # Add individual phase fill factors
    for i, pf in enumerate(phase_fill_factors):
        result_entry[f"Phase{i}(Fill%)"] = pf

    results.append(result_entry)
    print(f"x={x} done.")

# Save to Excel
df = pd.DataFrame(results)
df.to_excel("Lissajous_Fill_Factor_PerPhase.xlsx", index=False)
