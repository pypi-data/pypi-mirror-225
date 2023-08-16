<div align="center">

[![](./stargazerz/Assets/banner.png)](https://github.com/Frikallo/stargazerz)

[![PyPI - Downloads](https://img.shields.io/pypi/dd/stargazerz?color=orange)](https://github.com/Frikallo/MISST/releases/latest) [![License](https://img.shields.io/github/license/frikallo/stargazerz?color=orange)](https://github.com/Frikallo/MISST/blob/main/LICENSE) 

</div>

---

###

Original Repository of MISST : **M**usic/**I**nstrumental **S**tem **S**eparation **T**ool.

This application uses state-of-the-art [demucs](https://github.com/facebookresearch/demucs) source separation models to extract the 4 core stems from audio files (Bass, Drums, Other Instrumentals and Vocals). But it is not limited to this. MISST acts as a developped music player aswell, fit to enjoy and medal with your audio files as you see fit. MISST even comes prepared to import songs and playlists directly from your music library.

This project is OpenSource, feel free to use, study and/or send pull request.

## Key Features

- **Sound Wave Generation**: Generate different types of sound waves, such as sine, square, triangle, and sawtooth waves, with control over frequency, amplitude, and phase.
- **Envelope Generation**: Create amplitude envelopes, including ADSR (Attack, Decay, Sustain, Release), to shape the volume contour of sounds over time.
- **Digital Signal Processing (DSP) Effects**: Apply filters, delays, reverbs, modulation effects, and more to manipulate the synthesized audio.
- **Multi-track Composition**: Combine multiple sound waves or synthesized audio segments to create multi-track compositions, with control over volume, panning, and timing.
- **Real-time Audio Playback**: Listen to the synthesized audio in real-time, facilitating interactive sound design and experimentation.
- **Audio Export**: Export the synthesized audio data to common audio file formats such as WAV, MP3, and OGG.
- **Comprehensive Documentation and Examples**: Detailed documentation and examples are provided to help users quickly get started and explore SonicSynth's capabilities.

## Installation

You can install stargazerz using `pip`:

```shell
pip install stargazerz
```

## Usage
```python
import stargazerz

# Define Crawler
crawler = stargazerz.Crawler(threads=16, target="Frikallo/stargazerz")

# Run Crawler
crawler.run()

# Get Results after Crawler is done
crawler.print_results()

# Save results to file
crawler.save_results("emails", "emails.txt")
crawler.save_results("stargazers", "stargazers.txt")
crawler.save_results("all", "all.txt")
```

## Example Output
```shell
$ python3 stargazerz-example.py
[+] Target: Frikallo/stargazerz
[+] Threads: 16
[+] Starting crawler
[+] Crawler started
[+] Fetching page 1 of stargazers for Frikallo/stargazerz
[+] Fetching page 2 of stargazers for Frikallo/stargazerz
[+] Found 34 stargazers
[+] Fetching emails
Complete ✅: 100%|███████████████| 34/34 [00:18<00:00,  1.40stargazers/s]
[+] Crawler finished
[+] Time: 19.92 seconds
[-] Results
[+] Stargazers: 34
[+] Emails: 26
[+] Emails saved to emails.txt
[+] Stargazers saved to stargazers.txt
[+] All results saved to all.txt
```

