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
import requests
from pathlib import Path
from dotenv import load_dotenv
import os
import json


load_dotenv()

HF_API_KEY = os.getenv("HUGGINGFACE_API_TOKEN")


def generate_speech_from_text_inference(text: str, task_id: str, scene_index: int, speaker_wav: str = None, language="en") -> str:
    """
    HuggingFace Inference API version of XTTS-v2 speech generation.
    """

    print(f"HF_TTS: Generating speech for scene {scene_index}...")

    output_dir = Path(f"output/{task_id}/audio")
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path = output_dir / f"scene_{scene_index}.wav"

    # Read speaker reference if provided
    ref_audio_bytes = None
    if speaker_wav:
        with open(speaker_wav, "rb") as f:
            ref_audio_bytes = f.read()

    payload = {
        "inputs": text,
        "parameters": {
            "language": language,
        }
    }

    files = {
        "json": (None, json.dumps(payload), "application/json")
    }

    if ref_audio_bytes:
        files["speaker_wav"] = ("speaker.wav", ref_audio_bytes, "audio/wav")

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
    }

    response = requests.post(
        "https://api-inference.huggingface.co/models/coqui/XTTS-v2",
        headers=headers,
        files=files,
    )

    if response.status_code != 200:
        print("HF_TTS ERROR:", response.text)
        with open(file_path, "w") as f:
            f.write("TTS generation failed")
    else:
        with open(file_path, "wb") as f:
            f.write(response.content)

    print(f"HuggingFace TTS saved → {file_path}")
    return str(file_path)
