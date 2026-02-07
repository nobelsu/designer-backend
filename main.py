from dotenv import load_dotenv
from vercel.sandbox import Sandbox
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from pydantic import BaseModel

class RefreshProps(BaseModel):
    snapshotId: str

class DirectoryProps(BaseModel):
    sandboxId: str 
    path: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

load_dotenv('.env.local')

@app.get("/")
def readRoot():
    return {"message": "Success!"}

@app.get("/health")
def getHealth():
    return {"health": "Server is up and running!"}

@app.get("/sandbox")
def createSandbox():
    sandbox = Sandbox.create(
        ports=[3000], 
        source={"type": "git", "url":"https://github.com/nobelsu/expo-template"},
        team_id=os.getenv("VERCEL_TEAM_ID"),
        project_id=os.getenv("VERCEL_PROJECT_ID"),
        token=os.getenv("VERCEL_TOKEN"),
        timeout=10 * 60 * 1000
    )

    sandbox.run_command("npm", ["ci"])
    snapshot = sandbox.snapshot()

    return {
        "sandboxId": sandbox.sandbox_id,
        "snapshotId": snapshot.snapshot_id,
        "preview": sandbox.domain(3000),
    }

@app.post("/refresh")
def refreshSandbox(props: RefreshProps):
    sandbox = Sandbox.create(
        ports=[3000], 
        source={"type": "snapshot", "snapshot_id": props.snapshotId},
        team_id=os.getenv("VERCEL_TEAM_ID"),
        project_id=os.getenv("VERCEL_PROJECT_ID"),
        token=os.getenv("VERCEL_TOKEN"),
        timeout=10 * 60 * 1000
    )

    snapshot = sandbox.snapshot()

    return {
        "sandboxId": sandbox.sandbox_id,
        "snapshotId": snapshot.snapshot_id,
        "preview": sandbox.domain(3000),
    }

@app.post("/directory")
async def viewDirectory(props: DirectoryProps):
    sandbox = Sandbox.get(
        sandbox_id=props.sandboxId,
        team_id=os.getenv("VERCEL_TEAM_ID"),
        project_id=os.getenv("VERCEL_PROJECT_ID"),
        token=os.getenv("VERCEL_TOKEN"),
    )

    val = sandbox.run_command("ls", [props.path])

    return { 
        "STDOUT": val.stdout(),
        "STDERR": val.stderr()
    }