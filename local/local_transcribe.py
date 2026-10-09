#!/usr/bin/env python3
"""Local WhisperX + pyannote transcription.

Produces JSON, timestamped TXT and SRT files for an audio interview.
"""
from __future__ import annotations

import argparse
import gc
import json
import os
from pathlib import Path
from typing import Any, Callable

import torch
import whisperx
from whisperx.diarize import DiarizationPipeline, assign_word_speakers

ProgressCallback = Callable[[str], None]


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def hhmmss(seconds: float) -> str:
    seconds = max(0, int(seconds))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def srt_time(seconds: float) -> str:
    ms = max(0, int(round(seconds * 1000)))
    h, rem = divmod(ms, 3_600_000)
    m, rem = divmod(ms - h * 3_600_000, 60_000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def speaker_mapping(segments: list[dict[str, Any]]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for seg in segments:
        raw = seg.get("speaker")
        if raw is not None and raw not in mapping:
            mapping[raw] = f"Locuteur {len(mapping) + 1}"
    return mapping


def segment_line(seg: dict[str, Any], mapping: dict[str, str]) -> str:
    start = hhmmss(float(seg.get("start", 0)))
    end = hhmmss(float(seg.get("end", 0)))
    text = str(seg.get("text", "")).strip()
    speaker = mapping.get(seg.get("speaker"))
    if speaker:
        return f"{speaker} [{start} - {end}] : {text}"
    return f"[{start} - {end}] : {text}"


def write_outputs(result: dict[str, Any], audio_path: Path, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = audio_path.stem
    segments = result.get("segments", [])
    mapping = speaker_mapping(segments)

    json_path = output_dir / f"{stem}_transcript.json"
    payload = {
        "source_file": audio_path.name,
        "language": result.get("language"),
        "speaker_mapping": mapping,
        "segments": segments,
    }
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    txt_path = output_dir / f"{stem}_transcript.txt"
    with txt_path.open("w", encoding="utf-8") as f:
        for seg in segments:
            f.write(segment_line(seg, mapping) + "\n\n")

    srt_path = output_dir / f"{stem}_transcript.srt"
    with srt_path.open("w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, 1):
            start = srt_time(float(seg.get("start", 0)))
            end = srt_time(float(seg.get("end", 0)))
            text = str(seg.get("text", "")).strip()
            speaker = mapping.get(seg.get("speaker"))
            prefix = f"{speaker} : " if speaker else ""
            f.write(f"{i}\n{start} --> {end}\n{prefix}{text}\n\n")

    return [json_path, txt_path, srt_path]


def choose_device(requested: str) -> str:
    if requested == "auto":
        return "cuda" if torch.cuda.is_available() else "cpu"
    if requested == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA est indisponible sur cette machine. Utiliser --device cpu.")
    return requested


def transcribe_audio(
    audio_path: Path,
    output_dir: Path = Path("outputs"),
    model: str | None = None,
    language: str = "fr",
    num_speakers: int = 2,
    batch_size: int = 4,
    compute_type: str | None = None,
    device: str = "auto",
    no_diarization: bool = False,
    env_file: Path = Path(".env"),
    progress: ProgressCallback = print,
) -> list[Path]:
    load_env_file(env_file)

    if not audio_path.exists():
        raise FileNotFoundError(audio_path)

    selected_device = choose_device(device)
    model_name = model or ("medium" if selected_device == "cuda" else "small")
    selected_compute_type = compute_type or ("float16" if selected_device == "cuda" else "int8")

    if not no_diarization and not os.environ.get("HF_TOKEN"):
        raise RuntimeError(
            "HF_TOKEN absent. Ajouter le token Hugging Face dans .env ou lancer sans diarisation."
        )

    if selected_device == "cuda":
        progress(f"GPU : {torch.cuda.get_device_name(0)}")
    else:
        progress("Mode CPU : la transcription peut etre lente pour un entretien long.")
    progress(
        f"Whisper : {model_name} | langue={language} | device={selected_device} | compute={selected_compute_type}"
    )

    progress("1/3 Transcription WhisperX...")
    whisper_model = whisperx.load_model(
        model_name,
        selected_device,
        compute_type=selected_compute_type,
        language=language,
    )
    audio = whisperx.load_audio(str(audio_path))
    result = whisper_model.transcribe(audio, batch_size=batch_size, language=language)
    del whisper_model
    gc.collect()
    if selected_device == "cuda":
        torch.cuda.empty_cache()

    progress("2/3 Alignement temporel...")
    align_model, metadata = whisperx.load_align_model(
        language_code=result.get("language", language),
        device=selected_device,
    )
    result = whisperx.align(
        result["segments"],
        align_model,
        metadata,
        audio,
        selected_device,
        return_char_alignments=False,
    )
    result["language"] = result.get("language", language)
    del align_model
    gc.collect()
    if selected_device == "cuda":
        torch.cuda.empty_cache()

    if no_diarization:
        progress("3/3 Diarisation desactivee.")
    else:
        progress("3/3 Diarisation pyannote community-1...")
        diarize_model = DiarizationPipeline(
            model_name="pyannote/speaker-diarization-community-1",
            token=os.environ["HF_TOKEN"],
            device=selected_device,
        )
        diarize_segments = diarize_model(audio, num_speakers=num_speakers)
        result = assign_word_speakers(diarize_segments, result)

    paths = write_outputs(result, audio_path, output_dir)
    progress("Termine.")
    return paths


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Transcrire localement un entretien audio avec WhisperX."
    )
    p.add_argument("audio", type=Path, help="Chemin du fichier audio à transcrire.")
    p.add_argument("--output-dir", type=Path, default=Path("outputs"))
    p.add_argument("--model", default=None, help="Modèle WhisperX. Défaut : medium sur GPU, small sur CPU.")
    p.add_argument("--language", default="fr")
    p.add_argument("--num-speakers", type=int, default=2)
    p.add_argument("--batch-size", type=int, default=4)
    p.add_argument("--compute-type", default=None, choices=["float16", "float32", "int8"])
    p.add_argument("--device", default="auto", choices=["auto", "cuda", "cpu"])
    p.add_argument("--no-diarization", action="store_true", help="Transcrire sans distinguer les locuteurs.")
    p.add_argument("--env-file", type=Path, default=Path(".env"), help="Fichier contenant HF_TOKEN.")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    paths = transcribe_audio(
        audio_path=args.audio,
        output_dir=args.output_dir,
        model=args.model,
        language=args.language,
        num_speakers=args.num_speakers,
        batch_size=args.batch_size,
        compute_type=args.compute_type,
        device=args.device,
        no_diarization=args.no_diarization,
        env_file=args.env_file,
    )
    print("\nTerminé.")
    for path in paths:
        print(path)


if __name__ == "__main__":
    main()
