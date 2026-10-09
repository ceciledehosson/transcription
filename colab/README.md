# AutoTranscript - Google Colab

Ce dossier permet de transcrire un fichier audio dans **Google Colab** avec :

- **WhisperX 3.8.6** (`small` par défaut pour privilégier la stabilité) ;
- alignement temporel ;
- **pyannote.audio 4.0.7** et `speaker-diarization-community-1` ;
- nombre exact de locuteurs configurable (3 par défaut) ;
- sorties **JSON**, **TXT horodaté** et **SRT** ;
- conservation de l'audio et des résultats dans **Google Drive**.

Le modèle `medium` peut être utilisé après un test réussi, mais `small` est le
réglage conseillé pour démarrer, notamment avec des entretiens longs.

## Ouvrir directement dans Google Colab

[**Ouvrir AutoTranscript dans Google Colab**](https://colab.research.google.com/github/ceciledehosson/transcription/blob/main/colab/autotranscript_colab.ipynb)

Le notebook source est disponible ici : [`autotranscript_colab.ipynb`](autotranscript_colab.ipynb).

## Prérequis, une seule fois

1. Avoir un compte Hugging Face.
2. Ouvrir `pyannote/speaker-diarization-community-1` et accepter les conditions d'accès.
3. Créer un token Hugging Face en lecture. Un token *fine-grained* convient s'il peut lire les dépôts publics restreints auxquels le compte a accès.
4. Dans Colab, ajouter ce token dans **Secrets** sous le nom exact `HF_TOKEN` et autoriser le notebook à y accéder.

Ne jamais inscrire le token directement dans une cellule ou dans GitHub.

## Stockage persistant dans Google Drive

Le notebook monte Google Drive puis crée automatiquement :

- `Mon Drive/AutoTranscript/audio` pour les fichiers audio ;
- `Mon Drive/AutoTranscript/results` pour les sorties de transcription.

Déposer l'audio dans `AutoTranscript/audio` permet de le retrouver après un
reset du runtime sans nouvel upload. Les sorties complètes sont écrites
directement dans Drive.

Formats audio acceptés par le notebook : `.mp3`, `.wav`, `.m4a`, `.aac`,
`.flac`, `.ogg`, `.wma`.

## Utilisation

Le notebook suit une procédure linéaire :

1. installation des versions figées ;
2. redémarrage du runtime seulement si Colab le demande ;
3. vérification GPU + token ;
4. montage de Google Drive ;
5. sélection de l'audio depuis Drive ;
6. réglages (`small`, français, 3 locuteurs, batch 4 par défaut) ;
7. test facultatif de 3 minutes ;
8. transcription complète vers Drive ;
9. génération du TXT horodaté de recherche ;
10. création optionnelle d'un ZIP dans Drive.

Une fois le test de 3 minutes validé, il n'est pas nécessaire de le refaire après
chaque reset : après réinstallation éventuelle, on peut reprendre directement la
transcription complète.

## Fichiers audio longs

Pour un entretien long, conserver d'abord les réglages prudents du notebook :

```python
MODEL = "small"
BATCH_SIZE = 4
```

Si Colab se déconnecte pendant la transcription, relancer les cellules 2 à 5,
puis relancer la transcription complète. L'audio et les résultats déjà écrits
restent dans Google Drive.

Si un fichier audio est vraiment trop long pour passer en une fois, le plus sûr
est de le découper en plusieurs fichiers audio, puis de traiter chaque partie
séparément. Exemple depuis Colab ou un terminal disposant de `ffmpeg` :

```bash
ffmpeg -i entretien.m4a -f segment -segment_time 2700 -ar 16000 -ac 1 entretien_%03d.wav
```

`2700` correspond à 45 minutes. Les étiquettes de locuteurs devront alors être
vérifiées partie par partie, car la diarisation reclasse les locuteurs à chaque
fichier.

## En cas de déconnexion Colab

- Si Colab se reconnecte au même runtime, reprendre simplement l'exécution.
- Si le runtime est réellement réinitialisé, les paquets doivent être
  réinstallés : relancer la cellule 1 si nécessaire, puis les cellules 2 à 5 et
  enfin la transcription complète.
- L'audio reste dans Drive et n'a pas besoin d'être retéléversé.
- Les résultats déjà terminés restent dans Drive.
- Si le runtime est détruit **pendant** une transcription, l'exécution en cours
  est interrompue et doit être relancée.

## Versions figées

Voir `requirements-colab.txt`. WhisperX 3.8.6 requiert Python 3.10-3.13,
`torch ~= 2.8.0`, `pyannote-audio >= 4.0.0` et `huggingface-hub < 1.0.0`.
NumPy est fixé à 2.2.6 pour rester compatible avec l'environnement Colab testé.

## Sorties

WhisperX produit les sorties standard dans
`AutoTranscript/results/<nom_du_fichier>/`. Le notebook ajoute un fichier de
travail :

`Locuteur 1 [HH:MM:SS - HH:MM:SS] : ...`

Les noms `Locuteur 1`, `Locuteur 2`, etc. sont attribués selon l'ordre de
première apparition des clusters pyannote ; ils ne constituent pas une
identification de personne.

## Limites

La diarisation n'est pas parfaite, notamment en cas de chevauchement de parole.
La transcription destinée à l'analyse de recherche doit donc être relue/corrigée
à partir de l'audio. Le JSON brut doit être conservé séparément de la
transcription corrigée.
