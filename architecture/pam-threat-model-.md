← [Back to Main README](../README.md)

![Proxmox](https://img.shields.io/badge/Proxmox-E57000?style=flat\&logo=proxmox\&logoColor=white)
![Windows Server](https://img.shields.io/badge/Windows_Server_2022-0078D4?style=flat\&logo=windows\&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu_22.04-E95420?style=flat\&logo=ubuntu\&logoColor=white)
![HashiCorp Vault](https://img.shields.io/badge/HashiCorp_Vault-000000?style=flat\&logo=vault\&logoColor=white)
![Splunk](https://img.shields.io/badge/Splunk-000000?style=flat\&logo=splunk\&logoColor=white)

**Status:** ✅ Complete

# pam-threat-model.md — IAMPAM.LAB

**Author:** Edward E. Spence
**Lab:** IAMPAM.LAB
**Repo:** IAM-PRIVILEGED-ACCESS-ENGINEERING
**Version:** 1.3
**Last Updated:** 2026-04-03

---

## 1. Purpose of the PAM Threat Model

This document defines the privileged access threat landscape within the IAMPAM.LAB environment and models realistic attack paths against identity, credential, and PAM systems.

The goal is to evaluate how an attacker would exploit:

* privileged credentials
* administrative pathways
* application-layer PAM systems

and how the implemented controls mitigate those risks.

---

## 2. Scope

**Network:** 172.31.100.0/24

### Privileged Systems

* DC01 — Domain Controller — 172.31.100.10
* MGMT01 — Privileged Access Workstation — 172.31.100.20
* LINUX01 — Privileged Linux Server — 172.31.100.40
* PAMVAULT01 — HashiCorp Vault — 172.31.100.70
* DELINEA01 — Secret Server — 172.31.100.80
* PAM01 — PAM support node — 172.31.100.50

### Supporting Systems

* CLIENT01 — User Workstation — 172.31.100.30
* ID-SYNC01 — Identity Sync — 172.31.100.25
* SIEM01 — Splunk Enterprise — 172.31.100.60

---

## 3. Protected Assets

* Domain Admin credentials
* Vault secrets
* SSH keys
* Kerberos tickets
* Administrative sessions
* PAM workflows (Vault + Delinea)
* SIEM telemetry

---

## 4. Threat Actors

* External attacker via CLIENT01 foothold
* Malicious insider
* Compromised admin workstation
* Credential harvesting malware
* Advanced persistent threat (APT)

---

## 5. Threat Scenarios (Environment-Specific)

### 5.1 Privileged Credential Theft

An attacker gains access to CLIENT01 and attempts credential harvesting (e.g., LSASS dumping or token theft). Without proper controls, these credentials could be reused to access MGMT01 or Tier 0 systems.

---

### 5.2 Credential Reuse

An administrator reuses credentials across systems, allowing an attacker who compromises LINUX01 or CLIENT01 to reuse credentials against DC01 or Vault.

---

### 5.3 Lateral Movement

An attacker pivots from CLIENT01 using valid credentials to attempt access to MGMT01, LINUX01, or DC01 through RDP, WinRM, or SSH.

---

### 5.4 Non-Hardened Administrative Access

Administrative actions are attempted from CLIENT01 instead of MGMT01, exposing privileged credentials to an untrusted endpoint.

---

### 5.5 Standing Privilege Abuse

Accounts retain persistent elevated privileges, enabling attackers to maintain access after initial compromise.

---

### 5.6 Unauthorized Secret Retrieval

An attacker attempts to access Vault or Delinea APIs directly to retrieve credentials without going through MGMT01.

---

### 5.7 Secret Sprawl

Credentials are stored outside Vault (e.g., scripts, configs), allowing attackers to harvest secrets without interacting with PAM systems.

---

### 5.8 Inadequate Monitoring

An attacker performs low-volume credential abuse that is not detected due to reliance on a single log source.

---

### 5.9 Web-Based PAM Abuse (Delinea)

An attacker targets DELINEA01 via HTTP requests, exploiting IIS authentication behavior where failed logins may not generate Event ID 4625 locally.

---

## 6. Attack Paths of Concern

* CLIENT01 → Credential Theft → MGMT01 → DC01
* CLIENT01 → SSH Pivot → LINUX01
* MGMT01 compromise → full Tier 0 access
* Vault token theft → credential exposure
* DELINEA01 → IIS abuse → AD authentication

---

## 7. Security Controls (With Implementation References)

| Threat              | Control                | Implementation                    |
| ------------------- | ---------------------- | --------------------------------- |
| Credential Theft    | Credential isolation   | Vault (Module 05)                 |
| Credential Reuse    | Centralized secrets    | Vault policies (Module 05)        |
| Lateral Movement    | Tier model enforcement | Module 03 + tiered-admin-model.md |
| Non-Hardened Access | MGMT01 enforcement     | Module 02, 03, 06                 |
| Standing Privilege  | RBAC controls          | Module 02                         |
| Secret Sprawl       | Vault-only storage     | Module 05                         |
| Unauthorized Access | Vault + Delinea auth   | Module 05, 06                     |
| Monitoring Gaps     | SIEM correlation       | Module 07                         |
| Automation Response | Alert-driven logging   | Module 08                         |

---

## 8. Risk Rating (Likelihood vs Impact)

| Threat              | Likelihood | Impact   |
| ------------------- | ---------- | -------- |
| Credential Theft    | High       | Critical |
| Credential Reuse    | Medium     | High     |
| Lateral Movement    | High       | Critical |
| Non-Hardened Access | Medium     | High     |
| Standing Privilege  | Medium     | High     |
| Secret Sprawl       | Low        | Critical |
| Vault Compromise    | Low        | Critical |
| Delinea Abuse       | Medium     | High     |
| Monitoring Failure  | Medium     | High     |

---

## 9. Vault-Specific Threat Considerations

* token leakage
* policy misconfiguration
* API abuse

Vault compromise results in full credential exposure.

---

## 10. Delinea-Specific Threat Considerations

Authentication may occur at:

* IIS
* AD (DC01)

### Critical Insight

* 4625 events may not exist
* detection requires:

  * IIS logs
  * DC logs
  * Splunk correlation

---

## 11. Administrative Workstation Risk

MGMT01 compromise = full control path exposure.

---

## 12. Monitoring Strategy

Requires:

* multi-source log correlation
* SIEM visibility
* consistent admin path

---

## 13. Detection Strategy

```spl id="x7b4mc"
(index=iis host=DELINEA01 sc_status=401) OR
(index=wineventlog EventCode=4625 host=DELINEA01) OR
(index=wineventlog EventCode=4625 host=DC01)
| stats count by _time span=5m
| where count >= 3
```

---

## 14. MITRE ATT&CK Mapping

| Threat              | Technique |
| ------------------- | --------- |
| Credential Theft    | T1003     |
| Lateral Movement    | T1021     |
| Valid Accounts      | T1078     |
| Credential Exposure | T1552     |
| Auth Manipulation   | T1556     |

---

## 15. Assumptions and Validation

Assumptions:

* MGMT01 enforced as admin origin
* Vault controls secrets
* SIEM ingestion is functional

Validation:

* Confirmed through Module 09 architecture validation

---

## 16. Enterprise Alignment (Mapped)

| Framework             | Implementation                  |
| --------------------- | ------------------------------- |
| Zero Trust            | No implicit trust between tiers |
| Tier Model            | Tier 0/1/2 enforced             |
| PAM                   | Vault + Delinea                 |
| Detection Engineering | Splunk correlation              |
| Least Privilege       | RBAC + controlled access        |
| Credential Security   | Vault centralization            |

---

## 17. Final Risk Posture

After applying all controls, the environment significantly reduces exposure to credential theft and lateral movement by enforcing centralized secret management, strict administrative access paths, and multi-source detection. However, residual risk remains in areas such as MGMT01 compromise, Vault misconfiguration, and application-layer authentication gaps in Delinea. The architecture shifts risk from uncontrolled credential exposure to tightly monitored control points, making attacks more detectable and limiting their blast radius.

---

**E.E. Spence — PAM Engineering | IAMPAM.LAB**
