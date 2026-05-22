# -*- coding: utf-8 -*-
import sys
import pytest
from unittest.mock import patch
from zenix.cli import main
from zenix.cli import _print_cli_error
from zenix import NoiseType
from zenix import ZenixValidationError


def test_cli_version(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["zenix", "--version"])
    main()
    captured = capsys.readouterr()
    assert captured.out.strip()


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
    monkeypatch.setattr(sys, "argv", ["zenix", "-t", "pink", "-d", "0.2", "-v", "0.5",
                                      "--fade-in", "0.05", "--fade-out", "0.05", "--sample-rate", "40000"], )

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


def test_cli_output_file(monkeypatch, tmp_path):
    filepath = tmp_path / "cli.wav"

    monkeypatch.setattr(
        sys, "argv",
        ["zenix", "-d", "6", "-o", str(filepath)]
    )

    monkeypatch.setattr("zenix.cli.play_noise", lambda *a, **k: None)

    main()

    assert filepath.exists()


def test_cli_output_and_play(monkeypatch, tmp_path):
    filepath = tmp_path / "cli.wav"

    monkeypatch.setattr(
        sys, "argv",
        ["zenix", "-o", str(filepath)]
    )

    with patch("zenix.cli.play_noise") as mock_play:
        main()

    assert filepath.exists()
    mock_play.assert_called_once()


def test_cli_print_error(capsys):
    with pytest.raises(SystemExit) as exc:
        _print_cli_error("test error", exit_code=5)
    captured = capsys.readouterr()
    assert "[ZENIX ERROR] test error" in captured.err
    assert exc.value.code == 5


def test_cli_zenix_error(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["zenix"])
    def fake_generate(*args, **kwargs):
        raise ZenixValidationError("validation failed")
    monkeypatch.setattr("zenix.cli.generate_noise", fake_generate)
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "validation failed" in captured.err


def test_cli_unexpected_error(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["zenix"])
    def fake_generate(*args, **kwargs):
        raise RuntimeError("boom")
    monkeypatch.setattr("zenix.cli.generate_noise", fake_generate)
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "Unexpected error: boom" in captured.err
