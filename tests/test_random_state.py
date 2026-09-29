# -*- coding: utf-8 -*-
import numpy as np
import pytest

from zenix import Noise, NoiseType, generate_noise


@pytest.fixture
def global_random_state():
    original_state = np.random.get_state()
    try:
        np.random.seed(123)
        # Include a cached Gaussian value as well as the underlying RNG state.
        np.random.normal()
        yield np.random.get_state()
    finally:
        np.random.set_state(original_state)


@pytest.mark.parametrize("noise_type", list(NoiseType))
@pytest.mark.parametrize("seed", [7, None])
def test_generate_noise_preserves_global_random_state(noise_type, seed, global_random_state):
    generate_noise(noise_type=noise_type, duration=0.1, fade_in=0.01, fade_out=0.01, seed=seed)

    np.testing.assert_equal(np.random.get_state(), global_random_state)
    expected = np.random.RandomState()
    expected.set_state(global_random_state)
    np.testing.assert_array_equal(np.random.normal(size=5), expected.normal(size=5))
    np.testing.assert_array_equal(np.random.random(5), expected.random(5))


@pytest.mark.parametrize("noise_type", list(NoiseType))
@pytest.mark.parametrize("seed", [7, None])
def test_noise_preserves_global_random_state(noise_type, seed, global_random_state):
    noise = Noise(noise_type=noise_type, duration=0.1, fade_in=0.01, fade_out=0.01, seed=seed)
    np.testing.assert_equal(np.random.get_state(), global_random_state)

    audio = noise.audio
    np.testing.assert_equal(np.random.get_state(), global_random_state)
    assert noise.audio is audio
    np.testing.assert_equal(np.random.get_state(), global_random_state)

    regenerated = noise.generate()
    np.testing.assert_equal(np.random.get_state(), global_random_state)
    assert noise.audio is regenerated
    if seed is not None:
        np.testing.assert_array_equal(regenerated, audio)
    else:
        assert not np.array_equal(regenerated, audio)


@pytest.mark.parametrize("noise_type", list(NoiseType))
def test_unseeded_noise_is_independent_of_global_seed(noise_type, global_random_state):
    first = generate_noise(noise_type=noise_type, duration=0.1, fade_in=0.01, fade_out=0.01)
    np.random.set_state(global_random_state)
    second = generate_noise(noise_type=noise_type, duration=0.1, fade_in=0.01, fade_out=0.01)

    assert not np.array_equal(first, second)


@pytest.mark.parametrize("noise_type, expected", [
    (NoiseType.WHITE, [0, -870, 122, 2282, -4419, 11, -4, -9830, 5700, 3364, -3503, -961, 2830, -976, -453, 0]),
    (NoiseType.PINK, [0, 693, -585, -4626, -6981, -6904, -4323, -6201, -6480, -9130, -9830, -8319, -8632, -4420, -2664, 0]),
    (NoiseType.BROWN, [0, 2373, 4874, 9681, 5093, 5105, 5100, -5102, 814, 4306, 669, -327, 2610, 727, -106, 0]),
    (NoiseType.BLUE, [0, 589, 885, -4242, 2804, -10, -6218, 9830, -1479, -4346, 1609, 2399, -2718, 43, -1430, 0]),
    (NoiseType.VIOLET, [0, -89, -2274, 4316, -1724, -3802, 9830, -6927, -1756, 3648, 484, -3135, 1705, -1779, 2329, 0]),
])
def test_seeded_noise_matches_legacy_output(noise_type, expected):
    # PCM samples captured before RNG isolation, using the global RandomState.
    audio = generate_noise(
        noise_type=noise_type, duration=0.016, sample_rate=1000,
        fade_in=0.004, fade_out=0.004, volume=0.3, seed=7,
    )

    assert audio.dtype == np.int16
    np.testing.assert_array_equal(audio, expected)
