import tkinter as tk
import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk, filedialog
import math

def generate_lissajous(fx, fy, phase, img_size, sample_rate):

    totalsample = int(sample_rate /  math.gcd(int(fx), int(fy)))
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
    print("Fill factor:",fill_factor)

    return x, y, sample_map

def generate_lissajous_noint(fx, fy, phase, img_size, sample_rate):

    totalsample = int(sample_rate /  math.gcd(int(fx), int(fy)))
    t = np.arange(totalsample) / sample_rate
    x = (img_size / 2) * (1 + np.sin(2 * np.pi * fx * t))
    y = (img_size / 2) * (1 + np.sin(2 * np.pi * fy * t + phase))

    return x, y



def update_plot():
    fx = int(fx_var.get())
    fy = int(fy_var.get())
    phase = float(phase_var.get())
    sampling_rate = int(sampling_rate_var.get())
    x, y, sample_map = generate_lissajous(fx, fy, phase, 512, sampling_rate)
    x_noint,y_noint =generate_lissajous_noint(fx, fy, phase, 512, sampling_rate)

    plt.figure(figsize=(6, 6))
    plt.plot(x_noint, y_noint, 'r', alpha=0.7)
    plt.xlim(0, 512)
    plt.ylim(0, 512)
    plt.xticks([])
    plt.yticks([])
    plt.title(f"Lissajous: fx={fx}, fy={fy}, phase={phase} rad, Sampling={sampling_rate}")
    plt.show()

    color_map = np.zeros((sample_map.shape[0], sample_map.shape[1], 3), dtype=np.uint8)  
    color_map[np.where(sample_map > 0)] = [255, 0, 0]  

    plt.figure(figsize=(6, 6))
    plt.imshow(color_map)
    plt.axis("off")
    plt.title("Lissajous Sample Map (Red Pixels Indicate Scanned Points)")
    plt.show()


def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tif")])
    if not file_path:
        return

    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print("can not load the file")
        return

    color_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    color_image[np.where(image > 0)] = [0, 0, 255]
    color_image_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(6, 6))
    plt.imshow(color_image_rgb)
    plt.axis("off")
    plt.title("Modified Image (Non-zero pixels in Red)")
    plt.show()

root = tk.Tk()
root.title("Lissajous Scan & Image Processing")
root.geometry("600x500")


style = ttk.Style(root)
style.configure("TLabel", font=("Arial", 18, "bold"))
style.configure("TEntry", font=("Arial", 14))
style.configure("TRadiobutton", font=("Arial", 14))
style.configure("TButton", font=("Arial", 18, "bold"))

frame_controls = ttk.Frame(root)
frame_controls.pack(pady=10)

ttk.Label(frame_controls, text="X freq. (fx):").grid(row=0, column=0, padx=5, pady=5)
fx_var = tk.StringVar(value="2000")
fx_entry = ttk.Entry(frame_controls, textvariable=fx_var, width=10)
fx_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_controls, text="Y freq. (fy):").grid(row=1, column=0, padx=5, pady=5)
fy_var = tk.StringVar(value="2005")
fy_entry = ttk.Entry(frame_controls, textvariable=fy_var, width=10)
fy_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame_controls, text="Phase :").grid(row=2, column=0, padx=5, pady=5)
phase_var = tk.StringVar(value="0")
phase_options = [("0", "0"), ("π/2", "1.5708"), ("π", "3.1416"), ("3π/2", "4.7124")]
for i, (text, value) in enumerate(phase_options):
    ttk.Radiobutton(frame_controls, text=text, variable=phase_var, value=value).grid(row=2, column=i+1, padx=5, pady=5)

ttk.Label(frame_controls, text="Sampling Rate:").grid(row=3, column=0, padx=5, pady=5)
sampling_rate_var = tk.StringVar(value="20000000")
sampling_entry = ttk.Entry(frame_controls, textvariable=sampling_rate_var, width=10)
sampling_entry.grid(row=3, column=1, padx=5, pady=5)

update_button = ttk.Button(root, text="Generate Lissajous", command=update_plot)
update_button.pack(pady=10)

image_button = ttk.Button(root, text="Select Image & Process", command=select_image)
image_button.pack(pady=10)


root.mainloop()


