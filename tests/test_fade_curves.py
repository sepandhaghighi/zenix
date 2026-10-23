# -*- coding: utf-8 -*-
import numpy as np
import pytest

from zenix import FadeType, Noise, generate_noise
from zenix.functions import _apply_fade_in, _apply_fade_out, _create_fade_curve


@pytest.mark.parametrize("expected", [
    [],
    [0.0],
    [0.0, 1.0],
    [0.0, 0.14644661, 0.5, 0.85355339, 1.0],
])
@pytest.mark.parametrize("is_fade_in", [True, False])
def test_cosine_fade_curve(expected, is_fade_in):
    curve = _create_fade_curve(len(expected), FadeType.COSINE, is_fade_in)
    expected = np.array(expected, dtype=np.float32)
    if not is_fade_in:
        expected = expected[::-1]

    assert curve.dtype == np.float32
    assert curve.shape == expected.shape
    np.testing.assert_allclose(curve, expected, rtol=0, atol=1e-7)


@pytest.mark.parametrize("apply_fade, expected", [
    (_apply_fade_in, [0.0, 0.25, 0.75, 1.0]),
    (_apply_fade_out, [1.0, 0.75, 0.25, 0.0]),
])
def test_cosine_fade_clips_to_audio_length(apply_fade, expected):
    audio = np.ones(4, dtype=np.float32)

    apply_fade(audio, sample_rate=10, fade_duration=1.0, fade_type=FadeType.COSINE)

    assert audio.dtype == np.float32
    np.testing.assert_allclose(audio, expected, rtol=0, atol=1e-7)


@pytest.mark.parametrize("use_noise_object", [False, True])
def test_cosine_overlapping_fades(use_noise_object):
    params = dict(
        duration=0.007, sample_rate=1000, volume=0.3,
        fade_in=0.005, fade_out=0.005, fade_type=FadeType.COSINE, seed=7,
    )
    if use_noise_object:
        noise = Noise(**params)
        audio = noise.audio
        assert noise.audio is audio
        np.testing.assert_array_equal(noise.generate(), audio)
    else:
        audio = generate_noise(**params)

    # Five-point cosine envelopes applied to seven seeded white-noise samples.
    # The overlapping samples receive both gains before conversion to int16.
    assert audio.dtype == np.int16
    np.testing.assert_array_equal(audio, [0, -396, 95, 1726, -2293, 1, 0])
