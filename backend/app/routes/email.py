"""One-click unsubscribe from the weekly progress email. The link in each email carries a signed token, so no sign-in is needed."""
import html

from flask import Blueprint, request

from ..services import engagement

bp = Blueprint("email", __name__, url_prefix="/api/email")

PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | Graphite</title><style>body{{margin:0;font:17px/1.6 system-ui,sans-serif;background:#1c1e21;color:#eceef0;display:grid;place-items:center;min-height:100vh}}
main{{max-width:440px;padding:32px 20px}}h1{{font-size:1.5rem;margin:0 0 12px}}a{{color:#f2c14e}}</style></head>
<body><main><h1>{title}</h1><p>{text}</p><p><a href="/dashboard.html">Go to your dashboard</a></p></main></body></html>"""


@bp.get("/unsubscribe")
def unsubscribe():
    who = engagement.unsubscribe(request.args.get("t", ""))
    if who is None:
        return PAGE.format(title="That link didn't work", text="It may be incomplete. You can turn the weekly email off in Account on your dashboard."), 400
    text = ("The parent copy of the weekly progress email is off." if who == "parent"
            else "You won't get the weekly progress email anymore. You can turn it back on in Account on your dashboard.")
    return PAGE.format(title="You're unsubscribed", text=html.escape(text))
