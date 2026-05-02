# -*- coding: utf-8 -*-
import wave
import numpy as np
import pytest

from zenix import generate_noise, play_noise, save_noise
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
        fade_out=0.1,
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

    audio = generate_noise(duration=5)
    play_noise(audio, loop=False)

    assert calls["count"] == 1


def test_play_noise_loop_break(monkeypatch):
    calls = {"count": 0}

    def fake_play(_):
        calls["count"] += 1
        raise KeyboardInterrupt

    monkeypatch.setattr("zenix.functions.play", fake_play)

    audio = generate_noise(duration=5)
    play_noise(audio, loop=True)

    assert calls["count"] >= 1


def test_save_noise_creates_file(tmp_path):
    filepath = tmp_path / "test.wav"

    audio = generate_noise(duration=5)
    save_noise(str(filepath), audio)

    assert filepath.exists()
    assert filepath.stat().st_size > 0


def test_generate_and_save_pipeline(tmp_path):
    filepath = tmp_path / "pipeline.wav"

    duration = 5
    sample_rate = 8000

    audio = generate_noise(duration=duration, sample_rate=sample_rate)
    save_noise(str(filepath), audio, sample_rate=sample_rate)

    assert filepath.exists()

    with wave.open(str(filepath), "rb") as wf:
        assert wf.getnchannels() == 1
        assert wf.getsampwidth() == 2
        assert wf.getframerate() == sample_rate
        assert wf.getnframes() == int(duration * sample_rate)


@pytest.mark.parametrize("noise_type", list(NoiseType))
def test_save_noise_all_types(tmp_path, noise_type):
    filepath = tmp_path / f"{noise_type.value}.wav"

    audio = generate_noise(noise_type=noise_type, duration=5)
    save_noise(str(filepath), audio)

    assert filepath.exists()


def test_save_preserves_audio_amplitude(tmp_path):
    filepath = tmp_path / "amp.wav"

    audio = generate_noise(volume=1.0, duration=5)
    save_noise(str(filepath), audio)

    with wave.open(str(filepath), "rb") as wf:
        frames = wf.readframes(wf.getnframes())

    loaded = np.frombuffer(frames, dtype=np.int16)

    assert np.max(np.abs(loaded)) > 0


def test_save_noise_overwrite(tmp_path):
    filepath = tmp_path / "overwrite.wav"

    audio1 = generate_noise(duration=5)
    audio2 = generate_noise(duration=5)

    save_noise(str(filepath), audio1)
    size1 = filepath.stat().st_size

    save_noise(str(filepath), audio2)
    size2 = filepath.stat().st_size

    assert size1 != size2


def test_save_does_not_modify_audio(tmp_path):
    filepath = tmp_path / "immutability.wav"

    audio = generate_noise(duration=5)
    original = audio.copy()

    save_noise(str(filepath), audio)

    assert np.array_equal(audio, original)
