import os
import fitz  # PyMuPDF
import cv2
import numpy as np
from PIL import Image

def load_and_label_pdf(pdf_path, part_name, lab_number):
    # Step 1: Load the PDF and get the first page
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)

    # Step 2: Render the page to an image
    pix = page.get_pixmap(dpi=300)
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # Step 3: Convert to a format usable by OpenCV
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Step 4: Detect and label objects
    labeled_image = detect_and_label_objects(image, part_name, lab_number)

    # Step 5: Save the labeled image as a new PDF
    labeled_pdf_path = "labeled_output.pdf"
    save_image_as_pdf(labeled_image, labeled_pdf_path)

    return labeled_pdf_path

def detect_and_label_objects(image, part_name, lab_number):
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the range for gray color in HSV
    lower_gray = np.array([0, 0, 50])
    upper_gray = np.array([180, 50, 200])

    # Create a mask to filter out the gray shapes
    mask = cv2.inRange(hsv, lower_gray, upper_gray)

    # Find contours of the objects
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours by their y-coordinate first, then by their x-coordinate
    contours = sorted(contours, key=lambda c: (cv2.boundingRect(c)[1] // 50, cv2.boundingRect(c)[0]))

    # Label prefixes
    label_prefixes = ["AA", "CC", "DD", "GG", "CCB"] if "Ford" in part_name else ["M1", "M2"]

    # Extract the last four digits from the lab number
    last_four_digits = lab_number.split('-')[-1]

    # Loop through each contour and label the objects
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        label = f"{label_prefixes[i]} - {last_four_digits}" if i < len(label_prefixes) else f"Object {i + 1}"
        cv2.putText(image, label, (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0, 0, 255), 2)

    return image

def save_image_as_pdf(image, output_path):
    # Convert the labeled image back to RGB (Pillow format)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image)

    # Save the image as a PDF
    pil_image.save(output_path, "PDF", resolution=300.0)

def rename_file(old_name, new_name):
    try:
        os.rename(old_name, new_name)
        print(f'Successfully renamed to "{new_name}"')
    except Exception as e:
        print(f"Error renaming file: {str(e)}")





