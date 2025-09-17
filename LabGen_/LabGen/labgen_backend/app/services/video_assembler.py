import os
import moviepy
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

def assemble_video_from_assets(image_paths: list, audio_paths: list, task_id: str) -> str:
    """
    Assemble a video from image + audio assets using MoviePy.
    """
    print(f"Task {task_id}: Starting REAL video assembly.")

    output_dir = "generated_videos"
    os.makedirs(output_dir, exist_ok=True)
    output_video_path = os.path.join(output_dir, f"{task_id}.mp4")

    scene_clips = []
    for i, (img, aud) in enumerate(zip(image_paths, audio_paths)):
        try:
            audio_clip = AudioFileClip(aud)
            img_clip = ImageClip(img).set_duration(audio_clip.duration)
            scene = img_clip.set_audio(audio_clip)
            scene_clips.append(scene)
            print(f"Task {task_id}, Scene {i+1}: Added {img} + {aud}")
        except Exception as e:
            print(f"Task {task_id}, Scene {i+1}: Error processing assets -> {e}")

    if scene_clips:
        final_video = concatenate_videoclips(scene_clips, method="compose")
        final_video.write_videofile(output_video_path, fps=24)
        print(f"Task {task_id}: Final video saved at {output_video_path}")
    else:
        print(f"Task {task_id}: No clips generated, writing placeholder.")
        with open(output_video_path, "w") as f:
            f.write("Error: No clips generated.")

    return output_video_path
