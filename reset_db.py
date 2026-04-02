import redis

def preparar_entorn():
    # Canvia 'localhost' per la teva IP d'AWS si ho executes des de fora
    db = redis.Redis(host='localhost', port=6379, decode_responses=True)
    db.flushdb()
    db.set('tickets_disponibles', 20000)
    print(" Base de dades completament netejada.")
    print(" Entrades no numerades reiniciades a 20.000.")
    print(" Ja pots llançar el producer.py!")

if __name__ == '__main__':
    preparar_entorn()