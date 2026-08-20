#!/usr/bin/env python3
"""Download a YouTube video, or a full playlist, from a URL."""

import argparse
import sys

from yt_dlp import YoutubeDL


def build_opts(out_dir=".", audio_only=False, playlist=False):
    if playlist:
        # Group each playlist in its own folder, numbered in playlist order.
        # The fallbacks matter when the URL turns out not to be a playlist after
        # all: without them these fields render as the literal string "NA".
        outtmpl = (
            "%(playlist_title,playlist|Unknown Playlist)s/"
            "%(playlist_index&{:03d} - |)s%(title)s.%(ext)s"
        )
    else:
        outtmpl = "%(title)s.%(ext)s"

    opts = {
        "outtmpl": outtmpl,
        # Keep out_dir out of the template so a '%' in the path can't be read
        # as a template field.
        "paths": {"home": out_dir},
        "noplaylist": not playlist,
        # Keep going if a single entry is private/removed.
        "ignoreerrors": playlist,
        # Without these a stalled connection hangs the run with no output. That
        # looks like a freeze right after the previous file's cleanup messages.
        "socket_timeout": 30,
        "retries": 10,
    }

    if audio_only:
        opts["format"] = "bestaudio/best"
        opts["postprocessors"] = [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}
        ]
    else:
        # Best video + best audio, merged into an mp4 when possible.
        opts["format"] = "bestvideo*+bestaudio/best"
        opts["merge_output_format"] = "mp4"

    return opts


def download(url, out_dir=".", audio_only=False, playlist=False):
    opts = build_opts(out_dir, audio_only, playlist)

    with YoutubeDL(opts) as ydl:
        # Non-zero when an entry failed; with ignoreerrors that is the only
        # signal, since no exception is raised.
        return ydl.download([url])


def main():
    parser = argparse.ArgumentParser(description="Download a YouTube video or playlist.")
    parser.add_argument("url", help="YouTube video or playlist URL")
    parser.add_argument("-o", "--output", default=".", help="output directory (default: current)")
    parser.add_argument("-a", "--audio-only", action="store_true", help="extract audio as mp3")
    parser.add_argument(
        "-p",
        "--playlist",
        action="store_true",
        help="download every video in the playlist the URL points to",
    )
    args = parser.parse_args()

    try:
        ret = download(args.url, args.output, args.audio_only, args.playlist)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # yt-dlp's last line is a "Deleting original file ..." cleanup message, so
    # say when we are actually done rather than leaving that as the final word.
    if ret:
        print("Finished, but some downloads failed.")
        return 1
    print(f"Done. Saved to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
