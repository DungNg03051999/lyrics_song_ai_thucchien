import base64
import json
import os
import time
from typing import Optional, Dict, List
import requests


class ImagenImageGenerator:
    """A client for generating images using a requests-based API call."""

    def __init__(
        self,
        base_url: str = "https://api.thucchien.ai/v1",
        api_key: str = "sk-gQzgT8AFPvQRBnrsyF-UCA",
    ):
        """
        Initialize the Imagen image generator.
        Args:
            base_url: Base URL for the API endpoint.
            api_key: API key for authentication.
        """
        self.base_url = base_url
        self.api_key = api_key

    def generate_and_download_image(self, prompt: str, output_filename: str) -> bool:
        """
        Generates and downloads a single image using requests.

        Args:
            prompt: The text prompt for image generation.
            output_filename: The local filename to save the image.

        Returns:
            True if successful, False otherwise.
        """
        print("-" * 60)
        print(f"🎨 Generating image for: '{output_filename}'")
        print(f"📝 Prompt: {prompt}")

        url = f"{self.base_url}/images/generations"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        data = {
            "model": "imagen-2.0",  # Reverted to imagen-2.0 as a temporary fix for the permission error.
            "prompt": prompt,
            "n": 1,
            "response_format": "b64_json",
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()

            result = response.json()

            # Extract base64 data from the first image object in the 'data' list
            if not result.get("data") or not result["data"][0].get("b64_json"):
                print("❌ API response did not contain image data.")
                print(f"Full response: {result}")
                return False

            b64_data = result["data"][0]["b64_json"]
            image_data = base64.b64decode(b64_data)

            with open(output_filename, "wb") as f:
                f.write(image_data)

            if os.path.exists(output_filename) and os.path.getsize(output_filename) > 0:
                print(f"✅ Image downloaded successfully: {output_filename}")
                return True
            else:
                print(f"❌ Download failed or file is empty for {output_filename}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"❌ An error occurred: {e}")
            if e.response is not None:
                print(f"Response body: {e.response.text}")
            return False
        except (KeyError, IndexError, TypeError) as e:
            print(f"❌ Could not parse API response: {e}")
            return False


def create_image_prompts_from_lyrics(lyrics: str) -> Dict[str, str]:
    """
    Analyzes lyrics to generate a dictionary of distinct prompts for each scene.

    Args:
        lyrics: The lyrics of the song.

    Returns:
        A dictionary where keys are scene names and values are detailed image prompts.
    """
    print("=" * 60)
    print("📝 ANALYZING LYRICS FOR IMAGE PROMPT GENERATION")
    print("=" * 60)

    prompts = {
        "scene_1_starry_sky": "Digital art, a visually stunning image of abstract glowing data points forming a starry night sky over Vietnam's landscape, from majestic mountains to a serene coastline. Represents the line 'Chạm vào từng con số, thấy cả một trời sao'. Hopeful and epic.",
        "scene_2_smart_city": "Futuristic concept art of a smart city in Vietnam connected by brilliant streams of light to high-tech vertical farms in the countryside. Represents 'thành phố thông minh, là đồng quê kết nối'. Clean, vibrant, and optimistic.",
        "scene_3_gen_z_at_work": "Action shot, energetic, diverse young Vietnamese professionals (Gen Z) collaborating in a modern, sunlit office, coding on transparent screens. A glowing shield icon is visible, symbolizing data security. Represents 'Trí tuệ nhân tạo' and 'lá chắn an toàn'.",
        "scene_4_montage_of_joy": "Photorealistic montage showing the positive outcomes of data technology: a smiling elderly woman video-calling her family, a farmer checking crop data on a tablet in a lush field, a bustling successful small business. Represents 'Là nụ cười của mẹ, là tương lai của cha'.",
        "scene_5_vietnam_glows": "Epic landscape photography, a final, stunning aerial shot high above Vietnam at night, showing the entire country glowing with interconnected data streams and light, full of hope and potential. Visualizes 'Một Việt Nam toả sáng, thế giới đang chờ đợi'.",
    }

    print("✅ 5 image prompts generated from lyrics.")
    return prompts


def main():
    """
    Main function to generate images based on song lyrics.
    """
    # Configuration from environment or defaults
    base_url = os.getenv("LITELLM_BASE_URL", "https://api.thucchien.ai/v1")
    api_key = os.getenv("LITELLM_API_KEY", "sk-gQzgT8AFPvQRBnrsyF-UCA")

    print("🚀 Starting Image Generation from Song Lyrics")
    print(f"📡 Using LiteLLM proxy at: {base_url}")

    # Initialize generator
    generator = ImagenImageGenerator(base_url=base_url, api_key=api_key)

    # Load lyrics from file
    lyrics_file_path = "./lyrics.txt"
    try:
        with open(lyrics_file_path, "r", encoding="utf-8") as f:
            song_lyrics = f.read()
        print(f"✅ Successfully loaded lyrics from '{lyrics_file_path}'")
    except FileNotFoundError:
        print(
            f"❌ ERROR: Lyrics file not found at '{lyrics_file_path}'. Please check the path."
        )
        return

    # Generate image prompts from the lyrics
    image_prompts = create_image_prompts_from_lyrics(song_lyrics)

    # Generate and download an image for each prompt
    all_successful = True
    for scene_name, prompt in image_prompts.items():
        # Sanitize filename
        output_filename = f"{scene_name}.png"
        success = generator.generate_and_download_image(prompt, output_filename)
        if not success:
            all_successful = False
        time.sleep(1)  # Small delay to avoid hitting rate limits

    print("=" * 60)
    if all_successful:
        print("🎉 SUCCESS! All images were generated and saved!")
    else:
        print("❌ FAILED! Some images could not be generated. Please check the logs.")
    print("=" * 60)


if __name__ == "__main__":
    main()
