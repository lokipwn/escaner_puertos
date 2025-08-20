import socket
import threading
from concurrent.futures import ThreadPoolExecutor
import time
import ipaddress
import os

# Detectar si el sistema soporta colores
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORES_DISPONIBLES = True
except ImportError:
    COLORES_DISPONIBLES = False
    class ColorFallback:
        def __getattr__(self, name):
            return ""
    Fore = Back = Style = ColorFallback()

# Puertos más comunes y sus servicios
PUERTOS_COMUNES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 993: "IMAPS",
    995: "POP3S", 1433: "MSSQL", 3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 8080: "HTTP-Alt", 8443: "HTTPS-Alt"
}

# Funciones de colores
def print_banner():
    """Muestra el banner con colores"""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║         ESCANNER DE PUERTOS POR DOMINIO/IP                   ║")
    print("║                           lokipwn                            ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(f"{Style.RESET_ALL}")

def print_info(text):
    print(f"{Fore.CYAN}ℹ {text}{Style.RESET_ALL}")

def print_success(text):
    print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")

def print_warning(text):
    print(f"{Fore.YELLOW}⚠ {text}{Style.RESET_ALL}")

def print_error(text):
    print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}")

def print_highlight(text):
    print(f"{Fore.MAGENTA}{Style.BRIGHT}{text}{Style.RESET_ALL}")

def validar_host(host):
    """Valida si la IP o dominio es válido"""
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        try:
            socket.gethostbyname(host)
            return True
        except socket.gaierror:
            return False

def mostrar_puertos_comunes():
    """Muestra los puertos más comunes con colores"""
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}{'='*50}")
    print(f"{Fore.YELLOW}{Style.BRIGHT}PUERTOS MÁS COMUNES")
    print(f"{Fore.YELLOW}{Style.BRIGHT}{'='*50}")
    
    for puerto, servicio in PUERTOS_COMUNES.items():
        print(f"{Fore.GREEN}  {puerto:5} {Fore.WHITE}- {Fore.CYAN}{servicio}")
    
    print(f"{Fore.YELLOW}{Style.BRIGHT}{'='*50}{Style.RESET_ALL}")

def scan_port_rapido(host, port, timeout=0.5):
    """Escanea un puerto específico optimizado"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((host, port))
            return port, result == 0
    except:
        return port, False

def escanar_puertos_comunes(host):
    """Escanea solo los puertos más comunes"""
    if not validar_host(host):
        print_error("Host inválido")
        return []
    
    print_info(f"Escaneando puertos comunes en {host}...")
    
    open_ports = []
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(scan_port_rapido, host, port) 
                  for port in PUERTOS_COMUNES.keys()]
        
        for future in futures:
            port, is_open = future.result()
            if is_open:
                servicio = PUERTOS_COMUNES.get(port, "Desconocido")
                print_success(f"Puerto {port} ({servicio}) está ABIERTO")
                open_ports.append((port, servicio))
    
    elapsed = time.time() - start_time
    print_info(f"Escaneo completado en {elapsed:.2f} segundos")
    
    if open_ports:
        print_success(f"Puertos abiertos encontrados: {len(open_ports)}")
        for port, servicio in sorted(open_ports):
            print(f"    {port} - {servicio}")
    else:
        print_warning("No se encontraron puertos comunes abiertos")
    
    return open_ports

def escanar_rango_completo(host, start_port, end_port, max_threads=200):
    """Escaneo completo con validaciones"""
    if not validar_host(host):
        print_error("Host inválido")
        return []
    
    if not (1 <= start_port <= end_port <= 65535):
        print_error("Rango inválido. Use 1-65535")
        return []
    
    max_threads = min(max_threads, 1000)  # Limitar threads
    
    print_highlight(f"Escaneando {host}:{start_port}-{end_port}...")
    print_info(f"Usando {max_threads} threads concurrentes...")
    
    open_ports = []
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(scan_port_rapido, host, port) 
                  for port in range(start_port, end_port + 1)]
        
        completed = 0
        for future in futures:
            port, is_open = future.result()
            completed += 1
            
            if completed % 500 == 0:
                print_info(f"Progreso: {completed}/{end_port - start_port + 1} puertos")
            
            if is_open:
                servicio = PUERTOS_COMUNES.get(port, "Desconocido")
                print_success(f"Puerto {port} ({servicio}) está ABIERTO")
                open_ports.append((port, servicio))
    
    elapsed = time.time() - start_time
    
    # Estadísticas
    total_puertos = end_port - start_port + 1
    porcentaje = (len(open_ports) / total_puertos) * 100
    
    print_info(f"Escaneo completado en {elapsed:.2f} segundos")
    print_info(f"Total puertos: {total_puertos}")
    print_info(f"Puertos abiertos: {len(open_ports)} ({porcentaje:.2f}%)")
    
    if open_ports:
        exportar_opcion = input("¿Exportar resultados a archivo? (s/n): ").strip().lower()
        if exportar_opcion == 's':
            exportar_resultados([p[0] for p in open_ports])
    
    return open_ports

def exportar_resultados(open_ports, filename="resultados_scan.txt"):
    """Exporta los puertos abiertos a un archivo"""
    try:
        with open(filename, 'w') as f:
            f.write("=== RESULTADOS DEL ESCANEO ===\n")
            f.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Puertos abiertos encontrados: {len(open_ports)}\n\n")
            for port in sorted(open_ports):
                servicio = PUERTOS_COMUNES.get(port, "Desconocido")
                f.write(f"Puerto {port} - {servicio}\n")
        print_success(f"Resultados exportados a {filename}")
    except Exception as e:
        print_error(f"Error exportando: {e}")

def main():
    try:
        print_banner()
        
        host = input(f"{Fore.CYAN}[+] Ingrese IP o dominio: {Style.RESET_ALL}").strip()
        if not host:
            print_error("Debe ingresar un host")
            return
            
        print_info("Seleccione una opción:")
        print(f"{Fore.GREEN}[1]{Style.RESET_ALL} Escanear puertos comunes (rápido)")
        print(f"{Fore.YELLOW}[2]{Style.RESET_ALL} Escanear rango personalizado")
        print(f"{Fore.BLUE}[3]{Style.RESET_ALL} Escanear puerto específico")
        print(f"{Fore.RED}[4]{Style.RESET_ALL} Salir")
        
        opcion = input(f"{Fore.CYAN}[+] Opción: {Style.RESET_ALL}").strip()
        
        if opcion == "1":
            mostrar_puertos_comunes()
            confirmar = input(f"{Fore.YELLOW}[+] ¿Escanear estos puertos? (s/n): {Style.RESET_ALL}").strip().lower()
            if confirmar == 's':
                escanar_puertos_comunes(host)
                
        elif opcion == "2":
            port_input = input(f"{Fore.CYAN}[+] Ingrese rango (ej: 1-1000): {Style.RESET_ALL}").strip()
            if '-' in port_input:
                try:
                    start, end = map(int, port_input.split('-'))
                    escanar_rango_completo(host, start, end)
                except ValueError:
                    print_error("Formato de rango inválido")
            else:
                print_error("Use formato inicio-fin")
                
        elif opcion == "3":
            try:
                port = int(input(f"{Fore.CYAN}[+] Ingrese puerto: {Style.RESET_ALL}").strip())
                if 1 <= port <= 65535:
                    port, is_open = scan_port_rapido(host, port)
                    servicio = PUERTOS_COMUNES.get(port, "Desconocido")
                    if is_open:
                        print_success(f"Puerto {port} ({servicio}) está ABIERTO")
                    else:
                        print_warning(f"Puerto {port} ({servicio}) está CERRADO")
                else:
                    print_error("Puerto debe ser 1-65535")
            except ValueError:
                print_error("Puerto debe ser un número")
                
        elif opcion == "4":
            print_info("Saliendo...")
        else:
            print_error("Opción inválida")
                
    except KeyboardInterrupt:
        print_warning("\nEscaneo interrumpido por el usuario")
    except Exception as e:
        print_error(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()
