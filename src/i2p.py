
import torch
from torchvision.models.detection import maskrcnn_resnet50_fpn
from PIL import Image
from torchvision import transforms
import argparse
import os

PIXEL_PATH = "data\\pix"
IMAGE_PATH = "data\\img"

CONFIDENCE_TH = 0.8
AREA_TH = 25

def segment_and_pixelate(image_path, scale_factor=0.1):
    # Load the image
    image = Image.open(
        os.path.join(IMAGE_PATH, image_path)
        ).convert("RGB")

    # Load a pre-trained Mask R-CNN model
    model = maskrcnn_resnet50_fpn(pretrained=True)
    model.eval()

    # Convert image to tensor
    transform = transforms.Compose([
        transforms.ToTensor()
    ])
    image_tensor = transform(image).unsqueeze(0)

    # Perform segmentation
    with torch.no_grad():
        prediction = model(image_tensor)



    
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
    new_size = (int(new_image.width * scale_factor), int(new_image.height * scale_factor))
    pixelated_image = new_image.resize(new_size, resample=Image.NEAREST)

    # Save the pixelated image
    output_path = os.path.join(PIXEL_PATH, image_path)
    os.makedirs(os.path.dirname(output_path),exist_ok=True)
    pixelated_image.save(output_path)

def main():
    parser = argparse.ArgumentParser(description="Extract frames from video at specified FPS.")
    parser.add_argument("input_image", type=str, help="Path to the input video file.")
    
    args = parser.parse_args()

    segment_and_pixelate(args.input_image,)


# python src/i2p.py horse.mp4\frame_4.png
if __name__ == "__main__":
    main()