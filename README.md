# YTDownloader

[![CI](https://github.com/pitchblackice/yt-downloader/actions/workflows/ci.yml/badge.svg)](https://github.com/pitchblackice/yt-downloader/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A small command-line wrapper around [yt-dlp](https://github.com/yt-dlp/yt-dlp) for downloading YouTube videos, audio, or full playlists.

## Requirements

- Python 3
- [ffmpeg](https://ffmpeg.org/) (required for audio extraction and merging separate video/audio streams)

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python download.py URL [-o OUTPUT_DIR] [-a] [-p]
```

| Flag | Description |
|---|---|
| `-o`, `--output` | Output directory (default: current directory) |
| `-a`, `--audio-only` | Extract audio only, saved as MP3 |
| `-p`, `--playlist` | Download every video in the playlist the URL points to |

### Examples

Download a single video (best video + audio, merged to MP4):

```bash
python download.py https://www.youtube.com/watch?v=VIDEO_ID
```

Download a video's audio only, as MP3:

```bash
python download.py -a https://www.youtube.com/watch?v=VIDEO_ID
```

Download an entire playlist into `./downloads`, numbered in playlist order:

```bash
python download.py -p -o downloads https://www.youtube.com/playlist?list=PLAYLIST_ID
```

When `-p` is used, each playlist is downloaded into its own subfolder named after the playlist title.

## Note

Only download content you have the rights to download. This tool is provided for personal, legal use (e.g. downloading your own content or content licensed for offline use).
