# AutoTranscript - utilisation locale

Cette procedure permet de transcrire localement un entretien audio avec
**WhisperX** et, si souhaite, de distinguer les locuteurs avec **pyannote.audio**.
Elle s'adresse a des etudiant.es qui doivent obtenir une premiere transcription
de travail a partir d'un entretien enregistre.

La transcription automatique doit toujours etre relue et corrigee a partir de
l'audio. Les etiquettes `Locuteur 1`, `Locuteur 2`, etc. ne sont pas une
identification certaine des personnes.

## A lire avant de commencer

L'installation locale est plus fragile que l'utilisation dans Google Colab,
parce qu'elle depend de la version de Python et des paquets deja presents sur
l'ordinateur. La methode conseillee ci-dessous utilise un environnement separe
avec **Python 3.12**.

A retenir :

- ne pas utiliser Python 3.13 ou 3.14 pour cette installation ;
- installer d'abord l'interface Streamlit ;
- installer ensuite le moteur de transcription ;
- pour distinguer les locuteurs, il faut un token Hugging Face ;
- sans diarisation, le token Hugging Face n'est pas necessaire.

## Ce que produit l'outil

Pour un fichier `entretien_01.m4a`, l'outil cree dans `outputs/` :

- `entretien_01_transcript.txt` : texte horodate, le plus pratique pour relire ;
- `entretien_01_transcript.srt` : sous-titres ;
- `entretien_01_transcript.json` : sortie structuree a conserver.

Les fichiers audio sont copies dans `audio/`. Les resultats sont ecrits dans
`outputs/`. Ces deux dossiers restent sur l'ordinateur local.

## Telecharger le depot

Methode simple, sans Git :

1. aller sur <https://github.com/ceciledehosson/transcription> ;
2. cliquer sur le bouton vert `Code` ;
3. cliquer sur `Download ZIP` ;
4. extraire le fichier ZIP dans `Documents` ;
5. ouvrir un terminal dans le dossier `Documents/transcription-main/local`.

Methode avec Git :

```bash
cd ~/Documents
git clone https://github.com/ceciledehosson/transcription.git
cd transcription/local
```

Si le dossier vient d'un ZIP, la commande sera plutot :

```bash
cd ~/Documents/transcription-main/local
```

## Prerequis

- Miniforge, Anaconda ou Miniconda, pour pouvoir creer un environnement Python
  3.12 meme si l'ordinateur utilise une autre version de Python.
- `ffmpeg`, necessaire pour lire les fichiers audio.
- Une connexion internet lors de la premiere installation et de la premiere
  transcription, pour telecharger les modeles.
- Pour la diarisation : un compte Hugging Face et un token en lecture.

Installer `ffmpeg` si la commande n'existe pas deja :

```bash
sudo apt install ffmpeg
```

Verifier :

```bash
ffmpeg -version
```

Sous macOS avec Homebrew :

```bash
brew install ffmpeg
```

Sous Windows :

```powershell
winget install Gyan.FFmpeg
```

## Installation conseillee avec Conda

Depuis le dossier `local` :

```bash
conda create -n transcription python=3.12 -y
conda activate transcription
python --version
```

La derniere commande doit afficher `Python 3.12...`.

Installer ensuite l'interface :

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements-ui.txt
python -m streamlit run streamlit_app.py
```

A ce stade, l'interface doit s'ouvrir dans le navigateur. Elle peut encore
afficher `Module absent : torch` au moment de lancer la transcription : c'est
normal tant que le moteur n'a pas ete installe.

Arreter Streamlit avec `Ctrl+C`, puis installer le moteur de transcription :

```bash
python -m pip install --index-url https://download.pytorch.org/whl/cpu "torch>=2.8,<3" "torchaudio>=2.8,<3"
python -m pip install --resume-retries 20 -r requirements-local.txt
```

Relancer ensuite :

```bash
python -m streamlit run streamlit_app.py
```

## Relancer l'outil plus tard

Les fois suivantes, il ne faut pas refaire l'installation. Il suffit de revenir
au dossier `local`, d'activer l'environnement, puis de lancer Streamlit :

```bash
cd ~/Documents/transcription-main/local
conda activate transcription
python -m streamlit run streamlit_app.py
```

Si le depot a ete telecharge avec Git :

```bash
cd ~/Documents/transcription/local
conda activate transcription
python -m streamlit run streamlit_app.py
```

## Installation sans Conda

Cette option convient seulement si Python 3.12 est deja installe sur
l'ordinateur.

```bash
cd ~/Documents/transcription-main/local
python3.12 -m venv .venv
source .venv/bin/activate
python --version
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements-ui.txt
python -m pip install --index-url https://download.pytorch.org/whl/cpu "torch>=2.8,<3" "torchaudio>=2.8,<3"
python -m pip install --resume-retries 20 -r requirements-local.txt
python -m streamlit run streamlit_app.py
```

## Token Hugging Face pour la diarisation

La diarisation sert a separer les locuteurs. Elle utilise un modele pyannote qui
doit etre telecharge une premiere fois depuis Hugging Face.

Etapes :

1. creer ou ouvrir un compte sur <https://huggingface.co/> ;
2. accepter les conditions du modele
   <https://huggingface.co/pyannote/speaker-diarization-community-1> ;
3. aller dans <https://huggingface.co/settings/tokens> ;
4. creer un token de type `Read` ;
5. copier ce token dans le champ `Token Hugging Face` de l'interface Streamlit.

Le token sert a autoriser le telechargement du modele. Il ne sert pas a envoyer
l'audio a Hugging Face.

Si l'on veut seulement transcrire sans distinguer les locuteurs, il suffit de
decocher `Distinguer les locuteurs` dans l'interface. Dans ce cas, aucun token
n'est necessaire.

## Utilisation dans l'interface

Dans la page Streamlit :

1. deposer le fichier audio ;
2. laisser `Distinguer les locuteurs` coche si l'on veut la diarisation ;
3. indiquer le nombre de locuteurs attendus ;
4. sur un ordinateur ordinaire, choisir plutot `cpu`, `small`, `int8` et une
   taille de lot de `4` ;
5. cliquer sur `Lancer la transcription` ;
6. telecharger le fichier TXT, SRT ou JSON.

L'adresse locale est generalement :

```text
http://localhost:8501
```

Le navigateur affiche seulement l'interface. Les fichiers restent dans les
dossiers locaux `audio/` et `outputs/`.

## Utilisation en ligne de commande

L'interface Streamlit est conseillee pour les etudiant.es. La ligne de commande
reste disponible si besoin.

Pour un entretien a deux personnes :

```bash
mkdir -p audio outputs
python local_transcribe.py audio/entretien_01.m4a --num-speakers 2
```

Pour un entretien a trois personnes :

```bash
python local_transcribe.py audio/entretien_01.m4a --num-speakers 3
```

Pour transcrire sans diarisation :

```bash
python local_transcribe.py audio/entretien_01.m4a --no-diarization
```

Pour forcer un reglage leger sur CPU :

```bash
python local_transcribe.py audio/entretien_01.m4a --device cpu --model small --compute-type int8 --batch-size 4
```

## Apres la transcription

1. Ouvrir le fichier TXT.
2. Reecouter l'audio en suivant les horodatages.
3. Corriger les mots mal reconnus, les coupes de phrases et les changements de
   locuteur.
4. Conserver separement le JSON brut et la transcription corrigee.
5. Anonymiser les noms propres si l'entretien doit etre partage ou analyse hors
   de l'espace de travail prevu.

## Problemes frequents

| Message ou situation | Que faire |
| --- | --- |
| `No module named streamlit` | Activer l'environnement avec `conda activate transcription`, puis lancer `python -m pip install -r requirements-ui.txt`. |
| `Module absent : torch` | L'interface est installee, mais pas le moteur. Installer `torch`, `torchaudio`, puis `requirements-local.txt`. |
| `Could not find a version that satisfies the requirement torch==2.8.0` | Ancienne consigne ou Python trop recent. Repartir avec l'environnement Conda en Python 3.12 et utiliser la commande non figee `"torch>=2.8,<3"`. |
| `Could not find ... whisperx==3.8.6` | Verifier que `python --version` affiche bien Python 3.12 et que l'installation de `requirements-local.txt` n'est pas lancee avec l'index PyTorch. |
| `partially initialized module 'torchvision' has no attribute 'extension'` | `torchvision` est inutile ici et peut etre incompatible. Lancer `python -m pip uninstall -y torchvision`, puis relancer Streamlit. |
| `ffmpeg not found` | Installer `ffmpeg`, puis rouvrir le terminal. |
| `HF_TOKEN absent` | Coller le token Hugging Face dans l'interface, ou decocher `Distinguer les locuteurs`. |
| Acces pyannote refuse | Accepter les conditions du modele pyannote avec le meme compte Hugging Face que celui du token. |
| Transcription tres lente | C'est normal sur CPU pour un entretien long. Tester d'abord un court extrait et choisir `small`, `int8`, taille de lot `4`. |

## Recommencer proprement

Si l'environnement est trop abime, on peut le supprimer puis le recreer :

```bash
conda deactivate
conda env remove -n transcription
conda create -n transcription python=3.12 -y
conda activate transcription
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements-ui.txt
python -m pip install --index-url https://download.pytorch.org/whl/cpu "torch>=2.8,<3" "torchaudio>=2.8,<3"
python -m pip install --resume-retries 20 -r requirements-local.txt
python -m streamlit run streamlit_app.py
```

## Donnees personnelles

Les fichiers audio et les transcriptions peuvent contenir des donnees
personnelles. Ne pas deposer dans GitHub :

- les fichiers audio ;
- les sorties de transcription ;
- le fichier `.env` ;
- les tokens Hugging Face.

Les dossiers `audio/` et `outputs/` sont ignores par Git.
