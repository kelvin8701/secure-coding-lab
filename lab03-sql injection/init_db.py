#!/usr/bin/env python3
"""init_db.py — (re)create the lab database with seed data.
Run this once before starting the app, and any time you want to reset state
(e.g. after the 'Bobby Tables' piggy-backed DROP TABLE exercise)."""
import sqlite3, os

DB = os.path.join(os.path.dirname(__file__), "lab.db")
if os.path.exists(DB):
    os.remove(DB)

con = sqlite3.connect(DB)
cur = con.cursor()

cur.executescript("""
CREATE TABLE users (
    id       INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    role     TEXT NOT NULL
);

CREATE TABLE products (
    id    INTEGER PRIMARY KEY,
    name  TEXT NOT NULL,
    price REAL NOT NULL
);

-- 'secrets' is the table students should NOT be able to read through the
-- product search. The UNION exercise (Part D) exfiltrates it anyway.
CREATE TABLE secrets (
    id          INTEGER PRIMARY KEY,
    description TEXT NOT NULL,
    value       TEXT NOT NULL
);
""")

cur.executemany("INSERT INTO users (username,password,role) VALUES (?,?,?)", [
    ("admin",  "S3cr3tAdminPw!", "admin"),
    ("alice",  "alicepass",      "user"),
    ("bob",    "bobpass",        "user"),
])

cur.executemany("INSERT INTO products (name,price) VALUES (?,?)", [
    ("USB Cable",      4.99),
    ("Mechanical Keyboard", 79.00),
    ("Laptop Stand",   32.50),
    ("Webcam 1080p",   45.00),
])

cur.executemany("INSERT INTO secrets (description,value) VALUES (?,?)", [
    ("API key",        "sk-live-91f3a7c2b8e4"),
    ("DB root password","r00t-d0_n0t-share"),
])

con.commit()
con.close()
print("Database initialised:", DB)
