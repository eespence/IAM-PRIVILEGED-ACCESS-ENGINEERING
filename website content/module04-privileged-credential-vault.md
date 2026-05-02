# Privileged Credential Vault

**Lab:** IAMPAM.LAB | **Status:** ✅ Complete | **Completed:** March 2026

---

Privileged credentials stored on domain systems are one of the most targeted assets in an enterprise environment. A domain compromise without credential vaulting means every password, service account, and admin token is immediately exposed.

This module introduces a dedicated credential vault layer into the IAMPAM.LAB environment using HashiCorp Vault 1.16 OSS — deployed on a dedicated VM named PAMVAULT01, isolated within the privileged identity network at 172.31.100.70.

---

## What Was Built

A standalone HashiCorp Vault instance deployed on Ubuntu Server 22.04 LTS providing:

- KV secrets storage for privileged credentials
- Access control enforcement through Vault policies
- Audit logging for all credential access events
- Token-based access control with scoped permissions

This implementation mirrors enterprise PAM vault isolation principles used by platforms such as CyberArk, Delinea, and BeyondTrust.

---

## VM Deployment — PAMVAULT01

A dedicated VM was provisioned within the segmented PAM network:

| Property | Value |
|---|---|
| Hostname | PAMVAULT01 |
| IP Address | 172.31.100.70 |
| OS | Ubuntu Server 22.04 LTS |
| Network | vmbrPAM — 172.31.100.0/24 |

[ SCREENSHOT: module04-01-proxmox-vm-created ]

---

## Vault Installation and Configuration

HashiCorp Vault 1.16 was installed from the official release, configured with a file-based storage backend, and set to listen on port 8200.

Key configuration decisions:

- TLS disabled for lab environment
- File storage backend at `/opt/vault/data`
- Vault runs as a dedicated system user — not root
- Firewall configured to allow only port 8200 and SSH

[ SCREENSHOT: module04-08-vault-binary-installed ]

---

## Vault Service Running

After configuration, Vault was registered as a systemd service and validated as active and running.

[ SCREENSHOT: module04-13-vault-service-running ]

---

## Vault Initialization

Vault was initialized generating unseal keys and a root token. Both were securely stored outside the vault environment per operational security requirements.

[ SCREENSHOT: module04-15-vault-initialized ]

---

## Vault Unsealed

Three unseal keys were applied to bring Vault out of sealed state and into operational status.

[ SCREENSHOT: module04-16-vault-unsealed ]

---

## Vault Login Success

Vault was authenticated using the root token confirming full operational status.

[ SCREENSHOT: module04-17-vault-login-success ]

---

## Secrets Management

The KV secrets engine was enabled and privileged credentials were stored and retrieved to validate the vault is functioning as the authoritative credential store.

[ SCREENSHOT: module04-19-secret-written ]

[ SCREENSHOT: module04-20-secret-retrieved ]

---

## Access Policy and Token-Based Control

A scoped Vault policy was created limiting access to specific secret paths. A token was generated bound to that policy — enforcing least privilege access to credentials.

[ SCREENSHOT: module04-21-policy-created ]

[ SCREENSHOT: module04-22-token-created ]

---

## MITRE ATT&CK Alignment

| Technique | Threat Mitigated |
|---|---|
| T1552 | Unsecured Credentials |
| T1003 | Credential Access |
| T1562 | Defense Evasion Detection |
| T1078 | Valid Account Abuse |
| T1021 | Lateral Movement |

---

## Enterprise Mapping

| Capability | Lab Implementation | Enterprise Equivalent |
|---|---|---|
| Credential Vaulting | Vault KV engine | CyberArk Safe |
| Access Logging | Vault audit logs | Session recording |
| Segmentation | Tiered secret paths | PAM zones |
| Access Control | Vault policies | RBAC / Just-In-Time |

---

## Why This Matters

Without credential vaulting, privileged passwords live in scripts, spreadsheets, and the minds of administrators. A single breach exposes everything. This implementation ensures credentials are stored in a controlled, auditable vault — retrieved only through policy-enforced access — directly mitigating credential theft and lateral movement attack paths.

---

👉 **[View Full Module on GitHub](https://github.com/eespence/IAM-PRIVILEGED-ACCESS-ENGINEERING)**

---

**E.E. Spence — PAM Engineering | IAMPAM.LAB**