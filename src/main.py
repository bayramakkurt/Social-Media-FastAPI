#Main APP

from fastapi import FastAPI
from .database import Base, engine #Kendi yazdığımız database dosyasından Base ve engine değişkenlerini aldık.
from .api import router

Base.metadata.create_all(bind = engine)



app = FastAPI(
    title="Social Media APP",
    description="Protect Social Media APP",
    version="0.1"
)

app.include_router(router)