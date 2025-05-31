import pandas as pd
import matplotlib.pyplot as plt

# 讀取 Excel 資料
df = pd.read_excel("Lissajous_Fill_Factor_PerPhase.xlsx")

# 嚴格抓 Phase0~Phase7 對應欄位
phase_labels = ['0', 'π/4', 'π/2', '3π/4', 'π', '5π/4', '3π/2', '7π/4']
phase_cols = [f"Phase{i}(Fill%)" for i in range(8)]

# x 軸與 ratio (frame rate)
x = df["x"]
ratio = df["ratio"]
combined = df["Combined8PhaseFill(%)"]

# 畫圖
plt.figure(figsize=(12, 6))
colors = plt.cm.tab10.colors  # 可選 colormap

# 畫每一條 Phase 線
for i, col in enumerate(phase_cols):
    if col in df.columns:
        plt.plot(x, df[col], '-o', label=f"Phase {i} ({phase_labels[i]})", color=colors[i % len(colors)])

# 畫 Combined 線（粉紅色）
plt.plot(x, combined, '-s', linewidth=2, color='pink', label="Combined 8 Phases")

# 加上 ratio 標籤
for i in range(len(x)):
    plt.text(x[i], combined[i] + 1.5, f"{ratio[i]} Hz", ha='center', fontsize=9, color='black')

# 圖表設定
plt.xlabel("x (fx = ratio * x, fy = ratio * (x - 1))")
plt.ylabel("Fill Factor (%)")
plt.title("Lissajous Fill Factor per Phase with Frame Rate (ratio)")
plt.legend(ncol=3, loc='center left', bbox_to_anchor=(1, 0.5))
plt.grid(True)
plt.ylim(0, 105)
plt.tight_layout()
plt.show()
