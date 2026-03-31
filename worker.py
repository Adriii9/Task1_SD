from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis

# 1. Inicialitzem la API i la connexió a Redis
app = FastAPI()
db = redis.Redis(host='localhost', port=6379, decode_responses=True)

# 2. Definim els models de dades per les peticions
class UnnumberedRequest(BaseModel):
    client_id: str
    request_id: str

class NumberedRequest(BaseModel):
    client_id: str
    seat_id: str
    request_id: str

# 3. Endpoint per comprar entrades no numerades
@app.post("/buy/unnumbered")
def buy_unnumbered(req: UnnumberedRequest):
    
    quedan = db.decr('tickets_disponibles')
    
    if quedan >= 0:
        
        return {"status": "success", "message": f"Ticket purchased. Remaining: {quedan}"}
    else:
        # Fallo: En ca de que s'agotin
        
        db.incr('tickets_disponibles')
        raise HTTPException(status_code=400, detail="Tickets sold out")

# 4. Endpoint para comprar entradas numeradas
@app.post("/buy/numbered")
def buy_numbered(req: NumberedRequest):
    
    clave_asiento = f"asiento:{req.seat_id}"
    
    exito = db.setnx(clave_asiento, req.client_id)
    
    if exito:
        return {"status": "success", "message": f"Seat {req.seat_id} purchased"}
    else:
        
        raise HTTPException(status_code=400, detail="Seat already sold")