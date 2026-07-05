#!/usr/bin/env python3
"""Contract test: report-template.html tokens <-> SKILL.md docs must stay in sync.

Run: python3 scripts/check_contract.py   (exit 0 = contract holds)
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOKEN = re.compile(r"\{\{([A-Z][A-Z0-9_]*)\}\}")

failures = []

for tpl_name in ("report-template.html", "journal-template.html"):
    tpl_path = ROOT / tpl_name
    if not tpl_path.exists():
        failures.append(f"{tpl_name}: file missing")
        continue
    tpl = tpl_path.read_text()
    skill = (ROOT / "SKILL.md").read_text()

    tpl_tokens = set(TOKEN.findall(tpl))
    skill_tokens = set(TOKEN.findall(skill))

    undocumented = tpl_tokens - skill_tokens
    if undocumented:
        failures.append(f"{tpl_name}: tokens NOT documented in SKILL.md: {sorted(undocumented)}")

    # Fill every token with a dummy value; nothing must remain.
    filled = tpl
    for t in tpl_tokens:
        filled = filled.replace("{{" + t + "}}", "50" if t.startswith("STAT_") else "<p>x</p>")
    leftovers = TOKEN.findall(filled) + re.findall(r"\{\{", filled)
    if leftovers:
        failures.append(f"{tpl_name}: unfillable leftovers after substitution: {leftovers[:5]}")

    # Structural sanity: self-contained, no external requests.
    for pat, msg in (
        (r'src="https?://', "external <script/img src>"),
        (r'href="https?://[^"]*\.(?:css|woff2?)', "external stylesheet/font"),
        (r"@import", "CSS @import"),
    ):
        if re.search(pat, tpl):
            failures.append(f"{tpl_name}: not self-contained — {msg}")

# SKILL.md tokens that no template uses (docs drift the other way).
skill = (ROOT / "SKILL.md").read_text()
all_tpl_tokens = set()
for tpl_name in ("report-template.html", "journal-template.html"):
    p = ROOT / tpl_name
    if p.exists():
        all_tpl_tokens |= set(TOKEN.findall(p.read_text()))
phantom = set(TOKEN.findall(skill)) - all_tpl_tokens - {"TOKEN"}  # {{TOKEN}} = generic prose in SKILL.md
if phantom:
    failures.append(f"SKILL.md documents tokens that exist in no template: {sorted(phantom)}")

if failures:
    print("CONTRACT BROKEN:")
    for f in failures:
        print(f"  ✗ {f}")
    sys.exit(1)
print(f"contract OK — {len(all_tpl_tokens)} tokens in sync across templates and SKILL.md")
