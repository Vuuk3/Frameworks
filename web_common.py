from collections.abc import Iterable
from html import escape

from django.http import HttpResponse


NAVIGATION = (
    ("/", "Главная"),
    ("/mentors/", "Наставники"),
    ("/specializations/", "Специализации"),
    ("/applications/", "Заявки"),
    ("/users/", "Пользователи"),
)


def page(title: str, content: str) -> HttpResponse:
    """Build a small HTML page with common navigation and CSS."""
    links = "".join(
        f'<a href="{url}">{escape(label)}</a>'
        for url, label in NAVIGATION
    )
    document = f"""<!doctype html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(title)}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            color: #1f2937;
            background: #f3f4f6;
        }}
        nav {{
            padding: 16px max(24px, calc((100% - 960px) / 2));
            background: #1f4b3f;
        }}
        nav a {{
            margin-right: 20px;
            color: white;
            text-decoration: none;
        }}
        main {{
            max-width: 960px;
            margin: 32px auto;
            padding: 28px;
            background: white;
            border-radius: 8px;
        }}
        h1 {{ margin-top: 0; }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
            gap: 16px;
        }}
        .card {{
            padding: 18px;
            border: 1px solid #d1d5db;
            border-radius: 6px;
        }}
        .card h2 {{ margin-top: 0; font-size: 20px; }}
        a {{ color: #176b55; }}
        .muted {{ color: #6b7280; }}
        .status {{ font-weight: bold; }}
    </style>
</head>
<body>
    <nav>{links}</nav>
    <main>{content}</main>
</body>
</html>"""
    return HttpResponse(document)


def cards(items: Iterable[str]) -> str:
    """Wrap prepared card fragments in a responsive grid."""
    return '<div class="grid">' + "".join(items) + "</div>"
