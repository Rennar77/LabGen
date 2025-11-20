# import os
# from pathlib import Path
# import torch
# from diffusers import StableDiffusionPipeline
# from dotenv import load_dotenv

# load_dotenv()

# # Load the model once globally (instead of reloading for every scene)
# def load_hf_pipeline():
#     device = "cuda" if torch.cuda.is_available() else "cpu"
#     torch_dtype = torch.float16 if device == "cuda" else torch.float32

#     print(f"HUGGINGFACE_IMG_GEN: Loading Stable Diffusion on {device} with dtype {torch_dtype}")

#     pipe = StableDiffusionPipeline.from_pretrained(
#         "stabilityai/stable-diffusion-2-1",
#         torch_dtype=torch_dtype
#     )
#     pipe = pipe.to(device)

#     # Enable some performance optimizations if not on CPU
#     if device == "cuda":
#         pipe.enable_attention_slicing()  # reduces VRAM usage
#         pipe.enable_sequential_cpu_offload()  # offload unused weights to CPU

#     return pipe

# # Global pipeline instance (reused across scenes)
# HF_PIPE = load_hf_pipeline()

# def generate_image_from_prompt(prompt: str, task_id: str, scene_index: int) -> str:
#     print(f"HUGGINGFACE_IMG_GEN: Generating image for scene {scene_index} with prompt: '{prompt}'")

#     output_dir = Path(f"output/{task_id}/images")
#     output_dir.mkdir(parents=True, exist_ok=True)
#     file_path = output_dir / f"hf_scene_{scene_index}.png"

#     try:
#         image = HF_PIPE(prompt).images[0]
#         image.save(file_path)
#         print(f"HUGGINGFACE_IMG_GEN: Saved image to {file_path}")

#     except Exception as e:
#         print(f"HUGGINGFACE_IMG_GEN: Error during image generation: {e}")
#         # Fallback: placeholder file
#         with open(file_path, 'w') as f:
#             f.write(f"Error generating image for prompt: {prompt}")
#         return str(file_path)

#     return str(file_path)
import os
from pathlib import Path
import requests
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HUGGINGFACE_API_TOKEN")

def generate_image_from_prompt(prompt: str, task_id: str, scene_index: int) -> str:
    """
    Generate an image from a prompt using HuggingFace Inference Router API
    (Stable Diffusion 2.1). Saves output to output/{task_id}/images.
    """
    print(f"HUGGINGFACE_IMG_GEN: Generating image for scene {scene_index} with prompt: '{prompt}'")

    # Prepare output directory
    output_dir = Path(f"output/{task_id}/images")
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path = output_dir / f"hf_scene_{scene_index}.png"

    # Prepare request
    payload = {"inputs": prompt}
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}

    try:
        response = requests.post(
            "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-2-1",
            headers=headers,
            json=payload,
            timeout=180  # allow extra time for large image generation
        )

        if response.status_code != 200:
            print("HF_IMG ERROR:", response.text)
            # Fallback placeholder file
            with open(file_path, "w") as f:
                f.write(f"Image generation failed: {response.text}")
            return str(file_path)

        # Save generated image
        with open(file_path, "wb") as f:
            f.write(response.content)

        print(f"HUGGINGFACE_IMG_GEN: Saved image → {file_path}")

    except Exception as e:
        print(f"HUGGINGFACE_IMG_GEN: Exception during image generation: {e}")
        # Fallback placeholder file
        with open(file_path, "w") as f:
            f.write(f"Exception generating image: {e}")
        return str(file_path)

    return str(file_path)
