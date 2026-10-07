import json
import sys
from pathlib import Path

from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from commissioning_rag import Index

folder = ROOT / "datasets/rag-formats"
folder.mkdir(exist_ok=True)
p = folder / "inspection.pdf"
pdf = canvas.Canvas(str(p))
pdf.drawString(72, 720, "Valve calibration interval is forty-two hours.")
pdf.save()
(folder / "constants.java").write_text(
    "public class Constants { static final int HYDRO_REFERENCE = 719; }\n"
)
(folder / "measurements.csv").write_text("sample,pressure_kpa\n1,200\n2,210\n")
(folder / "event.json").write_text(
    json.dumps({"event_type": "synthetic-test", "sequence": 42})
)
(folder / "notes.txt").write_text(
    "The reference bearing tolerance is seven micrometers.\n"
)
idx = Index(ROOT / "rag/format-test.sqlite", folder)
idx.update()
assert not idx.stale()
for query, want in [
    ('"forty"', "inspection.pdf"),
    ('"HYDRO_REFERENCE"', "constants.java"),
    ('"pressure"', "measurements.csv"),
    ('"synthetic"', "event.json"),
    ('"micrometers"', "notes.txt"),
]:
    hits = idx.retrieve(query, False)
    assert any(h["path"].endswith(want) for h in hits), (query, hits)
hits = idx.retrieve("How often should the valve be calibrated?")
assert hits[0]["path"].endswith("inspection.pdf"), hits
(ROOT / "evidence/rag-formats.json").write_text(
    json.dumps(
        {
            "status": "PASS",
            "formats": ["PDF text", "Java code", "CSV", "JSON", "plain text"],
            "pdf_semantic_citation": hits[0],
            "no_OCR": True,
        },
        indent=2,
    )
    + "\n"
)
print(
    "PASS local PDF-text/code/CSV/JSON/text extraction and cited PDF semantic retrieval"
)
