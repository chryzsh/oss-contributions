#!/usr/bin/env python3
"""Regenerate README.md from GITHUB_USER's GitHub activity.

Run manually with `gh` authenticated locally, or via the scheduled
GitHub Action (.github/workflows/update.yml), which runs it with the
Action's own token.

See CLAUDE.md for how each section is derived and why the detection
works the way it does.
"""
import json
import subprocess
from collections import defaultdict
from datetime import datetime, timezone

GITHUB_USER = "chryzsh"

# Repos to leave out of the PR table entirely.
EXCLUDE_REPOS: set[str] = set()

# Public non-fork repos to leave out of "Original tools" (not real tools:
# this showcase repo itself, blog/personal site, curated lists, unrelated utilities).
EXCLUDE_ORIGINAL_TOOLS: set[str] = {
    "oss-contributions",
    "chryzsh.github.io",
    "elevated-access",
    "awesome-bof",
    "awesome-bloodhound",
    "awesome-windows-security",
    "cloud-hacking-labs",
    "practical-hacking",
    "json_chunker",
    "GPTCommentDetector",
}

# Forks to leave out of "Forks extended" even if they show commits ahead
# (e.g. a fork kept only as an unmodified reference copy with a stray branch,
# or work-in-progress from a job rather than a personal OSS contribution).
EXCLUDE_FORKS: set[str] = {
    "BloodHound",  # SpecterOps day-job branches (BED-xxxx tickets), not OSS work
}

# repo name -> hand-written one-liner, overrides the auto-generated commit-message
# summary. Add one here once a newly-detected fork's auto text isn't good enough.
EXTENDED_FORK_NOTES: dict[str, str] = {
    "sccm-http-looter": "NTLM authentication support",
    "go-cmloot": "Add ACL hunting capabilities to find files you should not have access to",
    "SCCM-CVE-2026-47301-Remote-Code-Execution-Exploit": "Added chunked upload support (--chunk-size) + Build-Cab.ps1 helper",
    "hashcat-6.2.6-SCCM": "Added AES-256 SCCM module (-m 19851) + OpenCL kernel fixes",
    "PXEThief": "Added Scapy TFTP client, fixed Windows Firewall bypass/cleanup crash",
}

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


def gh_json(args: list[str]):
    out = subprocess.run(["gh"] + args, check=True, capture_output=True, text=True)
    return json.loads(out.stdout)


def gh_json_soft(args: list[str], default=None):
    """Like gh_json, but returns `default` instead of raising on failure
    (used for compare calls against branches/refs that can 404)."""
    out = subprocess.run(["gh"] + args, capture_output=True, text=True)
    if out.returncode != 0:
        return default
    try:
        return json.loads(out.stdout)
    except json.JSONDecodeError:
        return default


def run_gh_search() -> list[dict]:
    prs = gh_json([
        "search", "prs", f"--author={GITHUB_USER}", "--limit", "200",
        "--json", "repository,number,title,state,url,createdAt",
    ])
    for pr in prs:
        pr["state"] = pr["state"].upper()
    return prs


def categorize(repo: str) -> str:
    low = repo.lower()
    for keyword, category in CATEGORY_RULES:
        if keyword in low:
            return category
    return DEFAULT_CATEGORY


def get_original_tools() -> list[dict]:
    """Public, non-fork repos owned by GITHUB_USER. See CLAUDE.md: 'a tool I
    built from scratch' == isFork == False on my own profile."""
    repos = gh_json([
        "repo", "list", GITHUB_USER, "--limit", "200",
        "--json", "name,isFork,isPrivate,description,url,pushedAt",
    ])
    tools = [
        r for r in repos
        if not r["isFork"] and not r["isPrivate"] and r["name"] not in EXCLUDE_ORIGINAL_TOOLS
    ]
    tools.sort(key=lambda r: r["pushedAt"], reverse=True)
    return tools


def get_forks() -> list[dict]:
    """Public forks owned by GITHUB_USER, with upstream parent info."""
    query = f"""
    {{ user(login: "{GITHUB_USER}") {{
        repositories(first: 100, isFork: true, ownerAffiliations: OWNER, privacy: PUBLIC) {{
          nodes {{
            name
            url
            pushedAt
            defaultBranchRef {{ name }}
            parent {{ nameWithOwner defaultBranchRef {{ name }} }}
          }}
        }}
    }}}}"""
    data = gh_json(["api", "graphql", "-f", f"query={query}"])
    return data["data"]["user"]["repositories"]["nodes"]


def branch_names(fork_repo: str) -> list[str]:
    out = subprocess.run(
        ["gh", "api", f"repos/{GITHUB_USER}/{fork_repo}/branches", "--jq", ".[].name"],
        capture_output=True, text=True,
    )
    if out.returncode != 0:
        return []
    return [b for b in out.stdout.splitlines() if b]


def compare(parent: str, base_branch: str, fork_repo: str, branch: str) -> dict | None:
    return gh_json_soft([
        "api", f"repos/{parent}/compare/{base_branch}...{GITHUB_USER}:{fork_repo}:{branch}",
    ])


def find_extended_forks(prd_upstreams: set[str]) -> list[dict]:
    """A fork counts as 'extended' when some branch has commits the parent's
    default branch doesn't. Skips any fork whose upstream already has a
    tracked PR from me (a merged PR still shows the fork as 'ahead' because
    squash-merge rewrites commit hashes — that work is already represented
    in the PR table, not here). See CLAUDE.md for the full reasoning."""
    results = []
    for fork in get_forks():
        name = fork["name"]
        parent = fork.get("parent")
        if not parent or name in EXCLUDE_FORKS:
            continue
        upstream = parent["nameWithOwner"]
        if upstream in prd_upstreams:
            continue
        base_branch = parent["defaultBranchRef"]["name"]

        best_branch, best_ahead, best_commits = None, 0, []
        for branch in branch_names(name):
            cmp = compare(upstream, base_branch, name, branch)
            if not cmp:
                continue
            ahead = cmp.get("ahead_by", 0)
            if ahead > best_ahead:
                best_branch = branch
                best_ahead = ahead
                best_commits = [c["commit"]["message"].splitlines()[0] for c in cmp.get("commits", [])]

        if best_ahead == 0:
            continue

        note = EXTENDED_FORK_NOTES.get(name)
        if not note:
            # Newest-first, most recent 3 commit subjects as a placeholder
            # until someone writes a proper one-liner in EXTENDED_FORK_NOTES.
            note = "; ".join(reversed(best_commits[-3:]))

        results.append({
            "name": name,
            "url": fork["url"],
            "upstream": upstream,
            "branch": best_branch,
            "ahead_by": best_ahead,
            "date": fork["pushedAt"][:10],
            "note": note,
        })

    results.sort(key=lambda f: f["date"], reverse=True)
    return results


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
        "Pull requests to other people's repos. Excludes PRs to my own repos.",
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

    original_tools = get_original_tools()
    if original_tools:
        lines.append(f"## Original tools ({len(original_tools)})")
        lines.append("")
        lines.append(
            "Public repos I wrote from scratch, not forks. Auto-detected "
            "(`isFork == false`); curate exclusions via `EXCLUDE_ORIGINAL_TOOLS`."
        )
        lines.append("")
        lines.append("| Tool | Description |")
        lines.append("|------|-------------|")
        for tool in original_tools:
            desc = tool["description"] or "—"
            lines.append(f"| [{tool['name']}]({tool['url']}) | {desc} |")
        lines.append("")

    prd_upstreams = {pr["repository"]["nameWithOwner"] for pr in filtered}
    extended_forks = find_extended_forks(prd_upstreams)
    if extended_forks:
        lines.append(f"## Forks extended with own commits ({len(extended_forks)})")
        lines.append("")
        lines.append(
            "Forks with commits on some branch that aren't in an already-tracked "
            "PR above. Auto-detected; see CLAUDE.md for the detection logic and "
            "`EXTENDED_FORK_NOTES` to override the one-liner."
        )
        lines.append("")
        lines.append("| Date | Fork | Upstream | Branch | My changes |")
        lines.append("|------|------|----------|--------|------------|")
        for fork in extended_forks:
            lines.append(
                f"| {fork['date']} | [{fork['name']}]({fork['url']}) | {fork['upstream']} "
                f"| `{fork['branch']}` (+{fork['ahead_by']}) | {fork['note']} |"
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
