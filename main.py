from typing import Union
from dotenv import load_dotenv
from vercel.sandbox import Sandbox
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv('.env.local')

@app.get("/")
def read_root():
    return {"message": "Success!"}

@app.get("/health")
def read_root():
    return {"health": "Server is up and running!"}

@app.get("/sandbox")
def createSandbox():
    sandbox = Sandbox.create(
        ports=[3000], 
        source={"type": "git", "url":"https://github.com/nobelsu/expo-template"},
        team_id=os.getenv("VERCEL_TEAM_ID"),
        project_id=os.getenv("VERCEL_PROJECT_ID"),
        token=os.getenv("VERCEL_TOKEN"),
    )

    sandbox.run_command("npm", ["ci"])
    sandbox.run_command_detached("npx", ["expo", "start", "--web", "--port", "3000"])

    return {
        "sandboxID": sandbox.sandbox_id,
        "preview": sandbox.domain(3000),
    }