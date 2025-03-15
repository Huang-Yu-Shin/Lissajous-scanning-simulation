import numpy as np
import matplotlib.pyplot as plt

# Function to compute frame rate
def compute_frame_rate(fx, fy):
    return np.gcd(int(fx), int(fy))

# Function to compute number of lobes
def compute_number_of_lobes(fx, fy, frame_rate):
    Nx = fx // frame_rate
    Ny = fy // frame_rate
    return Nx, Ny

# Function to compute the distance h between lines
def compute_h(Ax, Ay, Nx, Ny):
    numerator = 2 * Ax * Ay * np.sin(np.pi / (2 * Nx)) * np.sin(np.pi / (2 * Ny))
    denominator = np.sqrt((Ax * np.sin(np.pi / (2 * Ny)))**2 + (Ay * np.sin(np.pi / (2 * Nx)))**2)
    return numerator / denominator

# Function to compute optimal scan size
def compute_optimal_size(FWHM, Nx, Ny):
    return FWHM * np.sqrt(Nx**2 + Ny**2) / np.pi

# Function to compute pixelwise field of view (FOVpx)
def compute_FOVpx(FWHM, Nx, Ny, dP):
    numerator = 2 * FWHM * np.sqrt(np.sin(np.pi / (2 * Ny))**2 + np.sin(np.pi / (2 * Nx))**2)
    denominator = dP * np.sin(np.pi / (2 * Ny)) * np.sin(np.pi / (2 * Nx))
    return numerator / denominator

# Function to compute Fcp
def compute_Fcp(Nx, Ny, frame_rate):
    return 4 * Nx * Ny * frame_rate

# Function to compute the fill factor
def compute_fill_factor(image, resolution):
    non_zero_pixels = np.count_nonzero(image)
    total_pixels = resolution * resolution
    fill_factor = (non_zero_pixels / total_pixels) * 100  # As a percentage
    return fill_factor

# Function to map Lissajous figure to pixel grid and calculate fill factor
def calculate_lissajous_fill_factor(fx, fy, Ax, Ay, sampling_frequency, resolution=128, duration=1):
    t = np.linspace(0, duration, int(sampling_frequency * duration))  # Time vector based on sampling frequency
    x = Ax * np.sin(2 * np.pi * fx * t)
    y = Ay * np.sin(2 * np.pi * fy * t)

    # Initialize image
    image = np.zeros((resolution, resolution))

    # Map Lissajous points to the pixel grid
    x_pixel = np.floor((x + Ax) * (resolution - 1) / (2 * Ax)).astype(int)
    y_pixel = np.floor((y + Ay) * (resolution - 1) / (2 * Ay)).astype(int)

    for i in range(len(x_pixel)):
        if 0 <= x_pixel[i] < resolution and 0 <= y_pixel[i] < resolution:
            image[y_pixel[i], x_pixel[i]] += 1

    # Compute the fill factor
    fill_factor = compute_fill_factor(image, resolution)
    
    return fill_factor

# Function to find the best parameter setting over a range of frequencies considering sampling frequency
def find_best_parameters(fx_range, fy_range, FWHM, dP, sampling_frequency, min_frame_rate=60, resolution=128):
    best_params = None
    max_lobes = 0

    for fx in fx_range:
        for fy in fy_range:
            frame_rate = compute_frame_rate(fx, fy)
            
            if frame_rate >= min_frame_rate:
                Nx, Ny = compute_number_of_lobes(fx, fy, frame_rate)
                h = compute_h(FWHM, FWHM, Nx, Ny)
                FOVpx = compute_FOVpx(FWHM, Nx, Ny, dP)
                Fcp = compute_Fcp(Nx, Ny, frame_rate)

                # Calculate the fill factor for this parameter set
                fill_factor = calculate_lissajous_fill_factor(fx, fy, FWHM, FWHM, sampling_frequency, resolution)

                # Only consider parameters that satisfy the sampling frequency condition
                if sampling_frequency >= 6 * Fcp:
                    if Nx + Ny > max_lobes:  # Maximize based on number of lobes (better resolution)
                        max_lobes = Nx + Ny
                        best_params = {
                            'fx': fx,
                            'fy': fy,
                            'frame_rate': frame_rate,
                            'Nx': Nx,
                            'Ny': Ny,
                            'h': h,
                            'FOVpx': FOVpx,
                            'Fcp': Fcp,
                            'fill_factor (%)': fill_factor
                        }

    return best_params

# Function to plot Lissajous figure and highlight sampling points
def plot_lissajous_with_sampling(fx, fy, Ax, Ay, sampling_frequency, duration=1, resolution=128):
    t = np.linspace(0, duration, int(sampling_frequency * duration))  # Time vector based on sampling frequency
    x = Ax * np.sin(2 * np.pi * fx * t)
    y = Ay * np.sin(2 * np.pi * fy * t)

    # Plot Lissajous figure
    plt.figure(figsize=(6, 6))
    plt.plot(x, y, label='Lissajous Curve')
    plt.title(f'Lissajous Figure (fx={fx}Hz, fy={fy}Hz)')
    plt.xlabel('X-axis displacement')
    plt.ylabel('Y-axis displacement')
    plt.grid(True)
    plt.legend()


# Example usage
fx_range = range(2000, 2200, 1)  # Frequency range in Hz along x-axis
fy_range = range(2000, 2200, 1)  # Frequency range in Hz along y-axis
FWHM = 10  # Full Width Half Maximum in micrometers
dP = FWHM / 3  # Pixel size set to FWHM/3
sampling_frequency = 50000000  # Sampling frequency in Hz
resolution = 128  # Image resolution

# Find the best parameters
best_params = find_best_parameters(fx_range, fy_range, FWHM, dP, sampling_frequency, resolution=resolution)
print("Best Parameters:")
for key, value in best_params.items():
    print(f"{key}: {value}")

# Plot the Lissajous pattern with sampling points and display the fill factor
plot_lissajous_with_sampling(best_params['fx'], best_params['fy'], 1, 1, sampling_frequency, duration=1, resolution=resolution)

# Compute and display the FOV
FOV = best_params['FOVpx'] * dP  # Compute FOV in micrometers
print(f"Computed Field of View (FOV): {FOV:.2f} micrometers")
plt.show()
