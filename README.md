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
| Ordinateur peu puissant ou sans installation locale possible | Google Colab |
| Besoin d'une interface simple avec boutons | Local avec Streamlit |
| Données à garder sur l'ordinateur personnel | Local avec Streamlit |
| Utilisateur à l'aise avec le terminal | Local en ligne de commande |

## Utilisation locale avec Streamlit

Depuis la racine du dépôt :

```bash
cd local
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-local.txt
python -m streamlit run streamlit_app.py
```

Sous Windows PowerShell, remplacer l'activation de l'environnement par :

```powershell
.\.venv\Scripts\Activate.ps1
```

L'interface s'ouvre ensuite dans le navigateur, généralement à l'adresse :

```text
http://localhost:8501
```

La procédure détaillée est dans [`local/README.md`](local/README.md).

Si l'installation échoue sur un gros paquet NVIDIA/CUDA, voir la procédure CPU
dans [`local/README.md`](local/README.md).

## Utilisation dans Google Colab

Le notebook se trouve dans [`colab/autotranscript_colab.ipynb`](colab/autotranscript_colab.ipynb).

Une fois le dépôt créé sur GitHub, il pourra être ouvert directement avec :

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

