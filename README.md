<div align="center">
<img src="https://github.com/sepandhaghighi/zenix/raw/main/otherfiles/logo.png" width="350">
<h1>Zenix: A Lightweight Tool for Procedural Noise Generation</h1>
<br/>
<a href="https://www.python.org/"><img src="https://img.shields.io/badge/built%20with-Python3-green.svg" alt="built with Python3"></a>
<a href="https://github.com/sepandhaghighi/zenix"><img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/sepandhaghighi/zenix"></a>
<a href="https://badge.fury.io/py/zenix"><img src="https://badge.fury.io/py/zenix.svg" alt="PyPI version"></a>
</div>			
				
## Overview	

<p align="justify">		
Zenix is a lightweight tool for generating procedural noise such as white, pink, and brown noise. It can be used both as a command-line application and as a Python library, making it suitable for quick terminal usage as well as integration into Python projects. Zenix generates noise programmatically using NumPy and plays it through an audio backend, allowing developers to create continuous background sound for focus, concentration, relaxation, or acoustic masking. With support for multiple noise types, configurable parameters, fade-in effects, and looping playback, Zenix provides a simple yet flexible way to work with procedural noise in both interactive and programmatic environments.
</p>

<table>
	<tr>
		<td align="center">PyPI Counter</td>
		<td align="center"><a href="http://pepy.tech/project/zenix"><img src="http://pepy.tech/badge/zenix"></a></td>
	</tr>
	<tr>
		<td align="center">Github Stars</td>
		<td align="center"><a href="https://github.com/sepandhaghighi/zenix"><img src="https://img.shields.io/github/stars/sepandhaghighi/zenix.svg?style=social&label=Stars"></a></td>
	</tr>
</table>



<table>
	<tr> 
		<td align="center">Branch</td>
		<td align="center">main</td>	
		<td align="center">dev</td>	
	</tr>
	<tr>
		<td align="center">CI</td>
		<td align="center"><img src="https://github.com/sepandhaghighi/zenix/actions/workflows/test.yml/badge.svg?branch=main"></td>
		<td align="center"><img src="https://github.com/sepandhaghighi/zenix/actions/workflows/test.yml/badge.svg?branch=dev"></td>
	</tr>
</table>

## Installation		

### Source Code
- Download [Version 0.1](https://github.com/sepandhaghighi/zenix/archive/v0.1.zip) or [Latest Source](https://github.com/sepandhaghighi/zenix/archive/dev.zip)
- `pip install .`				

### PyPI

- Check [Python Packaging User Guide](https://packaging.python.org/installing/)     
- `pip install zenix==0.1`						


## Usage

### CLI

```bash
zenix --type=white --duration=120 --volume=0.25 --fade-in=2 --loop
```

#### Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--type` | Noise type (`white`, `pink`, `brown`) | `white` |
| `--duration` | Duration of generated noise in seconds | `30` |
| `--volume` | Output volume multiplier | `0.3` |
| `--fade-in` | Fade-in duration in seconds | `2` |
| `--loop` | Enable continuous looping playback | `False` |


### Library

```python
import tempfile
from zenix import generate_noise, play_noise, NoiseType
audio = generate_noise(
        noise_type=NoiseType.WHITE,
        duration=120,
        sample_rate=44000,
        volume=0.25,
        fade_in=2,
    )
with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
    temp_path = tmp.name
play_noise(filepath=temp_path, audio=audio, sample_rate=44000, loop=True)
```

#### Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `noise_type` | Noise type (`white`, `pink`, `brown`) | `white` |
| `duration` | Duration of generated noise in seconds | `30` |
| `sample_rate` | Audio sample rate in Hz | `44100` |
| `volume` | Output volume multiplier | `0.3` |
| `fade_in` | Fade-in duration in seconds | `2` |

## Issues & Bug Reports			

Just fill an issue and describe it. We'll check it ASAP!

- Please complete the issue template

## Show Your Support
								
<h3>Star This Repo</h3>					

Give a ⭐️ if this project helped you!

<h3>Donate to Our Project</h3>	

<h4>Bitcoin</h4>
1KtNLEEeUbTEK9PdN6Ya3ZAKXaqoKUuxCy
<h4>Ethereum</h4>
0xcD4Db18B6664A9662123D4307B074aE968535388
<h4>Litecoin</h4>
Ldnz5gMcEeV8BAdsyf8FstWDC6uyYR6pgZ
<h4>Doge</h4>
DDUnKpFQbBqLpFVZ9DfuVysBdr249HxVDh
<h4>Tron</h4>
TCZxzPZLcJHr2qR3uPUB1tXB6L3FDSSAx7
<h4>Ripple</h4>
rN7ZuRG7HDGHR5nof8nu5LrsbmSB61V1qq
<h4>Binance Coin</h4>
bnb1zglwcf0ac3d0s2f6ck5kgwvcru4tlctt4p5qef
<h4>Tether</h4>
0xcD4Db18B6664A9662123D4307B074aE968535388
<h4>Dash</h4>
Xd3Yn2qZJ7VE8nbKw2fS98aLxR5M6WUU3s
<h4>Stellar</h4>		
GALPOLPISRHIYHLQER2TLJRGUSZH52RYDK6C3HIU4PSMNAV65Q36EGNL
<h4>Zilliqa</h4>
zil1knmz8zj88cf0exr2ry7nav9elehxfcgqu3c5e5
<h4>Coffeete</h4>
<a href="http://www.coffeete.ir/opensource">
<img src="http://www.coffeete.ir/images/buttons/lemonchiffon.png" style="width:260px;" />
</a>

