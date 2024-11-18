import cv2
from PIL import Image
import fitz  # PyMuPDF
import numpy as np


def load_and_label_pdf(pdf_path, part_name):
    # Open the PDF and get the first page
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)
    
    # Render page to an image with high DPI
    pix = page.get_pixmap(dpi=300)
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    
    # Convert to a format usable by OpenCV
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    # Detect and label objects in the image
    coordinates = detect_and_label_objects(image, part_name)
    
    # Save the labeled image as a new PDF page
    labeled_pdf_path = "labeled_output.pdf"
    save_image_as_pdf(image, labeled_pdf_path)
    
    # Display the labeled image using OpenCV
    # cv2.imshow('Labeled Image', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

def detect_and_label_objects(image, part_name):
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

    # List to store coordinates of bounding boxes
    coordinates = []

    if "Ford" in part_name:
        label_prefixes = ["AA", "CC", "DD", "GG", "CCB"]
    else:
        label_prefixes = ["M1", "M2"]

     # Extract the last four digits from the lab number
    lab_number = "24-2020" #get the lab number
    last_four_digits = lab_number.split('-')[-1]

    # Loop through each contour and label the objects
    for i, contour in enumerate(contours):
        # Get the bounding box for each contour
        x, y, w, h = cv2.boundingRect(contour)
        coordinates.append((x, y, w, h))
        
        # Draw a rectangle around each object and label it
        # Only reactivate if planning to develop and need some indicators of where your object is
        # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Red color for visibility
        # Use the appropriate label
        if i < len(label_prefixes):
            label = f"{label_prefixes[i]} - {last_four_digits}"  # Replace 'XXXX' with the actual lab number
        else:
            label = f"Object {i + 1}"
        cv2.putText(image, label, (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0, 0, 255), 2)
    
    return coordinates

def save_image_as_pdf(image, output_path):
    # Convert the labeled image back to RGB (Pillow format)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image)
    
    # Save the image as a PDF
    pil_image.save(output_path, "PDF", resolution=300.0)

# Path to your uploaded PDF
pdf_path = "round_3.pdf"
part_name = "Ford Bronco"
load_and_label_pdf(pdf_path, part_name)



