# AutoTranscript — utilisation locale

Cette procédure permet de transcrire localement un entretien audio avec
**WhisperX** et, si souhaité, une diarisation des locuteurs avec **pyannote**.
Elle s'adresse aux étudiant·es qui doivent produire une première transcription
de travail à partir d'un entretien enregistré.

La sortie automatique doit toujours être relue et corrigée à partir de l'audio.
Elle ne constitue pas une transcription de recherche finalisée.

## Ce que produit le script

Pour un fichier `entretien_01.m4a`, le script crée dans `outputs/` :

- `entretien_01_transcript.txt` : texte horodaté, le plus pratique pour relire ;
- `entretien_01_transcript.srt` : sous-titres ;
- `entretien_01_transcript.json` : sortie structurée à conserver.

Avec diarisation, les locuteurs sont nommés `Locuteur 1`, `Locuteur 2`, etc.,
selon leur ordre d'apparition. Ces étiquettes ne sont pas une identification des
personnes : elles doivent être vérifiées et éventuellement renommées après
écoute.

## Prérequis

- Python 3.10 à 3.13.
- `ffmpeg`, nécessaire pour lire les fichiers audio.
- Une connexion internet lors de la première utilisation, pour télécharger les
  modèles.
- Pour distinguer les locuteurs : un compte Hugging Face, l'acceptation des
  conditions d'accès du modèle `pyannote/speaker-diarization-community-1`, puis
  un token Hugging Face en lecture.

Les fichiers audio et les transcriptions peuvent contenir des données
personnelles. Ils doivent rester dans les dossiers locaux `audio/` et `outputs/`,
qui ne doivent pas être ajoutés au dépôt GitHub.

## Installation

Depuis le dossier du dépôt :

```bash
cd local
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-local.txt
```

Sous Windows PowerShell :

```powershell
cd local
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-local.txt
```

Installer ensuite `ffmpeg` si la commande n'est pas déjà disponible :

- Ubuntu/Debian : `sudo apt install ffmpeg`
- macOS avec Homebrew : `brew install ffmpeg`
- Windows : `winget install Gyan.FFmpeg`

Vérifier l'installation :

```bash
ffmpeg -version
```

## Ajouter le token Hugging Face

La diarisation pyannote nécessite un token. Le plus simple est de copier le
fichier d'exemple :

```bash
cp .env.example .env
```

Puis de remplacer la valeur par le token personnel :

```text
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxx
```

Ne jamais déposer le fichier `.env` dans GitHub et ne jamais transmettre son
token à quelqu'un d'autre.

Si l'on veut seulement obtenir une transcription sans distinguer les locuteurs,
le token n'est pas nécessaire : il faudra lancer le script avec
`--no-diarization`.

## Utilisation avec l'interface graphique

L'interface graphique est le mode conseillé pour les étudiant·es.

Depuis le dossier `local`, lancer :

```bash
streamlit run streamlit_app.py
```

Une page s'ouvre dans le navigateur, en général à l'adresse :

```text
http://localhost:8501
```

L'utilisation se fait ensuite dans la page :

1. déposer le fichier audio ;
2. choisir si l'on veut distinguer les locuteurs ;
3. indiquer le nombre de locuteurs si la diarisation est activée ;
4. laisser les réglages par défaut, ou choisir `cpu`, `small` et `int8` sur une
   machine peu puissante ;
5. lancer la transcription ;
6. télécharger le fichier TXT, SRT ou JSON.

Cette interface est locale : les fichiers sont copiés dans `audio/` et les
résultats sont écrits dans `outputs/`. Le navigateur ne sert qu'à afficher une
interface sur l'ordinateur qui exécute Python.

Les statistiques d'usage Streamlit sont désactivées dans
`.streamlit/config.toml`.

## Utilisation en ligne de commande

Créer un dossier `audio/`, y placer l'entretien, puis lancer :

```bash
mkdir -p audio outputs
python local_transcribe.py audio/entretien_01.m4a --num-speakers 2
```

Pour un entretien à trois personnes :

```bash
python local_transcribe.py audio/entretien_01.m4a --num-speakers 3
```

Pour transcrire sans diarisation :

```bash
python local_transcribe.py audio/entretien_01.m4a --no-diarization
```

Par défaut, le script utilise le GPU NVIDIA s'il est disponible. Sans GPU, il
passe en mode CPU avec un modèle plus léger. Pour forcer un réglage adapté à un
ordinateur peu puissant :

```bash
python local_transcribe.py audio/entretien_01.m4a --device cpu --model small --compute-type int8 --batch-size 4
```

Pour privilégier la qualité sur une machine équipée d'un GPU NVIDIA :

```bash
python local_transcribe.py audio/entretien_01.m4a --device cuda --model medium --compute-type float16 --batch-size 8
```

## Après la transcription

1. Ouvrir le fichier TXT.
2. Réécouter l'audio en suivant les horodatages.
3. Corriger les mots mal reconnus, les coupes de phrases et les changements de
   locuteur.
4. Conserver séparément le JSON brut et la transcription corrigée.
5. Anonymiser les noms propres si l'entretien doit être partagé ou analysé hors
   de l'espace de travail prévu.

## Problèmes fréquents

- `ffmpeg not found` : installer `ffmpeg`, puis rouvrir le terminal.
- `HF_TOKEN absent` : vérifier le fichier `.env` ou lancer avec
  `--no-diarization`.
- Accès pyannote refusé : vérifier que les conditions du modèle Hugging Face ont
  bien été acceptées avec le même compte que celui du token.
- Mémoire GPU insuffisante : utiliser `--model small` et diminuer
  `--batch-size`.
- Exécution très lente : c'est normal sur CPU pour des entretiens longs ; lancer
  d'abord un court extrait permet de vérifier que tout fonctionne.

## Versions

Les versions sont indiquées dans `requirements-local.txt`. Elles reprennent la
configuration WhisperX + pyannote utilisée dans la version Colab, avec un usage
local possible sur GPU ou CPU.

