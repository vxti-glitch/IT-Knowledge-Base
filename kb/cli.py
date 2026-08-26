import argparse
from pathlib import Path

from .builder import build_site
from .parser import ArticleValidationError, discover_articles


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build and validate the IT support knowledge base"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    build = subparsers.add_parser(
        "build", help="Validate content and build the static site"
    )
    build.add_argument("--docs", type=Path, default=Path("docs"))
    build.add_argument("--output", type=Path, default=Path("output"))

    check = subparsers.add_parser(
        "check", help="Validate article content without building"
    )
    check.add_argument("--docs", type=Path, default=Path("docs"))
    return parser


def main() -> int:
    args = create_parser().parse_args()
    try:
        if args.command == "check":
            articles = discover_articles(args.docs)
            print(f"Validation passed: {len(articles)} published articles.")
            return 0
        build_site(args.docs, args.output)
        return 0
    except ArticleValidationError as exc:
        print(str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
