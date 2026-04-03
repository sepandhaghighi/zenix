# -*- coding: utf-8 -*-
import numpy as np
import pytest

from zenix import generate_noise, play_noise
from zenix import NoiseType


@pytest.mark.parametrize("noise_type", list(NoiseType))
def test_generate_noise_all_types(noise_type):
    duration = 1.0
    sample_rate = 8000

    audio = generate_noise(
        noise_type=noise_type,
        duration=duration,
        sample_rate=sample_rate,
        volume=1.0,
        fade_in=0.1,
    )

    assert isinstance(audio, np.ndarray)
    assert audio.dtype == np.int16
    assert len(audio) == int(duration * sample_rate)


@pytest.mark.parametrize("noise_type", list(NoiseType))
def test_generate_noise_volume_scaling(noise_type):
    audio_low = generate_noise(noise_type=noise_type, volume=0.1)
    audio_high = generate_noise(noise_type=noise_type, volume=1.0)

    assert np.max(np.abs(audio_high)) >= np.max(np.abs(audio_low))


def test_generate_noise_invalid_type():
    with pytest.raises(ValueError):
        generate_noise(noise_type="invalid")  # type: ignore


def test_play_noise_calls_backend(monkeypatch):
    calls = {"count": 0}

    def fake_play(_):
        calls["count"] += 1

    monkeypatch.setattr("zenix.functions.play", fake_play)

    audio = generate_noise(duration=0.1)
    play_noise(audio, loop=False)

    assert calls["count"] == 1


def test_play_noise_loop_break(monkeypatch):
    calls = {"count": 0}

    def fake_play(_):
        calls["count"] += 1
        raise KeyboardInterrupt

    monkeypatch.setattr("zenix.functions.play", fake_play)

    audio = generate_noise(duration=0.1)
    play_noise(audio, loop=True)

    assert calls["count"] >= 1
