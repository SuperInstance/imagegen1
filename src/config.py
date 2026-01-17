import os
from pathlib import Path
import yaml

class Config:
    def __init__(self, config_file=None):
        if config_file and os.path.exists(config_file):
            self.load_config(config_file)
        else:
            self.set_defaults()

    def set_defaults(self):
        self.models_dir = "models"
        self.max_image_size = 1024
        self.default_text_model = "llama2"
        self.default_image_model = "stable-diffusion-xl"
        self.audio_sample_rate = 22050
        self.mcp_port = 8000

    def load_config(self, config_file):
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)

        # Apply configuration with defaults
        self.models_dir = config.get('models_dir', 'models')
        self.max_image_size = config.get('max_image_size', 1024)
        self.default_text_model = config.get('default_text_model', 'llama2')
        self.default_image_model = config.get('default_image_model', 'stable-diffusion-xl')
        self.audio_sample_rate = config.get('audio_sample_rate', 22050)
        self.mcp_port = config.get('mcp_port', 8000)