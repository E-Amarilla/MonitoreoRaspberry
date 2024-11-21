import os
import time
import threading
import smtplib
import subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Utilizar variables de entorno para evitar almacenar contraseñas en el código.
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "pruebascremona@gmail.com")  # Cambia a tu correo
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "dplb esea fqfw aaei")  # Cambia a tu contraseña
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_email(subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = "samuu8756@gmail.com"
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, "samuu8756@gmail.com", msg.as_string())
        print("Notificación por correo enviada.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

def is_router_up(router_ip):
    attempts = 3
    success_count = 0

    for _ in range(attempts):
        command = f"ping -c 1 {router_ip}"

        try:
            # Ejecuta el ping y captura la salida
            response = subprocess.check_output(command, shell=True, text=True)

            # Si la respuesta contiene "ttl" (indicando éxito en el ping en Linux)
            if "ttl" in response.lower():
                success_count += 1
            # Verifica si el mensaje es "inaccesible" para descartar que esté encendido
            elif "inaccessible" in response.lower() or "unreachable" in response.lower():
                print("La respuesta al ping fue: 'Host de destino inaccesible'. Considerando el router como APAGADO.")
                return False  # Devuelve inmediatamente si es inaccesible

        except subprocess.CalledProcessError:
            # Esto maneja "Tiempo de espera agotado"
            print("La respuesta al ping fue: 'Tiempo de espera agotado para esta solicitud'. Considerando el router como APAGADO.")

        time.sleep(1)

    return success_count >= (attempts // 2) + 1

def monitor_router(router_ip, stop_event):
    last_status = None
    while not stop_event.is_set():
        current_status = is_router_up(router_ip)
        if current_status != last_status:
            if current_status:
                print(f"Router {router_ip} está ENCENDIDO.")
                send_email("Estado del Router", f"El router {router_ip} está ENCENDIDO.")
            else:
                print(f"Router {router_ip} está APAGADO.")
                send_email("Estado del Router", f"El router {router_ip} está APAGADO.")
            last_status = current_status
        time.sleep(5)

def stop_monitoring(stop_event):
    while not stop_event.is_set():
        # Aquí se usa un archivo de bandera para detener el monitoreo
        if os.path.exists("/tmp/stop_monitoring"):
            stop_event.set()
            print("Monitoreo detenido.")
            break
        time.sleep(1)

if __name__ == "__main__":
    router_ip = "192.168.10.35"  # Cambiar IP según router que queremos monitorear
    stop_event = threading.Event()

    monitor_thread = threading.Thread(target=monitor_router, args=(router_ip, stop_event))
    monitor_thread.start()

    stop_monitoring(stop_event)
    monitor_thread.join()