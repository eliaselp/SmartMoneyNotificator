from sm import analisis
import os
import platform
import sys
import time
import correo

def clear_console():
    os_system = platform.system()
    if os_system == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


last_analisis = ""
while(True):
    h = analisis()
    clear_console()
    if not h is None and last_analisis != str(h):
        last_analisis = str(h)
        mensaje = f'''
Informe de pares listos para el análisis:
{last_analisis}
'''
        correo.enviar_correo(email='liranzaelias@gmail.com',Asunto='SMART MONEY',s=mensaje)

    print(F'PARES LISTOS PARA EL ANALISIS: {h}')
    for i in range(10, 0, -1):
        sys.stdout.write("\rTiempo restante: {:02d}:{:02d} ".format(i // 60, i % 60))
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r" + " " * 50)  # Limpiar la línea después de la cuenta regresiva
    sys.stdout.flush()

