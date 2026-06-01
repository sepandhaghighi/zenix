# -*- coding: utf-8 -*-
import numpy as np
import pytest

from zenix import Noise, NoiseType
from zenix import ZenixValidationError


def test_noise_default_init():
    noise = Noise()

    assert noise.noise_type == NoiseType.WHITE
    assert noise.duration == 30.0
    assert noise.sample_rate == 44100
    assert noise.volume == 0.3
    assert noise.fade_in == 2.0
    assert noise.fade_out == 2.0


@pytest.mark.parametrize("noise_type", list(NoiseType))
def test_noise_init_all_types(noise_type):
    noise = Noise(
        noise_type=noise_type,
        duration=1.0,
        sample_rate=8000,
        volume=0.5,
        fade_in=0.1,
        fade_out=0.1,
    )

    assert noise.noise_type == noise_type
    assert noise.duration == 1.0
    assert noise.sample_rate == 8000
    assert noise.volume == 0.5
    assert noise.fade_in == 0.1
    assert noise.fade_out == 0.1


def test_noise_repr():
    noise = Noise(
        noise_type=NoiseType.PINK,
        duration=5,
        sample_rate=8000,
        volume=0.5,
        fade_in=1,
        fade_out=1,
    )

    assert repr(noise) == (
        "Noise("
        "noise_type='pink', "
        "duration=5, "
        "sample_rate=8000, "
        "volume=0.5, "
        "fade_in=1, "
        "fade_out=1)"
    )


@pytest.mark.parametrize("noise_type", list(NoiseType))
def test_generate_returns_audio(noise_type):
    noise = Noise(
        noise_type=noise_type,
        duration=1.0,
        sample_rate=8000,
    )

    audio = noise.generate()

    assert isinstance(audio, np.ndarray)
    assert audio.dtype == np.int16
    assert len(audio) == 8000


def test_audio_property_lazy_generation():
    noise = Noise(duration=1.0, sample_rate=8000)

    assert noise._audio is None

    audio = noise.audio

    assert isinstance(audio, np.ndarray)
    assert noise._audio is not None
    assert np.array_equal(audio, noise._audio)


def test_audio_property_cached():
    noise = Noise(duration=1.0, sample_rate=8000)

    audio1 = noise.audio
    audio2 = noise.audio

    assert audio1 is audio2


def test_play_calls_backend(monkeypatch):
    calls = {"count": 0}

    def fake_play(self, loop=False):
        calls["count"] += 1
        assert loop is True

    monkeypatch.setattr("zenix.noise.play_noise", fake_play)

    noise = Noise(duration=1.0)
    noise.play(loop=True)

    assert calls["count"] == 1


def test_save_calls_backend(monkeypatch, tmp_path):
    calls = {"count": 0}

    def fake_save(filepath, audio, sample_rate):
        calls["count"] += 1
        assert filepath.endswith(".wav")
        assert isinstance(audio, np.ndarray)

    monkeypatch.setattr("zenix.noise.save_noise", fake_save)

    noise = Noise(duration=1.0)
    noise.save(str(tmp_path / "test.wav"))

    assert calls["count"] == 1


def test_generate_stores_audio():
    noise = Noise(duration=1.0, sample_rate=8000)

    audio = noise.generate()

    assert noise._audio is not None
    assert np.array_equal(audio, noise._audio)


def test_invalid_noise_type():
    with pytest.raises(
        ZenixValidationError,
        match="`noise_type` must be an instance of NoiseType."
    ):
        Noise(noise_type="white")  # type: ignore


def test_invalid_duration():
    with pytest.raises(
        ZenixValidationError,
        match="`duration` must be a number greater than 0."
    ):
        Noise(duration=0)


def test_invalid_sample_rate():
    with pytest.raises(
        ZenixValidationError,
        match="`sample_rate` must be a positive integer."
    ):
        Noise(sample_rate=0)


def test_invalid_volume():
    with pytest.raises(
        ZenixValidationError,
        match="`volume` must be a number between 0.0 and 1.0."
    ):
        Noise(volume=1.5)


def test_invalid_fade_in():
    with pytest.raises(
        ZenixValidationError,
        match="`fade_in` must be a non-negative number not exceeding `duration`."
    ):
        Noise(duration=1, fade_in=2)


def test_invalid_fade_out():
    with pytest.raises(
        ZenixValidationError,
        match="`fade_out` must be a non-negative number not exceeding `duration`."
    ):
        Noise(duration=1, fade_out=2)