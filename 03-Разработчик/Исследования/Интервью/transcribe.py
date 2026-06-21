#!/usr/bin/env python3
"""
Расшифровка через faster-whisper (CPU). В --output_dir остаётся только .txt;
прочие типичные артефакты (vtt, srt, json, tsv) с тем же именем удаляются.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from faster_whisper import WhisperModel

# Не трогаем .txt; остальное — побочные форматы Whisper/конвертеров.
_ARTIFACT_SUFFIXES = (".vtt", ".srt", ".json", ".tsv")


def _remove_artifacts(out_dir: Path, stem: str) -> None:
    for suf in _ARTIFACT_SUFFIXES:
        path = out_dir / f"{stem}{suf}"
        if path.is_file():
            path.unlink()


def main() -> None:
    p = argparse.ArgumentParser(description="Расшифровка аудио (faster-whisper, CPU)")
    p.add_argument("audio", type=Path, help="Путь к файлу, например /in/interview.mp3")
    p.add_argument("--language", default="ru", help="Код языка или пусто для авто")
    p.add_argument("--model", default="small")
    p.add_argument("--output_dir", type=Path, required=True)
    p.add_argument(
        "--compute_type",
        default="int8",
        help="CPU: int8 (быстрее) или float32 (точнее, медленнее)",
    )
    args = p.parse_args()

    audio = args.audio
    if not audio.is_file():
        raise SystemExit(f"Нет файла: {audio}")

    out_dir = args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = audio.stem

    _remove_artifacts(out_dir, stem)

    lang = args.language or None
    model = WhisperModel(
        args.model,
        device="cpu",
        compute_type=args.compute_type,
    )

    segments_gen, info = model.transcribe(
        str(audio),
        language=lang,
        beam_size=5,
    )
    segments = list(segments_gen)

    lines = [s.text.strip() for s in segments if s.text.strip()]
    plain = "\n".join(lines) + ("\n" if lines else "")
    txt_path = out_dir / f"{stem}.txt"
    txt_path.write_text(plain, encoding="utf-8")

    _remove_artifacts(out_dir, stem)

    dur = getattr(info, "duration", None)
    dur_s = f"{dur:.1f}s" if dur is not None else "?"
    print(f"OK: {txt_path} ({info.language}, {dur_s})")


if __name__ == "__main__":
    main()
