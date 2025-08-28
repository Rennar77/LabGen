import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e:
    logger.error(f"Failed to initialize OpenAI client: {e}")
    client = None

def generate_speech_from_text(text: str, task_id: str, scene_index: int) -> str:
    """
    Calls the OpenAI Text-to-Speech (TTS) API to generate audio from text.
    """
    if not client:
        logger.error("OpenAI client not initialized. Cannot generate speech.")
        raise ConnectionError("OpenAI client is not initialized. Check API Key.")

    logger.info(f"[Task: {task_id}, Scene: {scene_index}] Generating speech with OpenAI TTS. Text: '{text}'")

    output_dir = f"media/output/{task_id}"
    os.makedirs(output_dir, exist_ok=True)
    file_path = f"{output_dir}/scene_{scene_index}.mp3"

    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )

        response.stream_to_file(file_path)
        
        logger.info(f"[Task: {task_id}, Scene: {scene_index}] Audio successfully saved to: {file_path}")
        return file_path

    except Exception as e:
        logger.error(f"[Task: {task_id}, Scene: {scene_index}] Failed to generate or save audio: {e}")
        raise
