# AutoTranscript — Google Colab

Ce dossier permet de transcrire un fichier audio dans **Google Colab** avec :

- **WhisperX 3.8.6** (`medium` par défaut) ;
- alignement temporel ;
- **pyannote.audio 4.0.7** et `speaker-diarization-community-1` ;
- nombre exact de locuteurs configurable (3 par défaut) ;
- sorties **JSON**, **TXT horodaté** et **SRT** ;
- conservation de l'audio et des résultats dans **Google Drive**.

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

## Utilisation

Le notebook suit une procédure linéaire :

1. installation des versions figées ;
2. redémarrage automatique du runtime ;
3. vérification GPU + token ;
4. montage de Google Drive ;
5. sélection de l'audio depuis Drive ;
6. réglages (`medium`, français, 3 locuteurs par défaut) ;
7. test facultatif de 3 minutes ;
8. transcription complète vers Drive ;
9. génération du TXT horodaté de recherche ;
10. création optionnelle d'un ZIP dans Drive.

Une fois le test de 3 minutes validé, il n'est pas nécessaire de le refaire après
chaque reset : après réinstallation, on peut reprendre directement la
transcription complète.

## En cas de déconnexion Colab

- Si Colab se reconnecte au même runtime, reprendre simplement l'exécution.
- Si le runtime est réellement réinitialisé, les paquets doivent être
  réinstallés : relancer les cellules 1 à 5 puis passer directement à la
  transcription complète.
- L'audio reste dans Drive et n'a pas besoin d'être retéléversé.
- Les résultats déjà terminés restent dans Drive.
- Si le runtime est détruit **pendant** une transcription, l'exécution en cours
  est interrompue et doit être relancée.

## Versions figées

Voir `requirements-colab.txt`. WhisperX 3.8.6 requiert Python 3.10–3.13,
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

