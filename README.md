🌐 Escáner de Puertos por Dominio/IP
Una herramienta de escaneo de puertos rápida y eficiente, desarrollada en Python, que permite identificar puertos abiertos en cualquier dominio o dirección IP. Esta herramienta es ideal para investigadores de seguridad, desarrolladores y administradores de red que necesitan realizar auditorías básicas de puertos de manera ágil.

🚀 Características Principales
Detección de Colores: Interfaz de línea de comandos amigable con mensajes de estado y resultados claros y con colores.

Múltiples Opciones de Escaneo:

Escaneo Rápido: Escanea los puertos comunes para una verificación veloz.

Escaneo de Rango Personalizado: Permite definir un rango de puertos específico (ej. 1-1000) para un análisis más detallado.

Escaneo de Puerto Único: Permite verificar el estado de un puerto en particular.

Rendimiento Óptimo: Utiliza ThreadPoolExecutor para el escaneo concurrente, lo que reduce significativamente el tiempo de espera.

Validación de Entradas: Verifica la validez del dominio o dirección IP ingresados para evitar errores.

Exportación de Resultados: Permite exportar los puertos abiertos a un archivo de texto para su posterior análisis.

📋 Requisitos
Para ejecutar el escáner, solo necesitas tener Python 3 instalado.

Python: Se recomienda Python 3.6 o superior.

La herramienta utiliza la librería colorama para mostrar la salida con colores. Si no la tienes instalada, puedes instalarla con el siguiente comando:

Bash

pip install colorama
💻 Uso
1. Clonar el repositorio
Bash

git clone https://github.com/lokipwn/escaner_puertos.git
cd escaner_puertos
2. Ejecutar el script
Bash

python port_dominio_scanner.py
3. Interacción con el programa
Una vez que el script se ejecute, serás guiado a través de un menú interactivo.

Ingresa el host: Introduce la dirección IP o el dominio que deseas escanear.

[+] Ingrese IP o dominio: google.com
Selecciona una opción: Elige entre las opciones disponibles (1, 2, 3, o 4) para iniciar el tipo de escaneo deseado.

Seleccione una opción:
[1] Escanear puertos comunes (rápido)
[2] Escanear rango personalizado
[3] Escanear puerto específico
[4] Salir
4. Ejemplos
Escaneo de Puertos Comunes:

[+] Opción: 1
...
[+] ¿Escanear estos puertos? (s/n): s
Escaneo de Rango Personalizado:

[+] Opción: 2
[+] Ingrese rango (ej: 1-1000): 1-1024
Escaneo de Puerto Específico:

[+] Opción: 3
[+] Ingrese puerto: 80
🤝 Contribuciones
Si deseas contribuir a este proyecto, ¡eres bienvenido! Siéntete libre de abrir un pull request con mejoras, correcciones de errores o nuevas funcionalidades.

📃 ⚠️ Descargo de Responsabilidad (Disclaimer)
Esta herramienta, "Escáner de Puertos por Dominio/IP", es proporcionada "tal cual" y es de uso exclusivo con fines educativos y de investigación.

El autor lokipwn no se hace responsable del uso indebido o ilegal que se le pueda dar a este software.

Uso Ético: Se recomienda encarecidamente utilizar esta herramienta únicamente en sistemas de tu propiedad, con permiso explícito o en entornos de prueba controlados.

Responsabilidad del Usuario: El usuario es el único responsable de cualquier acción que tome y de las consecuencias legales que de ello se deriven. El escaneo de puertos en sistemas sin autorización puede ser ilegal y está penalizado en muchas jurisdicciones.

Al utilizar este software, aceptas plenamente estos términos y condiciones.
