#!/usr/bin/env python3
"""Regenerate README.md from GitHub PRs authored by GITHUB_USER.

Run manually with `gh` authenticated locally, or via the scheduled
GitHub Action (.github/workflows/update.yml), which runs it with the
Action's own token.
"""
import json
import subprocess
from collections import defaultdict
from datetime import datetime, timezone

GITHUB_USER = "chryzsh"

# Repos to leave out entirely (this showcase repo itself, sandbox/test PRs, etc).
EXCLUDE_REPOS: set[str] = set()

# Keyword -> category. First match wins, checked against "owner/repo" lowercase.
CATEGORY_RULES = [
    ("sccm", "SCCM / ConfigMgr"),
    ("misconfiguration-manager", "SCCM / ConfigMgr"),
    ("configmanbearpig", "SCCM / ConfigMgr"),
    ("bof", "BOF / C2 tooling"),
    ("c2-", "BOF / C2 tooling"),
    ("bloodhound", "AD / BloodHound"),
    ("tierzerotable", "AD / BloodHound"),
    ("mssqlhound", "AD / BloodHound"),
    ("adokit", "AD / BloodHound"),
    ("prowlarr", "Media / indexers"),
    ("radarr", "Media / indexers"),
]
DEFAULT_CATEGORY = "Other"

STATE_ICON = {"OPEN": "🟢 Open", "MERGED": "🟣 Merged", "CLOSED": "⚪ Closed"}

# Manually maintained — not derivable from `gh search`. Edit by hand when adding one.
ORIGINAL_TOOLS = [
    {
        "name": "PXEHacker",
        "url": "https://github.com/chryzsh/PXEHacker",
        "description": "Original repo, not a fork",
    },
]

EXTENDED_FORKS = [
    {
        "date": "2026-08-27",
        "fork": "sccm-http-looter",
        "url": "https://github.com/chryzsh/sccm-http-looter",
        "upstream": "",
        "changes": "NTLM authentication support",
    },
    {
        "date": "2026-08-27",
        "fork": "go-cmloot",
        "url": "https://github.com/chryzsh/go-cmloot",
        "upstream": "",
        "changes": "Add ACL hunting capabilities to find files you should not have access to",
    },
    {
        "date": "2026-08-20",
        "fork": "SCCM-CVE-2026-47301-Remote-Code-Execution-Exploit",
        "url": "https://github.com/chryzsh/SCCM-CVE-2026-47301-Remote-Code-Execution-Exploit",
        "upstream": "OmriBaso/SCCM-CVE-2026-47301-Remote-Code-Execution-Exploit",
        "changes": "Added chunked upload support (--chunk-size) + Build-Cab.ps1 helper",
    },
    {
        "date": "2026-03-18",
        "fork": "hashcat-6.2.6-SCCM",
        "url": "https://github.com/chryzsh/hashcat-6.2.6-SCCM",
        "upstream": "The-Viper-One/hashcat-6.2.6-SCCM",
        "changes": "Added AES-256 SCCM module (-m 19851) + OpenCL kernel fixes",
    },
    {
        "date": "2026-03-18",
        "fork": "PXEThief",
        "url": "https://github.com/chryzsh/PXEThief",
        "upstream": "MWR-CyberSec/PXEThief",
        "changes": "Added Scapy TFTP client, fixed Windows Firewall bypass/cleanup crash",
    },
]


def run_gh_search() -> list[dict]:
    out = subprocess.run(
        [
            "gh", "search", "prs", f"--author={GITHUB_USER}", "--limit", "200",
            "--json", "repository,number,title,state,url,createdAt",
        ],
        check=True, capture_output=True, text=True,
    )
    prs = json.loads(out.stdout)
    for pr in prs:
        pr["state"] = pr["state"].upper()
    return prs


def categorize(repo: str) -> str:
    low = repo.lower()
    for keyword, category in CATEGORY_RULES:
        if keyword in low:
            return category
    return DEFAULT_CATEGORY


def build_readme(prs: list[dict]) -> str:
    self_owned = f"{GITHUB_USER}/"
    filtered = [
        pr for pr in prs
        if not pr["repository"]["nameWithOwner"].startswith(self_owned)
        and pr["repository"]["nameWithOwner"] not in EXCLUDE_REPOS
    ]
    filtered.sort(key=lambda pr: pr["createdAt"], reverse=True)

    by_category: dict[str, list[dict]] = defaultdict(list)
    for pr in filtered:
        by_category[categorize(pr["repository"]["nameWithOwner"])].append(pr)

    merged = sum(1 for pr in filtered if pr["state"] == "MERGED")
    open_ = sum(1 for pr in filtered if pr["state"] == "OPEN")
    closed = sum(1 for pr in filtered if pr["state"] == "CLOSED")
    repo_count = len({pr["repository"]["nameWithOwner"] for pr in filtered})

    lines = [
        "# Open source contributions",
        "",
        f"Pull requests to other people's repos. Excludes PRs to my own repos.",
        f"Regenerated automatically from `gh search prs --author={GITHUB_USER}`.",
        "",
        f"**{len(filtered)} total** across **{repo_count} repos** — "
        f"{merged} merged, {open_} open, {closed} closed.",
        "",
    ]

    ordered_categories = [
        "SCCM / ConfigMgr", "BOF / C2 tooling", "AD / BloodHound",
        "Media / indexers", DEFAULT_CATEGORY,
    ]
    for category in ordered_categories:
        prs_in_cat = by_category.get(category)
        if not prs_in_cat:
            continue
        lines.append(f"## {category} ({len(prs_in_cat)})")
        lines.append("")
        lines.append("| Date | Repo | PR | State |")
        lines.append("|------|------|-----|-------|")
        for pr in prs_in_cat:
            date = pr["createdAt"][:10]
            repo = pr["repository"]["nameWithOwner"]
            title = pr["title"].replace("|", "\\|")
            state = STATE_ICON.get(pr["state"], pr["state"])
            lines.append(f"| {date} | {repo} | [#{pr['number']} {title}]({pr['url']}) | {state} |")
        lines.append("")

    if ORIGINAL_TOOLS:
        lines.append(f"## Original tools ({len(ORIGINAL_TOOLS)})")
        lines.append("")
        lines.append("Repos I wrote from scratch, not forks. Manually maintained.")
        lines.append("")
        lines.append("| Tool | Description |")
        lines.append("|------|-------------|")
        for tool in ORIGINAL_TOOLS:
            lines.append(f"| [{tool['name']}]({tool['url']}) | {tool['description']} |")
        lines.append("")

    if EXTENDED_FORKS:
        lines.append(f"## Forks extended with own commits ({len(EXTENDED_FORKS)})")
        lines.append("")
        lines.append("Forks where I added real functionality on top of upstream. Manually maintained.")
        lines.append("")
        lines.append("| Date | Fork | Upstream | My changes |")
        lines.append("|------|------|----------|------------|")
        for fork in EXTENDED_FORKS:
            upstream = fork["upstream"] or "—"
            lines.append(
                f"| {fork['date']} | [{fork['fork']}]({fork['url']}) | {upstream} | {fork['changes']} |"
            )
        lines.append("")

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines.append(f"_Last updated: {generated_at}_")
    return "\n".join(lines) + "\n"


def main() -> None:
    prs = run_gh_search()
    readme = build_readme(prs)
    with open("README.md", "w") as f:
        f.write(readme)


if __name__ == "__main__":
    main()
