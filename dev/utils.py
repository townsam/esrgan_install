import cv2
import numpy as np


def crop_text_bands3(image):
    """Crops text bands from the image by identifying non-text regions."""
    if image is None:
        raise ValueError("Invalid image provided.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 15, 10
    )
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    thresh_cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    projection = np.sum(thresh_cleaned, axis=1)
    projection_normalized = projection / np.max(projection)
    binary_profile = (projection_normalized <= 0.05).astype(np.uint8)

    def longest_run(arr):
        max_count = count = 0
        max_start = start = 0
        for i, val in enumerate(arr):
            if val == 1:
                if count == 0:
                    start = i
                count += 1
                if count > max_count:
                    max_count = count
                    max_start = start
            else:
                count = 0
        return max_start, max_start + max_count

    peak_start, peak_end = longest_run(binary_profile)
    peak_start = max(0, peak_start)
    peak_end = min(image.shape[0], peak_end)

    if peak_end - peak_start == 0:
        return image

    cropped_image = image[peak_start:peak_end, :]
    return cropped_image


def crop_text_bands5(image):
    """Crops text bands from the image by identifying non-text regions (alternative version)."""
    if image is None:
        raise ValueError("Invalid image provided.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 15, 10
    )
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    thresh_cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    projection = np.sum(thresh_cleaned, axis=1)
    projection_normalized = projection / np.max(projection)
    binary_profile = (projection_normalized <= 0.01).astype(np.uint8)

    def longest_run(arr):
        max_count = count = 0
        max_start = start = 0
        for i, val in enumerate(arr):
            if val == 1:
                if count == 0:
                    start = i
                count += 1
                if count > max_count:
                    max_count = count
                    max_start = start
            else:
                count = 0
        return max_start, max_start + max_count

    peak_start, peak_end = longest_run(binary_profile)
    peak_start = max(0, peak_start)
    peak_end = min(image.shape[0], peak_end)

    if peak_end - peak_start == 0:
        return image

    cropped_image = image[peak_start:peak_end, :]
    return cropped_image


def detect_and_deskew_object(image):
    """Detects the largest object in an image, crops it, and deskews it."""
    if image is None:
        raise ValueError("Invalid image provided.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)  # Invert colors
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        raise Exception("No contours found in the image.")

    largest_contour = max(contours, key=cv2.contourArea)
    rect = cv2.minAreaRect(largest_contour)
    box = cv2.boxPoints(rect)
    box = np.int32(box)

    def order_points(pts):
        rect = np.zeros((4, 2), dtype="float32")
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]  # Top-left
        rect[2] = pts[np.argmax(s)]  # Bottom-right
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]  # Top-right
        rect[3] = pts[np.argmax(diff)]  # Bottom-left
        return rect

    ordered_box = order_points(box)
    (tl, tr, br, bl) = ordered_box

    widthA = np.linalg.norm(br - bl)
    widthB = np.linalg.norm(tr - tl)
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.linalg.norm(tr - br)
    heightB = np.linalg.norm(tl - bl)
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array(
        [
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1],
        ],
        dtype="float32",
    )

    M = cv2.getPerspectiveTransform(ordered_box, dst)
    deskewed = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return deskewed


def mock_process_image(input_path, output_path):
    """Mocks the processing of an image by copying it."""
    image = cv2.imread(input_path)
    if image is not None:
        cv2.imwrite(output_path, image)
    else:
        print(f"Failed to read image at {input_path}. Skipping.")


def save_image(output_path, image):
    """Saves an image to the specified path."""
    try:
        cv2.imwrite(output_path, image)
        print(f"Saved processed image to {output_path}")
    except Exception as e:
        print(f"Error saving image to {output_path}: {e}")