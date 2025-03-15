import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import cv2.ximgproc as xip
from skimage.restoration import denoise_bilateral
from skimage.filters import frangi
from skimage.morphology import closing, disk
from skimage import exposure

samples = 833600
resolution_256 = 256
resolution_64 = 64

input_image = cv2.imread('C:/YuShin/Lissajous scanning simulation/test.png', cv2.IMREAD_GRAYSCALE)
input_image_resized = cv2.resize(input_image, (resolution_256, resolution_256))

colorbar_256 = None
colorbar_64 = None


def update_image(fx, fy):
    global colorbar_256, colorbar_64

    t = np.linspace(0, 1, samples)
    Ax = resolution_256 / 2
    Ay = resolution_256 / 2
    x = Ax * np.sin(2 * np.pi * fx * t)
    y = Ay * np.sin(2 * np.pi * fy * t)

    x_pixel_256 = np.floor((x + Ax) * (resolution_256 - 1) / resolution_256).astype(int)
    y_pixel_256 = np.floor((y + Ay) * (resolution_256 - 1) / resolution_256).astype(int)
    x_pixel_64 = np.floor((x + Ax) * (resolution_64 - 1) / resolution_256).astype(int)
    y_pixel_64 = np.floor((y + Ay) * (resolution_64 - 1) / resolution_256).astype(int)

    sample_count_map_256 = np.zeros((resolution_256, resolution_256))
    sample_count_map_64 = np.zeros((resolution_64, resolution_64))
    image_mapped_256 = np.zeros((resolution_256, resolution_256))
    image_mapped_64 = np.zeros((resolution_64, resolution_64))

    for i in range(samples):
        sample_count_map_256[y_pixel_256[i], x_pixel_256[i]] += 1
        sample_count_map_64[y_pixel_64[i], x_pixel_64[i]] += 1
        image_mapped_256[y_pixel_256[i], x_pixel_256[i]] = input_image_resized[y_pixel_256[i], x_pixel_256[i]]
        image_mapped_64[y_pixel_64[i], x_pixel_64[i]] = input_image_resized[y_pixel_256[i], x_pixel_256[i]]

    ax[0].clear()
    ax[0].imshow(input_image_resized, cmap='gray', origin='lower')
    ax[0].set_title('Original Img', fontsize=14)

    ax[1].clear()
    ax[1].imshow(image_mapped_256, cmap='gray', origin='lower')
    ax[1].set_title('Mapped Img(256x256 @ 1µm/pixel)', fontsize=14)

    ax[2].clear()
    ax[2].imshow(image_mapped_64, cmap='gray', origin='lower')
    ax[2].set_title('Mapped Img(64x64 @ 5µm/pixel)', fontsize=14)

    mask = (image_mapped_256 == 0).astype(np.uint8)
    image_mapped_256_filled = cv2.inpaint(image_mapped_256.astype(np.uint8), mask, inpaintRadius=9, flags=cv2.INPAINT_NS)

    kernel_sharpening = np.array([[0, -1,  0],
                              [-1,  5, -1],
                              [0, -1,  0]])
    sharpened = cv2.filter2D(image_mapped_256_filled, -1, kernel_sharpening)

    resized_interpolated =sharpened

    ax[3].clear()
    ax[3].imshow(resized_interpolated, cmap='gray', origin='lower')
    ax[3].set_title('Interpolated (Cubic) from 256x256', fontsize=14)

    if colorbar_256:
        colorbar_256.remove()
    if colorbar_64:
        colorbar_64.remove()

    ax[4].clear()
    im_256 = ax[4].imshow(sample_count_map_256, cmap='hot', origin='lower')
    ax[4].set_title('Sample Count Map(256x256)', fontsize=14)
    colorbar_256 = plt.colorbar(im_256, ax=ax[4])

    ax[5].clear()
    im_64 = ax[5].imshow(sample_count_map_64, cmap='hot', origin='lower')
    ax[5].set_title('Sample Count Map(64x64)', fontsize=14)
    colorbar_64 = plt.colorbar(im_64, ax=ax[5])

    canvas.draw()


root = tk.Tk()
root.title("Lissajous Sample Count Map & Mapped Image")

x_freq_label = ttk.Label(root, text="Enter X Frequency (Hz):")
x_freq_label.pack(pady=5)
x_freq_entry = ttk.Entry(root)
x_freq_entry.insert(0, "2160")
x_freq_entry.pack(pady=5)

y_freq_label = ttk.Label(root, text="Enter Y Frequency (Hz):")
y_freq_label.pack(pady=5)
y_freq_entry = ttk.Entry(root)
y_freq_entry.insert(0, "2100")
y_freq_entry.pack(pady=5)


def on_submit():
    try:
        fx = int(x_freq_entry.get())
        fy = int(y_freq_entry.get())
        if 1 <= fx <= 3200 and 1 <= fy <= 3200:
            update_image(fx, fy)
        else:
            print("Frequency out of range. Please enter values between 1 and 3200.")
    except ValueError:
        print("Invalid input. Please enter integer values.")


submit_button = ttk.Button(root, text="Update Mapped Image", command=on_submit)
submit_button.pack(pady=10)

# 改成 2 列 3 行，圖比較大
fig, ax = plt.subplots(2, 3, figsize=(18, 10))
ax = ax.flatten()  # 攤平為 1 維 list，程式不需要改動

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

update_image(3000, 2000)

root.mainloop()
