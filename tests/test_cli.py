# -*- coding: utf-8 -*-
import sys
import pytest
from unittest import mock

from zenix.cli import _parse_args, _run
from zenix.params import NoiseType


def test_parse_args_defaults(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prog"])
    args = _parse_args()

    assert args.type == NoiseType.WHITE.value
    assert args.loop is False


def test_parse_args_all_types(monkeypatch):
    for noise_type in NoiseType:
        monkeypatch.setattr(sys, "argv", ["prog", "-t", noise_type.value])
        args = _parse_args()
        assert args.type == noise_type.value


def test_parse_args_custom(monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        ["prog", "-t", "pink", "-d", "2", "-v", "0.5", "--fade-in", "0.2", "--loop"],
    )
    args = _parse_args()

    assert args.type == "pink"
    assert args.duration == 2.0
    assert args.volume == 0.5
    assert args.fade_in == 0.2
    assert args.loop is True


def test_run_invalid_volume():
    args = mock.Mock()
    args.volume = 2.0

    with pytest.raises(SystemExit):
        _run(args)


@mock.patch("zenix.cli.play_noise")
@mock.patch("zenix.cli.generate_noise")
def test_run_calls_generate_and_play(mock_generate, mock_play):
    args = mock.Mock()
    args.type = NoiseType.WHITE.value
    args.duration = 1.0
    args.volume = 0.5
    args.fade_in = 0.1
    args.loop = False

    mock_generate.return_value = "audio"

    _run(args)

    mock_generate.assert_called_once()
    mock_play.assert_called_once()


@mock.patch("zenix.cli.play_noise")
@mock.patch("zenix.cli.generate_noise")
def test_run_all_noise_types(mock_generate, mock_play):
    for noise_type in NoiseType:
        args = mock.Mock()
        args.type = noise_type.value
        args.duration = 0.5
        args.volume = 0.5
        args.fade_in = 0.1
        args.loop = False

        mock_generate.return_value = "audio"

        _run(args)

        mock_generate.assert_called()
        mock_play.assert_called()