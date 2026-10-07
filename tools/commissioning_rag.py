"""Workspace-only incremental local retrieval, FTS and Nomic embeddings."""

import hashlib
import json
import math
import sqlite3
import urllib.request
from pathlib import Path

ROOT = Path("/home/joe/LLM-Workspace").resolve()
ALLOWED = {".txt", ".md", ".py", ".java", ".js", ".json", ".csv", ".pdf"}


def files(directory):
    directory = Path(directory).resolve()
    if directory == ROOT or not directory.is_relative_to(ROOT):
        raise ValueError(
            "Authorize a specific workspace subdirectory, not entire home or workspace"
        )
    for p in sorted(directory.rglob("*")):
        if (
            p.is_file()
            and p.suffix.lower() in ALLOWED
            and p.resolve().is_relative_to(directory)
        ):
            yield p


def embed(text, query=False):
    token = (
        Path("/home/joe/.lmstudio/credentials/local-work-api.token").read_text().strip()
    )
    payload = {
        "model": "text-embedding-nomic-embed-text-v1.5",
        "input": ("search_query: " if query else "search_document: ") + text,
    }
    req = urllib.request.Request(
        "http://127.0.0.1:1234/v1/embeddings",
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as f:
        return json.load(f)["data"][0]["embedding"]


def text_of(p):
    if p.suffix == ".pdf":
        from pypdf import PdfReader

        return "\n".join(page.extract_text() or "" for page in PdfReader(p).pages)
    return p.read_text(errors="replace")


class Index:
    def __init__(self, path, directory):
        self.directory = Path(directory).resolve()
        list(files(self.directory))
        db = Path(path).resolve()
        if not db.is_relative_to(ROOT):
            raise ValueError("DB must be local workspace")
        self.db = sqlite3.connect(db)
        self.db.execute(
            "create table if not exists chunks(path text, ordinal integer, sha256 text, text text, vector text, primary key(path,ordinal))"
        )
        self.db.execute(
            "create virtual table if not exists search using fts5(path, ordinal UNINDEXED, text)"
        )

    def hashes(self):
        return {
            str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in files(self.directory)
        }

    def stale(self):
        known = dict(self.db.execute("select path,sha256 from chunks group by path"))
        current = self.hashes()
        return sorted(
            k for k in set(known) | set(current) if known.get(k) != current.get(k)
        )

    def update(self):
        changed = self.stale()
        current = self.hashes()
        with self.db:
            for path in changed:
                self.db.execute("delete from chunks where path=?", (path,))
                self.db.execute("delete from search where path=?", (path,))
                if path not in current:
                    continue
                text = text_of(ROOT / path)
                # Byte-independent character chunks keep citations deterministic. Small enough for embedding token limit.
                for ordinal, start in enumerate(range(0, max(len(text), 1), 800)):
                    chunk = text[start : start + 800]
                    self.db.execute(
                        "insert into chunks values(?,?,?,?,?)",
                        (path, ordinal, current[path], chunk, json.dumps(embed(chunk))),
                    )
                    self.db.execute(
                        "insert into search values(?,?,?)", (path, ordinal, chunk)
                    )
        return changed

    def retrieve(self, query, semantic=True, k=3):
        if self.stale():
            raise ValueError("Index stale: update before retrieval")
        if not semantic:
            return [
                {"path": p, "chunk": n, "text": t, "score": s}
                for p, n, t, s in self.db.execute(
                    "select path,ordinal,text,bm25(search) from search where search match ? order by bm25(search) limit ?",
                    (query, k),
                )
            ]
        v = embed(query, True)
        vn = math.sqrt(sum(x * x for x in v))
        rows = []
        for p, n, h, t, raw in self.db.execute("select * from chunks"):
            w = json.loads(raw)
            den = vn * math.sqrt(sum(x * x for x in w))
            score = sum(a * b for a, b in zip(v, w)) / den if den else 0
            rows.append({"path": p, "chunk": n, "sha256": h, "text": t, "score": score})
        return sorted(rows, key=lambda x: x["score"], reverse=True)[:k]
