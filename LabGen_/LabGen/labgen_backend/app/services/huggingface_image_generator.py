import os
from pathlib import Path
import torch
from diffusers import StableDiffusionPipeline

def generate_image_from_prompt(prompt: str, task_id: str, scene_index: int) -> str:
    print(f"HUGGINGFACE_IMG_GEN: Generating image for scene {scene_index} with prompt: '{prompt}'")
    
    output_dir = Path(f"output/{task_id}/images")
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path = output_dir / f"hf_scene_{scene_index}.png"

    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"HUGGINGFACE_IMG_GEN: Using device: {device}")

        torch_dtype = torch.float16 if device == "cuda" else torch.float32
        
        pipe = StableDiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-2-1",
            torch_dtype=torch_dtype
        )
        pipe = pipe.to(device)

        image = pipe(prompt).images[0]

        image.save(file_path)
        print(f"HUGGINGFACE_IMG_GEN: Saved image to {file_path}")
        
    except Exception as e:
        print(f"HUGGINGFACE_IMG_GEN: An error occurred during image generation: {e}")
        # As a fallback, create a placeholder file to avoid breaking the pipeline
        with open(file_path, 'w') as f:
            f.write(f"Error generating image for prompt: {prompt}")
        return str(file_path)

    return str(file_path)
