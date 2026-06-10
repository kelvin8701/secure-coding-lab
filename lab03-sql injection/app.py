#!/usr/bin/env python3
"""
app.py — Secure Coding Lab 3: Injection (CWE-74)

INTENTIONALLY VULNERABLE TEACHING APP. Do not deploy on a public network.

Three endpoints, each demonstrating one injection class:
  /login   -> SQL injection (tautology auth bypass + piggy-backed query)
  /search  -> SQL injection (UNION-based data extraction)
  /ping    -> OS command injection

Every vulnerable line is marked  # >>> VULNERABLE <<<  with the safe version
shown directly beneath it (commented out). Part E of the lab is literally
swapping the marked line for the safe one.
"""
import sqlite3, subprocess, os
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
DB = os.path.join(os.path.dirname(__file__), "lab.db")

def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con


@app.route("/")
def home():
    return render_template("home.html")


# ---------------------------------------------------------------------------
# /login  — SQL INJECTION
# The username/password from the form are concatenated straight into the SQL
# string. A tautology like  ' OR '1'='1  makes the WHERE clause always true.
# ---------------------------------------------------------------------------
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
            # executescript() is used so piggy-backed queries (; DROP TABLE...)
            # are demonstrable. With the secure version above, switch to
            # con.execute(sql, (username, password)).
            cur = con.executescript(sql) if False else con.execute(sql)
            rows = cur.fetchall()
            con.commit()
            if rows:
                result = {"ok": True, "user": rows[0]["username"], "role": rows[0]["role"]}
            else:
                result = {"ok": False}
        except Exception as e:
            result = {"error": str(e)}
    return render_template("login.html", result=result, query=query_shown)


# ---------------------------------------------------------------------------
# /search — SQL INJECTION (UNION-based extraction)
# The search term is concatenated into a SELECT over products. A UNION SELECT
# lets the attacker append rows from any other table (e.g. users, secrets).
# ---------------------------------------------------------------------------
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
    return render_template("search.html", rows=rows, term=term,
                           error=error, query=query_shown)


# ---------------------------------------------------------------------------
# /ping — OS COMMAND INJECTION
# The host parameter is interpolated into a shell command run with shell=True.
# A metacharacter like  ; id  appends a second command.
# ---------------------------------------------------------------------------
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
    return render_template("ping.html", output=output, host=host, cmd=cmd_shown)


if __name__ == "__main__":
    if not os.path.exists(DB):
        import init_db  # noqa: F401  (creates the DB on first run)
    app.run(host="127.0.0.1", port=5000, debug=True)
