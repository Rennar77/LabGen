import os
from pathlib import Path
import torch
from transformers import AutoProcessor, BarkModel
from scipy.io.wavfile import write as write_wav

def generate_speech_from_text(text: str, task_id: str, scene_index: int) -> str:
    print(f"HUGGINGFACE_TTS_GEN: Generating speech for scene {scene_index}: '{text[:50]}...'")
    
    output_dir = Path(f"output/{task_id}/audio")
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path = output_dir / f"hf_scene_{scene_index}.wav"
    
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"HUGGINGFACE_TTS_GEN: Using device: {device}")

        processor = AutoProcessor.from_pretrained("suno/bark-small")
        model = BarkModel.from_pretrained("suno/bark-small")
        
        if device == "cuda":
            # if torch.cuda.is_available() and torch.cuda.get_device_capability()[0] >= 7:
            #     model = model.to_bettertransformer() # for flash attention
            model.to(device)
        else:
             model.to(device)


        # Bark can benefit from this on lower VRAM GPUs
        if device == "cuda":
             model.enable_offload_cpu()


        inputs = processor(text, voice_preset="v2/en_speaker_6", return_tensors="pt").to(device)
        
        # Generate audio
        with torch.no_grad():
            speech_output = model.generate(**inputs, do_sample=True, fine_temperature=0.4, coarse_temperature=0.8)

        sampling_rate = model.generation_config.sample_rate
        audio_array = speech_output.cpu().numpy().squeeze()
        
        write_wav(file_path, rate=sampling_rate, data=audio_array)

        print(f"HUGGINGFACE_TTS_GEN: Saved audio to {file_path}")

    except Exception as e:
        print(f"HUGGINGFACE_TTS_GEN: An error occurred during speech generation: {e}")
        with open(file_path, 'w') as f:
            f.write(f"Error generating audio for text: {text}")
        return str(file_path)

    return str(file_path)
