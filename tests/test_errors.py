import pytest
import numpy as np
from zenix import generate_noise, play_noise


def test_invalid_noise_type():
    with pytest.raises(ValueError, match="`noise_type` must be an instance of NoiseType."):
        generate_noise(noise_type="white")


def test_invalid_duration_type():
    with pytest.raises(ValueError, match="`duration` must be int or float."):
        generate_noise(duration="10")


def test_invalid_duration_value():
    with pytest.raises(ValueError, match="`duration` must be greater than 0."):
        generate_noise(duration=0)


def test_invalid_sample_rate_type():
    with pytest.raises(ValueError, match="`sample_rate` must be int."):
        generate_noise(sample_rate=44100.0)


def test_invalid_sample_rate_value():
    with pytest.raises(ValueError, match="`sample_rate` must be greater than 0."):
        generate_noise(sample_rate=0)


def test_invalid_volume_type():
    with pytest.raises(ValueError, match="`volume` must be int or float."):
        generate_noise(volume="0.5")


def test_invalid_volume_range_low():
    with pytest.raises(ValueError, match="`volume` must be between 0.0 and 1.0."):
        generate_noise(volume=-0.1)


def test_invalid_volume_range_high():
    with pytest.raises(ValueError, match="`volume` must be between 0.0 and 1.0."):
        generate_noise(volume=1.5)


def test_invalid_fade_in_type():
    with pytest.raises(ValueError, match="`fade_in` must be int or float."):
        generate_noise(fade_in="2")


def test_invalid_fade_in_value():
    with pytest.raises(ValueError, match="`fade_in` must be greater than or equal to 0."):
        generate_noise(fade_in=-1)


def test_invalid_fade_in_range():
    with pytest.raises(ValueError, match="`fade_in` must not exceed `duration`."):
        generate_noise(duration=1, fade_in=2)


def test_invalid_audio_type():
    with pytest.raises(ValueError, match="`audio` must be a numpy.ndarray."):
        play_noise(audio="not-array")


def test_invalid_audio_dtype():
    audio = np.zeros(100, dtype=np.float32)
    with pytest.raises(ValueError, match="`audio` must have dtype int16."):
        play_noise(audio=audio)


def test_invalid_audio_dimension():
    audio = np.zeros((2, 100), dtype=np.int16)
    with pytest.raises(ValueError, match="`audio` must be a 1D array."):
        play_noise(audio=audio)


def test_invalid_audio_empty():
    audio = np.array([], dtype=np.int16)
    with pytest.raises(ValueError, match="`audio` must not be empty."):
        play_noise(audio=audio)


def test_invalid_play_sample_rate_type():
    audio = np.zeros(100, dtype=np.int16)
    with pytest.raises(ValueError, match="`sample_rate` must be int."):
        play_noise(audio=audio, sample_rate=44100.0)


def test_invalid_play_sample_rate_value():
    audio = np.zeros(100, dtype=np.int16)
    with pytest.raises(ValueError, match="`sample_rate` must be greater than 0."):
        play_noise(audio=audio, sample_rate=0)


def test_invalid_loop_type():
    audio = np.zeros(100, dtype=np.int16)
    with pytest.raises(ValueError, match="`loop` must be bool."):
        play_noise(audio=audio, loop="yes")
