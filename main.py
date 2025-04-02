# main.py
from backend import api

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Schedule 1 Helper")

app.mount("/", StaticFiles(html=True, directory="frontend/out"), name="static")
