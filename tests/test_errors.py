import pytest
import numpy as np
from zenix import generate_noise, play_noise, save_noise


def test_invalid_noise_type():
    with pytest.raises(ValueError, match="`noise_type` must be an instance of NoiseType."):
        generate_noise(noise_type="white")


def test_invalid_duration_type():
    with pytest.raises(ValueError, match="`duration` must be a number greater than 0."):
        generate_noise(duration="10")


def test_invalid_duration_value():
    with pytest.raises(ValueError, match="`duration` must be a number greater than 0."):
        generate_noise(duration=0)


def test_invalid_sample_rate_type():
    with pytest.raises(ValueError, match="`sample_rate` must be a positive integer."):
        generate_noise(sample_rate=44100.0)


def test_invalid_sample_rate_value():
    with pytest.raises(ValueError, match="`sample_rate` must be a positive integer."):
        generate_noise(sample_rate=0)


def test_invalid_volume_type():
    with pytest.raises(ValueError, match="`volume` must be a number between 0.0 and 1.0."):
        generate_noise(volume="0.5")


def test_invalid_volume_range_low():
    with pytest.raises(ValueError, match="`volume` must be a number between 0.0 and 1.0."):
        generate_noise(volume=-0.1)


def test_invalid_volume_range_high():
    with pytest.raises(ValueError, match="`volume` must be a number between 0.0 and 1.0."):
        generate_noise(volume=1.5)


def test_invalid_fade_in_type():
    with pytest.raises(ValueError, match="`fade_in` must be a non-negative number not exceeding `duration`."):
        generate_noise(fade_in="2")


def test_invalid_fade_in_value():
    with pytest.raises(ValueError, match="`fade_in` must be a non-negative number not exceeding `duration`."):
        generate_noise(fade_in=-1)


def test_invalid_fade_in_range():
    with pytest.raises(ValueError, match="`fade_in` must be a non-negative number not exceeding `duration`."):
        generate_noise(duration=1, fade_in=2)


def test_invalid_fade_out_type():
    with pytest.raises(ValueError, match="`fade_out` must be a non-negative number not exceeding `duration`."):
        generate_noise(fade_out="2")


def test_invalid_fade_out_value():
    with pytest.raises(ValueError, match="`fade_out` must be a non-negative number not exceeding `duration`."):
        generate_noise(fade_out=-1)


def test_invalid_fade_out_range():
    with pytest.raises(ValueError, match="`fade_out` must be a non-negative number not exceeding `duration`."):
        generate_noise(duration=1, fade_out=2, fade_in=0.1)


def test_invalid_audio_type():
    with pytest.raises(ValueError, match="`audio` must be a non-empty 1D numpy.ndarray with dtype int16."):
        play_noise(audio="not-array")


def test_invalid_audio_dtype():
    audio = np.zeros(100, dtype=np.float32)
    with pytest.raises(ValueError, match="`audio` must be a non-empty 1D numpy.ndarray with dtype int16."):
        play_noise(audio=audio)


def test_invalid_audio_dimension():
    audio = np.zeros((2, 100), dtype=np.int16)
    with pytest.raises(ValueError, match="`audio` must be a non-empty 1D numpy.ndarray with dtype int16."):
        play_noise(audio=audio)


def test_invalid_audio_empty():
    audio = np.array([], dtype=np.int16)
    with pytest.raises(ValueError, match="`audio` must be a non-empty 1D numpy.ndarray with dtype int16."):
        play_noise(audio=audio)


def test_invalid_play_sample_rate_type():
    audio = np.zeros(100, dtype=np.int16)
    with pytest.raises(ValueError, match="`sample_rate` must be a positive integer."):
        play_noise(audio=audio, sample_rate=44100.0)


def test_invalid_play_sample_rate_value():
    audio = np.zeros(100, dtype=np.int16)
    with pytest.raises(ValueError, match="`sample_rate` must be a positive integer."):
        play_noise(audio=audio, sample_rate=0)


def test_invalid_loop_type():
    audio = np.zeros(100, dtype=np.int16)
    with pytest.raises(ValueError, match="`loop` must be bool."):
        play_noise(audio=audio, loop="yes")


def test_invalid_filepath():
    audio = np.zeros(100, dtype=np.int16)
    with pytest.raises(ValueError):
        save_noise("", audio)
