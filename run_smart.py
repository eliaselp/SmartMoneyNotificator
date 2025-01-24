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
    pares,Horario = analisis()
    clear_console()
    if not pares is None and last_analisis != str(pares):
        last_analisis = str(pares)
        mensaje = f'''
Informe de pares listos para el análisis:
{last_analisis}
'''
        correo.enviar_correo(email='liranzaelias@gmail.com',Asunto=f'SMART MONEY {Horario}',s=mensaje)

    print(F'PARES LISTOS PARA EL ANALISIS: {pares}')

    for i in range(10, 0, -1):
        sys.stdout.write("\rTiempo restante: {:02d}:{:02d} ".format(i // 60, i % 60))
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r" + " " * 50)  # Limpiar la línea después de la cuenta regresiva
    sys.stdout.flush()

