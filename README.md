# ReadCube Papers Skill

An **agent skill** for AI coding assistants (e.g., [Antigravity](https://blog.google/technology/google-deepmind/gemini-agent-antigravity/), [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview)) that provides access to [ReadCube Papers](https://www.papersapp.com/) libraries via an unofficial API.

This skill enables AI agents to retrieve paper metadata, annotations, and references from a user's ReadCube Papers library during conversations — useful for literature reviews, citation management, and manuscript preparation.

> **⚠️ Disclaimer**: This skill uses an unofficial API reverse-engineered from the ReadCube Papers web application. It is not affiliated with or endorsed by ReadCube/Digital Science. The API may change without notice, potentially breaking this tool.

## What is an Agent Skill?

Agent skills are modular packages that extend the capabilities of AI coding agents. When installed in the `~/.agents/skills/` directory, the agent automatically detects and uses the skill based on user requests. For example, asking _"search my ReadCube library for papers about CRISPR"_ will trigger this skill.

### Installation

```bash
# Clone into the skills directory
git clone https://github.com/YusukeKimata-Moo/readcube-papers-skill.git ~/.agents/skills/readcube-papers
```

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

Once installed and environment variables are set, simply ask your AI agent in natural language. The skill is triggered automatically.

### Example Prompts

**Browsing your library:**

- _"List all papers in my ReadCube library"_
- _"Show my ReadCube collections"_

**Searching papers:**

- _"Search my ReadCube library for papers about CRISPR-Cas9"_
- _"Find papers by Zhang in my library"_
- _"Look up papers published in Nature in 2024 from my ReadCube"_
- _"Search my library for papers related to single-cell RNA-seq"_

**Retrieving details:**

- _"Get the abstract and DOI of the paper about genome editing in my library"_
- _"Show my annotations and highlights for that paper"_

**Manuscript support:**

- _"Find references in my ReadCube about protein localization for the Introduction section"_
- _"List all papers tagged 'review' in my library"_

### CLI Reference

The agent calls the script internally, but you can also use it directly:

```bash
python scripts/readcube_papers.py login                          # Test login
python scripts/readcube_papers.py collections                    # List collections
python scripts/readcube_papers.py list                           # List all papers (JSON)
python scripts/readcube_papers.py --format markdown list         # List all papers (Markdown)
python scripts/readcube_papers.py search "apoptosis"             # Search all fields
python scripts/readcube_papers.py search "Tanaka" --field authors # Search by author
python scripts/readcube_papers.py get <item_id>                  # Get paper details
python scripts/readcube_papers.py annotations <item_id>          # Get annotations
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

