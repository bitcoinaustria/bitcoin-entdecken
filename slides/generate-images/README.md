# generate-images — AI-Bildgenerierung für die Präsentationen

Erzeugt Folienbilder über **Replicate.com** oder **fal.ai** (u. a. Google Imagen4). Läuft mit `uv`, aufgerufen vom `slides/`-Verzeichnis aus:

```bash
uv --directory generate-images run generate_image.py [options] "prompt"
```

**API-Keys** (Umgebungsvariablen): `REPLICATE_API` für Replicate, `FAL_AI` für fal.ai.

## Beispiele

```bash
# Standard (Replicate, flux-krea-dev)
uv --directory generate-images run generate_image.py "cybercriminal with bitcoin symbols"

# Google Imagen4 via fal.ai
uv --directory generate-images run generate_image.py -m imagen4 "bitcoin logo in cyberpunk style"

# Provider erzwingen
uv --directory generate-images run generate_image.py -p fal -m imagen4 "crypto hacker scene"

# Alle Modelle beider Provider auflisten
uv --directory generate-images run generate_image.py --list-models

# Folienbild direkt ersetzen (M8 = Kriminalität)
uv --directory generate-images run generate_image.py -m imagen4 -r M8 -n kriminalitaet-neu "cybercriminal silhouette"

# Mehrere Bilder (fal.ai, 1–4)
uv --directory generate-images run generate_image.py -m imagen4 --num-images 3 "bitcoin mining facility"

# Negative Prompts (nur fal.ai) und reproduzierbarer Seed
uv --directory generate-images run generate_image.py -m imagen4 --negative-prompt "ugly, blurry" --seed 42 "clean bitcoin symbol"

# Bildbearbeitung mit flux-kontext-pro (Input-Bild nötig, mit Auto-Replace)
uv --directory generate-images run generate_image.py -m flux-kontext-pro -i pix/existing.jpg -r M8 -y "make more abstract"
```

## Modelle

- **Replicate:** flux-krea-dev (Default), flux-kontext-pro (braucht Input-Bild), flux-pro, flux-dev, sdxl
- **fal.ai:** imagen4, imagen4-turbo
- `-p auto` (Default) wählt den Provider passend zum Modell.

## Metadaten

Jedes generierte Bild bekommt eine gleichnamige JSON-Datei (`generated-<timestamp>.json`) mit Prompt, Provider/Modell, allen Parametern (Aspect Ratio, Seed, Negative Prompt), ggf. Folien-Ersetzung und Input-Bild. Bild + JSON gehören zusammen committet.
