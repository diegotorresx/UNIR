import cv2
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage.measure import shannon_entropy

INPUT_DIR = "imagenes_originales"
OUTPUT_DIR = "resultados"
HIST_DIR = "histogramas"
COMPARE_DIR = "comparativas"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(HIST_DIR, exist_ok=True)
os.makedirs(COMPARE_DIR, exist_ok=True)

images = ["1041.png", "1132.png", "1150.png", "1.png"]


def calculate_metrics(gray_image):
    return {
        "media_intensidad": np.mean(gray_image),
        "desviacion_estandar_contraste": np.std(gray_image),
        "entropia": shannon_entropy(gray_image),
        "min_intensidad": np.min(gray_image),
        "max_intensidad": np.max(gray_image)
    }


def gamma_correction(image, gamma=0.5):
    inv_gamma = 1.0 / gamma
    table = np.array([
        ((i / 255.0) ** inv_gamma) * 255
        for i in range(256)
    ]).astype("uint8")
    return cv2.LUT(image, table)


def contrast_stretching(image):
    min_val = np.min(image)
    max_val = np.max(image)
    stretched = (image - min_val) * (255 / (max_val - min_val))
    return np.clip(stretched, 0, 255).astype(np.uint8)


def histogram_equalization(image):
    ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
    return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)


def clahe_enhancement(image):
    ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    ycrcb[:, :, 0] = clahe.apply(ycrcb[:, :, 0])
    return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)


def arithmetic_brightness_contrast(image):
    return cv2.convertScaleAbs(image, alpha=1.35, beta=35)


def save_histogram(gray_image, title, output_path):
    plt.figure(figsize=(6, 4))
    plt.hist(gray_image.ravel(), bins=256, range=[0, 256])
    plt.title(title)
    plt.xlabel("Nivel de intensidad")
    plt.ylabel("Frecuencia")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def save_comparison(original, processed_images, image_name):
    titles = [
        "Original",
        "Gamma",
        "Contrast stretching",
        "Ecualización histograma",
        "CLAHE",
        "Operador aritmético"
    ]

    all_images = [original] + processed_images

    plt.figure(figsize=(16, 8))

    for i, img in enumerate(all_images):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.subplot(2, 3, i + 1)
        plt.imshow(img_rgb)
        plt.title(titles[i])
        plt.axis("off")

    plt.tight_layout()
    output_path = os.path.join(COMPARE_DIR, f"comparativa_{image_name}")
    plt.savefig(output_path, dpi=300)
    plt.close()


metrics_list = []

for image_name in images:
    image_path = os.path.join(INPUT_DIR, image_name)
    image = cv2.imread(image_path)

    if image is None:
        print(f"No se pudo cargar la imagen: {image_name}")
        continue

    base_name = os.path.splitext(image_name)[0]

    gamma_img = gamma_correction(image, gamma=0.5)
    stretch_img = contrast_stretching(image)
    hist_eq_img = histogram_equalization(image)
    clahe_img = clahe_enhancement(image)
    arithmetic_img = arithmetic_brightness_contrast(image)

    processed = {
        "original": image,
        "gamma": gamma_img,
        "contrast_stretching": stretch_img,
        "histogram_equalization": hist_eq_img,
        "clahe": clahe_img,
        "arithmetic": arithmetic_img
    }

    for technique, img in processed.items():
        output_img_path = os.path.join(OUTPUT_DIR, f"{base_name}_{technique}.png")
        cv2.imwrite(output_img_path, img)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        hist_path = os.path.join(HIST_DIR, f"{base_name}_{technique}_hist.png")
        save_histogram(gray, f"{base_name} - {technique}", hist_path)

        metrics = calculate_metrics(gray)
        metrics["imagen"] = image_name
        metrics["tecnica"] = technique
        metrics_list.append(metrics)

    save_comparison(
        image,
        [gamma_img, stretch_img, hist_eq_img, clahe_img, arithmetic_img],
        image_name
    )

df_metrics = pd.DataFrame(metrics_list)
df_metrics = df_metrics[
    [
        "imagen",
        "tecnica",
        "media_intensidad",
        "desviacion_estandar_contraste",
        "entropia",
        "min_intensidad",
        "max_intensidad"
    ]
]

df_metrics.to_csv("metricas_resultados.csv", index=False, encoding="utf-8-sig")

print("Procesamiento finalizado correctamente.")
print("Revisa las carpetas resultados, histogramas, comparativas y el archivo metricas_resultados.csv.")