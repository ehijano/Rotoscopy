import argparse
import cv2
import os
import sys



OUTPUT_FOLDER = 'data\\img'
VIDEO_FOLDER = 'data\\vid'

def save_frames(video_name:str, fps:int=12) -> None:

    output_folder = os.path.join(OUTPUT_FOLDER, video_name)
    video_path = os.path.join(VIDEO_FOLDER, video_name)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    if not os.path.isfile(video_path):
        raise Exception("No video file found")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(video_fps / fps)
    
    frame_count = 0
    saved_frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_count % frame_interval == 0:
            cv2.imwrite(os.path.join(output_folder, f"frame_{saved_frame_count}.png"), frame)
            saved_frame_count += 1
        
        frame_count += 1
    
    cap.release()
    print(f"Saved {saved_frame_count} frames.")

def main():
    parser = argparse.ArgumentParser(description="Extract frames from video at specified FPS.")
    parser.add_argument("video_name", type=str, help="Path to the input video file.")
    parser.add_argument("--fps", type=int, default=12, help="Frames per second to extract (default is 12).")
    
    args = parser.parse_args()
    
    save_frames(video_name=args.video_name, fps = args.fps)

# python src/v2i.py horse.mp4 --fps 12
if __name__ == "__main__":
    main()