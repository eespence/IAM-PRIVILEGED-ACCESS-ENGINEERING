← [Back to Module 06 — Delinea Secret Server](../module/06-delinea-secret-server.md)



# SQL Express Deployment Runbook

## Overview

This runbook defines the validated procedure for deploying Microsoft SQL Server 2022 Express within the IAMPAM.LAB environment.
The installation supports lab-based application deployments, including Delinea Secret Server.

This process reflects a practical deployment approach using SQL Express in a non-production environment.

---

## Environment

| Component     | Value                   |
| ------------- | ----------------------- |
| Hostname      | DELINEA01               |
| Domain        | IAMPAM.LAB              |
| SQL Version   | SQL Server 2022 Express |
| Instance Name | SQLEXPRESS              |

---

## Purpose

SQL Server Express provides the database engine required for application testing and identity security workflows within the lab environment.
This runbook standardizes the installation to ensure consistency across rebuilds and future deployments.

---

## Prerequisites

* Windows Server installed and operational
* Administrative access available (`IAMPAM\Administrator`)
* System connected to lab network
* Minimum 10–15 GB available disk space

---

## Installation Source

Download SQL Server 2022 Express (version-locked installer):

```text id="7f8k3d"
https://download.microsoft.com/download/5/1/4/5145fe04-4d30-4b85-b0d1-39533663a2f1/SQL2022-SSEI-Expr.exe
```

Note:
Avoid using Microsoft fwlink or generic download pages, as they may redirect to newer versions and introduce inconsistencies in lab environments.

---

## Installation Procedure

1. Launch the installer as Administrator

2. Select:

   * **Custom Installation** (recommended for visibility and control)

3. Choose download location and proceed

4. When SQL Server Installation Center launches:

   * Select **New SQL Server stand-alone installation**

---

## Feature Selection

Select:

* Database Engine Services

Do not select additional features unless required.

---

## Instance Configuration

* Instance Name:

```text id="v2s9aa"
SQLEXPRESS
```

This creates the standard instance:

```text id="5g1nks"
DELINEA01\SQLEXPRESS
```

---

## Server Configuration

Use default service accounts for lab deployment.

No changes required unless testing service account hardening scenarios.

---

## Database Engine Configuration

### Authentication Mode

Select:

* Mixed Mode (SQL Server authentication and Windows authentication)

Set a lab password for `sa` account.

Add current user:

```text id="t1pl9k"
IAMPAM\Administrator
```

as SQL Server administrator.

---

## Installation Completion

Allow installation to complete with no errors.

---

## Service Validation

Verify SQL service is running:

```powershell id="j5g4cx"
Get-Service -Name 'MSSQL$SQLEXPRESS'
```

Expected:

```text id="z7k0hf"
Running
```

---

## Instance Validation

Verify SQL instance identity:

```powershell id="a9l3rt"
sqlcmd -S .\SQLEXPRESS -Q "SELECT @@SERVERNAME"
```

Expected:

```text id="2k2w0y"
DELINEA01\SQLEXPRESS
```

---

## Authentication Mode Validation

Verify Mixed Mode is enabled:

```powershell id="9w5u6z"
sqlcmd -S .\SQLEXPRESS -Q "SELECT SERVERPROPERTY('IsIntegratedSecurityOnly')"
```

Expected:

```text id="xq7u3b"
0
```

Meaning:

* `0` = Mixed Mode enabled
* `1` = Windows Authentication only

---

## Collation Validation

Verify SQL instance collation:

```powershell id="n3t8vz"
sqlcmd -S DELINEA01\SQLEXPRESS -E -Q "SELECT SERVERPROPERTY('Collation') AS InstanceCollation;"
```

Expected:

```text id="n7k9lf"
SQL_Latin1_General_CP1_CI_AS
```

Note:
If collation differs, reinstall SQL Server with the correct collation. Changing collation post-installation is not recommended for this lab scenario.

---

## Connectivity Validation

Confirm database query execution:

```powershell id="k3p8qm"
sqlcmd -S DELINEA01\SQLEXPRESS -E -Q "SELECT name FROM sys.databases;"
```

This verifies that the instance is reachable and operational.

---

## Operational Notes

* SQL Server Express is sufficient for lab and sandbox deployments
* Resource limitations (CPU, RAM, DB size) exist in Express edition
* Production environments should use a supported full SQL Server edition

---

## Screenshot Evidence

| Description             | Filename                      |
| ----------------------- | ----------------------------- |
| SQL Server installation | module06-07-sql-installed.png |

---

## References

Microsoft SQL Server 2022 Express Download
https://download.microsoft.com/download/5/1/4/5145fe04-4d30-4b85-b0d1-39533663a2f1/SQL2022-SSEI-Expr.exe

Microsoft SQL Server Documentation
https://learn.microsoft.com/en-us/sql/

---

## Summary

This runbook provides a consistent and repeatable SQL Server 2022 Express deployment process for the IAMPAM.LAB environment.
The configuration ensures the SQL instance is operational and ready for application integration without introducing unnecessary complexity.
