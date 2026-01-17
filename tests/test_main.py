import sys
sys.path.insert(0, '.')
sys.path.insert(0, 'src')

from main import GenerationApp

def test_app_initialization():
    app = GenerationApp()

    # Check that all components are initialized
    assert app.hardware_detector is not None
    assert app.model_manager is not None
    assert app.image_generator is not None
    assert app.text_generator is not None
    assert app.audio_generator is not None

if __name__ == "__main__":
    try:
        test_app_initialization()
        print("✅ Test passed!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise