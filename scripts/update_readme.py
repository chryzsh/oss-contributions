#!/usr/bin/env python3
"""Regenerate README.md from GITHUB_USER's GitHub activity.

Run manually with `gh` authenticated locally, or via the scheduled
GitHub Action (.github/workflows/update.yml), which runs it with the
Action's own token.

See CLAUDE.md for how each section is derived and why the detection
works the way it does.
"""
import html
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
    "cookie-monster": "Fixed an ANSI file path declaration and a hex output cast bug",
    "asciinema": "Added a transcript encoder, clip/search commands, and txt-encoder improvements for working with recorded terminal sessions (the castr tooling)",
    "SharpDPAPI": "Strips null bytes from decrypted output strings that were corrupting downstream parsing",
    "smbtakeover": "Fixed BOF bugs causing (null) output and handle/memory leaks; added an OC2 Python script for the BOF",
    "DPAPI_BOF": "Added SCCM CRED-3 and CRED-4 disk-triage BOFs and a RECON-7 BOF, split out from the base DPAPI BOFs",
    "PassTheCert": "Fixed certificate loading, added private key validation, and improved error messages",
    "Seatbelt": "Fixed remote WMI auth: added PacketPrivacy and corrected implicit credential handling",
    "linux_bof": "Added netstat and uname BOFs, fixed a syscall ID and a type bug in beacon.h",
    "TIBER-Cases": "Updated for TheHive5 compatibility",
    "RelayInformer": "Added an unauthenticated SMB signing enforcement check, plus NTLM preflight fixes for HTTP relay targets",
    "ADExplorerSnapshot": "Added dump-output tooling: a single shared pass for object-based dumps, output written beside the snapshot instead of the tool directory, plus a missing header column fix",
    "cloudprowl": "Added a modular architecture with token caching, JSON export, and a privilege-escalation analyzer that flags managed-identity takeover paths",
    "ai-postex": "Fixed C++/WinRT build errors and missing Arsenal Kit definitions, plus assorted correctness and performance fixes in the semantic search and credential finder code",
    "cred1py": "Completed end-to-end CRED1 decryption: AES-256 support, policy retrieval plus NAA credential extraction, an SCCM SubjectKeyIdentifier CMS fix, and a local/offline decrypt mode",
    "SQLRecon": "Sped up CLR assembly load time for the DLL",
    "OperatorsKit": "Added HRESULT diagnostics to AddTaskScheduler for clearer failure output",
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


def is_own_commit(commit_entry: dict) -> bool:
    """True unless GitHub resolves this commit's author to a real account
    that isn't GITHUB_USER. A fork can share a branch with its upstream
    (mirrored at fork time, or synced later) without chryzsh ever having
    touched it — `cookie-monster`'s "CS-4.12" branch and `asciinema`'s
    "python" branch both turned out to be 100% the upstream maintainer's own
    commits, just sitting on a same-named branch in the fork. Raw `ahead_by`
    can't tell that apart from real work; only the resolved author can.

    An unresolvable author (GitHub's literal "invalid-email-address" login,
    or no `author` object at all — happens when git was never configured,
    e.g. author name "Your Name") is treated as GITHUB_USER's own commit:
    nobody else can push to GITHUB_USER's own fork, so it can't be someone
    else's authored work even though GitHub can't identify whose."""
    author = commit_entry.get("author")
    if not author:
        return True
    login = author.get("login")
    if not login or login == "invalid-email-address":
        return True
    return login == GITHUB_USER


def find_extended_forks(prd_upstreams: set[str]) -> list[dict]:
    """A fork counts as 'extended' when some branch has commits, actually
    authored by GITHUB_USER, that the parent's default branch doesn't. Skips
    any fork whose upstream already has a tracked PR from me (a merged PR
    still shows the fork as 'ahead' because squash-merge rewrites commit
    hashes — that work is already represented in the PR table, not here).
    See CLAUDE.md for the full reasoning."""
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
            own_commits = [c for c in cmp.get("commits", []) if is_own_commit(c)]
            ahead = len(own_commits)
            if ahead > best_ahead:
                best_branch = branch
                best_ahead = ahead
                best_commits = [c["commit"]["message"].splitlines()[0] for c in own_commits]

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


def render_pr_table(prs_in_cat: list[dict]) -> list[str]:
    """Raw HTML table (not a markdown table) grouped by repo via rowspan, so a
    repo with many PRs shows its name/link once instead of once per row.
    Plain markdown tables can't rowspan; GitHub renders embedded HTML in a
    README fine, so we drop to HTML for just this table. Repos are ordered by
    their most recent PR (same ordering feel as the old ungrouped, date-sorted
    table); PRs within a repo are already date-descending from the caller."""
    groups: dict[str, list[dict]] = {}
    order: list[str] = []
    for pr in prs_in_cat:  # already sorted newest-first by the caller
        repo = pr["repository"]["nameWithOwner"]
        if repo not in groups:
            groups[repo] = []
            order.append(repo)
        groups[repo].append(pr)

    lines = [
        "<table>",
        "<thead><tr><th>Date</th><th>Repo</th><th>PR</th><th>State</th></tr></thead>",
        "<tbody>",
    ]
    for repo in order:
        rows = groups[repo]
        repo_link = f'<a href="https://github.com/{html.escape(repo)}">{html.escape(repo)}</a>'
        for i, pr in enumerate(rows):
            date = pr["createdAt"][:10]
            title = html.escape(pr["title"])
            state = STATE_ICON.get(pr["state"], pr["state"])
            lines.append("<tr>")
            lines.append(f"<td>{date}</td>")
            if i == 0:
                lines.append(f'<td rowspan="{len(rows)}">{repo_link}</td>')
            lines.append(f'<td><a href="{pr["url"]}">#{pr["number"]} {title}</a></td>')
            lines.append(f"<td>{state}</td>")
            lines.append("</tr>")
    lines.append("</tbody>")
    lines.append("</table>")
    return lines


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
        lines.extend(render_pr_table(prs_in_cat))
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
            upstream_link = f"[{fork['upstream']}](https://github.com/{fork['upstream']})"
            lines.append(
                f"| {fork['date']} | [{fork['name']}]({fork['url']}) | {upstream_link} "
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
