import subprocess
import urllib.request
import json

def run_command(command):
    try:
        result = subprocess.run(command, text=True, capture_output=True, check=False)
        return {"stdout": result.stdout.strip(), "stderr": result.stderr.strip(), "return_code": result.returncode}
    except Exception as e:
        return {"stdout": "", "stderr": str(e), "return_code": -1}

def obtener_pais_ip(ip_puerto):
    # Separamos la IP del puerto (ej: "142.250.191.142:443" -> "142.250.191.142")
    ip = ip_puerto.split(":")[0]
    
    # Ignorar IPs privadas (Loopback, red local, etc.)
    if ip.startswith("127.") or ip.startswith("192.168.") or ip.startswith("10.") or ip.startswith("172."):
        return "Red Local (LAN)"
        
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,country"
        with urllib.request.urlopen(url, timeout=3) as response:
            data = json.loads(response.read().decode())
            if data.get("status") == "success":
                return data.get("country", "Desconocido")
    except:
        pass
    return "Desconocido / Pública"

output_netstat = run_command(["netstat", "-ano"])
if output_netstat["return_code"] != 0:
    print("Error al ejecutar netstat.")
    exit()

busca = input("¿Qué proceso quieres buscar? (Ej: chrome, powershell): ").lower()

pid_ips = {}
lineas = output_netstat["stdout"].splitlines()

for linea in lineas:
    partes = linea.split()
    if len(partes) >= 5:
        ip_remota = partes[2]
        pid = partes[-1]
        
        if pid.isdigit() and pid != "0":
            if pid not in pid_ips:
                pid_ips[pid] = set()
            
            if not ip_remota.startswith("0.0.0.0") and not ip_remota.startswith("[") and not ip_remota.startswith("*"):
                pid_ips[pid].add(ip_remota)

print(f"\n[+] Buscando conexiones e Inteligencia de IPs para: '{busca}'\n")
print(f"{'PID':<10} {'Proceso':<22} {'Dirección Remota':<22} {'País Orijen/Destino'}")
print("-" * 80)

coincidencias = 0

for pid, ips in pid_ips.items():
    output_tasklist = run_command(["tasklist", "/fi", f"PID eq {pid}"])
    resultado_task = output_tasklist["stdout"]
    
    if busca in resultado_task.lower():
        nombre_proceso = "Desconocido"
        for l in resultado_task.splitlines():
            if pid in l:
                nombre_proceso = l.split()[0]
                break
        
        if ips:
            for ip in ips:
                pais = obtener_pais_ip(ip)
                print(f"{pid:<10} {nombre_proceso:<22} {ip:<22} {pais}")
                coincidencias += 1
        else:
            print(f"{pid:<10} {nombre_proceso:<22} Escucha Local          -")
            coincidencias += 1

if coincidencias == 0:
    print("[-] No se encontraron conexiones para ese proceso.")