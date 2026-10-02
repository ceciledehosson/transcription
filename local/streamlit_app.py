from __future__ import annotations

import os
import re
from pathlib import Path

import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
AUDIO_DIR = BASE_DIR / "audio"
OUTPUT_DIR = BASE_DIR / "outputs"
ENV_FILE = BASE_DIR / ".env"


def safe_filename(filename: str) -> str:
    name = Path(filename).name
    name = re.sub(r"[^\w.\- ]+", "_", name, flags=re.UNICODE)
    return name.strip().replace(" ", "_") or "entretien_audio"


def download_button(path: Path) -> None:
    if not path.exists():
        return
    labels = {
        ".txt": "Télécharger le TXT",
        ".srt": "Télécharger le SRT",
        ".json": "Télécharger le JSON",
    }
    st.download_button(
        labels.get(path.suffix, f"Télécharger {path.name}"),
        data=path.read_bytes(),
        file_name=path.name,
        mime="text/plain" if path.suffix in {".txt", ".srt"} else "application/json",
    )


st.set_page_config(page_title="AutoTranscript local", layout="centered")

st.title("AutoTranscript local")
st.caption("Transcrire un entretien audio depuis cet ordinateur.")

with st.expander("À savoir avant de commencer", expanded=True):
    st.markdown(
        """
        - Les fichiers restent dans les dossiers locaux `audio/` et `outputs/`.
        - La première exécution télécharge les modèles nécessaires.
        - La transcription automatique doit être relue et corrigée à partir de l'audio.
        - Les étiquettes `Locuteur 1`, `Locuteur 2`, etc. doivent être vérifiées.
        """
    )

uploaded_file = st.file_uploader(
    "Choisir le fichier audio de l'entretien",
    type=["mp3", "wav", "m4a", "ogg", "flac", "aac", "mp4", "mkv", "mov"],
)

with st.sidebar:
    st.header("Réglages")
    diarization = st.checkbox("Distinguer les locuteurs", value=True)
    num_speakers = st.number_input(
        "Nombre de locuteurs",
        min_value=1,
        max_value=8,
        value=2,
        step=1,
        disabled=not diarization,
    )
    language = st.text_input("Langue", value="fr")
    device = st.selectbox("Machine", ["auto", "cpu", "cuda"], index=0)
    model = st.selectbox("Modèle Whisper", ["auto", "small", "medium", "large-v3"], index=0)
    compute_type = st.selectbox("Calcul", ["auto", "int8", "float16", "float32"], index=0)
    batch_size = st.slider("Taille des lots", min_value=1, max_value=16, value=8)

    hf_token = ""
    if diarization:
        hf_token = st.text_input(
            "Token Hugging Face",
            type="password",
            help="Optionnel si HF_TOKEN est déjà présent dans le fichier .env.",
        )

    st.markdown("---")
    st.caption("Sur CPU, commencer par `small` et `int8` est souvent plus prudent.")

if uploaded_file is not None:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    audio_path = AUDIO_DIR / safe_filename(uploaded_file.name)
    audio_path.write_bytes(uploaded_file.getbuffer())
    st.audio(audio_path.read_bytes())
    st.info(f"Fichier prêt : `{audio_path.name}`")

    if st.button("Lancer la transcription", type="primary"):
        if hf_token.strip():
            os.environ["HF_TOKEN"] = hf_token.strip()

        messages: list[str] = []
        status = st.empty()

        def progress(message: str) -> None:
            messages.append(message)
            status.markdown("\n".join(f"- {item}" for item in messages))

        try:
            from local_transcribe import transcribe_audio

            with st.spinner("Transcription en cours..."):
                paths = transcribe_audio(
                    audio_path=audio_path,
                    output_dir=OUTPUT_DIR,
                    model=None if model == "auto" else model,
                    language=language.strip() or "fr",
                    num_speakers=int(num_speakers),
                    batch_size=int(batch_size),
                    compute_type=None if compute_type == "auto" else compute_type,
                    device=device,
                    no_diarization=not diarization,
                    env_file=ENV_FILE,
                    progress=progress,
                )
        except ModuleNotFoundError as exc:
            missing = exc.name or "une dépendance Python"
            st.error(
                f"Module absent : {missing}. L'interface est installée, mais le moteur de transcription ne l'est pas encore."
            )
            st.code(
                "python -m pip install --index-url https://download.pytorch.org/whl/cpu torch==2.8.0 torchaudio==2.8.0\n"
                "python -m pip install --resume-retries 20 -r requirements-local.txt",
                language="bash",
            )
        except Exception as exc:
            st.error(str(exc))
        else:
            st.success("Transcription terminée.")
            txt_paths = [path for path in paths if path.suffix == ".txt"]
            if txt_paths:
                st.subheader("Aperçu du TXT")
                st.text_area(
                    "Transcription horodatée",
                    txt_paths[0].read_text(encoding="utf-8"),
                    height=360,
                )

            st.subheader("Téléchargements")
            cols = st.columns(len(paths))
            for col, path in zip(cols, paths):
                with col:
                    download_button(path)
else:
    st.warning("Déposer un fichier audio pour commencer.")
