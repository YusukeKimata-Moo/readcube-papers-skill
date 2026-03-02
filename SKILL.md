---
name: readcube-papers
description: >-
  Access ReadCube Papers library to retrieve paper metadata, annotations, and references.
  Use when the user requests: fetching papers from ReadCube Papers library, searching references
  by title/author/DOI/keyword, retrieving paper annotations or highlights, listing paper
  collections, or exporting reference information. Triggers on mentions of "ReadCube",
  "Papers", "paper library", or requests to look up references from the user's library.
---

# ReadCube Papers

Access the user's ReadCube Papers library via unofficial API.

> **Note**: This uses an unofficial API reverse-engineered from the ReadCube Papers web app. It may break if ReadCube changes their API.

## Authentication

Credentials are provided via environment variables:

- `READCUBE_EMAIL` - ReadCube account email
- `READCUBE_PASSWORD` - ReadCube account password

The user must set these before using this skill. On Windows PowerShell:

```powershell
$env:READCUBE_EMAIL = "user@example.com"
$env:READCUBE_PASSWORD = "password"
```

## Script Usage

The script is at `scripts/readcube_papers.py`. It requires no external dependencies (uses only `urllib`).

### Commands

```bash
# Test login
python scripts/readcube_papers.py login

# List collections
python scripts/readcube_papers.py collections

# List all papers (JSON)
python scripts/readcube_papers.py list

# List all papers (Markdown, verbose)
python scripts/readcube_papers.py --format markdown list --verbose

# Get specific paper details
python scripts/readcube_papers.py get <item_id>

# Get annotations for a paper
python scripts/readcube_papers.py annotations <item_id>

# Search papers
python scripts/readcube_papers.py search "keyword"
python scripts/readcube_papers.py search "Smith" --field authors
python scripts/readcube_papers.py search "10.1234/example" --field doi
python scripts/readcube_papers.py --format markdown search "vacuole" --field title --verbose
```

### Output Formats

- `--format json` (default): Structured JSON output for programmatic use
- `--format markdown`: Human-readable markdown with paper metadata

### Typical Workflow

1. Run `list` to get all papers and their IDs
2. Use `get <item_id>` to retrieve detailed info for a specific paper
3. Use `annotations <item_id>` to get highlights and notes
4. Use `search` to filter papers by keyword across fields

### Available Fields per Paper

| Field            | Description               |
| ---------------- | ------------------------- |
| `title`          | Paper title               |
| `authors`        | Author list               |
| `year`           | Publication year          |
| `journal`        | Journal name              |
| `journal_abbrev` | Abbreviated journal name  |
| `doi`            | Digital Object Identifier |
| `abstract`       | Paper abstract            |
| `volume`         | Journal volume            |
| `pagination`     | Page numbers              |
| `url`            | Paper URL                 |
| `tags`           | User-assigned tags        |
| `rating`         | User rating               |
| `notes`          | User notes                |

### Annotation Fields

| Field      | Description                                                  |
| ---------- | ------------------------------------------------------------ |
| `text`     | Highlighted text                                             |
| `note`     | User's note on the highlight                                 |
| `page`     | Page number                                                  |
| `color_id` | Highlight color (0=Yellow, 1=Red, 2=Green, 3=Blue, 4=Purple) |
| `type`     | Annotation type                                              |
