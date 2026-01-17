import sys
sys.path.append('.')
from src.models.manager import ModelManager
from src.hardware.detector import HardwareDetector


def test_model_compatibility_check():
    detector = HardwareDetector()
    manager = ModelManager(detector)

    # Test with mock model specs
    model_spec = {
        'name': 'stable-diffusion-xl',
        'min_vram_gb': 6,
        'recommended_vram_gb': 12,
        'requires_cuda': True
    }

    hardware = detector.detect_specs()
    is_compatible, reason = manager.check_compatibility(model_spec, hardware)

    # Should return compatibility status and reason
    assert isinstance(is_compatible, bool)
    assert isinstance(reason, str)