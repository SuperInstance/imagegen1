import pytest
from src.hardware.detector import HardwareDetector

def test_hardware_detection():
    detector = HardwareDetector()
    specs = detector.detect_specs()

    # Check key components are detected
    assert 'gpu' in specs
    assert 'cpu' in specs
    assert 'memory' in specs
    assert 'storage' in specs

    # Check GPU specs include memory and compute capability
    if specs['gpu']['available']:
        assert 'memory_mb' in specs['gpu']
        assert 'compute_capability' in specs['gpu']