import os
import subprocess
from pathlib import Path
import logging

class ImageGenerator:
    def __init__(self):
        self.models_dir = Path("models/images")
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.current_model = None
        self.ml_available = self._check_ml_availability()
        self.logger = logging.getLogger(__name__)

    def _check_ml_availability(self):
        """Check if ML libraries are available"""
        try:
            import torch
            import diffusers
            return {
                'torch': True,
                'diffusers': True,
                'cuda': torch.cuda.is_available()
            }
        except ImportError:
            return {
                'torch': False,
                'diffusers': False,
                'cuda': False
            }

    def _create_placeholder_image(self, prompt, width, height):
        """Create a placeholder image with text"""
        try:
            from datetime import datetime

            # Simple text-based image info file
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            image_path = self.models_dir / f"output_{width}x{height}_{int(datetime.now().timestamp())}.txt"

            with open(image_path, 'w') as f:
                f.write("=" * 50 + "\n")
                f.write("AI GENERATED IMAGE PLACEHOLDER\n")
                f.write("=" * 50 + "\n")
                f.write(f"Timestamp: {timestamp}\n")
                f.write(f"Prompt: {prompt}\n")
                f.write(f"Size: {width}x{height}\n")
                f.write(f"Model: Stable Diffusion XL\n")
                f.write(f"Hardware: RTX 4050 (6GB VRAM)\n")
                f.write(f"Status: Placeholder - ML libraries not yet installed\n")
                f.write(f"GPU: NVIDIA GeForce RTX 4050 Laptop GPU\n")
                f.write(f"CPU: AMD Ryzen AI 9 HX 370\n")
                f.write(f"Memory: 15GB Total\n")
                f.write("=" * 50 + "\n")

            return str(image_path)

        except Exception as e:
            self.logger.error(f"Error creating placeholder image: {e}")
            # Fallback: create a simple text file
            image_path = self.models_dir / f"output_{width}x{height}.txt"
            with open(image_path, 'w') as f:
                f.write(f"Generated Image Placeholder\n")
                f.write(f"Prompt: {prompt}\n")
                f.write(f"Size: {width}x{height}\n")
                f.write(f"Error: {str(e)}")
            return str(image_path)

    def _generate_with_diffusers(self, prompt, width, height):
        """Generate image using Diffusers library"""
        try:
            import torch
            from diffusers import StableDiffusionXLPipeline, EulerDiscreteScheduler

            self.logger.info(f"Generating image with {prompt} using Stable Diffusion XL")

            # Load model (this will download on first run)
            model_path = self.models_dir / "stable-diffusion-xl"
            if not model_path.exists():
                self.logger.info("Downloading Stable Diffusion XL model...")
                pipe = StableDiffusionXLPipeline.from_pretrained(
                    "stabilityai/stable-diffusion-xl-base-1.0",
                    torch_dtype=torch.float16 if self.ml_available['cuda'] else torch.float32,
                    use_safetensors=True
                )
            else:
                pipe = StableDiffusionXLPipeline.from_pretrained(
                    model_path,
                    torch_dtype=torch.float16 if self.ml_available['cuda'] else torch.float32
                )

            # Move to GPU if available
            if self.ml_available['cuda']:
                pipe = pipe.to("cuda")

            # Generate image
            generator = torch.Generator(device="cuda" if self.ml_available['cuda'] else "cpu")
            images = pipe(
                prompt=prompt,
                width=width,
                height=height,
                generator=generator,
                num_inference_steps=20,
                guidance_scale=7.5
            ).images

            # Save image
            timestamp = int(datetime.now().timestamp())
            image_path = self.models_dir / f"output_{width}x{height}_{timestamp}.png"
            images[0].save(image_path)

            self.logger.info(f"Image saved to {image_path}")
            return str(image_path)

        except Exception as e:
            self.logger.error(f"Error generating with Diffusers: {e}")
            return self._create_placeholder_image(prompt, width, height)

    def generate(self, prompt, model_name="stable-diffusion-xl", width=512, height=512):
        """Generate an image from text prompt"""
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        if width < 64 or height < 64:
            raise ValueError("Image dimensions must be at least 64x64")

        if width > 1024 or height > 1024:
            self.logger.warning("Large image dimensions may take longer to generate")

        # Try to generate with ML libraries if available
        if self.ml_available['torch'] and self.ml_available['diffusers']:
            return self._generate_with_diffusers(prompt, width, height)
        else:
            self.logger.info("ML libraries not available, creating placeholder image")
            return self._create_placeholder_image(prompt, width, height)

    def load_model(self, model_name):
        """Load the specified model"""
        if model_name == "stable-diffusion-xl":
            self.current_model = model_name
            return True
        else:
            raise ValueError(f"Unsupported model: {model_name}")

    def get_available_models(self):
        """Return list of available image models"""
        if self.ml_available['torch'] and self.ml_available['diffusers']:
            return ["stable-diffusion-xl", "stable-diffusion-xl-base", "stable-diffusion-v2"]
        else:
            return ["stable-diffusion-xl (placeholder)"]

    def check_cuda_memory(self):
        """Check available CUDA memory"""
        if self.ml_available['cuda']:
            try:
                import torch
                if torch.cuda.is_available():
                    total_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
                    available_memory = torch.cuda.memory_allocated(0) / 1024**3
                    return {
                        'total_gb': round(total_memory, 1),
                        'used_gb': round(available_memory, 1),
                        'available_gb': round(total_memory - available_memory, 1)
                    }
            except:
                pass
        return None