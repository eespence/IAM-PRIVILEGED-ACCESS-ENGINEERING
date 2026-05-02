# Tiered Administration Model

**Lab:** IAMPAM.LAB | **Status:** ✅ Complete | **Completed:** March 2026

---

Enforcing administrative tier isolation is one of the most critical controls in a privileged access management architecture. Without hard boundaries between administrative tiers, a compromised low-privilege account can be used to move laterally and eventually reach domain-level assets.

This module implements a three-tier administrative boundary using Active Directory OU scoping and GPO-based deny logon controls across the IAMPAM.LAB environment.

---

## The Tier Model

| Tier | Systems | Role |
|---|---|---|
| Tier 0 | DC01 | Domain Controller — Identity Infrastructure |
| Tier 1 | MGMT01, ID-SYNC01 | Administrative Servers |
| Tier 2 | CLIENT01 | User Workstations |

Higher-tier credentials must never authenticate on lower-tier systems. This is enforced through Group Policy — not just policy documentation.

---

## How Enforcement Works

Three GPOs were created and linked to each tier:

- **GPO-Tier0-Logon-Restrictions** — denies Tier 1 and Tier 2 admins from logging on to DC01
- **GPO-Tier1-Logon-Restrictions** — denies Tier 0 and Tier 2 admins from logging on to MGMT01 and ID-SYNC01
- **GPO-Tier2-Logon-Restrictions** — denies Tier 0 and Tier 1 admins from logging on to CLIENT01

Each GPO uses a deny-based enforcement model applied through User Rights Assignment — specifically the **Deny log on locally** policy setting.

[ SCREENSHOT: module02-04-tier0-gpo ]

---

## OU Structure

Active Directory OUs were created to scope GPO enforcement to the correct systems:

- **IAM-PAM-Tier1-Servers** — contains MGMT01 and ID-SYNC01
- **IAM-PAM-Tier2-Workstations** — contains CLIENT01
- DC01 remains in the default Domain Controllers OU

[ SCREENSHOT: module02-03-tier-ou-structure ]

---

## Group Membership Validation

Logon control groups were created and validated before GPO enforcement was applied:

- `adm-t0-administrator` → PAM-Tier0-Logon-Allowed
- `adm-t1-serveradmin` → PAM-Tier1-Logon-Allowed
- `adm-t2-helpdesk` → PAM-Tier2-Logon-Allowed

[ SCREENSHOT: module02-02-logon-group-membership ]

---

## GPO Validation

After enforcement GPOs were applied and validated using:

```powershell
gpresult /r
```

[ SCREENSHOT: module02-08-gpo-validation ]

---

## MITRE ATT&CK Alignment

| Technique | Threat Mitigated |
|---|---|
| T1021 | Lateral Movement |
| T1078 | Valid Account Abuse |
| T1550.002 | Pass-the-Hash |
| T1068 | Privilege Escalation |
| T1110 | Brute Force |

---

## Validation Results

Every cross-tier login denial was validated:

- Tier 2 login to DC01 — Denied ✔
- Tier 1 login to DC01 — Denied ✔
- Tier 0 login to MGMT01 — Allowed ✔
- Tier 1 login to MGMT01 — Allowed ✔
- Tier 2 login to MGMT01 — Denied ✔
- Tier 0 login to CLIENT01 — Denied ✔
- Tier 2 login to CLIENT01 — Allowed ✔

---

## Why This Matters

Without tier isolation a single compromised helpdesk account can become a path to domain compromise. This implementation ensures that credential theft on a lower-tier system cannot be weaponized against higher-tier infrastructure — directly mitigating pass-the-hash and lateral movement attack paths.

---

👉 **[View Full Module on GitHub](https://github.com/eespence/IAM-PRIVILEGED-ACCESS-ENGINEERING)**

---

**E.E. Spence — PAM Engineering | IAMPAM.LAB**