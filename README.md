# Transcription d'entretiens audio

Ce dépôt regroupe deux façons de produire une première transcription automatique
d'un entretien audio :

- `colab/` : utilisation dans Google Colab, avec GPU et stockage dans Google
  Drive ;
- `local/` : utilisation locale sur ordinateur, avec une interface graphique
  Streamlit et une ligne de commande.

Dans les deux cas, la transcription automatique doit être relue et corrigée à
partir de l'audio. Les étiquettes de locuteurs produites par la diarisation
doivent aussi être vérifiées.

## Choisir une méthode

| Situation | Méthode conseillée |
| --- | --- |
| Ordinateur peu puissant ou installation locale difficile | Google Colab |
| Étudiantes et étudiants sous Windows ou macOS | Local avec Streamlit, procédure Conda |
| Données à garder sur l'ordinateur personnel | Local avec Streamlit |
| Utilisateur à l'aise avec le terminal | Local en ligne de commande |

## Utilisation locale avec Streamlit

La procédure détaillée pour **Windows**, **macOS** et **Linux** est dans
[`local/README.md`](local/README.md).

Point important : l'installation locale est conseillée avec un environnement
séparé en **Python 3.12**. Python 3.13 ou 3.14 peut provoquer des erreurs avec
WhisperX, PyTorch ou pyannote.

Le principe général est :

1. télécharger le dépôt ;
2. ouvrir Miniforge Prompt, Anaconda Prompt ou Terminal ;
3. créer un environnement Conda `transcription` en Python 3.12 ;
4. installer `ffmpeg` dans cet environnement ;
5. installer Streamlit ;
6. installer le moteur de transcription adapté au système ;
7. lancer `python -m streamlit run streamlit_app.py`.

Pour distinguer les locuteurs, il faut aussi un token Hugging Face. Sans
diarisation, aucun token n'est nécessaire.

## Utilisation dans Google Colab

Le notebook se trouve dans [`colab/autotranscript_colab.ipynb`](colab/autotranscript_colab.ipynb).

Il peut être ouvert directement avec :

[Ouvrir AutoTranscript dans Google Colab](https://colab.research.google.com/github/ceciledehosson/transcription/blob/main/colab/autotranscript_colab.ipynb)

La procédure détaillée est dans [`colab/README.md`](colab/README.md).

## Données personnelles

Les fichiers audio et les transcriptions peuvent contenir des données
personnelles. Ne pas déposer dans GitHub :

- les fichiers audio ;
- les sorties de transcription ;
- les tokens Hugging Face ;
- les fichiers `.env`.

Les dossiers `audio/` et `outputs/` sont ignorés par Git.
