# AutoTranscript - utilisation locale

Cette procédure permet de transcrire localement un entretien audio avec
**WhisperX** et, si souhaité, de distinguer les locuteurs avec **pyannote.audio**.
Elle s'adresse à des étudiantes et étudiants qui doivent obtenir une première
transcription de travail à partir d'un entretien enregistré.

La transcription automatique doit toujours être relue et corrigée à partir de
l'audio. Les étiquettes `Locuteur 1`, `Locuteur 2`, etc. ne sont pas une
identification certaine des personnes.

## À lire avant de commencer

L'installation locale dépend du système utilisé. La méthode conseillée pour les
étudiantes et étudiants est la même sur **Windows**, **macOS** et **Linux** :
utiliser Conda avec un environnement séparé en **Python 3.12**.

À retenir :

- ne pas utiliser Python 3.13 ou 3.14 pour cette installation ;
- installer d'abord l'interface Streamlit ;
- installer ensuite le moteur de transcription ;
- pour distinguer les locuteurs, il faut un token Hugging Face ;
- sans diarisation, le token Hugging Face n'est pas nécessaire ;
- les fichiers audio restent dans le dossier local `audio/` ;
- les résultats restent dans le dossier local `outputs/`.

## Ce que produit l'outil

Pour un fichier `entretien_01.m4a`, l'outil crée dans `outputs/` :

- `entretien_01_transcript.txt` : texte horodaté, le plus pratique pour relire ;
- `entretien_01_transcript.srt` : sous-titres ;
- `entretien_01_transcript.json` : sortie structurée à conserver.

## Étape 1 - Installer Conda si nécessaire

Si Miniforge, Miniconda ou Anaconda est déjà installé, passer directement à
l'étape suivante.

Sinon, installer **Miniforge** :

- Windows : télécharger l'installateur Windows depuis
  <https://github.com/conda-forge/miniforge/releases>, puis lancer le fichier
  `.exe` ;
- macOS : télécharger l'installateur macOS depuis
  <https://github.com/conda-forge/miniforge/releases> ; choisir `arm64` pour les
  Mac récents Apple Silicon, et `x86_64` pour les Mac Intel ;
- Linux : installer Miniforge ou utiliser l'installation Conda déjà disponible.

Après installation :

- sous Windows, ouvrir **Miniforge Prompt** ou **Anaconda Prompt** ;
- sous macOS, ouvrir **Terminal** ;
- sous Linux, ouvrir le terminal habituel.

## Étape 2 - Télécharger le dépôt

Méthode simple, sans Git :

1. aller sur <https://github.com/ceciledehosson/transcription> ;
2. cliquer sur le bouton vert `Code` ;
3. cliquer sur `Download ZIP` ;
4. extraire le fichier ZIP dans `Documents`.

Le dossier obtenu s'appelle en général `transcription-main`.

Méthode avec Git, si Git est installé :

Windows, dans Miniforge Prompt ou Anaconda Prompt :

```bat
cd %USERPROFILE%\Documents
git clone https://github.com/ceciledehosson/transcription.git
cd transcription\local
```

macOS ou Linux :

```bash
cd ~/Documents
git clone https://github.com/ceciledehosson/transcription.git
cd transcription/local
```

## Étape 3 - Aller dans le bon dossier

Si le dépôt a été téléchargé en ZIP :

Windows, dans Miniforge Prompt ou Anaconda Prompt :

```bat
cd %USERPROFILE%\Documents\transcription-main\local
```

macOS ou Linux :

```bash
cd ~/Documents/transcription-main/local
```

Si le dossier n'a pas été extrait dans `Documents`, adapter seulement cette
partie du chemin.

## Étape 4 - Créer l'environnement Python

Les commandes suivantes sont identiques sur Windows, macOS et Linux :

```bash
conda create -n transcription python=3.12 -y
conda activate transcription
python --version
```

La dernière commande doit afficher `Python 3.12...`.

Installer ensuite `ffmpeg` dans le même environnement :

```bash
conda install -c conda-forge ffmpeg -y
ffmpeg -version
```

## Étape 5 - Installer et lancer l'interface

Toujours dans le dossier `local`, avec l'environnement `transcription` activé :

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements-ui.txt
python -m streamlit run streamlit_app.py
```

Une page doit s'ouvrir dans le navigateur, généralement à l'adresse :

```text
http://localhost:8501
```

À ce stade, l'interface peut encore afficher `Module absent : torch` au moment
de lancer la transcription. C'est normal tant que le moteur de transcription n'a
pas été installé.

Arrêter Streamlit avec `Ctrl+C` dans le terminal.

## Étape 6 - Installer le moteur de transcription

### Windows

```bash
python -m pip install --index-url https://download.pytorch.org/whl/cpu "torch>=2.8,<3" "torchaudio>=2.8,<3"
python -m pip install --resume-retries 20 -r requirements-local.txt
```

### macOS

```bash
python -m pip install "torch>=2.8,<3" "torchaudio>=2.8,<3"
python -m pip install --resume-retries 20 -r requirements-local.txt
```

### Linux

```bash
python -m pip install --index-url https://download.pytorch.org/whl/cpu "torch>=2.8,<3" "torchaudio>=2.8,<3"
python -m pip install --resume-retries 20 -r requirements-local.txt
```

Relancer ensuite l'interface :

```bash
python -m streamlit run streamlit_app.py
```

## Relancer l'outil plus tard

Les fois suivantes, il ne faut pas refaire l'installation.

Windows, si le dépôt vient du ZIP :

```bat
cd %USERPROFILE%\Documents\transcription-main\local
conda activate transcription
python -m streamlit run streamlit_app.py
```

Windows, si le dépôt vient de Git :

```bat
cd %USERPROFILE%\Documents\transcription\local
conda activate transcription
python -m streamlit run streamlit_app.py
```

macOS ou Linux, si le dépôt vient du ZIP :

```bash
cd ~/Documents/transcription-main/local
conda activate transcription
python -m streamlit run streamlit_app.py
```

macOS ou Linux, si le dépôt vient de Git :

```bash
cd ~/Documents/transcription/local
conda activate transcription
python -m streamlit run streamlit_app.py
```

## Token Hugging Face pour la diarisation

La diarisation sert à séparer les locuteurs. Elle utilise un modèle pyannote qui
doit être téléchargé une première fois depuis Hugging Face.

Étapes :

1. créer ou ouvrir un compte sur <https://huggingface.co/> ;
2. accepter les conditions du modèle
   <https://huggingface.co/pyannote/speaker-diarization-community-1> ;
3. aller dans <https://huggingface.co/settings/tokens> ;
4. créer un token de type `Read` ;
5. copier ce token dans le champ `Token Hugging Face` de l'interface Streamlit.

Le token sert à autoriser le téléchargement du modèle. Il ne sert pas à envoyer
l'audio à Hugging Face.

Si l'on veut seulement transcrire sans distinguer les locuteurs, il suffit de
décocher `Distinguer les locuteurs` dans l'interface. Dans ce cas, aucun token
n'est nécessaire.

## Utilisation dans l'interface

Dans la page Streamlit :

1. déposer le fichier audio ;
2. laisser `Distinguer les locuteurs` coché si l'on veut la diarisation ;
3. indiquer le nombre de locuteurs attendus ;
4. sur un ordinateur ordinaire, choisir plutôt `cpu`, `small`, `int8` et une
   taille de lot de `4` ;
5. cliquer sur `Lancer la transcription` ;
6. télécharger le fichier TXT, SRT ou JSON.

Le navigateur affiche seulement l'interface. Les fichiers restent dans les
dossiers locaux `audio/` et `outputs/`.

## Utilisation en ligne de commande

L'interface Streamlit est conseillée pour les étudiantes et étudiants. La ligne
de commande reste disponible si besoin.

Pour un entretien à deux personnes :

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

Pour forcer un réglage léger sur CPU :

```bash
python local_transcribe.py audio/entretien_01.m4a --device cpu --model small --compute-type int8 --batch-size 4
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

| Message ou situation | Que faire |
| --- | --- |
| `conda` n'est pas reconnu | Ouvrir Miniforge Prompt ou Anaconda Prompt sous Windows. Sous macOS, vérifier que Miniforge ou Anaconda est bien installé. |
| `No module named streamlit` | Activer l'environnement avec `conda activate transcription`, puis lancer `python -m pip install -r requirements-ui.txt`. |
| `Module absent : torch` | L'interface est installée, mais pas le moteur. Installer `torch`, `torchaudio`, puis `requirements-local.txt`, en suivant la section Windows, macOS ou Linux. |
| `Could not find a version that satisfies the requirement torch==2.8.0` | Ancienne consigne ou Python trop récent. Repartir avec l'environnement Conda en Python 3.12 et utiliser la commande non figée `"torch>=2.8,<3"`. |
| `Could not find ... whisperx==3.8.6` | Vérifier que `python --version` affiche bien Python 3.12 et que l'installation de `requirements-local.txt` n'est pas lancée avec l'index PyTorch. |
| `partially initialized module 'torchvision' has no attribute 'extension'` | `torchvision` est inutile ici et peut être incompatible. Lancer `python -m pip uninstall -y torchvision`, puis relancer Streamlit. |
| `ffmpeg not found` | Lancer `conda install -c conda-forge ffmpeg -y`, puis rouvrir le terminal si nécessaire. |
| `HF_TOKEN absent` | Coller le token Hugging Face dans l'interface, ou décocher `Distinguer les locuteurs`. |
| Accès pyannote refusé | Accepter les conditions du modèle pyannote avec le même compte Hugging Face que celui du token. |
| Transcription très lente | C'est normal sur CPU pour un entretien long. Tester d'abord un court extrait et choisir `small`, `int8`, taille de lot `4`. |

## Recommencer proprement

Si l'environnement est trop abîmé, on peut le supprimer puis le recréer :

```bash
conda deactivate
conda env remove -n transcription
conda create -n transcription python=3.12 -y
conda activate transcription
conda install -c conda-forge ffmpeg -y
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements-ui.txt
```

Puis reprendre à l'étape 6 avec la commande correspondant au système utilisé :
Windows, macOS ou Linux.

## Données personnelles

Les fichiers audio et les transcriptions peuvent contenir des données
personnelles. Ne pas déposer dans GitHub :

- les fichiers audio ;
- les sorties de transcription ;
- le fichier `.env` ;
- les tokens Hugging Face.

Les dossiers `audio/` et `outputs/` sont ignorés par Git.
