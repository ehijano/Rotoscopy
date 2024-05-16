from PIL import Image
import argparse
import os

OUTPUT_PATH = "data\\gif"
OUTPUT_SPRITE_PATH = "data\\sprite"
PIXEL_PATH = "data\\pix"

def create_gif(input_folder, output_file, sprite_output_file, frame_duration=1000):
    # Get list of PNG files in the input_folder
    images = [img for img in os.listdir(input_folder) if img.endswith(".png")]
    # Sort images to ensure they are in the correct order
    images.sort()
    
    # Define the background color and mode
    background_color = (255, 255, 255)  # White background, adjust as needed
    
    frames = []
    for img in images:
        frame = Image.open(os.path.join(input_folder, img))
        # Convert to RGBA to handle transparency in source images
        rgba_frame = frame.convert("RGBA")
        # Create a new image with white background
        background = Image.new("RGBA", rgba_frame.size, background_color + (255,))
        # Composite the image over the background
        background.paste(rgba_frame, mask=rgba_frame)
        frames.append(background.convert("RGB"))  # Convert to RGB to avoid GIF issues with RGBA


    # Save frames as a GIF
    frames[0].save(
        output_file,
        format='GIF',
        append_images=frames[1:],
        save_all=True,
        duration=frame_duration,
        loop=0
    )


    # Create sprite image
    sprite_width = frames[0].width * len(frames)
    sprite_height = frames[0].height
    sprite_image = Image.new("RGB", (sprite_width, sprite_height), background_color)
    
    for index, frame in enumerate(frames):
        sprite_image.paste(frame, (index * frame.width, 0))
    
    # Save the sprite image
    sprite_image.save(sprite_output_file, format='PNG')

def main():
    parser = argparse.ArgumentParser(description="Extract frames from video at specified FPS.")
    parser.add_argument("input_path", type=str, help="Path to the input image files.")
    
    args = parser.parse_args()
    create_gif(
        input_folder = os.path.join(PIXEL_PATH,args.input_path), 
        output_file=os.path.join(OUTPUT_PATH,f'{args.input_path}.gif'), 
        sprite_output_file=os.path.join(OUTPUT_SPRITE_PATH,f'{args.input_path}.png'),
        frame_duration=100)


# python src/p2g.py horse.mp4
if __name__ == "__main__":
    main()