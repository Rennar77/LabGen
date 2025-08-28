import json
from .protocol_parser import parse_protocol
from .storyboard_generator import generate_storyboard_from_steps
from .video_assembler import assemble_video_from_assets
from app.core.config import GENERATION_BACKEND

# Import all possible generator backends
from . import openai_image_generator
from . import openai_tts_generator
from . import huggingface_image_generator
from . import huggingface_tts_generator

# Select the generator functions based on configuration at module load time
if GENERATION_BACKEND == "huggingface":
    image_generator = huggingface_image_generator.generate_image_from_prompt
    tts_generator = huggingface_tts_generator.generate_speech_from_text
    print("INFO: Using Hugging Face generation backend.")
else:
    image_generator = openai_image_generator.generate_image_from_prompt
    tts_generator = openai_tts_generator.generate_speech_from_text
    print("INFO: Using OpenAI generation backend (default).")


def process_video_generation(task_id: str, tasks: dict):
    print(f"Starting video generation for task: {task_id}")
    
    protocol_text = tasks[task_id].get("protocol_text")

    if not protocol_text:
        print(f"Error: Protocol text not found for task {task_id}. Marking as FAILED.")
        tasks[task_id]["status"] = "FAILED"
        return

    try:
        tasks[task_id]["status"] = "PROCESSING"
        
        # Step 1: Parse protocol text into structured steps
        print(f"Task {task_id}: Parsing protocol text...")
        structured_protocol = parse_protocol(protocol_text)
        print(f"Task {task_id}: Protocol parsed. Structured output:")
        print(json.dumps(structured_protocol, indent=2))

        # Step 2: Generate storyboard from structured steps
        print(f"Task {task_id}: Generating storyboard...")
        storyboard = generate_storyboard_from_steps(structured_protocol)
        print(f"Task {task_id}: Storyboard generated. Full storyboard JSON:")
        print(json.dumps(storyboard, indent=2))
        
        # Step 3: Generate assets (images and audio) for each scene
        print(f"Task {task_id}: Generating scene assets...")
        generated_assets = []
        image_paths = []
        audio_paths = []
        
        for scene in storyboard:  # storyboard is a list, not a dict
            scene_index = scene.get("scene_number")
            visual_prompt = scene.get("visual_description")   # <-- matches your JSON
            narration_script = scene.get("narration_script")  # <-- matches your JSON

            # Generate image using the selected backend
            image_path = image_generator(visual_prompt, task_id, scene_index)
            print(f"Task {task_id}, Scene {scene_index}: Generated image at {image_path}")

            # Generate audio using the selected backend
            audio_path = tts_generator(narration_script, task_id, scene_index)
            print(f"Task {task_id}, Scene {scene_index}: Generated audio at {audio_path}")

            generated_assets.append({
                "scene": scene_index,
                "image": image_path,
                "audio": audio_path
            })
            image_paths.append(image_path)
            audio_paths.append(audio_path)

        tasks[task_id]["assets"] = generated_assets
        print(f"Task {task_id}: All scene assets generated.")

        # Step 4: Combine assets into a video
        print(f"Task {task_id}: Assembling final video...")
        final_video_path = assemble_video_from_assets(image_paths, audio_paths, task_id)

        # Finalize task
        tasks[task_id]["status"] = "COMPLETED"
        tasks[task_id]["video_url"] = final_video_path
        print(f"Task {task_id} status: COMPLETED")
        print(f"Task {task_id} final video URL: {tasks[task_id]['video_url']}")

    except Exception as e:
        print(f"An error occurred during video generation for task {task_id}: {e}")
        tasks[task_id]["status"] = "FAILED"
