# Editierbare Eventvorlagen

Die Vorlagen erzeugen Social-Media-Dateien und druckfertige PDFs aus einem gemeinsamen Eventdatensatz. Datum, Uhrzeit, Ort und Anmeldelink müssen dadurch nur einmal geändert werden.

## Enthaltene Formate

| Datei | Varianten |
|---|---|
| `src/layouts/social.html` | Vorderseite, Rückseite, schwarz und orange |
| `src/layouts/poster-a3.html` | finales Eventposter, zwei Alternativen |
| `src/layouts/poster-general-a3.html` | „Geht’s sich no aus?“ und „21 Millionen“ |
| `src/layouts/flyer-a5.html` | Bankenrettung, Semmel und alternative Vorderseiten |
| `src/layouts/bauzaun.html` | Hauptmotiv und Bildvariante in 340 × 165 cm |

Der frühere Claude-Canvas und ältere Dubletten sind nicht Teil der editierbaren Quelle. Ihre eigenständigen Gestaltungsvarianten wurden in die obigen Dateien übernommen.

## Voraussetzungen

- Node.js 20 oder neuer
- pnpm
- Chromium, Chrome oder Brave
- Poppler (`pdfinfo`, `pdfimages` und `pdftoppm`)

```bash
cd templates/events
pnpm install
```

Unter macOS findet der Export Brave und Google Chrome automatisch. In anderen Umgebungen kann `BROWSER_PATH` auf einen Chromium-Browser zeigen; Playwrights eigener Browser funktioniert ebenfalls.

## Event ändern oder anlegen

Einen vorhandenen Datensatz unter `src/events/` kopieren und alle Angaben aktualisieren:

```json
{
  "id": "ort-2026-09-12",
  "date": "2026-09-12",
  "start": "17:00",
  "end": "19:00",
  "venue": "Veranstaltungsort",
  "address": "Straße 1",
  "postalCode": "8010",
  "city": "Graz",
  "region": "Steiermark",
  "registrationUrl": "https://example.org/anmeldung",
  "summary": "Kurzer Veranstaltungstext",
  "outputs": []
}
```

`outputs` legt fest, welche Layoutseiten gemeinsam in welche Datei exportiert werden. Die bestehenden Datensätze zeigen alle unterstützten Ausgabetypen. Der QR-Code wird immer aus `registrationUrl` erzeugt.

Unvollständige Daten erhalten die Endung `.entwurf.json`. Sie werden von Prüfung und Export bewusst ignoriert.

## Prüfen und exportieren

```bash
pnpm check
pnpm export:event -- voitsberg-2026-08-28
pnpm export:event -- poertschach-2026-08-21
pnpm export:event -- allgemein
pnpm export:event -- --all
```

Fertige Dateien liegen danach unter `exports/<event-id>/`. Nicht mehr konfigurierte Dateien im jeweiligen Eventordner werden beim Export entfernt. PDF-Ausgaben werden auf Seitenzahl, randlose Außenkanten und eine formatabhängige Mindestauflösung der Rasterbilder geprüft; das Poster-PNG entsteht mit 300 DPI aus dem geprüften PDF. Text, Logos und QR-Codes bleiben in den PDFs Vektoren.

Beim 340 × 165 cm großen Bauzaun erreicht das vorhandene Semmelbild in der aktuellen Größe rund 21 PPI; der Export verhindert mit einer Untergrenze von 20 PPI eine weitere unbemerkte Verschlechterung. Für etwa 50 PPI wäre eine echte Bildquelle mit ungefähr 2500 × 3750 Pixeln nötig. Bloßes Hochskalieren erzeugt keine zusätzlichen Details.

## Wo wird was geändert?

- Termin, Ort, Anmeldelink, Kurztext: `src/events/*.json`
- Text oder Aufbau einer Kampagne: `src/layouts/*.html`
- Markenweite Maße, Fonts und Druckverhalten: `src/shared.css`
- Ausgabeverfahren und Prüfungen: `export.mjs`
- Semmel- und Zeitungsbild: `src/assets/`
- Logos: kanonisch unter [`brand-assets/logo`](../../brand-assets/logo/)
