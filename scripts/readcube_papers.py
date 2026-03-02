#!/usr/bin/env python3
"""
ReadCube Papers API client.
Unofficial API for accessing ReadCube Papers library.
"""

import argparse
import json
import os
import sys
import re
import urllib.request
import urllib.parse
import urllib.error

# Fix encoding for Windows (cp932 cannot handle many Unicode chars)
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")


class ReadCubeClient:
    """Client for ReadCube Papers unofficial API."""

    LOGIN_URL = "https://services.readcube.com/authentication/login"
    SYNC_BASE = "https://sync.readcube.com"

    def __init__(self):
        self.cookie = None
        self.default_collection_id = None

    def login(self, email: str, password: str) -> bool:
        """Login with email/password and store cookie."""
        data = urllib.parse.urlencode({
            "client": "webapp",
            "api": "",
            "client_version": "",
            "email": email,
            "password": password,
        }).encode("utf-8")

        req = urllib.request.Request(self.LOGIN_URL, data=data, method="POST")
        try:
            with urllib.request.urlopen(req) as resp:
                # Extract cookies from response headers
                cookies = []
                for header in resp.headers.get_all("Set-Cookie") or []:
                    # Extract cookie name=value part (before ;)
                    cookie_part = header.split(";")[0].strip()
                    cookies.append(cookie_part)
                self.cookie = "; ".join(cookies)
                if self.cookie:
                    return True
                return False
        except urllib.error.HTTPError as e:
            print(f"Login failed: HTTP {e.code}", file=sys.stderr)
            return False
        except Exception as e:
            print(f"Login failed: {e}", file=sys.stderr)
            return False

    def _request(self, url: str) -> dict:
        """Make authenticated GET request."""
        if not self.cookie:
            raise RuntimeError("Not authenticated. Call login() first.")
        req = urllib.request.Request(url)
        req.add_header("Cookie", self.cookie)
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def get_collections(self) -> list:
        """Get all collections."""
        data = self._request(f"{self.SYNC_BASE}/collections/")
        if data.get("status") == "ok":
            return data.get("collections", [])
        return []

    def get_default_collection_id(self) -> str:
        """Get the first collection ID."""
        collections = self.get_collections()
        if collections:
            self.default_collection_id = collections[0]["id"]
            return self.default_collection_id
        return None

    def get_items(self, collection_id: str, size: int = 50) -> list:
        """Get all items in a collection with pagination."""
        url = f"{self.SYNC_BASE}/collections/{collection_id}/items?size={size}"
        results = []
        while True:
            data = self._request(url)
            if data.get("status") != "ok":
                break
            items = data.get("items", [])
            if not items:
                break
            for item in items:
                results.append(self._parse_item(item, collection_id))
            total = data.get("total", len(results))
            print(f"Fetched {len(results)}/{total} items...", file=sys.stderr)
            scroll_id = data.get("scroll_id")
            if scroll_id:
                url = (
                    f"{self.SYNC_BASE}/collections/{collection_id}/items"
                    f"?sort%5B%5D=title,asc&size={size}&scroll_id={scroll_id}"
                )
            else:
                break
        return results

    def get_item(self, collection_id: str, item_id: str) -> dict:
        """Get a single item's details."""
        url = f"{self.SYNC_BASE}/collections/{collection_id}/items/{item_id}"
        data = self._request(url)
        if data.get("status") == "ok":
            return self._parse_item(data.get("item", {}), collection_id)
        return None

    def get_annotations(self, collection_id: str, item_id: str) -> list:
        """Get annotations for an item."""
        url = (
            f"{self.SYNC_BASE}/collections/{collection_id}"
            f"/items/{item_id}/annotations"
        )
        data = self._request(url)
        results = []
        if data.get("status") == "ok":
            for anno in data.get("annotations", []):
                results.append({
                    "id": anno.get("id", ""),
                    "type": anno.get("type", ""),
                    "text": anno.get("text", ""),
                    "note": anno.get("note", ""),
                    "color_id": anno.get("color_id", 0),
                    "page": anno.get("page_start", 0),
                    "item_id": anno.get("item_id", ""),
                    "user_name": anno.get("user_name", ""),
                    "modified": anno.get("modified", ""),
                })
        return results

    def search_items(self, collection_id: str, query: str, field: str = "all") -> list:
        """Search items by keyword in specified field."""
        items = self.get_items(collection_id)
        query_lower = query.lower()
        results = []
        for item in items:
            match = False
            if field in ("all", "title"):
                if query_lower in item.get("title", "").lower():
                    match = True
            if field in ("all", "authors"):
                for author in item.get("authors", []):
                    if query_lower in author.lower():
                        match = True
                        break
            if field in ("all", "doi"):
                if query_lower in item.get("doi", "").lower():
                    match = True
            if field in ("all", "journal"):
                if query_lower in item.get("journal", "").lower():
                    match = True
            if field in ("all", "year"):
                if query_lower == str(item.get("year", "")):
                    match = True
            if field in ("all", "tags"):
                for tag in item.get("tags", []):
                    if query_lower in tag.lower():
                        match = True
                        break
            if field in ("all", "abstract"):
                if query_lower in item.get("abstract", "").lower():
                    match = True
            if match:
                results.append(item)
        return results

    def _parse_item(self, item_data: dict, collection_id: str) -> dict:
        """Parse raw item data into structured dict."""
        article = item_data.get("article", {})
        user_data = item_data.get("user_data", {})
        ext_ids = item_data.get("ext_ids", {})
        return {
            "id": item_data.get("id", ""),
            "collection_id": collection_id,
            "title": article.get("title", ""),
            "journal": article.get("journal", "Unknown"),
            "journal_abbrev": article.get("journal_abbrev", ""),
            "authors": article.get("authors", []),
            "year": article.get("year", None),
            "abstract": article.get("abstract", ""),
            "volume": article.get("volume", ""),
            "pagination": article.get("pagination", ""),
            "issn": article.get("issn", ""),
            "url": article.get("url", ""),
            "doi": ext_ids.get("doi", ""),
            "tags": user_data.get("tags", []),
            "rating": user_data.get("rating", None),
            "notes": user_data.get("notes", ""),
        }


def format_markdown(items: list, verbose: bool = False) -> str:
    """Format items as markdown."""
    lines = []
    for item in items:
        authors_str = ", ".join(item.get("authors", [])[:3])
        if len(item.get("authors", [])) > 3:
            authors_str += " et al."
        title = item.get("title", "No title")
        year = item.get("year", "N/A")
        journal = item.get("journal", "Unknown")
        doi = item.get("doi", "")

        lines.append(f"### {title}")
        lines.append(f"- **Authors**: {authors_str}")
        lines.append(f"- **Year**: {year}")
        lines.append(f"- **Journal**: {journal}")
        if doi:
            lines.append(f"- **DOI**: [{doi}](https://doi.org/{doi})")
        if verbose:
            if item.get("abstract"):
                lines.append(f"- **Abstract**: {item['abstract'][:300]}...")
            if item.get("tags"):
                lines.append(f"- **Tags**: {', '.join(item['tags'])}")
            if item.get("notes"):
                lines.append(f"- **Notes**: {item['notes'][:200]}")
            if item.get("rating"):
                lines.append(f"- **Rating**: {'★' * item['rating']}")
        lines.append("")
    return "\n".join(lines)


def format_annotations_markdown(annotations: list) -> str:
    """Format annotations as markdown."""
    if not annotations:
        return "No annotations found."
    lines = []
    color_names = {0: "Yellow", 1: "Red", 2: "Green", 3: "Blue", 4: "Purple"}
    for anno in annotations:
        color = color_names.get(anno.get("color_id", 0), "Unknown")
        lines.append(f"- **[{color}] p.{anno.get('page', '?')}**: {anno.get('text', '')}")
        if anno.get("note"):
            lines.append(f"  - *Note*: {anno['note']}")
    return "\n".join(lines)


def get_credentials():
    """Get credentials from environment variables or args."""
    email = os.environ.get("READCUBE_EMAIL", "")
    password = os.environ.get("READCUBE_PASSWORD", "")
    return email, password


def main():
    parser = argparse.ArgumentParser(
        description="ReadCube Papers API client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--email", default=None, help="ReadCube email (or set READCUBE_EMAIL env var)"
    )
    parser.add_argument(
        "--password", default=None,
        help="ReadCube password (or set READCUBE_PASSWORD env var)",
    )
    parser.add_argument(
        "--format", choices=["json", "markdown"], default="json",
        help="Output format (default: json)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # login
    subparsers.add_parser("login", help="Test login credentials")

    # collections
    subparsers.add_parser("collections", help="List all collections")

    # list
    list_parser = subparsers.add_parser("list", help="List items in a collection")
    list_parser.add_argument(
        "--collection", default=None, help="Collection ID (default: first collection)"
    )
    list_parser.add_argument(
        "--verbose", action="store_true", help="Include abstract, tags, notes"
    )

    # get
    get_parser = subparsers.add_parser("get", help="Get item details")
    get_parser.add_argument("item_id", help="Item ID")
    get_parser.add_argument(
        "--collection", default=None, help="Collection ID (default: first collection)"
    )

    # annotations
    anno_parser = subparsers.add_parser(
        "annotations", help="Get annotations for an item"
    )
    anno_parser.add_argument("item_id", help="Item ID")
    anno_parser.add_argument(
        "--collection", default=None, help="Collection ID (default: first collection)"
    )

    # search
    search_parser = subparsers.add_parser("search", help="Search items")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument(
        "--field",
        choices=["all", "title", "authors", "doi", "journal", "year", "tags", "abstract"],
        default="all",
        help="Field to search in (default: all)",
    )
    search_parser.add_argument(
        "--collection", default=None, help="Collection ID (default: first collection)"
    )
    search_parser.add_argument(
        "--verbose", action="store_true", help="Include abstract, tags, notes"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Resolve credentials
    email = args.email or os.environ.get("READCUBE_EMAIL", "")
    password = args.password or os.environ.get("READCUBE_PASSWORD", "")
    if not email or not password:
        print(
            "Error: Email and password required.\n"
            "Use --email/--password or set READCUBE_EMAIL/READCUBE_PASSWORD env vars.",
            file=sys.stderr,
        )
        sys.exit(1)

    client = ReadCubeClient()
    if not client.login(email, password):
        print("Error: Login failed. Check credentials.", file=sys.stderr)
        sys.exit(1)

    if args.command == "login":
        print("Login successful!")
        sys.exit(0)

    # Ensure we have a default collection
    if not client.get_default_collection_id():
        print("Error: No collections found.", file=sys.stderr)
        sys.exit(1)

    output_format = args.format

    if args.command == "collections":
        collections = client.get_collections()
        if output_format == "json":
            print(json.dumps(collections, indent=2, ensure_ascii=False))
        else:
            for c in collections:
                print(f"- **{c.get('id', '')}**: {c.get('name', 'Unnamed')}")

    elif args.command == "list":
        cid = args.collection or client.default_collection_id
        items = client.get_items(cid)
        if output_format == "json":
            print(json.dumps(items, indent=2, ensure_ascii=False))
        else:
            print(f"# Library ({len(items)} items)\n")
            print(format_markdown(items, verbose=args.verbose))

    elif args.command == "get":
        cid = args.collection or client.default_collection_id
        item = client.get_item(cid, args.item_id)
        if item:
            if output_format == "json":
                print(json.dumps(item, indent=2, ensure_ascii=False))
            else:
                print(format_markdown([item], verbose=True))
        else:
            print("Item not found.", file=sys.stderr)
            sys.exit(1)

    elif args.command == "annotations":
        cid = args.collection or client.default_collection_id
        annotations = client.get_annotations(cid, args.item_id)
        if output_format == "json":
            print(json.dumps(annotations, indent=2, ensure_ascii=False))
        else:
            print(format_annotations_markdown(annotations))

    elif args.command == "search":
        cid = args.collection or client.default_collection_id
        results = client.search_items(cid, args.query, field=args.field)
        if output_format == "json":
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            print(f"# Search results for '{args.query}' ({len(results)} matches)\n")
            print(format_markdown(results, verbose=args.verbose))


if __name__ == "__main__":
    main()
