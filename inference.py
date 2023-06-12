from ultralytics import YOLO
import supervision as sv
import cv2
import numpy as np

model = YOLO('detection.pt')
generator = sv.get_video_frames_generator('test_vid.mp4')
no_of_frames = len(list(generator))#find a better method
generator = sv.get_video_frames_generator('test_vid.mp4')
#writing video 
frameSize = (480, 848)
out = cv2.VideoWriter('inference.avi',cv2.VideoWriter_fourcc(*'DIVX'), 60, frameSize)
#
for i in range(no_of_frames): 
    iterator = iter(generator)
    frame = next(iterator)
    # detect
    results = model(frame, imgsz=1280)[0]
    detections = sv.Detections.from_yolov8(results)
    # annotate
    box_annotator = sv.BoxAnnotator(thickness=4, text_thickness=4, text_scale=2)
    frame = box_annotator.annotate(scene=frame, detections=detections, labels = 'stock empty!')
    #write
    out.write(frame)
out.release()
