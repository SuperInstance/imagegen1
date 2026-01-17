import argparse
from src.hardware.detector import HardwareDetector
from src.models.manager import ModelManager
from src.generation.image import ImageGenerator
from src.generation.text import TextGenerator
from src.generation.audio import AudioGenerator
from src.mcp_server import MCPServer
from src.config import Config

class GenerationApp:
    def __init__(self, config_file=None):
        self.config = Config(config_file)
        self.hardware_detector = HardwareDetector()
        self.model_manager = ModelManager(self.hardware_detector)
        self.image_generator = ImageGenerator()
        self.text_generator = TextGenerator()
        self.audio_generator = AudioGenerator()
        self.mcp_server = MCPServer()

    def start(self):
        print("Starting Generation Server...")
        print(f"Hardware specs: {self.hardware_detector.detect_specs()}")
        print(f"Available text models: {self.text_generator.get_available_models()}")

        # Start MCP server
        self.mcp_server.start()
        print("MCP Server started on port", self.config.mcp_port)

        return True

def main():
    parser = argparse.ArgumentParser(description='Local Generation Server')
    parser.add_argument('--config', default='config.yaml', help='Configuration file')
    parser.add_argument('--download-models', action='store_true', help='Download compatible models')

    args = parser.parse_args()

    app = GenerationApp(args.config)

    if args.download_models:
        print("Downloading compatible models...")
        # Implementation for model downloading
        pass

    app.start()

if __name__ == "__main__":
    main()