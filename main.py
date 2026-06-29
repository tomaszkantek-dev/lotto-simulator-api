from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import random

app = FastAPI(title="Lotto Simulator API")

class LottoTicket(BaseModel):
    # Oczekujemy dokładnie 6 unikalnych liczb od 1 do 49
    numbers: list[int] = Field(..., min_items=6, max_items=6)

@app.post("/play")
def play_lotto(ticket: LottoTicket):
    user_numbers = ticket.numbers
    
    # 1. Walidacja biznesowa danych wejściowych
    if any(n < 1 or n > 49 for n in user_numbers):
        raise HTTPException(status_code=400, detail="All numbers must be between 1 and 49.")
    
    if len(set(user_numbers)) != 6:
        raise HTTPException(status_code=400, detail="Numbers on the ticket must be unique.")
    
    # 2. Wydajne generowanie losowania (Pula maszynowa)
    pool = list(range(1, 50))
    random.shuffle(pool)
    winning_numbers = pool[:6]
    
    # 3. Matematyczne wyznaczenie trafień (Część wspólna zbiorów)
    hits = list(set(user_numbers).intersection(set(winning_numbers)))
    
    return {
        "user_ticket": sorted(user_numbers),
        "winning_numbers": sorted(winning_numbers),
        "hit_count": len(hits),
        "hit_numbers": sorted(hits),
        "is_jackpot": len(hits) == 6
    }
