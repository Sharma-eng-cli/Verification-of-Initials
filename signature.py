import cv2
from skimage.metrics import structural_similarity as ssim
import numpy as np


def match(path1, path2):
    # Read images
    img1 = cv2.imread(path1)
    img2 = cv2.imread(path2)

    # Convert to grayscale
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Resize images to the same dimensions
    img1_gray = cv2.resize(img1_gray, (300, 300))
    img2_gray = cv2.resize(img2_gray, (300, 300))

    # Compute Structural Similarity Index (SSIM)
    similarity_value = ssim(img1_gray, img2_gray) * 100  # Convert to percentage

    # Display both images side by side
    combined_img = np.hstack((img1, img2))
    cv2.imshow("Signature Comparison", combined_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return round(similarity_value, 2)  # Round to 2 decimal places


def pad_image_to_match_size(img1, img2):
    """Pads images to match both height and width."""
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]

    # Pad height
    if h1 < h2:
        pad_top = (h2 - h1) // 2
        pad_bottom = h2 - h1 - pad_top
        img1 = cv2.copyMakeBorder(img1, pad_top, pad_bottom, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0])
    elif h2 < h1:
        pad_top = (h1 - h2) // 2
        pad_bottom = h1 - h2 - pad_top
        img2 = cv2.copyMakeBorder(img2, pad_top, pad_bottom, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0])

    # Pad width
    h1, w1 = img1.shape[:2]  # Get new dimensions
    h2, w2 = img2.shape[:2]

    if w1 < w2:
        pad_left = (w2 - w1) // 2
        pad_right = w2 - w1 - pad_left
        img1 = cv2.copyMakeBorder(img1, 0, 0, pad_left, pad_right, cv2.BORDER_CONSTANT, value=[0, 0, 0])
    elif w2 < w1:
        pad_left = (w1 - w2) // 2
        pad_right = w1 - w2 - pad_left
        img2 = cv2.copyMakeBorder(img2, 0, 0, pad_left, pad_right, cv2.BORDER_CONSTANT, value=[0, 0, 0])

    return img1, img2


def match(path1, path2):
    """Compares two images and returns similarity percentage."""

    # Load images
    img1 = cv2.imread(path1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(path2, cv2.IMREAD_GRAYSCALE)

    if img1 is None or img2 is None:
        raise ValueError("One or both images could not be loaded. Check file paths.")

    # Ensure images have the same height & width
    img1, img2 = pad_image_to_match_size(img1, img2)

    # Compute Structural Similarity Index (SSIM)
    similarity, _ = ssim(img1, img2, full=True)

    return similarity * 100  # Convert to percentage

