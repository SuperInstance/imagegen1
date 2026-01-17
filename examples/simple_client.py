#!/usr/bin/env python3
"""
Simple Client Example for Local Generation Server

This example demonstrates how to interact with the Local Generation Server
using both the MCP protocol and direct REST API calls.
"""

import requests
import json
import asyncio
import aiohttp
from typing import Dict, Any, Optional
import base64
import io
from PIL import Image


class GenerationClient:
    """Simple client for the Local Generation Server"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()

    def generate_image(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate an image using the server"""
        payload = {
            "prompt": prompt,
            **kwargs
        }

        try:
            response = self.session.post(
                f"{self.base_url}/generate/image",
                json=payload,
                timeout=300
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def generate_text(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate text using the server"""
        payload = {
            "prompt": prompt,
            **kwargs
        }

        try:
            response = self.session.post(
                f"{self.base_url}/generate/text",
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def generate_audio(self, text: str, **kwargs) -> Dict[str, Any]:
        """Generate audio using the server"""
        payload = {
            "text": text,
            **kwargs
        }

        try:
            response = self.session.post(
                f"{self.base_url}/generate/audio",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def get_server_info(self) -> Dict[str, Any]:
        """Get server information"""
        try:
            response = self.session.get(f"{self.base_url}/info")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}


class AsyncGenerationClient:
    """Async client for the Local Generation Server"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    async def generate_image(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate an image asynchronously"""
        payload = {
            "prompt": prompt,
            **kwargs
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/generate/image",
                    json=payload,
                    timeout=300
                ) as response:
                    response.raise_for_status()
                    return await response.json()
        except Exception as e:
            return {"error": str(e)}

    async def generate_text(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate text asynchronously"""
        payload = {
            "prompt": prompt,
            **kwargs
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/generate/text",
                    json=payload,
                    timeout=60
                ) as response:
                    response.raise_for_status()
                    return await response.json()
        except Exception as e:
            return {"error": str(e)}


def save_image_from_response(response: Dict[str, Any], filename: str = "generated_image.png"):
    """Save image from server response to file"""
    if "error" in response:
        print(f"Error generating image: {response['error']}")
        return False

    if "image_url" in response:
        # Download the image
        try:
            img_response = requests.get(response["image_url"])
            img_response.raise_for_status()

            # Save to file
            with open(filename, "wb") as f:
                f.write(img_response.content)
            print(f"Image saved as {filename}")
            return True
        except Exception as e:
            print(f"Error saving image: {e}")
            return False

    elif "image_data" in response:
        # Handle base64 encoded image
        try:
            image_data = base64.b64decode(response["image_data"])
            image = Image.open(io.BytesIO(image_data))
            image.save(filename)
            print(f"Image saved as {filename}")
            return True
        except Exception as e:
            print(f"Error saving image: {e}")
            return False

    return False


def demo_basic_usage():
    """Demonstrate basic usage of the generation client"""
    print("=== Basic Usage Demo ===")

    # Initialize client
    client = GenerationClient()

    # Get server info
    print("\n1. Getting server information...")
    info = client.get_server_info()
    print(f"Server info: {json.dumps(info, indent=2)}")

    # Generate image
    print("\n2. Generating image...")
    image_result = client.generate_image(
        "A beautiful landscape with mountains and a lake",
        width=768,
        height=512,
        steps=25
    )
    save_image_from_response(image_result, "landscape.png")

    # Generate text
    print("\n3. Generating text...")
    text_result = client.generate_text(
        "Write a short story about a robot learning to paint",
        max_tokens=300,
        temperature=0.8
    )
    if "text" in text_result:
        print(f"Generated text:\n{text_result['text']}")
    else:
        print(f"Error: {text_result.get('error', 'Unknown error')}")

    # Generate audio
    print("\n4. Generating audio...")
    audio_result = client.generate_audio(
        "Hello! This is a text-to-speech demonstration.",
        voice="default",
        speed=1.1
    )
    if "audio_url" in audio_result:
        print(f"Audio generated: {audio_result['audio_url']}")
    else:
        print(f"Error: {audio_result.get('error', 'Unknown error')}")


async def demo_async_usage():
    """Demonstrate async usage of the generation client"""
    print("\n=== Async Usage Demo ===")

    # Initialize async client
    client = AsyncGenerationClient()

    # Generate multiple images concurrently
    print("\n1. Generating multiple images concurrently...")
    tasks = [
        client.generate_image("A cute cat", width=512, height=512),
        client.generate_image("A dog playing in a park", width=512, height=512),
        client.generate_image("A sunset over the ocean", width=512, height=512)
    ]

    results = await asyncio.gather(*tasks)

    for i, result in enumerate(results):
        filename = f"async_image_{i+1}.png"
        save_image_from_response(result, filename)

    # Generate text
    print("\n2. Generating text asynchronously...")
    text_result = await client.generate_text(
        "Explain the benefits of using local AI models",
        max_tokens=200
    )
    if "text" in text_result:
        print(f"Generated text:\n{text_result['text']}")
    else:
        print(f"Error: {text_result.get('error', 'Unknown error')}")


def demo_batch_processing():
    """Demonstrate batch processing with the server"""
    print("\n=== Batch Processing Demo ===")

    client = GenerationClient()

    # Batch image generation
    prompts = [
        "A futuristic cityscape",
        "A forest in autumn",
        "A beach at sunset",
        "A mountain peak"
    ]

    print("\n1. Batch generating images...")
    for i, prompt in enumerate(prompts):
        print(f"  Generating image {i+1}/{len(prompts)}: {prompt}")
        result = client.generate_image(prompt, width=512, height=512)
        filename = f"batch_image_{i+1}.png"
        save_image_from_response(result, filename)

    # Batch text generation
    text_prompts = [
        "What is machine learning?",
        "How does neural network work?",
        "What are the types of AI?"
    ]

    print("\n2. Batch generating text...")
    for i, prompt in enumerate(text_prompts):
        print(f"  Generating text {i+1}/{len(text_prompts)}")
        result = client.generate_text(prompt, max_tokens=150)
        if "text" in result:
            print(f"    {prompt}")
            print(f"    {result['text']}\n")


def main():
    """Main function to run all demos"""
    print("Local Generation Server - Simple Client Example")
    print("=" * 50)

    # Check if server is running
    client = GenerationClient()
    info = client.get_server_info()

    if "error" in info and "Connection" in info["error"]:
        print("Error: Server is not running. Please start the server first:")
        print("  python main.py")
        return

    print(f"Connected to server at {client.base_url}")

    # Run demos
    demo_basic_usage()

    # Run async demo (requires Python 3.7+)
    try:
        asyncio.run(demo_async_usage())
    except Exception as e:
        print(f"\nNote: Async demo skipped (requires Python 3.7+): {e}")

    demo_batch_processing()

    print("\n" + "=" * 50)
    print("Demo completed! Check the generated files:")
    print("- landscape.png")
    print("- async_image_1.png, async_image_2.png, async_image_3.png")
    print("- batch_image_1.png, batch_image_2.png, batch_image_3.png, batch_image_4.png")


if __name__ == "__main__":
    main()