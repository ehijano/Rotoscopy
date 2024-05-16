
import torch
from torchvision.models.detection import maskrcnn_resnet50_fpn, MaskRCNN_ResNet50_FPN_Weights
from PIL import Image, ImageEnhance, ImageFilter
from torchvision import transforms
import argparse
import os
import concurrent.futures
from typing import Callable, Any, Iterable
from dataclasses import dataclass
from tqdm import tqdm


PIXEL_PATH = "data\\pix"
IMAGE_PATH = "data\\img"

CONFIDENCE_TH = 0.7
AREA_TH = 25
SCALE = 0.1
ENHACEMENT=1.5

# Load a pre-trained Mask R-CNN model
MODEL = maskrcnn_resnet50_fpn(weights=MaskRCNN_ResNet50_FPN_Weights.DEFAULT)
MODEL.eval()

def paralell_call(
        callable: Callable[...,Any],
        args_generator: Iterable[Any],
)->list[Any]:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(callable, arg) for arg in args_generator]
        return [future.result() for future in tqdm(concurrent.futures.as_completed(futures), total = len(futures))]
    

@dataclass
class ImageStats:
    image_path:str
    image_name:str
    frame_name:str

def segment_and_pixelate(image_stats:ImageStats,):


    image_path = image_stats.image_path
    image_name = image_stats.image_name
    frame_name = image_stats.frame_name

    # Load the image
    image = Image.open(
        image_path
        ).convert("RGB")


    # Convert image to tensor
    transform = transforms.Compose([
        transforms.ToTensor()
    ])
    image_tensor = transform(image).unsqueeze(0)

    # Perform segmentation
    with torch.no_grad():
        prediction = MODEL(image_tensor)

    
    # Initialize a mask to keep track of relevant areas
    relevant_mask = torch.zeros_like(prediction[0]['masks'][0, 0], dtype=torch.bool)

    # Process each detection
    for score, label, mask in zip(prediction[0]['scores'], prediction[0]['labels'], prediction[0]['masks']):
        # Check if the detection meets all criteria
        if score > CONFIDENCE_TH  and mask.sum() > AREA_TH:
            relevant_mask |= (mask[0] > 0.5) 


    # Apply mask to the image
    masked_image = Image.fromarray((relevant_mask.numpy() * 255).astype('uint8'), mode='L')
    new_image = Image.composite(image, Image.new("RGBA", image.size, (0, 0, 0, 0)), masked_image)

    # Resize image for pixel art
    new_size = (int(new_image.width * SCALE), int(new_image.height * SCALE))
    pixelated_image = new_image.resize(new_size, resample=Image.NEAREST)

    # Optionally enhance colors to make it more vibrant
    enhancer = ImageEnhance.Color(pixelated_image)
    small_image = enhancer.enhance(ENHACEMENT)
    
    # Apply a slight blur to soften the edges
    small_image = small_image.filter(ImageFilter.SMOOTH_MORE)

    # Save the pixelated image
    output_path = os.path.join(os.path.join(PIXEL_PATH, image_name) , frame_name)
    os.makedirs(os.path.dirname(output_path),exist_ok=True)
    small_image.save(output_path)

def main():
    parser = argparse.ArgumentParser(description="Extract frames from video at specified FPS.")
    parser.add_argument("input_image", type=str, help="Path to the input video file.")
    
    args = parser.parse_args()

    folder = os.path.join(IMAGE_PATH, args.input_image)

    #for image_file in os.listdir(folder):
    #    segment_and_pixelate(os.path.join(folder, image_file),MODEL, image_name = args.input_image, frame_name = image_file)

    args_generator = (ImageStats(image_path=os.path.join(folder, image_file), image_name=args.input_image, frame_name=image_file) for image_file in os.listdir(folder))
    _ = paralell_call(segment_and_pixelate, args_generator=args_generator)


# python src/i2p.py horse.mp4
if __name__ == "__main__":
    main()