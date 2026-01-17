from src.generation.text import TextGenerator

def test_text_generation():
    generator = TextGenerator()

    result = generator.generate(
        prompt="Explain quantum computing in simple terms",
        model_name="llama2",
        max_length=200
    )

    # Should return generated text
    assert isinstance(result, str)
    assert len(result) > 0