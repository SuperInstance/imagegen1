from src.config import Config

def test_config_loading():
    config = Config()

    # Check default configuration
    assert config.models_dir == "models"
    assert config.max_image_size == 1024
    assert config.default_text_model == "llama2"