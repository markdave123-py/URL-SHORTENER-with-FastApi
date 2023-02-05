
## main.py
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware

from .routes import shorten
from .routes import redirect
#from routes.redirect import router as RedirectRouter
from mongoengine import connect, disconnect, errors
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from decouple import config

MONGO_URI = config('MONGO_URI')
print(MONGO_URI)

app = FastAPI()

# Templates
templates = Jinja2Templates(directory = "templates")

@app.get("/", response_class = HTMLResponse)
async def index(request : Request):
    return templates.TemplateResponse("index.html", {"request" : request})

app.include_router(shorten.router, tags = ["Shorten long URL"], prefix = "/api/v1/shorten")

#app.include_router(redirect.router, tags = ["Redirect to Short URL"])

@app.on_event("startup")
async def create_db_client():
    try:
        connect(host = MONGO_URI)
        print("Successfully connected to the Mongo Atlas database.")
    except Exception as e:
        print(e)
        print("An error occurred while connecting to Mongo Atlas database.")

@app.on_event("shutdown")
async def shutdown_db_client():
    pass


