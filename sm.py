import requests
import v20
from datetime import datetime, time
import pytz

def analisis():

    def obtener_velas(api, instrumento, granularity, count):
        url = f"https://api-fxpractice.oanda.com/v3/instruments/{instrumento}/candles"
        headers = {
            "Authorization": f"Bearer {api.token}"
        }
        params = {
            "price": "M",
            "granularity": granularity,
            "count": count
        }
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data['candles']
        except requests.exceptions.RequestException as e:
            print(f"Ha ocurrido un error: {e}")
            return []

    def es_hora_valida():
        ahora_utc = datetime.now(pytz.utc)
        
        # Convertir la hora a las zonas horarias de Nueva York y Londres
        ahora_ny = ahora_utc.astimezone(pytz.timezone('America/New_York')).time()
        ahora_londres = ahora_utc.astimezone(pytz.timezone('Europe/London')).time()
        
        inicio = time(7, 30)
        fin = time(10, 0)
        
        return (inicio <= ahora_ny <= fin) or (inicio <= ahora_londres <= fin)

    # Reemplaza con tu token de acceso
    access_token = "f3e904968c185756ff8c5754a27fef3b-2fd77b934184a2d307b3fb46b491e707"

    # Crear un contexto de API
    api = v20.Context(hostname="api-fxpractice.oanda.com", token=access_token)

    # Lista de pares de divisas óptimos para los horarios de apertura
    pares_forex = [
        "EUR_USD",  # Mercado de Londres y Nueva York
        "GBP_USD",  # Mercado de Londres y Nueva York
        "USD_CHF",  # Mercado de Londres y Nueva York
        "GBP_CHF",  # Mercado de Londres
        "EUR_GBP",  # Mercado de Londres
        "USD_JPY",  # Mercado de Nueva York
        "AUD_USD"   # Mercado de Nueva York
    ]

    # Lista para almacenar los pares que cumplen las condiciones
    pares_filtrados = []
    if es_hora_valida():
        for par in pares_forex:
            # Obtener penúltima vela diaria
            velas_diarias = obtener_velas(api, par, granularity='D', count=2)
            if len(velas_diarias) == 2:
                penultima_vela_diaria = velas_diarias[0]
                print(f'Penúltima vela diaria para {par}:\nTiempo: {penultima_vela_diaria["time"]}, Apertura: {penultima_vela_diaria["mid"]["o"]}, Cierre: {penultima_vela_diaria["mid"]["c"]}, Máximo: {penultima_vela_diaria["mid"]["h"]}, Mínimo: {penultima_vela_diaria["mid"]["l"]}')
            
                # Obtener última vela de un minuto
                velas_un_minuto = obtener_velas(api, par, granularity='M1', count=1)
                if velas_un_minuto:
                    ultima_vela_un_minuto = velas_un_minuto[0]
                    print(f'Última vela de un minuto para {par}:\nTiempo: {ultima_vela_un_minuto["time"]}, Apertura: {ultima_vela_un_minuto["mid"]["o"]}, Cierre: {ultima_vela_un_minuto["mid"]["c"]}, Máximo: {ultima_vela_un_minuto["mid"]["h"]}, Mínimo: {ultima_vela_un_minuto["mid"]["l"]}')
                    
                    # Condiciones para filtrar los pares
                    if (ultima_vela_un_minuto["mid"]["h"] >= penultima_vela_diaria["mid"]["h"] or
                        ultima_vela_un_minuto["mid"]["l"] <= penultima_vela_diaria["mid"]["l"]):
                        pares_filtrados.append(par)
    else:
        print("No estamos en el horario correcto")
    # Imprimir la lista resultante
    print("Pares de divisas que cumplen las condiciones:")
    if pares_filtrados:
        return pares_filtrados
    return None


