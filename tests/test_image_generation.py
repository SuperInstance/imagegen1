from src.generation.image import ImageGenerator

def test_image_generation():
    generator = ImageGenerator()

    result = generator.generate(
        prompt="A beautiful landscape",
        model_name="stable-diffusion-xl",
        width=512,
        height=512
    )

    # Should return image data or path
    assert result is not None
    assert isinstance(result, (str, bytes))  # Path or bytes