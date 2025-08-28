import os
import logging
from openai import OpenAI
import requests
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e:
    logger.error(f"Failed to initialize OpenAI client: {e}")
    client = None

def generate_image_from_prompt(prompt: str, task_id: str, scene_index: int) -> str:
    """
    Calls the OpenAI DALL-E 3 API to generate an image from a prompt and saves it.
    """
    if not client:
        logger.error("OpenAI client not initialized. Cannot generate image.")
        raise ConnectionError("OpenAI client is not initialized. Check API Key.")

    logger.info(f"[Task: {task_id}, Scene: {scene_index}] Generating image with DALL-E 3. Prompt: '{prompt}'")

    output_dir = f"media/output/{task_id}"
    os.makedirs(output_dir, exist_ok=True)
    file_path = f"{output_dir}/scene_{scene_index}.png"

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        image_url = response.data[0].url
        logger.info(f"[Task: {task_id}, Scene: {scene_index}] Image generated, URL: {image_url}")

        image_response = requests.get(image_url, timeout=60)
        image_response.raise_for_status()

        with open(file_path, 'wb') as f:
            f.write(image_response.content)
            
        logger.info(f"[Task: {task_id}, Scene: {scene_index}] Image successfully saved to: {file_path}")
        return file_path

    except Exception as e:
        logger.error(f"[Task: {task_id}, Scene: {scene_index}] Failed to generate or save image: {e}")
        raise
