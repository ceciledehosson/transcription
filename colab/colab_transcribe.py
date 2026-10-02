#!/usr/bin/env python3
"""WhisperX + pyannote transcription for Google Colab.

Produces JSON, timestamped TXT and SRT with anonymised speaker labels.
"""
from __future__ import annotations

import argparse
import gc
import json
import os
from pathlib import Path
from typing import Any

import torch
import whisperx
from whisperx.diarize import DiarizationPipeline, assign_word_speakers


def hhmmss(seconds: float) -> str:
    seconds = max(0, int(seconds))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def srt_time(seconds: float) -> str:
    ms = max(0, int(round(seconds * 1000)))
    h, rem = divmod(ms, 3_600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def speaker_mapping(segments: list[dict[str, Any]]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for seg in segments:
        raw = seg.get("speaker")
        if raw is not None and raw not in mapping:
            mapping[raw] = f"Locuteur {len(mapping) + 1}"
    return mapping


def write_outputs(result: dict[str, Any], audio_path: Path, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = audio_path.stem
    segments = result.get("segments", [])
    mapping = speaker_mapping(segments)

    json_path = output_dir / f"{stem}_diarized.json"
    payload = {
        "source_file": audio_path.name,
        "language": result.get("language"),
        "speaker_mapping": mapping,
        "segments": segments,
    }
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    txt_path = output_dir / f"{stem}_diarized.txt"
    with txt_path.open("w", encoding="utf-8") as f:
        for seg in segments:
            speaker = mapping.get(seg.get("speaker"), "Locuteur ?")
            start = hhmmss(float(seg.get("start", 0)))
            end = hhmmss(float(seg.get("end", 0)))
            text = str(seg.get("text", "")).strip()
            f.write(f"{speaker} [{start} - {end}] : {text}\n\n")

    srt_path = output_dir / f"{stem}_diarized.srt"
    with srt_path.open("w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, 1):
            speaker = mapping.get(seg.get("speaker"), "Locuteur ?")
            start = srt_time(float(seg.get("start", 0)))
            end = srt_time(float(seg.get("end", 0)))
            text = str(seg.get("text", "")).strip()
            f.write(f"{i}\n{start} --> {end}\n{speaker} : {text}\n\n")

    return [json_path, txt_path, srt_path]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("audio", type=Path)
    p.add_argument("--output-dir", type=Path, default=Path("outputs"))
    p.add_argument("--model", default="medium")
    p.add_argument("--language", default="fr")
    p.add_argument("--num-speakers", type=int, default=3)
    p.add_argument("--batch-size", type=int, default=8)
    p.add_argument("--compute-type", default="float16", choices=["float16", "float32", "int8"])
    return p.parse_args()


def main() -> None:
    args = parse_args()
    token = os.environ.get("HF_TOKEN")
    if not token:
        raise RuntimeError("HF_TOKEN absent. Ajoutez le token dans Colab > Secrets puis chargez-le dans os.environ['HF_TOKEN'].")
    if not args.audio.exists():
        raise FileNotFoundError(args.audio)
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA indisponible. Dans Colab : Exécution > Modifier le type d'exécution > GPU T4.")

    device = "cuda"
    print(f"GPU : {torch.cuda.get_device_name(0)}")
    print(f"Whisper : {args.model} | langue={args.language} | locuteurs={args.num_speakers}")

    print("1/3 Transcription WhisperX...")
    model = whisperx.load_model(args.model, device, compute_type=args.compute_type, language=args.language)
    audio = whisperx.load_audio(str(args.audio))
    result = model.transcribe(audio, batch_size=args.batch_size, language=args.language)
    del model
    gc.collect()
    torch.cuda.empty_cache()

    print("2/3 Alignement temporel...")
    model_a, metadata = whisperx.load_align_model(language_code=result.get("language", args.language), device=device)
    result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
    result["language"] = result.get("language", args.language)
    del model_a
    gc.collect()
    torch.cuda.empty_cache()

    print("3/3 Diarisation pyannote community-1...")
    diarize_model = DiarizationPipeline(
        model_name="pyannote/speaker-diarization-community-1",
        token=token,
        device=device,
    )
    diarize_segments = diarize_model(audio, num_speakers=args.num_speakers)
    result = assign_word_speakers(diarize_segments, result)

    paths = write_outputs(result, args.audio, args.output_dir)
    print("\nTerminé.")
    for path in paths:
        print(path)


if __name__ == "__main__":
    main()
