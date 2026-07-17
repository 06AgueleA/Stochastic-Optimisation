import cv2
import pandas as pd
from ultralytics import YOLO
import math

# KEY VARIABLES
VIDEO_PATH = 'IntersectionCam.mp4'
MODEL_PATH = 'yolov8n.pt'  

# ALL OCCUPANCY ZONES
ZONES = {
    "North": [0, 300, 350, 345],     
    "East":  [1670, 205, 1720, 580], 
    "South": [1200, 840, 1460, 880], 
    "West":  [0, 660, 150, 730]      
}

#Function to generate vehicle counts
def generate_counts():
    model = YOLO(MODEL_PATH)
    cap = cv2.VideoCapture(VIDEO_PATH)
    
    #Get precise FPS (Approximately 30 for this video)
    fps = math.ceil((cap.get(cv2.CAP_PROP_FPS)))
    print(fps)
    
    # Dictionary to hold the overall MAX count for each second
    results_by_second = {}
    frame_index = 0

    while cap.isOpened():
        success, frame = cap.read()
        if not success: break
        
        # Determine the current real-world second of the video
        current_second = frame_index // fps
        
        # Initialize this second if its a new second
        if current_second not in results_by_second:
            results_by_second[current_second] = {"North": 0, "East": 0, "South": 0, "West": 0}
            
        # Could potentially set conf=0.20 to account for obscured/dark vehicles
        results = model(frame, classes=[2, 3, 5, 7], conf=0.25, verbose=False)
        
        # Tally cars currently inside the zones for this specific frame (Resets each frame)
        frame_counts = {"North": 0, "East": 0, "South": 0, "West": 0}
        
        for box in results[0].boxes:
            x_c, y_c = box.xywh[0][0].item(), box.xywh[0][1].item()
            for name, roi in ZONES.items():
                if roi[0] <= x_c <= roi[2] and roi[1] <= y_c <= roi[3]:
                    frame_counts[name] += 1
                    
        #(MAXIMUM LOGIC) Update the current second's count if this frame saw more cars than any other frame
        for name in ZONES.keys():
            if frame_counts[name] > results_by_second[current_second][name]:
                results_by_second[current_second][name] = frame_counts[name]

        #Move to the next frame
        frame_index += 1
        if frame_index % (fps * 10) == 0:
            print(f"Processed {current_second} seconds...")

    cap.release()
    
    #Format data for CSV (Sorts counts for each consecutive second)
    df_data = []
    for sec, counts in sorted(results_by_second.items()):
        row = {"second": sec}
        row.update(counts)
        df_data.append(row)
        
    df = pd.DataFrame(df_data)
    df.to_csv('traffic_counts.csv', index=False)
    print("\nSuccess: traffic_counts.csv generated.")

#Generates CSV (Function call)
generate_counts()


