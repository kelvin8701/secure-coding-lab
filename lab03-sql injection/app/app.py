#!/usr/bin/env python3
"""Secure Coding Lab 3: Injection (CWE-74) — intentionally vulnerable teaching app.
All HTML is inlined, so there is no templates/ folder to misplace."""
import sqlite3, subprocess, os
from flask import Flask, request, render_template_string
from jinja2 import DictLoader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, "lab.db")
app = Flask(__name__)


def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con


PAGE = """<!doctype html><html><head><meta charset="utf-8"><title>Lab 3 — {{ title }}</title>
<style>
body{font-family:system-ui,Arial,sans-serif;max-width:760px;margin:2rem auto;padding:0 1rem;color:#222}
nav a{margin-right:1rem;color:#2E75B6;text-decoration:none;font-weight:600}
h1{color:#1F3864}
input{padding:6px 8px;margin:4px 0;width:240px}
button{padding:6px 14px;background:#2E75B6;color:#fff;border:0;border-radius:4px;cursor:pointer}
.q{background:#F2F2F2;border-left:4px solid #C55A11;padding:8px 12px;font-family:Consolas,monospace;
   font-size:.85rem;white-space:pre-wrap;margin:10px 0}
.ok{color:#548235;font-weight:700}.no{color:#C00}.err{color:#C55A11}
table{border-collapse:collapse;margin-top:10px}td,th{border:1px solid #aaa;padding:4px 10px}
</style></head><body>
<nav><a href="/">Home</a><a href="/login">Login</a><a href="/search">Search</a><a href="/ping">Ping</a></nav>
<h1>{{ heading }}</h1>
{% block body %}{% endblock %}
</body></html>"""

HOME = """{% extends "page" %}{% block body %}
<p>Intentionally vulnerable teaching app. Three endpoints:</p>
<ul><li><b>Login</b> — SQL injection (auth bypass)</li>
<li><b>Search</b> — SQL injection (UNION extraction)</li>
<li><b>Ping</b> — OS command injection</li></ul>
{% endblock %}"""

LOGIN = """{% extends "page" %}{% block body %}
<form method="post">
<div><input name="username" placeholder="username"></div>
<div><input name="password" type="text" placeholder="password"></div>
<button>Log in</button></form>
{% if query %}<div class="q">SQL executed:
{{ query }}</div>{% endif %}
{% if result %}
  {% if result.ok %}<p class="ok">Logged in as {{ result.user }} (role: {{ result.role }})</p>
  {% elif result.error %}<p class="err">DB error: {{ result.error }}</p>
  {% else %}<p class="no">Invalid credentials.</p>{% endif %}
{% endif %}
{% endblock %}"""

SEARCH = """{% extends "page" %}{% block body %}
<form method="get"><input name="q" value="{{ term }}" placeholder="product name"><button>Search</button></form>
{% if query %}<div class="q">SQL executed:
{{ query }}</div>{% endif %}
{% if error %}<p class="err">DB error: {{ error }}</p>{% endif %}
{% if rows %}<table><tr><th>name</th><th>price</th></tr>
{% for r in rows %}<tr><td>{{ r[0] }}</td><td>{{ r[1] }}</td></tr>{% endfor %}</table>{% endif %}
{% endblock %}"""

PING = """{% extends "page" %}{% block body %}
<form method="get"><input name="host" value="{{ host }}" placeholder="hostname or IP"><button>Ping</button></form>
{% if cmd %}<div class="q">Shell command executed:
{{ cmd }}</div>{% endif %}
{% if output %}<div class="q">{{ output }}</div>{% endif %}
{% endblock %}"""

app.jinja_loader = DictLoader({"page": PAGE})


def render(tmpl, title, heading, **ctx):
    return render_template_string(tmpl, title=title, heading=heading, **ctx)


@app.route("/")
def home():
    return render(HOME, "Home", "Vulnerable App — Lab 3")


@app.route("/login", methods=["GET", "POST"])
def login():
    result = None
    query_shown = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        # >>> VULNERABLE <<<  string-built query, input is trusted as code
        sql = ("SELECT id, username, role FROM users "
               "WHERE username = '" + username + "' "
               "AND password = '" + password + "'")
        query_shown = sql
        # --- SECURE VERSION (Part E): parameterized query ---
        # sql = "SELECT id, username, role FROM users WHERE username = ? AND password = ?"
        # rows = db().execute(sql, (username, password)).fetchall()
        try:
            con = db()
            cur = con.execute(sql)        # single-statement; piggy-back is rejected
            rows = cur.fetchall()
            con.commit()
            if rows:
                result = {"ok": True, "user": rows[0]["username"], "role": rows[0]["role"]}
            else:
                result = {"ok": False}
        except Exception as e:
            result = {"error": str(e)}
    return render(LOGIN, "Login", "Login", result=result, query=query_shown)


@app.route("/search")
def search():
    term = request.args.get("q", "")
    rows, error, query_shown = [], None, None
    if term:
        # >>> VULNERABLE <<<  search term concatenated into the query
        sql = ("SELECT name, price FROM products "
               "WHERE name LIKE '%" + term + "%'")
        query_shown = sql
        # --- SECURE VERSION (Part E): parameterized LIKE ---
        # sql = "SELECT name, price FROM products WHERE name LIKE ?"
        # rows = db().execute(sql, ('%' + term + '%',)).fetchall()
        try:
            rows = db().execute(sql).fetchall()
        except Exception as e:
            error = str(e)
    return render(SEARCH, "Search", "Product Search",
                  rows=rows, term=term, error=error, query=query_shown)


@app.route("/ping")
def ping():
    host = request.args.get("host", "")
    output, cmd_shown = None, None
    if host:
        # >>> VULNERABLE <<<  shell=True + string interpolation
        cmd = "ping -c 1 " + host
        cmd_shown = cmd
        try:
            output = subprocess.run(cmd, shell=True, capture_output=True,
                                    text=True, timeout=5).stdout
        except Exception as e:
            output = str(e)
        # --- SECURE VERSION (Part E): no shell, argument list ---
        # output = subprocess.run(["ping", "-c", "1", host],
        #                         capture_output=True, text=True, timeout=5).stdout
    return render(PING, "Ping", "Network Ping Tool",
                  output=output, host=host, cmd=cmd_shown)


if __name__ == "__main__":
    if not os.path.exists(DB):
        import subprocess as _sp, sys as _sys
        _sp.run([_sys.executable, os.path.join(BASE_DIR, "init_db.py")])
    app.run(host="127.0.0.1", port=5000, debug=True)
