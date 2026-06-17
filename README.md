# NetProcess-Intel 🛡️

A lightweight Windows Blue Teaming tool written in Python for threat hunting and incident response. It correlates active network connections with running system processes, enriching the data with geographic IP intelligence.

## 🔍 How it Works

1. **Network Audit:** Scans active connections using native Windows tools to isolate PIDs communicating externally.
2. **Process Correlation:** Automatically maps those PIDs to actual running executable names (`.exe`).
3. **Threat Intel Enrichment:** Automatically filters local traffic and queries a public API to geolocate external IPs.

This is highly useful for detecting unauthorized processes (like `powershell.exe`, `cmd.exe`, or unknown binaries) communicating with suspicious foreign servers.

## 📋 Requirements & Compatibility

* **OS:** Windows (Only)
* **Python:** 3.x (No external libraries required like `requests`, it uses native `urllib`).

## 🚀 Usage

1. Open your terminal (CMD or PowerShell) as Administrator.
2. Run the script:
   ```bash
   python netprocess_intel.py

Enter the process name you want to audit (e.g., chrome, powershell, svchost).

## 📊 Sample Output

```text
[+] Buscando conexiones e Inteligencia de IPs para: 'powershell'

PID        Proceso                Dirección Remota       País Origen/Destino
--------------------------------------------------------------------------------
14320      powershell.exe         185.190.140.5:443      Netherlands
4312       powershell.exe         127.0.0.1:50311        Red Local (LAN) 

⚠️ Disclaimer
This tool is intended for educational purposes and authorized Blue Teaming/Incident Response activities only.
