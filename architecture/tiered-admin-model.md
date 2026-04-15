← [Back to Main README](../README.md)

![Active Directory](https://img.shields.io/badge/Active_Directory-0078D4?style=flat\&logo=microsoft\&logoColor=white)
![HashiCorp Vault](https://img.shields.io/badge/HashiCorp_Vault-1.16-black?style=flat\&logo=vault\&logoColor=white)
![Zero Trust](https://img.shields.io/badge/Zero_Trust-Aligned-blue?style=flat)

**Status:** ✅ Complete

# tiered-admin-model.md — IAMPAM.LAB

**Author:** Edward E. Spence
**Lab:** IAMPAM.LAB
**Repo:** IAM-PRIVILEGED-ACCESS-ENGINEERING
**Version:** 1.3
**Last Updated:** 2026-04-03

---

## 1. Purpose of the Tiered Administration Model

The Tiered Administration Model defines how administrative privileges are segmented, controlled, and isolated across the IAMPAM.LAB environment.

Its purpose is to enforce **controlled privilege execution**, not just identity assignment.

This model is designed to:

* prevent privileged credentials from crossing trust boundaries
* restrict where administrative actions are allowed to originate
* reduce lateral movement and privilege escalation paths
* separate user activity from privileged operations

---

## 2. Scope

**Network:** 172.31.100.0/24

**Systems in Scope:**

| System     | OS                        | Role                                                                   | IP            |
| ---------- | ------------------------- | ---------------------------------------------------------------------- | ------------- |
| DC01       | Windows Server 2022       | Domain Controller                                                      | 172.31.100.10 |
| MGMT01     | Windows Server 2022       | Privileged Access Workstation (PAW)                                    | 172.31.100.20 |
| CLIENT01   | Windows 11                | Standard User Workstation                                              | 172.31.100.30 |
| LINUX01    | Ubuntu Server 22.04.4 LTS | Privileged Linux Server                                                | 172.31.100.40 |
| ID-SYNC01  | Windows Server 2022       | Entra Connect / Identity Sync                                          | 172.31.100.25 |
| SIEM01     | Ubuntu Server 22.04.4 LTS | Splunk Enterprise 9.2                                                  | 172.31.100.60 |
| PAMVAULT01 | Ubuntu Server 22.04.4 LTS | HashiCorp Vault 1.16 OSS / Secrets Authority                           | 172.31.100.70 |
| DELINEA01  | Windows Server            | Secret Server (IIS-based PAM Platform)                                 | 172.31.100.80 |
| PAM01      | Windows Server            | Privileged Access Management support node / PAM architecture component | 172.31.100.50 |

This model governs:

* administrative login locations
* credential usage boundaries
* system-to-system administrative access
* privileged identity handling

For full architecture context, see Module 09.

---

## 3. Tiering Strategy Overview

The environment follows a **three-tier administrative model**, aligned with enterprise Active Directory and PAM design principles:

| Tier   | Function                                       |
| ------ | ---------------------------------------------- |
| Tier 0 | Identity and security control plane            |
| Tier 1 | Servers, PAM platforms, and monitoring systems |
| Tier 2 | Standard user endpoints                        |

**Key Principle:**

> Credentials from a higher tier must never be exposed to a lower tier system.

---

## 4. System Classification

### Tier 0

* DC01
* PAMVAULT01
* ID-SYNC01

### Tier 1

* LINUX01
* SIEM01
* DELINEA01
* PAM01

### Tier 2

* CLIENT01

### Control Plane

* MGMT01 (Privileged Access Workstation)

MGMT01 functions as a **tier control point** rather than a normal workload host. It is the approved administrative origin for Tier 0 and Tier 1 access.

---

## 5. Identity Classification

### Tier 0 Identities

* Domain Admin
* Enterprise Admin
* Vault Admin

### Tier 1 Identities

* Server Admin
* Linux sudo users
* Application administrators

### Tier 2 Identities

* Standard users

**Enforcement Principle:**
Tier 0 identities must only be used from MGMT01. Tier 1 identities must not be used on CLIENT01. Tier 2 identities must never be granted administrative access.

---

## 6. Approved Administrative Access Paths (With Enforcement)

### Windows Administration — Tier 0

MGMT01 → DC01

* Protocols: RDP, WinRM
* Enforcement:

  * restricted logon rights via GPO
  * firewall scoping for management access
  * admin groups limited to controlled systems

### Identity Synchronization Administration — Tier 0

MGMT01 → ID-SYNC01

* Protocols: RDP, WinRM
* Enforcement:

  * administrative access limited to MGMT01
  * privileged identities restricted to PAW usage

### Linux Administration — Tier 1

MGMT01 → LINUX01

* Protocol: SSH
* Enforcement:

  * SSH access restricted through host-level policy and source control
  * SSSD for AD identity integration
  * sudo group for controlled privilege escalation

(Implemented in Module 03)

### Vault Administration — Tier 0

MGMT01 → PAMVAULT01

* Protocols: Vault CLI / API
* Enforcement:

  * token-based authentication
  * policy-based secret access
  * centralized audit logging

(Implemented in Module 05)

### Delinea Administration — Tier 1

MGMT01 → DELINEA01

* Protocol: HTTPS (IIS web interface)
* Enforcement:

  * AD-backed authentication
  * role-based application access
  * controlled admin origin from MGMT01

(Implemented in Module 06)

### SIEM Administration — Tier 1

MGMT01 → SIEM01

* Protocols: SSH, Splunk Web
* Enforcement:

  * administrative access restricted to trusted admin origin
  * SIEM remains observability-focused, not identity-authoritative

---

## 7. Disallowed Access Paths (With Enforcement)

| Path                                    | Enforcement                                             |
| --------------------------------------- | ------------------------------------------------------- |
| CLIENT01 → DC01                         | GPO logon restrictions, admin path policy               |
| CLIENT01 → PAMVAULT01                   | network restriction + Vault auth requirements           |
| CLIENT01 → DELINEA01 admin functions    | role-based denial + no privileged identity use          |
| CLIENT01 → LINUX01 admin access         | SSH restrictions + no sudo rights                       |
| Tier 0 credentials on CLIENT01          | PAW-only admin practice + identity separation           |
| Direct privileged access outside MGMT01 | tier model enforcement + administrative process control |

**Key Rule:**

> No privileged administrative action originates from CLIENT01.

---

## 8. Administrative Workstation Enforcement (MGMT01)

MGMT01 is the **only authorized administrative workstation**.

### Controls

* dedicated administrative use only
* privileged sessions originate here
* separation from standard user activity

### Implementation Notes

These controls are enforced operationally through the PAW model and supported by the access path restrictions documented in Modules 02, 03, 05, and 06. The lab does not treat MGMT01 as a general-purpose endpoint.

### Security Outcome

* reduces credential leakage risk
* centralizes privileged activity
* makes admin paths auditable and predictable

---

## 9. Linux Administration (Module 03 Alignment)

LINUX01 is a Tier 1 system and is administered through controlled Linux access practices.

### Implemented Controls

* SSSD integrated with AD for centralized identity
* SSH-based administration from MGMT01
* sudo-based privilege escalation instead of shared root access
* no unrestricted administrative access from CLIENT01

### Enforcement Result

* identity-aware Linux administration
* no standing domain-admin credential reuse on Linux
* reduced pivot potential through controlled elevation

---

## 10. Vault Administration (Module 05 Alignment)

PAMVAULT01 is treated as a **Tier 0 secrets authority**.

### Architecture

* authentication: token-based access
* authorization: policy-driven secret access
* secret engine: KV-based secret storage in lab implementation

### Access Model

* administration originates from MGMT01
* secrets are retrieved on demand
* secrets are not stored persistently on endpoints

### Security Result

Vault functions as the authoritative credential boundary. Access to identity systems does not automatically grant access to secrets.

---

## 11. Delinea Administration (Module 06 Alignment)

DELINEA01 is a **Tier 1 application-layer PAM platform**.

### Role in the Tier Model

* provides web-based privileged access workflows
* brokers access to sensitive credentials and systems
* sits below the identity control plane but above standard endpoints

### Logging and Authentication Consideration

Delinea authentication behavior differs from OS-level authentication:

* some failures remain at IIS / application layer
* Event ID 4625 is not always generated locally
* detection may require IIS logs, DC logs, and Splunk correlation

### Security Result

Delinea is treated as a controlled administrative platform, not a trust root. Its access must still originate from MGMT01 and be monitored centrally.

---

## 12. Security Benefits (How They Are Achieved)

### Credential Isolation

Achieved through Vault centralization and PAW-only credential use.

### Lateral Movement Reduction

Achieved through tier separation, MGMT01-only admin paths, and denial of privileged activity from CLIENT01.

### Controlled Escalation

Achieved through:

* sudo on Linux
* Vault-mediated secret access
* Delinea-brokered administrative workflows

### Auditability

Achieved through centralized logging in SIEM01 and predictable privileged access paths.

---

## 13. MITRE ATT&CK Alignment

| Control                          | Threat Mitigated                    | Technique |
| -------------------------------- | ----------------------------------- | --------- |
| Tier Isolation                   | Valid account abuse across tiers    | T1078     |
| Lateral Movement Controls        | Remote administration abuse         | T1021     |
| Credential Protection            | Credential dumping / theft          | T1003     |
| Vault Control Boundary           | Unsecured credentials               | T1552     |
| Application-Layer PAM Monitoring | Authentication abuse / modification | T1556     |

---

## 14. Enterprise Alignment (Real Mapping)

| Framework / Model    | Lab Implementation                                                        |
| -------------------- | ------------------------------------------------------------------------- |
| Microsoft Tier Model | Tier 0/1/2 separation across DC, PAM, servers, and endpoints              |
| PAW Model            | MGMT01 as dedicated privileged admin origin                               |
| Zero Trust           | no implicit trust between endpoint, identity, and PAM layers              |
| PAM Architecture     | Vault as credential authority, Delinea as application-layer PAM interface |

This is not just terminology reuse. Each control in the lab maps to a real enforcement boundary or administrative path.

---

## 15. Diagram Reference

![Architecture](../architecture/iampam-pam-architecture.png)

The diagram visualizes:

* tier separation
* admin paths
* credential boundaries
* identity vs PAM control planes

---

## 16. Cross-Module Implementation Mapping

| Control                            | Module    |
| ---------------------------------- | --------- |
| Infrastructure                     | Module 01 |
| Active Directory                   | Module 02 |
| Linux Identity and Access Controls | Module 03 |
| Logging Foundations                | Module 04 |
| Vault PAM Controls                 | Module 05 |
| Delinea PAM Controls               | Module 06 |
| Monitoring and Detection           | Module 07 |
| Alert-Driven Automation            | Module 08 |

---

## 17. Final Summary

The tiered administration model in IAMPAM.LAB is not just a labeling exercise. It defines where privileged identities may be used, where administrative actions may originate, and how secrets are separated from authentication. Tier 0 systems establish identity and credential authority. Tier 1 systems deliver services and PAM functions without becoming identity trust roots. Tier 2 systems remain explicitly untrusted for privileged operations. MGMT01 anchors the model by acting as the only approved administrative origin. Vault enforces credential boundaries, Delinea introduces application-layer PAM controls, and SIEM01 provides the monitoring layer needed to verify enforcement. Together, these controls reduce credential exposure, constrain lateral movement, and make administrative behavior predictable and auditable.

---

**E.E. Spence — PAM Engineering | IAMPAM.LAB**
