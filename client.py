import requests
import redis
import time

def leer_benchmark_unnumbered(ruta_archivo):
    peticiones = []
    with open(ruta_archivo, 'r') as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith('#'): continue
            partes = linea.split()
            if partes[0] == 'BUY':
                peticiones.append({'client_id': partes[1], 'request_id': partes[2]})
    return peticiones

def leer_benchmark_numbered(ruta_archivo):
    peticiones = []
    with open(ruta_archivo, 'r') as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith('#'): continue
            partes = linea.split()
            if partes[0] == 'BUY':
                peticiones.append({
                    'client_id': partes[1], 
                    'seat_id': partes[2], 
                    'request_id': partes[3]
                })
    return peticiones

def limpiar_base_de_datos():
    """Esborra tot el de redis per crear les proves de nou."""
    db = redis.Redis(host='localhost', port=6379, decode_responses=True)
    db.flushdb() # Vacía la base de datos por completo
    print(" Netejant dades...")
    return db

def lanzar_peticiones(peticiones, url_endpoint):
    exitos = 0
    fallos = 0
    print(f" Iniciant enviament de {len(peticiones)} peticions a {url_endpoint}...")
    inicio = time.time()

    with requests.Session() as session:
        for peticion in peticiones:
            respuesta = session.post(url_endpoint, json=peticion)
            if respuesta.status_code == 200:
                exitos += 1
            else:
                fallos += 1

    fin = time.time()
    print("\n*--* RESULTATS *--*")
    print(f" Compres OK: {exitos}")
    print(f" Compres FAIL: {fallos}")
    print(f" Temps total: {fin - inicio:.2f} segons")
    print(f" Rendimient: {len(peticiones) / (fin - inicio):.2f} pet/seg\n")


   # --- EXECUCIÓ I PROVES ---
if __name__ == "__main__":
    db = limpiar_base_de_datos()
    
    
    print("=== PROVA 1: ENTRADES NO NUMERADES ===")
    db.set('tickets_disponibles', 20000)
    peticiones_un = leer_benchmark_unnumbered('benchmark_unnumbered_20000.txt')
    lanzar_peticiones(peticiones_un, "http://127.0.0.1:80/buy/unnumbered")

    
    print("=== PROVA 2: ENTRADAS NUMERADES ===")
    db = limpiar_base_de_datos()
    peticiones_num = leer_benchmark_numbered('benchmark_numbered_60000.txt')
    lanzar_peticiones(peticiones_num, "http://127.0.0.1:80/buy/numbered")

   
    print("=== PROVA 3: ENTRADAS NUMERADES AMB EL HOTSPOT  ===")
    db = limpiar_base_de_datos()
    peticiones_hotspot = leer_benchmark_numbered('benchmark_hotspot.txt')
    lanzar_peticiones(peticiones_hotspot, "http://127.0.0.1:80/buy/numbered")