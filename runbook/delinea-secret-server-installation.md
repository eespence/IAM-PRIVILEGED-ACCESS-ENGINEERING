← [Back to Module 06 — Delinea Secret Server](../module/06-delinea-secret-server.md)



# Delinea Secret Server Installation Runbook

## Overview

This runbook defines the validated procedure for deploying Delinea Secret Server (v12) on a Windows Server system within the IAMPAM.LAB environment.
The deployment is performed using Microsoft SQL Server Express and IIS with HTTPS binding.

This implementation aligns with Delinea Secret Server installation guidance and has been validated in a controlled lab environment.

---

## Environment

| Component        | Value                           |
| ---------------- | ------------------------------- |
| Hostname         | DELINEA01                       |
| Domain           | IAMPAM.LAB                      |
| SQL Instance     | DELINEA01\SQLEXPRESS            |
| Web Server       | IIS (Default Web Site)          |
| Application Path | C:\inetpub\wwwroot\SecretServer |

---

## Prerequisites

### Infrastructure

* System is domain joined
* DNS resolution is functional
* Administrative access available (`IAMPAM\Administrator`)

---

### SQL Server Requirements

SQL Server provides the backend database required for Secret Server.

* SQL Server Express installed
* Instance: `DELINEA01\SQLEXPRESS`
* Collation must be:

```text id="m0dqkz"
SQL_Latin1_General_CP1_CI_AS
```

---

### IIS / Windows Features

IIS hosts the Secret Server web application and required services.

```powershell id="y2j6vc"
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

```powershell id="i5pygq"
iisreset
```

---

## Required Configuration

### Enable SQL CLR

SQL CLR is required for database functions and assemblies used during Secret Server initialization.

```powershell id="q0l8el"
sqlcmd -S DELINEA01\SQLEXPRESS -E -Q "EXEC sp_configure 'show advanced options', 1; RECONFIGURE; EXEC sp_configure 'clr enabled', 1; RECONFIGURE;"
```

---

### Configure HTTPS Binding

HTTPS is required for secure access to the Secret Server interface.

```powershell id="r9c8hl"
New-SelfSignedCertificate -DnsName "DELINEA01" -CertStoreLocation Cert:\LocalMachine\My
```

```powershell id="tfv3pk"
Import-Module WebAdministration

Remove-WebBinding -Name "Default Web Site" -Protocol https -ErrorAction SilentlyContinue
New-WebBinding -Name "Default Web Site" -Protocol https -Port 443 -IPAddress "*"

Remove-Item IIS:\SslBindings\0.0.0.0!443 -ErrorAction SilentlyContinue
Get-Item cert:\LocalMachine\MY\<THUMBPRINT> | New-Item IIS:\SslBindings\0.0.0.0!443
```

```powershell id="v3y5jl"
iisreset
```

---

## Installation Procedure

1. Launch Delinea installer as Administrator

2. Select Secret Server

3. Database Configuration

   * Server: `DELINEA01\SQLEXPRESS`
   * Database: `SecretServer`
   * Authentication: Windows Authentication

4. Application Configuration

   * Site: Default Web Site
   * Path: `/SecretServer`
   * Service Account: `IAMPAM\Administrator`

5. Initial Administrator Account

   * Username: `admin`
   * Display Name: Delinea Administrator
   * Email: [admin@iampam.lab](mailto:admin@iampam.lab)

6. Email Configuration

   * Skip (lab environment)

7. Review and install

---

## Installation Completion

Expected result:

```text id="47ddhu"
Secret Server installed successfully
```

---

## Post-Installation Validation

1. Access:

```text id="h6l77u"
https://delinea01.iampam.lab/SecretServer
```

2. Log in using configured administrator account

3. Validate dashboard loads successfully

4. Create a test secret to confirm application functionality

---

## Section 7 — Screenshot Evidence

| Description                       | Filename                                |
| --------------------------------- | --------------------------------------- |
| Proxmox VM specifications         | module06-00-proxmox-specs.png           |
| IP configuration                  | module06-01-ip-config.png               |
| Domain join verification          | module06-02-domain-joined.png           |
| DNS resolution                    | module06-03-dns-resolution.png          |
| Port validation                   | module06-04-port-validation.png         |
| .NET installation                 | module06-05-dotnet-installed.png        |
| IIS installation                  | module06-06-iis-installed.png           |
| SQL Server installation           | module06-07-sql-installed.png           |
| Delinea installer interface       | module06-08-delinea-portal.png          |
| Installation success confirmation | module06-09-delinea-install-success.png |
| Delinea dashboard (logged-in)     | module06-10-delinea-dashboard.png       |
| Secret creation validation        | module06-11-delinea-secret-created.png  |

---

## References

Delinea Secret Server Installation Guide (v12)
https://docs.delinea.com/online-help/secret-server/setup/installation/index.htm

Microsoft IIS Documentation
https://learn.microsoft.com/en-us/iis/

---

## Summary

This runbook provides a validated and repeatable deployment procedure for Delinea Secret Server using SQL Server Express and IIS.
All required configurations are defined to ensure consistent and successful installation and application functionality.
