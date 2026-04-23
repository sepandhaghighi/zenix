# -*- coding: utf-8 -*-
import sys
import pytest
from unittest.mock import patch

from zenix.cli import main
from zenix import NoiseType


def test_cli_default(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["zenix"])

    with patch("zenix.cli.play_noise") as mock_play:
        with patch("zenix.cli.generate_noise", return_value="audio"):
            main()

    mock_play.assert_called_once()


@pytest.mark.parametrize("noise_type", [nt.value for nt in NoiseType])
def test_cli_all_noise_types(monkeypatch, noise_type):
    monkeypatch.setattr(sys, "argv", ["zenix", "-t", noise_type, "-d", "0.1"])

    with patch("zenix.cli.play_noise") as mock_play:
        with patch("zenix.cli.generate_noise", return_value="audio"):
            main()

    mock_play.assert_called_once()


def test_cli_custom_params(monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        ["zenix", "-t", "pink", "-d", "0.2", "-v", "0.5", "--fade-in", "0.05", "--fade-out", "0.05", "--sample-rate", "40000"],
    )

    with patch("zenix.cli.play_noise") as mock_play:
        with patch("zenix.cli.generate_noise", return_value="audio"):
            main()

    mock_play.assert_called_once()


def test_cli_loop_flag(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["zenix", "--loop"])

    with patch("zenix.cli.generate_noise", return_value="audio"):
        with patch("zenix.cli.play_noise") as mock_play:
            main()
    _, kwargs = mock_play.call_args
    assert kwargs["loop"] is True


def test_cli_invalid_volume(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["zenix", "-v", "2.0"])
    with pytest.raises(SystemExit):
        main()
