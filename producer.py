import pika
import json
import time

def leer_archivo(ruta, tipo):
    peticiones = []
    with open(ruta, 'r') as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith('#'): continue
            partes = linea.split()
            if partes[0] == 'BUY':
                if tipo == 'unnumbered':
                    peticiones.append({'client_id': partes[1], 'request_id': partes[2]})
                else:
                    peticiones.append({'client_id': partes[1], 'seat_id': partes[2], 'request_id': partes[3]})
    return peticiones

def enviar_a_rabbitmq(peticiones, nombre_cola):

    #DESCOMENTAR EN EL CAS QUE ES VULGUI PROBAR EN EL AWS ( OMPLIR CREDENCIALS I ESBORRAR L'ALTRA CONEXIÓ)
    #credenciales = pika.PlainCredentials('admin', 'admin123')
    #conexion = pika.BlockingConnection(pika.ConnectionParameters('10.0.1.185', credentials=credenciales))


    conexion = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    canal = conexion.channel()
    canal.queue_declare(queue=nombre_cola)

    print(f" Intriduïnt {len(peticiones)} missatges a la cua '{nombre_cola}'...")
    inicio = time.time()

    for peticion in peticiones:
        canal.basic_publish(exchange='', routing_key=nombre_cola, body=json.dumps(peticion))

    fin = time.time()
    conexion.close()
    print(f" ¡Enviats en{fin - inicio:.2f} segons!\n")

if __name__ == "__main__":
    print("=== 1. ENTRADAS NO NUMERADES ===")
    peticiones_un = leer_archivo('benchmark_unnumbered_20000.txt', 'unnumbered')
    enviar_a_rabbitmq(peticiones_un, 'cola_unnumbered')

    print("=== 2. ENTRADAS NUMERADES (NORMAL) ===")
    peticiones_num = leer_archivo('benchmark_numbered_60000.txt', 'numbered')
    enviar_a_rabbitmq(peticiones_num, 'cola_numbered')

    print("=== 3. ENTRADAS NUMERADES (HOTSPOT) ===")
    peticiones_hot = leer_archivo('benchmark_hotspot.txt', 'numbered')
    enviar_a_rabbitmq(peticiones_hot, 'cola_hotspot')