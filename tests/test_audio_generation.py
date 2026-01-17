from src.generation.audio import AudioGenerator

def test_audio_generation():
    generator = AudioGenerator()

    result = generator.generate(
        text="Hello, this is a test audio generation",
        model_name="tts-1",
        voice="default"
    )

    # Should return audio file path or bytes
    assert result is not None
    assert isinstance(result, (str, bytes))