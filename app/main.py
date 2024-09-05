from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mercadopago
import os
from dotenv import load_dotenv

load_dotenv() 

# Agrega credenciales
sdk = mercadopago.SDK(os.getenv("ACCESS_TOKEN"))

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
async def main():
    return {"message": "Hello World"}

class PreferenceItem(BaseModel):
    title: str
    quantity: int | None = None
    price: int


@app.post("/create_preference")
async def main(preference:PreferenceItem):
    try:
        preference_data = {
            "items" : [{
                "title": preference.title,
                "quantity": preference.quantity,
                "price": preference.price,
                "currency_id": "COP"
            }],
            "backs_url" : {
                "success": "",
                "failure": "",
                "pending": ""
            },
            "auto_return" : "approved"
        }

        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]

        return JSONResponse(content={
            "id": preference.id
        })
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="preference error",
            headers={"X-Error": e},
        )