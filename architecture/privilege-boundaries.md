← [Back to Main README](../README.md)

![HashiCorp Vault](https://img.shields.io/badge/HashiCorp_Vault-1.16-black?style=flat\&logo=vault\&logoColor=white)
![PAM](https://img.shields.io/badge/Privileged_Access_Management-red?style=flat)
![Zero Trust](https://img.shields.io/badge/Zero_Trust-Aligned-blue?style=flat)

**Status:** ✅ Complete

# privilege-boundaries.md — IAMPAM.LAB

**Author:** Edward E. Spence
**Lab:** IAMPAM.LAB
**Repo:** IAM-PRIVILEGED-ACCESS-ENGINEERING
**Version:** 1.2
**Last Updated:** 2026-04-03

---

## 1. Purpose of Privilege Boundaries

This document defines and enforces **privilege separation, trust boundaries, and access control constraints** within the IAMPAM.LAB environment.

The objective is to ensure that:

* credentials are never exposed outside controlled boundaries
* administrative actions are restricted to approved systems
* identity systems, application systems, and credential systems remain isolated
* privilege escalation is intentional, controlled, and observable

---

## 2. Scope

**Network:** 172.31.100.0/24

| System     | Role                            | IP            |
| ---------- | ------------------------------- | ------------- |
| DC01       | Domain Controller               | 172.31.100.10 |
| MGMT01     | Administrative Workstation      | 172.31.100.20 |
| CLIENT01   | User Workstation                | 172.31.100.30 |
| LINUX01    | Privileged Linux Server         | 172.31.100.40 |
| ID-SYNC01  | Identity Sync                   | 172.31.100.25 |
| SIEM01     | Monitoring (Splunk)             | 172.31.100.60 |
| PAMVAULT01 | Vault (Secrets Authority)       | 172.31.100.70 |
| DELINEA01  | Application PAM (Secret Server) | 172.31.100.80 |
| PAM01      | PAM support component           | 172.31.100.50 |

---

## 3. Core Trust Boundaries

1. Administrative Boundary
2. Credential Boundary
3. Endpoint Trust Boundary
4. Vault Trust Boundary
5. Application Boundary
6. Monitoring Boundary

---

## 4. Administrative Boundary

* All privileged actions originate from MGMT01
* No administrative activity from CLIENT01

**Enforcement:**

* Tiered admin model (Module 02)
* Access path enforcement (Module 03, 06)

---

## 5. Credential Boundary

* Credentials stored only in Vault
* No persistence on endpoints

**Enforcement:**

* Vault KV engine + policies (Module 05)

---

## 6. Endpoint Trust Boundary

| System   | Trust Level |
| -------- | ----------- |
| MGMT01   | Trusted     |
| CLIENT01 | Untrusted   |

**Principle:**
CLIENT01 is treated as a potential breach point.

---

## 7. Vault Trust Boundary

Vault separates identity from secrets.

**Core Principle:**

> Identity ≠ Authorization

**Enforcement:**

* token-based auth
* policy-controlled access
* centralized secret lifecycle

---

## 8. Application Boundary (Delinea)

### Risks

* Application-layer authentication bypass
* IIS exposure
* Session/token misuse

### Mitigations

| Risk           | Mitigation                                              |
| -------------- | ------------------------------------------------------- |
| Auth bypass    | AD-backed authentication + role enforcement (Module 06) |
| IIS exposure   | limited admin origin (MGMT01) + monitoring              |
| Session misuse | SIEM correlation + centralized logging                  |

### Key Insight

Authentication may not generate 4625 locally → requires multi-source detection.

---

## 9. Monitoring Boundary

SIEM01 provides observability only.

**Principle:**

> Observability must never become control authority

---

## 10. Identity vs PAM Plane Separation

| Plane    | Function                       |
| -------- | ------------------------------ |
| Identity | Authentication                 |
| PAM      | Credential control + execution |

---

## 11. Approved vs Denied Relationships

### Approved

* MGMT01 → privileged systems
* Vault → credential delivery
* Delinea → brokered access

### Denied

* CLIENT01 → admin access
* SIEM01 → control actions
* direct credential storage outside Vault

---

## 12. MITRE ATT&CK Alignment

| Boundary            | Threat              | Technique |
| ------------------- | ------------------- | --------- |
| Admin Boundary      | Lateral Movement    | T1021     |
| Credential Boundary | Credential Dumping  | T1003     |
| Endpoint            | Valid Accounts      | T1078     |
| Vault               | Credential Exposure | T1552     |
| Application         | Auth Abuse          | T1556     |
| Monitoring          | Defense Evasion     | T1562     |

---

## 13. Threat Reduction Outcomes

* credential theft reduced via Vault
* lateral movement restricted via MGMT01
* application-layer visibility via Delinea + SIEM

---

## 14. Enterprise Alignment (Mapped)

| Framework             | Implementation                  |
| --------------------- | ------------------------------- |
| Zero Trust            | no implicit trust across tiers  |
| PAM                   | Vault + Delinea                 |
| Tier Model            | strict 0/1/2 separation         |
| Least Privilege       | RBAC + controlled escalation    |
| Detection Engineering | Splunk multi-source correlation |

---

## 15. Assumptions and Limitations

### Assumptions

* MGMT01 is enforced
* Vault policies applied
* SIEM ingestion functional

### Limitations

The lab uses **logical segmentation only** within a single subnet (172.31.100.0/24).

In a production environment, this would be strengthened by:

* VLAN segmentation between tiers
* firewall enforcement between zones
* hardware-backed secrets (HSM)
* network-level PAM isolation

This limitation means boundary enforcement is **host- and policy-based rather than network-enforced**, increasing reliance on correct configuration.

---

## 16. Cross-Module Mapping

| Boundary         | Module    |
| ---------------- | --------- |
| Infrastructure   | Module 01 |
| Identity Control | Module 02 |
| Linux Controls   | Module 03 |
| Logging          | Module 04 |
| Vault Boundary   | Module 05 |
| Delinea Boundary | Module 06 |
| Monitoring       | Module 07 |
| Automation       | Module 08 |

---

## 17. Final Summary

The IAMPAM.LAB privilege boundary model enforces strict separation between identity systems, credential systems, application-layer PAM platforms, and user endpoints. Administrative access is constrained to MGMT01, Vault acts as the central authority for secrets, and Delinea introduces a controlled application-layer access plane. SIEM01 provides visibility without control authority, ensuring monitoring does not become a trust escalation path. While the lab relies on logical segmentation rather than network isolation, the enforced boundaries significantly reduce credential exposure, limit lateral movement, and ensure that privileged access remains controlled, observable, and auditable.

---

**E.E. Spence — PAM Engineering | IAMPAM.LAB**
