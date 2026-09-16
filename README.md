# Open source contributions

Pull requests to other people's repos. Excludes PRs to my own repos.
Regenerated automatically from `gh search prs --author=chryzsh`.

**75 total** across **22 repos** — 30 merged, 34 open, 11 closed.

## SCCM / ConfigMgr (39)

| Date | Repo | PR | State |
|------|------|-----|-------|
| 2026-09-16 | subat0mik/Misconfiguration-Manager | [#60 Link ELEVATE-2 and PREVENT-14 as associated offensive/defensive IDs](https://github.com/subat0mik/Misconfiguration-Manager/pull/60) | 🟣 Merged |
| 2026-09-16 | SpecterOps/ConfigManBearPig | [#14 fix: only count ACEs that actually grant Full Control on System Manag…](https://github.com/SpecterOps/ConfigManBearPig/pull/14) | 🟢 Open |
| 2026-09-16 | garrettfoster13/sccmhunter | [#139 fix: don't treat scoped ACEs on System Management as Full Control](https://github.com/garrettfoster13/sccmhunter/pull/139) | 🟢 Open |
| 2026-09-08 | Mayyhem/ludus_sccm | [#6 Add opt-in Script Approvers RBAC for NAA (EXEC-2 lab path)](https://github.com/Mayyhem/ludus_sccm/pull/6) | 🟢 Open |
| 2026-09-08 | Mayyhem/ludus_sccm | [#5 Add create_dp_loot_share role to make CRED-6 possible in the lab](https://github.com/Mayyhem/ludus_sccm/pull/5) | 🟢 Open |
| 2026-09-08 | SpecterOps/ConfigManBearPig | [#12 fix(context): normalize SPN/objectClass to a list before dlt persistence](https://github.com/SpecterOps/ConfigManBearPig/pull/12) | 🟢 Open |
| 2026-09-08 | SpecterOps/ConfigManBearPig | [#11 fix(http): stop trusting ambient system/environment proxy config](https://github.com/SpecterOps/ConfigManBearPig/pull/11) | 🟢 Open |
| 2026-09-08 | SpecterOps/ConfigManBearPig | [#10 fix(local): gate client-log scrape on the same SCCM-client check as WMI](https://github.com/SpecterOps/ConfigManBearPig/pull/10) | 🟢 Open |
| 2026-09-05 | Mayyhem/ludus_sccm | [#4 Add create_demo_users role for low-priv RDP demo access](https://github.com/Mayyhem/ludus_sccm/pull/4) | 🟢 Open |
| 2026-09-02 | garrettfoster13/sccmhunter | [#137 fix: smb_hunter can crash the entire scan if a single host profiling fails](https://github.com/garrettfoster13/sccmhunter/pull/137) | 🟢 Open |
| 2026-09-01 | garrettfoster13/sccmhunter | [#136 fix: relay attack terminates prematurely and crashes on every attempt](https://github.com/garrettfoster13/sccmhunter/pull/136) | 🟢 Open |
| 2026-09-01 | garrettfoster13/sccmhunter | [#135 fix: require -t, -tu and -ts for relay attack](https://github.com/garrettfoster13/sccmhunter/pull/135) | 🟢 Open |
| 2026-09-01 | garrettfoster13/sccmhunter | [#134 fix: add missing return statement in do_decrypt_parsers,](https://github.com/garrettfoster13/sccmhunter/pull/134) | 🟢 Open |
| 2026-09-01 | garrettfoster13/sccmhunter | [#133 Fix/ldap connection handling](https://github.com/garrettfoster13/sccmhunter/pull/133) | 🟢 Open |
| 2026-08-31 | SpecterOps/ConfigManBearPig | [#9 fix(registry): match hostnames case-insensitively against target_hosts_by_hostname](https://github.com/SpecterOps/ConfigManBearPig/pull/9) | 🟢 Open |
| 2026-08-28 | subat0mik/Misconfiguration-Manager | [#59 Add SCCMHunter implementation to ELEVATE-2](https://github.com/subat0mik/Misconfiguration-Manager/pull/59) | 🟢 Open |
| 2026-08-28 | garrettfoster13/sccmhunter | [#132 Fix SCCM client-push registration and DDR framing](https://github.com/garrettfoster13/sccmhunter/pull/132) | 🟢 Open |
| 2026-08-28 | garrettfoster13/sccmhunter | [#131 fix: pass hostname string, not raw Entry, for resolved computer membe…](https://github.com/garrettfoster13/sccmhunter/pull/131) | 🟢 Open |
| 2026-08-28 | garrettfoster13/sccmhunter | [#130 fix: stop crashing on NETBIOS timeout during SMB profiling (#106)](https://github.com/garrettfoster13/sccmhunter/pull/130) | ⚪ Closed |
| 2026-08-28 | garrettfoster13/sccmhunter | [#129 fix: use Cmd2ArgumentParser so the shell works on cmd2 >=4.0 (#124)](https://github.com/garrettfoster13/sccmhunter/pull/129) | 🟢 Open |
| 2026-08-28 | garrettfoster13/sccmhunter | [#128 fix: remove stray debug print(body) in sessionhunter's do_request](https://github.com/garrettfoster13/sccmhunter/pull/128) | 🟢 Open |
| 2026-08-28 | garrettfoster13/sccmhunter | [#127 fix: decrypt policy on modern SCCM (RSA-OAEP/AES-CBC)](https://github.com/garrettfoster13/sccmhunter/pull/127) | 🟢 Open |
| 2026-08-28 | Mayyhem/ludus_sccm | [#3 Add takeover_9_setup role — deliberate TAKEOVER-9 misconfiguration](https://github.com/Mayyhem/ludus_sccm/pull/3) | 🟢 Open |
| 2026-08-28 | subat0mik/Misconfiguration-Manager | [#58 Document task sequence credential variables beyond the NAA in CRED-1..4](https://github.com/subat0mik/Misconfiguration-Manager/pull/58) | 🟢 Open |
| 2026-08-28 | subat0mik/Misconfiguration-Manager | [#57 Flesh out TAKEOVER-9 with a full description](https://github.com/subat0mik/Misconfiguration-Manager/pull/57) | 🟢 Open |
| 2026-08-28 | subat0mik/Misconfiguration-Manager | [#56 Adding CRED-9 - deobfuscation of credentials stored in SCCM machine variables](https://github.com/subat0mik/Misconfiguration-Manager/pull/56) | 🟢 Open |
| 2026-08-28 | Mayyhem/SharpSCCM | [#65 Use EnumerateDirectories in local triage cache walk](https://github.com/Mayyhem/SharpSCCM/pull/65) | 🟢 Open |
| 2026-08-28 | subat0mik/Misconfiguration-Manager | [#55 Resync attack/defense matrix with technique write-ups](https://github.com/subat0mik/Misconfiguration-Manager/pull/55) | 🟢 Open |
| 2026-08-28 | subat0mik/Misconfiguration-Manager | [#54 Restructure RESOURCES.md into categorized tables](https://github.com/subat0mik/Misconfiguration-Manager/pull/54) | 🟢 Open |
| 2026-08-27 | Mayyhem/SharpSCCM | [#64 Add get policies command](https://github.com/Mayyhem/SharpSCCM/pull/64) | 🟢 Open |
| 2026-08-21 | Mayyhem/ludus_sccm | [#2 Various Ansible fixes and added ESC8](https://github.com/Mayyhem/ludus_sccm/pull/2) | 🟢 Open |
| 2026-05-07 | garrettfoster13/sccmhunter | [#122 Fix SHELL.__init__ missing accache parameter](https://github.com/garrettfoster13/sccmhunter/pull/122) | ⚪ Closed |
| 2026-03-24 | garrettfoster13/sccmhunter | [#116 Feature/kerberos approver auth](https://github.com/garrettfoster13/sccmhunter/pull/116) | 🟣 Merged |
| 2026-03-23 | Mayyhem/SharpSCCM | [#63 Use UTC for application assignment deadlines](https://github.com/Mayyhem/SharpSCCM/pull/63) | 🟣 Merged |
| 2026-03-22 | subat0mik/Misconfiguration-Manager | [#51 Expand CRED-6 to cover credential exposure on other site server shares](https://github.com/subat0mik/Misconfiguration-Manager/pull/51) | 🟣 Merged |
| 2026-03-22 | garrettfoster13/sccmhunter | [#115 Fix approver credential check failing with Kerberos auth](https://github.com/garrettfoster13/sccmhunter/pull/115) | 🟣 Merged |
| 2026-03-09 | garrettfoster13/sccmhunter | [#110 fix: addcomputer exit after failing to create machine account](https://github.com/garrettfoster13/sccmhunter/pull/110) | 🟣 Merged |
| 2026-03-09 | garrettfoster13/sccmhunter | [#109 fix: autopwn to convert computer hash to NTLM password format](https://github.com/garrettfoster13/sccmhunter/pull/109) | 🟣 Merged |
| 2026-03-08 | garrettfoster13/sccmhunter | [#108 fix: make add_admin use SMS00UNA instead of SMS00ALL when adding users to admin](https://github.com/garrettfoster13/sccmhunter/pull/108) | 🟣 Merged |

## BOF / C2 tooling (14)

| Date | Repo | PR | State |
|------|------|-----|-------|
| 2026-03-20 | brmkit/toastnotify-bof | [#1 OC2 compatibility fixes + CNA/OC2 scripts](https://github.com/brmkit/toastnotify-bof/pull/1) | 🟣 Merged |
| 2026-03-08 | coffeegist/bofhound | [#56 Fix TrustDirection/TrustType enum crash with newer bloodhound.py](https://github.com/coffeegist/bofhound/pull/56) | 🟣 Merged |
| 2026-02-26 | outflanknl/C2-Tool-Collection | [#6 Fix Kerberoast BOF crash on wildcard filters and output truncation](https://github.com/outflanknl/C2-Tool-Collection/pull/6) | 🟢 Open |
| 2026-02-10 | trustedsec/CS-Situational-Awareness-BOF | [#151 whoami: Fix various error handling and cleanup issues](https://github.com/trustedsec/CS-Situational-Awareness-BOF/pull/151) | 🟣 Merged |
| 2026-02-10 | trustedsec/CS-Remote-OPs-BOF | [#62 enableuser: Input validation and double semicolons fix](https://github.com/trustedsec/CS-Remote-OPs-BOF/pull/62) | ⚪ Closed |
| 2026-02-10 | trustedsec/CS-Remote-OPs-BOF | [#61 reg_set: Fix bug in cleanup/free](https://github.com/trustedsec/CS-Remote-OPs-BOF/pull/61) | 🟣 Merged |
| 2026-02-10 | trustedsec/CS-Remote-OPs-BOF | [#60 make_token_cert: Fix handle cleanup and NULL check](https://github.com/trustedsec/CS-Remote-OPs-BOF/pull/60) | 🟣 Merged |
| 2026-02-10 | trustedsec/CS-Remote-OPs-BOF | [#59 ghost_task: Fix time/day variable collision when parsing args](https://github.com/trustedsec/CS-Remote-OPs-BOF/pull/59) | 🟣 Merged |
| 2026-02-10 | trustedsec/CS-Remote-OPs-BOF | [#58 adduser: Null checks and input validation fix](https://github.com/trustedsec/CS-Remote-OPs-BOF/pull/58) | ⚪ Closed |
| 2026-02-09 | trustedsec/CS-Remote-OPs-BOF | [#57 addusertogroup: Fix various cleanup/safety and allocation issues ](https://github.com/trustedsec/CS-Remote-OPs-BOF/pull/57) | 🟣 Merged |
| 2026-01-22 | NetSPI/BOF-PE | [#2 Fix standalone arg parsing for directory paths](https://github.com/NetSPI/BOF-PE/pull/2) | 🟣 Merged |
| 2025-10-01 | trustedsec/CS-Situational-Awareness-BOF | [#142 Added LDAP signing and sealing to ldapsearch](https://github.com/trustedsec/CS-Situational-Awareness-BOF/pull/142) | 🟣 Merged |
| 2025-09-29 | trustedsec/CS-Situational-Awareness-BOF | [#141 Add ldapsecuritycheck BOF](https://github.com/trustedsec/CS-Situational-Awareness-BOF/pull/141) | 🟣 Merged |
| 2025-09-22 | trustedsec/CS-Situational-Awareness-BOF | [#139 Fixed OOB error](https://github.com/trustedsec/CS-Situational-Awareness-BOF/pull/139) | 🟣 Merged |

## AD / BloodHound (8)

| Date | Repo | PR | State |
|------|------|-----|-------|
| 2026-09-16 | SpecterOps/MSSQLHound | [#27 Fix IP-address targeting bugs in SID/linked-server resolution](https://github.com/SpecterOps/MSSQLHound/pull/27) | 🟢 Open |
| 2026-09-05 | SpecterOps/TierZeroTable | [#15 Add Entra Connect components](https://github.com/SpecterOps/TierZeroTable/pull/15) | 🟢 Open |
| 2026-09-05 | SpecterOps/TierZeroTable | [#14 Add VMWare vSphere related components](https://github.com/SpecterOps/TierZeroTable/pull/14) | 🟢 Open |
| 2026-05-26 | h4wkst3r/ADOKit | [#8 Fix credsValid to probe a real API endpoint](https://github.com/h4wkst3r/ADOKit/pull/8) | 🟣 Merged |
| 2026-03-23 | SpecterOps/BloodHoundQueryLibrary | [#51 Add "non-tier-zero shortest path to tier zero" queries](https://github.com/SpecterOps/BloodHoundQueryLibrary/pull/51) | 🟣 Merged |
| 2026-03-08 | SpecterOps/BloodHoundQueryLibrary | [#49 Add gMSA Cypher queries for BloodHound CE](https://github.com/SpecterOps/BloodHoundQueryLibrary/pull/49) | ⚪ Closed |
| 2025-11-26 | SpecterOps/TierZeroTable | [#11 Add DHCP administrators](https://github.com/SpecterOps/TierZeroTable/pull/11) | 🟣 Merged |
| 2024-04-23 | xforcered/ADOKit | [#1 Bug fix for whoami command](https://github.com/xforcered/ADOKit/pull/1) | 🟣 Merged |

## Media / indexers (9)

| Date | Repo | PR | State |
|------|------|-----|-------|
| 2021-08-13 | Prowlarr/Prowlarr | [#418 Fixed: (Indexer) PTP IMDB search](https://github.com/Prowlarr/Prowlarr/pull/418) | 🟣 Merged |
| 2021-08-03 | Radarr/Radarr | [#6522 New Language: Chinese (Cantonese) & Chinese (Mandarin) - Lang 35 & 38](https://github.com/Radarr/Radarr/pull/6522) | ⚪ Closed |
| 2021-08-03 | Prowlarr/Prowlarr | [#390 Fixed: (Indexer) Rutracker - multiple languages support](https://github.com/Prowlarr/Prowlarr/pull/390) | ⚪ Closed |
| 2021-08-03 | Prowlarr/Prowlarr | [#389 Fixed: Gazelle search using full IMDb ID](https://github.com/Prowlarr/Prowlarr/pull/389) | 🟣 Merged |
| 2021-08-02 | Prowlarr/Prowlarr | [#387 Fixed: (Indexer) Secret Cinema IMDbId search](https://github.com/Prowlarr/Prowlarr/pull/387) | ⚪ Closed |
| 2021-08-02 | Prowlarr/Prowlarr | [#385 Fix IMDb search for Secret Cinema indexer](https://github.com/Prowlarr/Prowlarr/pull/385) | ⚪ Closed |
| 2021-07-30 | Prowlarr/Prowlarr | [#374 Iptorrents tv episode search fix](https://github.com/Prowlarr/Prowlarr/pull/374) | 🟣 Merged |
| 2021-07-29 | Prowlarr/Prowlarr | [#372 New: (Indexer) - Secret Cinema](https://github.com/Prowlarr/Prowlarr/pull/372) | 🟣 Merged |
| 2021-07-29 | Prowlarr/Prowlarr | [#371 New: (Indexer) Rutracker.org](https://github.com/Prowlarr/Prowlarr/pull/371) | 🟣 Merged |

## Other (5)

| Date | Repo | PR | State |
|------|------|-----|-------|
| 2026-09-16 | praetorian-inc/Sulla | [#18 Add file creation and last-write timestamps to findings](https://github.com/praetorian-inc/Sulla/pull/18) | 🟢 Open |
| 2021-05-24 | ultrarunningdiscord/stravadiscordbot | [#30 fix vert and sorting](https://github.com/ultrarunningdiscord/stravadiscordbot/pull/30) | 🟣 Merged |
| 2021-05-24 | ultrarunningdiscord/stravadiscordbot | [#29 a simple test of vert leaderboard](https://github.com/ultrarunningdiscord/stravadiscordbot/pull/29) | 🟣 Merged |
| 2021-01-18 | RedSiege/C2concealer | [#3 Fixed certbot-auto deprecation](https://github.com/RedSiege/C2concealer/pull/3) | ⚪ Closed |
| 2019-10-23 | seajaysec/cypheroth | [#2 Added support for remote address](https://github.com/seajaysec/cypheroth/pull/2) | ⚪ Closed |

## Original tools (1)

Repos I wrote from scratch, not forks. Manually maintained.

| Tool | Description |
|------|-------------|
| [PXEHacker](https://github.com/chryzsh/PXEHacker) | Original repo, not a fork |

## Forks extended with own commits (5)

Forks where I added real functionality on top of upstream. Manually maintained.

| Date | Fork | Upstream | My changes |
|------|------|----------|------------|
| 2026-08-27 | [sccm-http-looter](https://github.com/chryzsh/sccm-http-looter) | — | NTLM authentication support |
| 2026-08-27 | [go-cmloot](https://github.com/chryzsh/go-cmloot) | — | Add ACL hunting capabilities to find files you should not have access to |
| 2026-08-20 | [SCCM-CVE-2026-47301-Remote-Code-Execution-Exploit](https://github.com/chryzsh/SCCM-CVE-2026-47301-Remote-Code-Execution-Exploit) | OmriBaso/SCCM-CVE-2026-47301-Remote-Code-Execution-Exploit | Added chunked upload support (--chunk-size) + Build-Cab.ps1 helper |
| 2026-03-18 | [hashcat-6.2.6-SCCM](https://github.com/chryzsh/hashcat-6.2.6-SCCM) | The-Viper-One/hashcat-6.2.6-SCCM | Added AES-256 SCCM module (-m 19851) + OpenCL kernel fixes |
| 2026-03-18 | [PXEThief](https://github.com/chryzsh/PXEThief) | MWR-CyberSec/PXEThief | Added Scapy TFTP client, fixed Windows Firewall bypass/cleanup crash |

_Last updated: 2026-09-16 19:06 UTC_
