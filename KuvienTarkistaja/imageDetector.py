import cv2
import numpy as np
from ultralytics import YOLO
import matplotlib.pyplot as plt
import os
import threading
from memory_profiler import profile
import gc

count = 0
amountOfFiles = 0

def detect_objects(image_path, model):
    """
    Detect objects in an image using YOLOv8.
    
    Args:
        image_path: Path to the input image
    
    Returns:
        Detected objects and class labels.
    """
    # Load YOLO model
    #model = YOLO()  # Load the model
    
    # Read image
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Perform detection
    results = model(image_rgb)[0]
    
    # Create a copy of the image for drawing
    annotated_image = image_rgb.copy()
    
    # Generate random colors for classes
    np.random.seed(42)  # For consistent colors
    colors = np.random.randint(0, 255, size=(100, 3), dtype=np.uint8)
    
    # To hold class names and their corresponding colors
    class_labels = {}
    
    # Process detections
    boxes = results.boxes
    names = results.names
    return boxes, names, annotated_image, colors

#TO DO VARMISTA ETTEI VUODA MUISTIA

def show_results(image_path,model, img_name, confidence_threshold):
    """
    Show original image and detection results side by side.

    Args:
        image_path: Path to the input image
        confidence_threshold: Minimum confidence score for detections
    """
    # Read original image
    original_image = cv2.imread(image_path)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    
    # Get detection results
    boxes, class_names, annotated_image, colors = detect_objects(image_path, model)
    
    
    if len(boxes) <= 0:
        return
    
    hasOnlyBench = 1
    # Process each detected object and apply confidence threshold filtering
    class_labels = {}
    for box in boxes:
        # Get box coordinates
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        
        # Get confidence score
        confidence = float(box.conf[0])
        
        # Only show detections above confidence threshold
        if confidence > confidence_threshold:
            # Get class id and name
            class_id = int(box.cls[0])
            class_name = class_names[class_id]
            
            # Get color for this class
            color = colors[class_id % len(colors)].tolist()
            
            # Draw bounding box
            cv2.rectangle(annotated_image, (x1, y1), (x2, y2), color, 2)
            
            # Store class name and color for legend
            class_labels[class_name] = color
            print(class_name)
            if class_name != 'bench':
                hasOnlyBench = 0

    if hasOnlyBench == 1: 
        return
            
    
    # Create figure
    
    # Show original image
    plt.subplot(1, 2, 1)
    plt.title('Alkuperäinen Kuva')
    plt.imshow(original_image)
    plt.axis('off')
    
    # Show detection results
    plt.subplot(1, 2, 2)
    plt.title('Huomatut objektit')
    plt.imshow(annotated_image)
    plt.axis('off')

    # Create legend
    legend_handles = []
    for class_name, color in class_labels.items():
        normalized_color = np.array(color) / 255.0  # Normalize the color
        legend_handles.append(plt.Line2D([0], [0], marker='o', color='w', label=class_name,
                                           markerfacecolor=normalized_color, markersize=10))

    plt.legend(handles=legend_handles, loc='upper right', title='Classes')

    plt.tight_layout()
    plt.savefig(final_output_directory + "/" + str(img_name) + "_detection.png")
    print(final_output_directory + "/" + str(img_name) + "_detection.png")
    plt.clf()
    del(boxes, class_names, annotated_image, colors)

# Example usage:
final_input_directory = ""
final_output_directory = ""

def set_input_directory(input_directory):
    global final_input_directory 
    final_input_directory = input_directory

def set_output_directory(output_directory):
    global final_output_directory 
    final_output_directory = output_directory

def delete_files_in_output_directory(output_directory):
    try:
        files = os.listdir(output_directory)
        for file in files:
            file_path = os.path.join(output_directory, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print("All files deleted successfully.")
    except OSError:
     print("Error occurred while deleting files.")
     quit()
     
def detect_files_in_input_directory(model): ##TO DO KORJAA MUISTIVUOTO
    count = 0
    delete_files_in_output_directory(final_output_directory)
    directory = final_input_directory
    amountOfFiles = 0

    for file in os.scandir(directory):
        extension = file.name[len(file.name) - 3] + file.name[len(file.name) - 2] + file.name[len(file.name) - 1]
        if extension.lower() != 'jpg' and extension.lower() != 'png':
            continue
        else:
            amountOfFiles += 1

    for entry in os.scandir(directory):
        #print(entry.name)
        extension = entry.name[len(entry.name) - 3] + entry.name[len(entry.name) - 2] + entry.name[len(entry.name) - 1]
        extension = extension.lower()
        print(extension)
        
        if extension != 'jpg' and extension != 'png':
            continue
        else:
            show_results(entry.path, model, entry.name[:-4], confidence_threshold=0.2)
            count += 1

@profile
def startDetecting(folder_input_path, folder_output_path):
    gc.enable()
    model = YOLO()
    set_input_directory(folder_input_path)
    set_output_directory(folder_output_path)
    plt.figure(figsize=(15, 7))
    detect_files_in_input_directory(model)
    percentageLeft()
    gc.disable()

def percentageLeft():
        while count < amountOfFiles:
            print(float(count / amountOfFiles))

class imageDetector:
    def __init__(self, folder_input_path, folder_output_path):
        self.folder_input_path = folder_input_path
        self.folder_output_path = folder_output_path
        detect_thread = threading.Thread(target=startDetecting, name="detecter", args=[folder_input_path,folder_output_path])
        detect_thread.start()