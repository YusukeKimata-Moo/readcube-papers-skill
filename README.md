# ReadCube Papers Skill

An unofficial API client for [ReadCube Papers](https://www.papersapp.com/) that retrieves paper metadata, annotations, and references from your personal library.

> **⚠️ Disclaimer**: This skill uses an unofficial API reverse-engineered from the ReadCube Papers web application. It is not affiliated with or endorsed by ReadCube/Digital Science. The API may change without notice, potentially breaking this tool.

## Features

- 🔐 **Email/password authentication** — No manual cookie extraction required
- 📚 **Library browsing** — List all papers in your collections
- 🔍 **Search** — Filter papers by title, authors, DOI, journal, year, tags, or abstract
- 📝 **Annotations** — Retrieve highlights and notes from PDFs
- 📄 **Multiple output formats** — JSON or Markdown

## Requirements

- Python 3.7+
- No external dependencies (uses only Python standard library)

## Setup

### 1. Set Environment Variables

**Windows (PowerShell) — Persistent:**

```powershell
[System.Environment]::SetEnvironmentVariable("READCUBE_EMAIL", "your@email.com", "User")
[System.Environment]::SetEnvironmentVariable("READCUBE_PASSWORD", "yourpassword", "User")
```

**Windows (PowerShell) — Session only:**

```powershell
$env:READCUBE_EMAIL = "your@email.com"
$env:READCUBE_PASSWORD = "yourpassword"
```

**macOS/Linux:**

```bash
export READCUBE_EMAIL="your@email.com"
export READCUBE_PASSWORD="yourpassword"
```

### 2. Test Login

```bash
python scripts/readcube_papers.py login
# Output: Login successful!
```

## Usage

### List Collections

```bash
python scripts/readcube_papers.py collections
```

### List All Papers

```bash
# JSON output (default)
python scripts/readcube_papers.py list

# Markdown output with abstracts, tags, and notes
python scripts/readcube_papers.py --format markdown list --verbose
```

### Get Paper Details

```bash
python scripts/readcube_papers.py get <item_id>
python scripts/readcube_papers.py --format markdown get <item_id>
```

### Get Annotations

```bash
python scripts/readcube_papers.py annotations <item_id>
python scripts/readcube_papers.py --format markdown annotations <item_id>
```

### Search Papers

```bash
# Search all fields
python scripts/readcube_papers.py search "vacuole"

# Search specific field
python scripts/readcube_papers.py search "Smith" --field authors
python scripts/readcube_papers.py search "10.1073/pnas.1814160116" --field doi
python scripts/readcube_papers.py search "2024" --field year

# Markdown output with details
python scripts/readcube_papers.py --format markdown search "zygote" --field title --verbose
```

### CLI Options

You can also pass credentials directly instead of using environment variables:

```bash
python scripts/readcube_papers.py --email your@email.com --password yourpass list
```

## Available Paper Fields

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

## API Endpoints Used

| Endpoint                                                    | Method | Purpose                 |
| ----------------------------------------------------------- | ------ | ----------------------- |
| `services.readcube.com/authentication/login`                | POST   | Authentication          |
| `sync.readcube.com/collections/`                            | GET    | List collections        |
| `sync.readcube.com/collections/{id}/items`                  | GET    | List papers (paginated) |
| `sync.readcube.com/collections/{id}/items/{id}`             | GET    | Paper details           |
| `sync.readcube.com/collections/{id}/items/{id}/annotations` | GET    | Annotations             |

## Acknowledgments

API endpoint information was referenced from the [Joplin ReadCube Papers plugin](https://github.com/SeptemberHX/joplin-plugin-readcube-papers) by SeptemberHX and the accompanying [API documentation](https://blog.hxgpark.com/posts/ReadCubePapersAPI/).

## License

MIT
