# Delinea Secret Server Governance

**Lab:** IAMPAM.LAB | **Status:** ✅ Complete | **Completed:** March 2026

---

Privileged credential management requires more than just storing passwords — it requires controlled access, audit visibility, and a platform that enforces who can retrieve what and when. This module deploys Delinea Secret Server within the IAMPAM.LAB environment as the centralized privileged credential management system.

Delinea Secret Server was deployed on DELINEA01 using IIS as the web host and SQL Server Express as the backend database — mirroring real enterprise PAM deployments and providing a fully operational credential governance platform.

---

## What Was Built

A fully operational Delinea Secret Server instance deployed and validated within the IAMPAM.LAB environment providing:

- Centralized privileged credential storage
- Controlled credential retrieval and access enforcement
- Folder-based secret segmentation by department
- RBAC enforcement through local group assignments mirroring Active Directory structure
- Full application validation through secret creation and retrieval

---

## Architecture

| Component | Configuration |
|---|---|
| Host | DELINEA01 |
| URL | https://delinea01.iampam.lab/SecretServer |
| Web Server | IIS — Default Web Site |
| Database | SQL Server Express — DELINEA01\SQLEXPRESS |
| Database Name | SecretServer |
| Authentication | Windows Authentication |
| Service Account | IAMPAM\Administrator |

---

## Prerequisites

Before installation the following infrastructure was validated:

- IIS with full WCF, WAS, and compression modules installed
- SQL Server Express with Mixed Mode authentication and correct collation
- HTTPS binding configured on Default Web Site
- SQL CLR enabled on the SQL instance
- Domain join verified — DELINEA01 joined to IAMPAM.LAB

[ SCREENSHOT: module06-02-domain-joined ]

[ SCREENSHOT: module06-06-iis-installed ]

[ SCREENSHOT: module06-07-sql-installed ]

---

## Installation

Delinea Secret Server was installed using the official installer with the following configuration:

- SQL Server instance: `DELINEA01\SQLEXPRESS`
- Database: `SecretServer`
- IIS Application Path: `/SecretServer`
- Authentication: Windows Authentication

[ SCREENSHOT: module06-08-delinea-portal ]

[ SCREENSHOT: module06-09-delinea-install-success ]

---

## Validation

Validation confirmed the system is not just installed but fully operational. Login was verified using the configured administrator account and a secret was created and retrieved to confirm:

- Database connectivity
- Encryption functionality
- Application logic
- UI accessibility

[ SCREENSHOT: module06-10-delinea-dashboard ]

[ SCREENSHOT: module06-11-delinea-secret-created ]

---

## RBAC and Folder Structure

Folder-based secret segmentation was implemented to enforce department-aligned access control:

- `Fairmount Manufacturing/Engineering` — ENG-Users Read access
- `Fairmount Manufacturing/Finance` — FIN-Users Read access
- `Fairmount Manufacturing/IT-Security` — IT-Admins Owner access
- SEC-Analysts — Read access across all Fairmount folders

**Note:** Due to single-user licensing constraints in the lab environment, direct Active Directory integration with Delinea could not be completed. AD group structure was replicated using local Delinea groups to maintain architectural accuracy. This ensures that once AD integration is enabled, group synchronization can occur without requiring redesign of access controls.

---

## Troubleshooting Encountered

Real-world deployment challenges were encountered and resolved during this module:

- **IIS prerequisite failures** — resolved by installing full IIS feature set including WCF and WAS components
- **HTTPS binding not detected** — resolved by rebinding SSL certificate to Default Web Site
- **SQL CLR disabled** — resolved by enabling CLR via sp_configure
- **Partial database state** — resolved by dropping the existing database and performing a clean reinstallation

These challenges reflect real enterprise PAM deployment scenarios where infrastructure dependencies must be validated before application installation.

---

## Key Takeaways

- Application-specific dependencies must be validated before installation begins
- IIS and SQL must be configured and validated independently before integration
- Functional validation through secret creation is required beyond installation success
- Separation of infrastructure and application runbooks improves maintainability
- In production environments a dedicated service account with least privilege should replace the administrator account

---

## Enterprise Mapping

| Capability | Lab Implementation | Enterprise Equivalent |
|---|---|---|
| Credential Storage | Delinea Secret Server KV | CyberArk Safe |
| Access Control | Folder-based RBAC | PAM Zones |
| Audit Logging | Delinea audit trail | Session recording |
| Web Hosting | IIS | Enterprise web tier |

---

## Why This Matters

Without a dedicated PAM platform, privileged credentials are managed informally — shared spreadsheets, email threads, and memory. Delinea Secret Server enforces controlled retrieval, full auditability, and role-based access that scales across departments. This deployment proves the full PAM stack is operational end to end within the IAMPAM.LAB environment.

---

👉 **[View Full Module on GitHub](https://github.com/eespence/IAM-PRIVILEGED-ACCESS-ENGINEERING)**

---

**E.E. Spence — PAM Engineering | IAMPAM.LAB**