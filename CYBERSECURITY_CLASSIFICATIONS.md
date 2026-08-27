# 🛡️ GracefulOS: Complete Cybersecurity Classifications Guide

Welcome to the cybersecurity breakdown of **GracefulOS**. This document lists all **41 cybersecurity categories, standards, frameworks, and technologies** that GracefulOS is based on, explained in simple, plain English.

---

## 🏷️ Category 1: Industry Product Classifications (What It Is)

1. **Agentic AI Security Control Plane**  
   The central governance and supervisory layer that sits between an autonomous AI agent and the operating system to police and enforce boundaries on all execution.
2. **AI Runtime Security (AIRS)**  
   Real-time monitoring, inspection, and threat prevention during the live execution of an AI model.
3. **Host-Based AI Firewall (HAIF)**  
   Intercepts, filters, and blocks function calls, tool arguments, and script payloads before Windows executes them.
4. **AI Endpoint Detection & Response (AI-EDR)**  
   Endpoint security designed to detect behavioral anomalies in AI processes and physically terminate rogue processes.
5. **Security Orchestration, Automation, and Response (SOAR)**  
   Millisecond-level automated playbooks that execute process isolation, firewall blocking, and filesystem freezing.
6. **Security Information and Event Management (SIEM)**  
   Real-time log aggregation, event correlation, and anomaly scoring engine.
7. **Security Operations Center (SOC) Console**  
   Live visual dashboard (`http://127.0.0.1:7777`) providing real-time telemetry, agent degradation postures, active alerts, and approval queues.

---

## 🛡️ Category 2: Dynamic Access Control & Risk Models (NIST & Gartner)

8. **Risk-Adaptive Access Control (RAdAC - NIST Standard)**  
   Security permissions are not static; permissions expand or contract dynamically based on real-time calculated threat levels.
9. **Continuous Adaptive Risk and Trust Assessment (CARTA - Gartner Framework)**  
   Continually evaluates risk scores from `0` to `100` across 6 degradation states:  
   `NORMAL` → `WATCH` → `RESTRICTED` → `READ_ONLY` → `ISOLATED` → `CONTAINED`.
10. **Principle of Least Privilege (PoLP)**  
    Restricting an AI agent strictly to the minimum capabilities necessary for its active task and immediately revoking them when done.
11. **Human-in-the-Loop (HITL) Policy Override**  
    Mandatory human sign-off requiring administrator approval before privileged or destructive actions can run.
12. **Just-In-Time (JIT) Privilege Elevation (`Allow Once`)**  
    Granting single-use execution tokens that permit one execution and immediately expire.
13. **Workspace Trust Policy Allowlisting (`Always Allow`)**  
    Permanent pattern matching for trusted build and test scripts so GracefulOS allows them without repeatedly prompting.
14. **Blast Radius Containment**  
    Setting hard mathematical quotas on file modifications, RAM/CPU consumption, network endpoints, and child processes.

---

## 🪤 Category 3: Active Cyber Deception (MITRE D3FEND)

15. **Honeypot Canary Tripwires**  
    Planting decoy credential files (`fake_admin_token.txt`, `fake_cloud_key.txt`, `fake_password.txt`) in the filesystem.
16. **Deception-Based Early Warning (+60 Risk Penalty)**  
    Triggering an immediate high-severity breach alarm and +60 risk penalty if an agent attempts to read decoy credentials.
17. **Breadcrumb Traps**  
    Simulated registry entries and fake environment variables that expose unauthorized agent exploration.

---

## 🔒 Category 4: Windows 11 Operating System & Kernel Sandboxing

18. **Win32 Kernel Job Objects**  
    Windows NT kernel-level sandboxing that binds parent and child processes into a single manageable unit.
19. **Hard Resource Quotas**  
    Enforcing physical limits (512MB RAM cap, CPU cycle rate limiting) directly in the Windows kernel.
20. **Atomic Process Tree Termination (`TerminateJobObject`)**  
    Single-call kernel kill-switch that terminates an AI agent and all spawned sub-processes simultaneously.
21. **Mandatory Integrity Control (MIC) / Low-Integrity SIDs**  
    Dropping the AI agent's process token to Low Integrity (`SECURITY_MANDATORY_LOW_RID` / `0x1000`) to prevent writes to user or system directories.
22. **Restricted Access Tokens**  
    Stripping administrative and debug privileges (`SeDebugPrivilege`, `SeShutdownPrivilege`, `SeImpersonatePrivilege`) from the AI's execution thread.
23. **NTFS Discretionary Access Control Lists (DACL Hardening)**  
    Directly commanding the Windows NTFS driver to lock workspace directories as Read-Only (`[WinError 5: Access is denied]`).
24. **Endpoint Micro-Segmentation**  
    Dynamically generating Windows Defender Firewall rules via `netsh` to sever network connections during degradation.
25. **Event Tracing for Windows (ETW)**  
    Kernel-level telemetry logging for process creation, DLL loading, and network socket operations.
26. **Local Named Pipe IPC**  
    High-security local Windows Named Pipes (`\\.\pipe\GracefulOS`) for offline, tamper-resistant inter-process communication.

---

## 🔐 Category 5: Cryptography & Data Protection

27. **Cryptographic Non-Repudiation (NIST SP 800-53 AU-9)**  
    Cryptographically tying every logged action, tool call, and risk score change to the agent and timestamp.
28. **Append-Only SHA-256 Hash Chaining**  
    Blockchain-style hashing where each audit record incorporates the previous record's hash, making log tampering mathematically impossible.
29. **Windows Data Protection API (DPAPI - `CryptProtectData`)**  
    Encrypting sensitive agent tokens, metadata, and database keys using Windows native user-bound cryptography.
30. **Ephemeral Credential Management**  
    Generating short-lived temporary access tokens with strict Time-To-Live (TTL) expiration.

---

## 🕵️ Category 6: Digital Forensics & Incident Response (DFIR)

31. **Incident Replay Engine**  
    Digital forensics engine that lets security analysts step forwards and backwards through an attack timeline to observe the incident.
32. **Automated Evidence Preservation**  
    Automatically generating an encrypted incident `.zip` snapshot containing memory state, audit logs, and process hierarchy upon containment.
33. **Incident Ticket Lifecycle**  
    Tracking alerts from initial detection, triage, containment, through to administrator release.

---

## 🤖 Category 7: AI Threat Defense (OWASP Top 10 for LLMs)

34. **Indirect Prompt Injection Defense (LLM01)**  
    Intercepting and sanitizing untrusted inputs from web pages and files before they reach the model.
35. **Insecure Output Handling Defense (LLM02)**  
    Sandboxing and validating commands generated by the LLM before they reach PowerShell or CMD.
36. **Model Context Protocol (MCP) Tool Validation**  
    Enforcing strict JSON schema verification, input sanitization, and AST (Abstract Syntax Tree) code inspection on all AI tools.
37. **Prompt Guard / Guardian AI**  
    Multi-layered deterministic heuristic filters and classification models scanning for evasion and jailbreaks.

---

## ⚙️ Category 8: Secure System Architecture Principles (Saltzer & Schroeder)

38. **Fail-Safe / Fail-Secure Defaults**  
    If any component (like the LLM Guardian) crashes or times out, the system locks down (`FAIL_SECURE`) rather than opening up.
39. **Complete Mediation**  
    Every single access request must be checked through the security control plane—no bypass paths exist.
40. **Economy of Mechanism**  
    Clean, local-only Python and Win32 architecture with zero external cloud dependencies, Docker, or Kubernetes bloat.
41. **Unbreakable Security Invariants (INV-001 through INV-008)**  
    Hard-coded mathematical rules that cannot be disabled by any configuration (e.g., self-defense against service tampering and log deletion).

---

## 📊 Summary
> **GracefulOS is an all-in-one local Agentic AI Security Control Plane combining RAdAC Dynamic Sandboxing, Endpoint EDR/SOAR, Canary Honeypots, and an Immutable Cryptographic SIEM on Windows 11.**
