#!/usr/bin/env python3
"""Generate zh-TW narration, subtitles, and narrated chapter/final videos."""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

import edge_tts
from pydub import AudioSegment


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "narration" / "zh-TW.txt"
WORK_DIR = ROOT / "media" / "narration"
OUTPUT_DIR = ROOT / "output"

VOICE = "zh-TW-HsiaoChenNeural"
RATE = "+5%"
INTRO_SILENCE_MS = 650
SEGMENT_GAP_MS = 280
OUTRO_SILENCE_MS = 900


@dataclass(frozen=True)
class Chapter:
    number: int
    section_keys: tuple[str, ...]
    source_dir: str
    scene_name: str


CHAPTERS = (
    Chapter(1, ("第 1 章：交換名片",), "ch01_signaling", "Chapter1Signaling"),
    Chapter(2, ("第 2 章：尋找秘密通道",), "ch02_ice_stun_turn", "Chapter2IceStunTurn"),
    Chapter(3, ("第 3 章：遞送加密金鑰",), "ch03_dtls_srtp", "Chapter3DtlsSrtp"),
    Chapter(4, ("第 4 章：應對交通堵塞",), "ch04_abr", "Chapter4Abr"),
    Chapter(
        5,
        ("第 5 章：從兩人世界到百人派對", "總結"),
        "ch05_topologies",
        "Chapter5Topologies",
    ),
)


def run(command: list[str]) -> None:
    print("+", " ".join(command))
    subprocess.run(command, cwd=ROOT, check=True)


def probe_duration(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(json.loads(result.stdout)["format"]["duration"])


def parse_sections(path: Path) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = re.fullmatch(r"【(.+)】", line)
        if match:
            current = match.group(1)
            sections[current] = []
        elif current is not None:
            sections[current].append(line)
    return {key: "".join(value) for key, value in sections.items()}


def split_for_narration(text: str, max_chars: int = 34) -> list[str]:
    sentences = [part.strip() for part in re.split(r"(?<=[。！？])", text) if part.strip()]
    segments: list[str] = []
    for sentence in sentences:
        if len(sentence) <= max_chars:
            segments.append(sentence)
            continue

        clauses = [part.strip() for part in re.split(r"(?<=[，；：])", sentence) if part.strip()]
        current = ""
        for clause in clauses:
            if current and len(current) + len(clause) > max_chars:
                segments.append(current)
                current = clause
            else:
                current += clause
        if current:
            segments.append(current)
    return segments


def srt_timestamp(milliseconds: int) -> str:
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    seconds, millis = divmod(remainder, 1_000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{millis:03}"


def wrap_subtitle(text: str, width: int = 24) -> str:
    if len(text) <= width:
        return text

    lines: list[str] = []
    remaining = text
    preferred_breaks = "，；：、。！？ "
    while len(remaining) > width:
        break_at = max(remaining.rfind(char, 0, width + 1) for char in preferred_breaks)
        if break_at < width // 2:
            break_at = width
            while break_at < len(remaining) and remaining[break_at].isascii() and remaining[break_at].isalnum():
                break_at += 1
        elif remaining[break_at] in preferred_breaks[:-1]:
            break_at += 1
        lines.append(remaining[:break_at].strip())
        remaining = remaining[break_at:].strip()
    if remaining:
        lines.append(remaining)
    return "\n".join(lines)


def write_srt(entries: list[tuple[int, int, str]], path: Path) -> None:
    blocks = []
    for index, (start_ms, end_ms, text) in enumerate(entries, start=1):
        blocks.append(
            f"{index}\n{srt_timestamp(start_ms)} --> {srt_timestamp(end_ms)}\n"
            f"{wrap_subtitle(text)}\n"
        )
    path.write_text("\n".join(blocks), encoding="utf-8")


async def synthesize(text: str, destination: Path, force: bool) -> None:
    if destination.exists() and not force:
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(1, 4):
        try:
            await edge_tts.Communicate(text, VOICE, rate=RATE).save(str(destination))
            return
        except Exception:
            if attempt == 3:
                raise
            await asyncio.sleep(attempt * 1.5)


async def build_chapter_audio(
    chapter: Chapter,
    sections: dict[str, str],
    force: bool,
) -> tuple[Path, Path, int, list[tuple[int, int, str]]]:
    text = "".join(sections[key] for key in chapter.section_keys)
    segments = split_for_narration(text)
    chapter_dir = WORK_DIR / f"ch{chapter.number:02}"
    segment_paths = [chapter_dir / f"segment-{index:02}.mp3" for index in range(1, len(segments) + 1)]

    for text_segment, segment_path in zip(segments, segment_paths):
        await synthesize(text_segment, segment_path, force)

    combined = AudioSegment.silent(duration=INTRO_SILENCE_MS)
    cursor_ms = INTRO_SILENCE_MS
    subtitle_entries: list[tuple[int, int, str]] = []

    for text_segment, segment_path in zip(segments, segment_paths):
        audio_segment = AudioSegment.from_file(segment_path)
        start_ms = cursor_ms
        end_ms = start_ms + len(audio_segment)
        subtitle_entries.append((start_ms, end_ms, text_segment))
        combined += audio_segment
        combined += AudioSegment.silent(duration=SEGMENT_GAP_MS)
        cursor_ms = end_ms + SEGMENT_GAP_MS

    combined += AudioSegment.silent(duration=OUTRO_SILENCE_MS)
    audio_path = chapter_dir / f"chapter-{chapter.number:02}.wav"
    srt_path = chapter_dir / f"chapter-{chapter.number:02}.srt"
    combined.export(audio_path, format="wav")
    write_srt(subtitle_entries, srt_path)
    return audio_path, srt_path, len(combined), subtitle_entries


def source_video(chapter: Chapter, profile: str) -> Path:
    return (
        ROOT
        / "media"
        / "videos"
        / chapter.source_dir
        / profile
        / f"{chapter.scene_name}.mp4"
    )


def mux_chapter(
    chapter: Chapter,
    profile: str,
    fps: int,
    audio_path: Path,
    srt_path: Path,
    audio_duration_ms: int,
) -> Path:
    video_path = source_video(chapter, profile)
    if not video_path.exists():
        raise FileNotFoundError(f"Missing rendered chapter: {video_path}")

    chapter_output_dir = OUTPUT_DIR / "chapters"
    chapter_output_dir.mkdir(parents=True, exist_ok=True)
    output_path = chapter_output_dir / f"{chapter.scene_name}.mp4"
    video_duration = probe_duration(video_path)
    audio_duration = audio_duration_ms / 1_000
    speed_factor = audio_duration / video_duration

    run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "warning",
            "-i",
            str(video_path),
            "-i",
            str(audio_path),
            "-f",
            "srt",
            "-i",
            str(srt_path),
            "-filter_complex",
            f"[0:v]setpts={speed_factor:.9f}*PTS[v]",
            "-map",
            "[v]",
            "-map",
            "1:a:0",
            "-map",
            "2:s:0",
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "16",
            "-pix_fmt",
            "yuv420p",
            "-r",
            str(fps),
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-ar",
            "48000",
            "-ac",
            "2",
            "-af",
            "loudnorm=I=-16:TP=-1.5:LRA=11",
            "-c:s",
            "mov_text",
            "-metadata:s:a:0",
            "language=zho",
            "-metadata:s:s:0",
            "language=zho",
            "-t",
            f"{audio_duration:.3f}",
            str(output_path),
        ]
    )
    return output_path


def concatenate_chapters(chapter_paths: list[Path], global_srt_path: Path) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    concat_path = OUTPUT_DIR / "narrated-concat.txt"
    av_path = OUTPUT_DIR / "webrtc_story_av.mp4"
    final_path = OUTPUT_DIR / "webrtc_story.mp4"
    concat_path.write_text(
        "".join(f"file '{path.resolve()}'\n" for path in chapter_paths),
        encoding="utf-8",
    )

    run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "warning",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_path),
            "-map",
            "0:v:0",
            "-map",
            "0:a:0",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-af",
            "aresample=async=1:first_pts=0",
            str(av_path),
        ]
    )
    run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "warning",
            "-i",
            str(av_path),
            "-f",
            "srt",
            "-i",
            str(global_srt_path),
            "-map",
            "0:v:0",
            "-map",
            "0:a:0",
            "-map",
            "1:s:0",
            "-c:v",
            "copy",
            "-c:a",
            "copy",
            "-c:s",
            "mov_text",
            "-metadata:s:a:0",
            "language=zho",
            "-metadata:s:s:0",
            "language=zho",
            str(final_path),
        ]
    )
    av_path.unlink(missing_ok=True)
    return final_path


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", default="1080p30")
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--force-tts", action="store_true")
    args = parser.parse_args()

    sections = parse_sections(SCRIPT_PATH)
    chapter_paths: list[Path] = []
    global_entries: list[tuple[int, int, str]] = []
    global_cursor_ms = 0

    for chapter in CHAPTERS:
        audio_path, srt_path, duration_ms, entries = await build_chapter_audio(
            chapter, sections, args.force_tts
        )
        print(f"Chapter {chapter.number}: {duration_ms / 1_000:.2f}s narration")
        chapter_paths.append(
            mux_chapter(
                chapter,
                args.profile,
                args.fps,
                audio_path,
                srt_path,
                duration_ms,
            )
        )
        global_entries.extend(
            (start + global_cursor_ms, end + global_cursor_ms, text)
            for start, end, text in entries
        )
        global_cursor_ms += duration_ms

    global_srt_path = OUTPUT_DIR / "webrtc_story.srt"
    write_srt(global_entries, global_srt_path)
    final_path = concatenate_chapters(chapter_paths, global_srt_path)
    print(f"Created narrated video: {final_path}")


if __name__ == "__main__":
    asyncio.run(main())
