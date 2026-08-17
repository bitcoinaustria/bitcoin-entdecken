# AGENTS.md — Eventvorlagen

Diese Regeln gelten für die editierbaren Social- und Druckvorlagen in diesem Ordner. Die Bedienung und der Vorlagenkatalog stehen in [README.md](README.md).

## Quellen und Ausgaben

- Änderliche Veranstaltungsdaten gehören ausschließlich in `src/events/*.json`, damit Datum, Ort und QR-Ziel in allen Formaten übereinstimmen.
- Layoutdateien enthalten keine konkreten Termine oder Veranstaltungsorte. Kampagnentexte und Gestaltung bleiben dagegen im jeweiligen HTML-Layout.
- `exports/` wird ausschließlich durch `pnpm export:event -- <event-id>` erzeugt. Generierte JPEG-, PNG- und PDF-Dateien nicht manuell bearbeiten.
- Neue Ausgabedateien tragen die Event-ID im Ordnernamen. Dadurch bleiben frühere Termine erhalten und Vorschauen werden nicht aus veralteten Dateicaches geladen.

## Gestaltung

- Farben und Logos kommen aus dem Root-[README](../../README.md) und `brand-assets/`; keine neuen Markenregeln erfinden.
- Poppins Regular, Bold und Black liegen für reproduzierbare Offline-Exporte unter `src/assets/fonts/`.
- Druckseiten bleiben randlos. Die kleine vertikale Überfüllung in `shared.css` verhindert weiße Rundungskanten im Chromium-PDF und darf nur nach einem Außenrandtest geändert werden.
- Unvollständige Termine bleiben `*.entwurf.json`; Platzhalter wie `XX:00` dürfen nie exportierbar sein.

## Qualitätsprüfung

```bash
pnpm install
pnpm check
pnpm export:event -- voitsberg-2026-08-28
```

Der Export prüft Datensätze, Platzhalter, Seitenzahlen, Poppins-Ladung, Rasterbildauflösung und die Außenkanten aller nicht weißen PDF-Seiten. Für PDF/PNG-Prüfungen werden `pdfinfo`, `pdfimages` und `pdftoppm` aus Poppler benötigt.
