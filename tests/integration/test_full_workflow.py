import sys
import os
import unittest
sys.path.append('.')

from main import GenerationApp

class TestFullWorkflow(unittest.TestCase):
    def setUp(self):
        self.app = GenerationApp()

    def test_image_generation(self):
        """Test that image generator returns a valid path"""
        image_result = self.app.image_generator.generate("Test prompt")
        self.assertIsNotNone(image_result)
        self.assertIsInstance(image_result, str)
        self.assertTrue(os.path.exists(image_result))

    def test_text_generation(self):
        """Test that text generator returns a string"""
        text_result = self.app.text_generator.generate("Hello world")
        self.assertIsInstance(text_result, str)

    def test_audio_generation(self):
        """Test that audio generator returns a string"""
        audio_result = self.app.audio_generator.generate("Test audio")
        self.assertIsNotNone(audio_result)
        self.assertIsInstance(audio_result, str)

    def test_model_compatibility_check(self):
        """Test model compatibility checking returns boolean and reason"""
        model_spec = {'min_vram_gb': 4, 'requires_cuda': False}
        hardware = self.app.hardware_detector.detect_specs()
        is_compatible, reason = self.app.model_manager.check_compatibility(model_spec, hardware)
        self.assertIsInstance(is_compatible, bool)
        self.assertIsInstance(reason, str)

if __name__ == '__main__':
    unittest.main()