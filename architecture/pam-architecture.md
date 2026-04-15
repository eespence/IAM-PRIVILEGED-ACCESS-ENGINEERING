← [Back to Main README](../README.md)

![HashiCorp Vault](https://img.shields.io/badge/HashiCorp_Vault-1.16-black?style=flat\&logo=vault\&logoColor=white)
![PAM](https://img.shields.io/badge/Privileged_Access_Management-red?style=flat)
![Splunk](https://img.shields.io/badge/Splunk-Enterprise-000000?style=flat\&logo=splunk\&logoColor=white)

**Status:** ✅ Complete

# pam-architecture.md — IAMPAM.LAB

**Author:** Edward E. Spence
**Lab:** IAMPAM.LAB
**Repo:** IAM-PRIVILEGED-ACCESS-ENGINEERING
**Version:** 1.2
**Last Updated:** 2026-04-03

---

## 1. Purpose of the PAM Architecture

This document defines the **Privileged Access Management (PAM) architecture layer** within the IAMPAM.LAB environment.

The purpose is to:

* centralize credential control
* enforce controlled administrative access paths
* eliminate credential persistence on endpoints
* provide full visibility into privileged operations

This architecture reflects real-world implementations using platforms such as:

* HashiCorp Vault (credential authority)
* Delinea Secret Server (application-layer PAM)
* Splunk Enterprise (monitoring and detection)

---

## 2. Scope

This document describes the PAM layer introduced on top of the existing hybrid identity environment.

### In Scope

* Vault-based credential management
* Delinea application-layer PAM
* Administrative access path enforcement
* Privileged session monitoring
* SIEM integration

### Out of Scope

* Active Directory redesign
* Entra ID configuration
* AWS federation logic
* Network topology redesign

---

## 3. Environment Overview

**Network:** 172.31.100.0/24

| System     | OS                        | Role                                           | IP            |
| ---------- | ------------------------- | ---------------------------------------------- | ------------- |
| DC01       | Windows Server 2022       | Domain Controller (Kerberos / LDAP)            | 172.31.100.10 |
| MGMT01     | Windows Server 2022       | Privileged Access Workstation (PAW)            | 172.31.100.20 |
| CLIENT01   | Windows 11                | Standard User Workstation                      | 172.31.100.30 |
| LINUX01    | Ubuntu Server 22.04.4 LTS | Privileged Linux Server                        | 172.31.100.40 |
| ID-SYNC01  | Windows Server 2022       | Entra Connect / Identity Sync                  | 172.31.100.25 |
| SIEM01     | Ubuntu Server 22.04.4 LTS | Splunk Enterprise 9.2                          | 172.31.100.60 |
| PAMVAULT01 | Ubuntu Server 22.04.4 LTS | HashiCorp Vault 1.16 OSS                       | 172.31.100.70 |
| DELINEA01  | Windows Server            | Secret Server (IIS PAM Platform)               | 172.31.100.80 |
| PAM01      | Windows Server            | PAM support node / privileged access component | 172.31.100.50 |

---

## 4. Architecture Overview

The PAM architecture introduces a **controlled privileged access plane** layered on top of identity systems.

### Core Components

* **Identity Plane**

  * DC01
  * ID-SYNC01

* **Privileged Access Plane**

  * MGMT01 (control point)
  * PAMVAULT01 (credential authority)
  * DELINEA01 (application PAM interface)
  * PAM01 (supporting PAM component)

* **Monitoring Plane**

  * SIEM01 (Splunk)

---

## 5. Architectural Principles

### 5.1 Centralized Credential Authority

All privileged credentials are stored and managed within Vault.

### 5.2 Controlled Administrative Origin

All privileged actions originate from MGMT01.

### 5.3 Credential Isolation

Credentials are never stored on CLIENT01 or unmanaged endpoints.

### 5.4 Application-Aware PAM

Delinea introduces a web-based PAM layer with different authentication behavior than OS-level systems.

### 5.5 Full Observability

All privileged activity is logged and correlated through SIEM01.

---

## 6. Privileged Access Flow (End-to-End)

### Standard Administrative Flow

Administrator → MGMT01 → Vault / Delinea → Target System

---

### Windows Administration

MGMT01 → DC01

* Protocols: RDP / WinRM
* Credential source: Vault or AD-controlled

---

### Linux Administration

MGMT01 → LINUX01

* Protocol: SSH
* Privilege: sudo-based
* Identity: AD via SSSD

(Implemented in Module 03)

---

### Vault Credential Flow

MGMT01 → PAMVAULT01

* Protocol: Vault CLI / API
* Auth: token-based
* Control: policy-driven

(Implemented in Module 05)

---

### Delinea Access Flow

MGMT01 → DELINEA01

* Protocol: HTTPS (IIS)
* Auth: AD (Kerberos / LDAP)
* Function: credential brokering

(Implemented in Module 06)

---

## 7. Credential Lifecycle Model

Credentials follow a controlled lifecycle:

Request → Validate → Issue → Use → Expire

### Enforcement

* No persistent credentials on endpoints
* Access requires policy validation
* Credentials are time-bound or controlled

---

## 8. Vault Architecture (Tier 0 Control)

Vault functions as the **primary credential trust boundary**.

### Components

* Authentication: token-based
* Authorization: policy-driven
* Secret Engine: KV

### Enforcement

* secrets retrieved only from MGMT01
* no direct credential storage on endpoints
* centralized audit logging

### Risk

Vault compromise = full credential exposure

---

## 9. Delinea Architecture (Application PAM Layer)

Delinea introduces an **application-layer privileged access control plane**.

### Function

* web-based privileged access
* AD-integrated authentication
* credential brokering

### Key Behavior

Authentication may occur at:

* IIS layer
* application layer
* Active Directory (DC01)

### Critical Insight

* Event ID 4625 is NOT reliable for Delinea failures
* authentication failures may appear in:

  * IIS logs
  * DC01
  * not DELINEA01

---

## 10. Logging and Monitoring Architecture

All systems forward logs to **SIEM01 (Splunk Enterprise)**.

### Data Sources

* DC01 → authentication logs
* LINUX01 → SSH / sudo
* PAMVAULT01 → Vault audit logs
* DELINEA01 → IIS + application logs
* MGMT01 → administrative activity

---

## 11. Detection Strategy (Multi-Source Correlation)

Single-source detection is unreliable.

### Required Correlation

```spl
(index=iis host=DELINEA01 sc_status=401) OR
(index=wineventlog EventCode=4625 host=DELINEA01) OR
(index=wineventlog EventCode=4625 host=DC01)
| stats count by _time span=5m
| where count >= 3
```

This ensures visibility across:

* application layer
* OS layer
* identity layer

---

## 12. Security Controls Summary

| Control              | Implementation    |
| -------------------- | ----------------- |
| Admin Path Control   | MGMT01 only       |
| Credential Storage   | Vault             |
| Application PAM      | Delinea           |
| Identity Enforcement | AD / Kerberos     |
| Monitoring           | Splunk            |
| Linux Control        | SSH + sudo + SSSD |

---

## 13. Diagram Reference

![PAM Architecture](../architecture/iampam-pam-architecture.png)

The diagram shows:

* identity plane vs PAM plane
* admin access paths
* credential boundaries
* logging pipeline

---

## 14. Cross-Module Mapping

| Component            | Module    |
| -------------------- | --------- |
| Infrastructure       | Module 01 |
| Active Directory     | Module 02 |
| Linux Access Control | Module 03 |
| Logging Pipeline     | Module 04 |
| Vault PAM            | Module 05 |
| Delinea PAM          | Module 06 |
| Detection            | Module 07 |
| Automation           | Module 08 |

---

## 15. Architectural Constraints

* single Vault instance
* no session recording
* limited automation scope
* single subnet environment

---

## 16. Final Architecture Summary

The PAM architecture in IAMPAM.LAB introduces a layered control model where identity, credential authority, and privileged execution are separated into distinct planes. Active Directory provides authentication, Vault governs credential access, and Delinea introduces application-level PAM workflows. MGMT01 enforces a single administrative origin, while SIEM01 ensures all activity is observable. This combination reduces credential exposure, constrains administrative access paths, and enables reliable detection across multiple logging sources.

---

**E.E. Spence — PAM Engineering | IAMPAM.LAB**
