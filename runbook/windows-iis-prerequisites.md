← [Back to Module 06 — Delinea Secret Server](../module/06-delinea-secret-server.md)



# Windows IIS Application Prerequisites Runbook

## Overview

This runbook defines the required Internet Information Services (IIS) and Windows feature configuration for hosting web-based applications within the IAMPAM.LAB environment.
This configuration supports applications such as Delinea Secret Server and can be reused for other IIS-hosted services.

---

## Environment

| Component  | Value                  |
| ---------- | ---------------------- |
| Hostname   | DELINEA01              |
| Domain     | IAMPAM.LAB             |
| Web Server | IIS (Default Web Site) |
| OS         | Windows Server         |

---

## Purpose

IIS provides the web hosting platform required for application deployment.
This runbook standardizes the installation of required features to ensure compatibility with applications that depend on .NET, WCF, and IIS services.

---

## Prerequisites

* Windows Server installed and operational
* Administrative access available (`IAMPAM\Administrator`)
* System connected to lab network

---

## IIS and Feature Installation

Install required IIS roles and Windows features:

```powershell
Install-WindowsFeature `
Web-Server, Web-WebServer, Web-Common-Http, Web-Default-Doc, `
Web-Dir-Browsing, Web-Http-Errors, Web-Static-Content, Web-Http-Redirect, `
Web-Health, Web-Http-Logging, `
Web-Performance, Web-Stat-Compression, Web-Dyn-Compression, `
Web-Security, Web-Filtering, Web-Windows-Auth, `
Web-App-Dev, Web-Asp-Net45, Web-Net-Ext45, Web-ISAPI-Ext, `
Web-ISAPI-Filter, Web-AppInit, `
Web-Mgmt-Tools, Web-Mgmt-Console, Web-Scripting-Tools, `
NET-Framework-45-Features, NET-Framework-45-ASPNET, `
NET-WCF-Services45, NET-WCF-HTTP-Activation45, NET-WCF-TCP-Activation45, `
NET-WCF-TCP-PortSharing45, `
WAS, WAS-Process-Model, WAS-Config-APIs `
-IncludeManagementTools
```

Restart IIS after installation:

```powershell
iisreset
```

---

## Feature Verification

Verify IIS role installation:

```powershell
Get-WindowsFeature Web-Server
```

Expected:

```text
Installed
```

---

## WCF and WAS Verification

Verify required components:

```powershell
Get-WindowsFeature NET-WCF-HTTP-Activation45, NET-WCF-TCP-Activation45, NET-WCF-TCP-PortSharing45, WAS, WAS-Process-Model, WAS-Config-APIs
```

Expected:

```text
Install State: Installed
```

---

## Default Web Site Validation

Verify IIS site is running:

```powershell
Get-Website -Name "Default Web Site"
```

Expected:

```text
State: Started
```

---

## HTTPS Certificate Configuration

### Create Self-Signed Certificate

```powershell
New-SelfSignedCertificate -DnsName "DELINEA01" -CertStoreLocation Cert:\LocalMachine\My
```

---

### Bind Certificate to IIS

```powershell
Import-Module WebAdministration

Remove-WebBinding -Name "Default Web Site" -Protocol https -ErrorAction SilentlyContinue

New-WebBinding -Name "Default Web Site" -Protocol https -Port 443 -IPAddress "*"

Remove-Item IIS:\SslBindings\0.0.0.0!443 -ErrorAction SilentlyContinue

Get-Item cert:\LocalMachine\MY\<THUMBPRINT> | New-Item IIS:\SslBindings\0.0.0.0!443
```

Restart IIS:

```powershell
iisreset
```

---

## HTTPS Validation

Verify HTTPS binding:

```powershell
Get-WebBinding -Name "Default Web Site" -Protocol https
```

Expected:

```text
*:443:
```

---

Verify certificate binding:

```powershell
netsh http show sslcert ipport=0.0.0.0:443
```

Expected:

* Certificate hash present
* Store name: MY

---

## Optional Access Validation

Verify IIS responds over HTTPS:

```text
https://delinea01.iampam.lab
```

Note:
This confirms IIS and certificate binding only.
Application-specific endpoints (e.g., `/SecretServer`) are validated in application runbooks.

---

## Operational Notes

* This configuration is intended for lab and sandbox environments
* Self-signed certificates are acceptable for testing
* Production deployments should use trusted certificates and hardened IIS configurations

---

## Screenshot Evidence

| Description      | Filename                      |
| ---------------- | ----------------------------- |
| IIS installation | module06-06-iis-installed.png |

---

## References

Microsoft IIS Documentation
https://learn.microsoft.com/en-us/iis/

Microsoft Windows Server Roles and Features
https://learn.microsoft.com/en-us/windows-server/

---

## Summary

This runbook provides a consistent IIS configuration required for hosting web-based applications in the IAMPAM.LAB environment.
It ensures IIS is installed, configured, and ready for application deployment without coupling to a specific application.
