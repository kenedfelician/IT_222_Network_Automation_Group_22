# IT 222 — Network Automation
## Assignment 22: Data Processing Office Network

# GROUP MEMBERS REGISTRATION NUMBER

| No. | Registration Number |
| --- | ------------------- |
| 01  | 2024/1369           |
| 02  | 2024/1306           |
| 03  | 2024/1572           |
| 04  | 2024/0819           |

**Course:** IT222 — Data Communication and Advanced Networking
**Institution:** St. John's University of Tanzania (SJUT), BSc ICT
**Author:** Baraka Maxmilian Mango (Reg. No. 2024/1369)
**Tools:** GNS3, Python 3, Netmiko

---

## 1. Scenario Overview

Data Processing Company runs two offices — **Site A** and **Site B**. Each office has
two user groups with different roles:

- **DataEntry** — staff who enter data (VLAN 38)
- **Systems** — system administrators (VLAN 48)

Requirements:
- DataEntry and Systems traffic must stay **logically separated** (different VLANs) so
  they don't mix at Layer 2.
- Despite the separation, users must still be able to **communicate across sites**
  (Site A ↔ Site B) over a routed link running **OSPF**.

---

## 2. Topology

```
                    SITE A                                          SITE B
 ┌─────────────────────────────────────┐        ┌─────────────────────────────────────┐
 │  DataEntry-PC1        Systems-PC1    │        │  DataEntry-PC2        Systems-PC2    │
 │  192.168.38.10/24     192.168.48.10  │        │  192.168.138.10/24    192.168.148.10 │
 │  VLAN 38              VLAN 48        │        │  VLAN 38              VLAN 48        │
 │       │                   │          │        │       │                   │          │
 │       └─────┐       ┌─────┘          │        │       └─────┐       ┌─────┘          │
 │          SW1 Gi0/2   SW1 Gi0/3       │        │          SW2 Gi0/2   SW2 Gi0/3       │
 │              \       /                │        │              \       /               │
 │               SW1 (802.1Q trunk)      │        │               SW2 (802.1Q trunk)     │
 │               Gi0/1 ── R1 Gi0/0       │        │               Gi0/1 ── R2 Gi0/0       │
 │                                       │        │                                       │
 │        R1 Gi0/0.38 = 192.168.38.1     │        │        R2 Gi0/0.38 = 192.168.138.1    │
 │        R1 Gi0/0.48 = 192.168.48.1     │        │        R2 Gi0/0.48 = 192.168.148.1    │
 │        R1 Gi0/1 = 10.22.22.1/30 ──────┼── OSPF ─┼──── 10.22.22.2/30 = R2 Gi0/1          │
 └───────────────────────────────────────┘  Area 0 └───────────────────────────────────────┘
```

**Devices used in GNS3:**

| Role | Device | Count |
|---|---|---|
| Router | c3725 / c7200 / IOSv | 2 (R1, R2) |
| Switch | GNS3 built-in / IOSvL2 Ethernet Switch | 2 (SW1, SW2) |
| End host | VPCS | 4 (DataEntry-PC1/2, Systems-PC1/2) |

---

## 3. IP Addressing & VLAN Table

| Device | Interface | VLAN | Address / Role |
|---|---|---|---|
| R1 | Gi0/0 (trunk → SW1) | 38, 48 | 802.1Q trunk |
| R1 | Gi0/0.38 | 38 – DataEntry | 192.168.38.1/24 (Site A gateway) |
| R1 | Gi0/0.48 | 48 – Systems | 192.168.48.1/24 (Site A gateway) |
| R1 | Gi0/1 | — | 10.22.22.1/30 (link to R2) |
| R2 | Gi0/0 (trunk → SW2) | 38, 48 | 802.1Q trunk |
| R2 | Gi0/0.38 | 38 – DataEntry | 192.168.138.1/24 (Site B gateway) |
| R2 | Gi0/0.48 | 48 – Systems | 192.168.148.1/24 (Site B gateway) |
| R2 | Gi0/1 | — | 10.22.22.2/30 (link to R1) |
| SW1 | Gi0/1 | Trunk (38, 48) | → R1 |
| SW1 | Gi0/2 | 38 – DataEntry | → DataEntry-PC1 (192.168.38.10/24) |
| SW1 | Gi0/3 | 48 – Systems | → Systems-PC1 (192.168.48.10/24) |
| SW2 | Gi0/1 | Trunk (38, 48) | → R2 |
| SW2 | Gi0/2 | 38 – DataEntry | → DataEntry-PC2 (192.168.138.10/24) |
| SW2 | Gi0/3 | 48 – Systems | → Systems-PC2 (192.168.148.10/24) |

OSPF Process 1, Area 0 advertises: `192.168.38.0/24`, `192.168.48.0/24`,
`192.168.138.0/24`, `192.168.148.0/24`, and `10.22.22.0/30`.

> **⚠ Correction note:** Earlier drafts of `r2_config.py` had R2's trunk and
> R1-link interfaces swapped (trunk on Gi0/1, R1-link on Gi0/0), based on an
> unverified assumption about SW2's cabling. The official assignment spec
> confirms R2 must **mirror R1 exactly** — trunk on `Gi0/0`, routed link on
> `Gi0/1`. This has been corrected in the current scripts.

---

## 4. GNS3 Cabling

| From | To |
|---|---|
| R1 Gi0/0 | SW1 Gi0/1 (trunk) |
| SW1 Gi0/2 | DataEntry-PC1 (VPCS1) |
| SW1 Gi0/3 | Systems-PC1 (VPCS2) |
| R1 Gi0/1 | R2 Gi0/1 (routed link, 10.22.22.0/30) |
| R2 Gi0/0 | SW2 Gi0/1 (trunk) |
| SW2 Gi0/2 | DataEntry-PC2 (VPCS3) |
| SW2 Gi0/3 | Systems-PC2 (VPCS4) |

GNS3 host: `192.168.15.128`. Console (TELNET) ports per device — check GNS3's
**Topology Summary** panel, as they vary per project (e.g. R1: 5005, R2: 5007,
SW1: 5019, SW2: 5022 in this project's current session).

---

## 5. Credentials

All four devices use the same local login, created by the `*_config.py` scripts:

| Field | Value |
|---|---|
| Username | `admin22` |
| Password | `Admin@2226` |
| Enable secret | `Enable@2226` |

On a device's **first-ever run**, leave `username`/`password`/`secret` blank in the
script (the device has no login yet). On any run **after** that, fill them in —
otherwise Netmiko's login will fail against a device that already expects them.

---

## 6. Project Scripts

| Script | Purpose |
|---|---|
| `r1_config.py` | Applies hostname, login, VLAN subinterfaces, routed link, and OSPF on R1 |
| `r2_config.py` | Same, for R2 |
| `sw1_config.py` | Applies hostname, login, VLANs 38/48, trunk, and access ports on SW1 |
| `sw2_config.py` | Same, for SW2 |
| `r1_verify.py` / `r2_verify.py` | Runs `show ip interface brief`, `show running-config`, `show ip route`, `show ip protocols`, `show ip ospf neighbor` |
| `r2_test.py` | Pings the routed link and Site A gateways from R2, plus a traceroute — proves inter-site OSPF reachability |

Each script follows the same structure: connect via Netmiko → apply/verify config →
print output → save config (config scripts only) → disconnect, wrapped in
try/except for timeout, auth, and general errors.

---

## 7. Known Issue: Slow GNS3 Host

This project's GNS3 host has run at up to ~95% RAM during testing, which causes
console output to lag. That triggers a few Netmiko failure modes that **are not
configuration bugs** — they're timing issues:

| Symptom | Cause | Fix applied |
|---|---|---|
| `Pattern not detected: 'command text'` during config push | Netmiko's per-line echo check (`cmd_verify`) times out on a slow echo | `cmd_verify=False` on `send_config_set` |
| `Pattern not detected: 'terminal width 511'` | Netmiko's own startup command (disable paging) times out | `read_timeout_override=60` on the connection |
| Timeout on `show running-config` | Long output, default read window too short | `read_timeout=60–120` on `send_command` |
| Garbled/partial reads generally | Console can't keep up with Netmiko's default fast timing | `fast_cli=False`, `global_delay_factor=2–4` |

If scripts still fail after these settings, the most effective next step is
freeing RAM on the GNS3 VM host (closing other apps/VMs) — the settings above
give Netmiko more patience, but they can't fix a genuinely overloaded host.

---

## 8. Run Order

1. Start all devices in GNS3 and wait for them to fully boot.
2. `sw1_config.py` → `sw2_config.py`
3. `r1_config.py` → `r2_config.py`
4. `r1_verify.py` → `r2_verify.py` — confirm subinterfaces are up and
   `show ip ospf neighbor` shows the other router as **FULL**.
5. `r2_test.py` — confirm ping/traceroute reachability to Site A.
6. From the actual PCs (VPCS), ping across sites to get final end-to-end proof
   (e.g. DataEntry-PC1 → DataEntry-PC2).

---

## 9. Requirements Verification Matrix

| Requirement | Configuration | Verification command | Test |
|---|---|---|---|
| Separate DataEntry & Systems | VLAN 38/48, access ports | `show vlan brief`, `show interfaces status` | Confirm PCs are on the correct VLAN |
| Carry both VLANs to router | 802.1Q trunk SW↔R | `show interfaces trunk` (switch side only — not valid on routers) | Confirm VLAN 38/48 pass over trunk |
| Inter-VLAN routing within a site | Router subinterfaces (.38/.48) | `show ip interface brief` | DataEntry-PC1 ping Systems-PC1 |
| Site A ↔ Site B connectivity | Routed link R1–R2 + OSPF | `show ip ospf neighbor`, `show ip route` | DataEntry-PC1 ping DataEntry-PC2; Systems-PC1 ping Systems-PC2 |

---

## 10. Prerequisites

```
pip install netmiko
```

GNS3 project must be running with all devices started before executing any script.

---

## 11. Next Steps

- [ ] Write `sw1_verify.py` / `sw2_verify.py` (VLAN, trunk, port status)
- [ ] Write `sw1_test.py` / `sw2_test.py` (local intra-VLAN + intra-site pings)
- [ ] Write `network_test.py` — full cross-site DataEntry/Systems connectivity test
- [ ] Write `network_verify.py` — single script confirming the whole topology end to end
