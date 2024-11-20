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
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Use adaptive thresholding to create a binary image
    adaptive_thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )

    # Use Canny edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Combine the adaptive threshold and edges for better contour detection
    combined_mask = cv2.bitwise_or(adaptive_thresh, edges)

    # Find contours of the objects
    contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Set a minimum contour area to filter out small noises
    min_contour_area = 5000  # Adjust this value as needed

    # Filter out small contours
    filtered_contours = [c for c in contours if cv2.contourArea(c) > min_contour_area]

    # Sort contours into rows and then sort each row from left to right
    sorted_contours = sort_contours_by_rows(filtered_contours)

    # Label prefixes based on part name
    label_prefixes = ["AA", "CC", "DD", "GG", "CCB"] if "Ford" in part_name else ["M1", "M2"]

    # Extract the last four digits from the lab number
    last_four_digits = lab_number.split('-')[-1]

    # Loop through each contour and label the objects
    labeled_image = image.copy()
    label_index = 0  # To track the current label

    for contour in sorted_contours:
        # Get the bounding box for the contour
        x, y, w, h = cv2.boundingRect(contour)

        # Use the appropriate label from the prefix list
        if label_index < len(label_prefixes):
            label = f"{label_prefixes[label_index]} - {last_four_digits}"
        else:
            label = f"Object {label_index + 1}"  # Fallback label if more contours than expected
        label_index += 1

        # Commented out the bounding box drawing for future debugging purposes
        # cv2.rectangle(labeled_image, (x, y), (x + w, y + h), (0, 255, 0), 3)

        # Draw the label text above the detected object
        cv2.putText(labeled_image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0, 0, 255), 2)

    return labeled_image

def sort_contours_by_rows(contours):
    # Sort contours first by their y-coordinate
    sorted_by_y = sorted(contours, key=lambda c: cv2.boundingRect(c)[1])

    # Group contours that are in the same row by checking their y-coordinates and heights
    rows = []
    current_row = []
    y_threshold = 60  # Threshold to consider contours in the same row
    prev_y = None

    for contour in sorted_by_y:
        _, y, _, h = cv2.boundingRect(contour)
        if prev_y is None or abs(y - prev_y) < h * 0.5:  # Use height to cluster into rows
            current_row.append(contour)
        else:
            rows.append(current_row)
            current_row = [contour]
        prev_y = y

    # Append the last row if not empty
    if current_row:
        rows.append(current_row)

    # Sort each row by the x-coordinate
    sorted_contours = []
    for row in rows:
        sorted_row = sorted(row, key=lambda c: cv2.boundingRect(c)[0])
        sorted_contours.extend(sorted_row)

    return sorted_contours

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














