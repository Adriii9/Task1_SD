import random

def generar_escenario_hotspot(archivo_entrada, archivo_salida, total_asientos=20000):
    # El 5% de 20.000 son 1000 asientos "Hotspot"
    limite_hotspot = int(total_asientos * 0.05) 
    
    lineas_procesadas = 0
    peticiones_hotspot = 0
    
    with open(archivo_entrada, 'r') as f_in, open(archivo_salida, 'w') as f_out:
        for linea in f_in:
            linea = linea.strip()
            
            if not linea or linea.startswith('#'):
                f_out.write(linea + '\n')
                continue
            
            partes = linea.split()
            if partes[0] == 'BUY':
                client_id = partes[1]
                request_id = partes[3] # El 2 és el seient original, el qual canviarem
                
                
                if random.random() < 0.80:
                    # 80% de probabilitat: Va al Hotspot seients del 1 al 1000
                    nuevo_asiento = random.randint(1, limite_hotspot)
                    peticiones_hotspot += 1
                else:
                    # 20% de probabilitat: Va a la resta del estadi, del 1001 al 20.000
                    nuevo_asiento = random.randint(limite_hotspot + 1, total_asientos)
                    
                # Escribimos la nueva línea en el archivo trucado
                f_out.write(f"BUY {client_id} {nuevo_asiento} {request_id}\n")
                lineas_procesadas += 1

    print(f" RESUM:")
    print(f" - Total de peticions: {lineas_procesadas}")
    print(f" - Peticions al Hotspot (1-{limite_hotspot}): {peticiones_hotspot} ({(peticiones_hotspot/lineas_procesadas)*100:.1f}%)")

if __name__ == "__main__":
    generar_escenario_hotspot('benchmark_numbered_60000.txt', 'benchmark_hotspot.txt')
    print(" Archivo 'benchmark_hotspot.txt' creado con éxito.")