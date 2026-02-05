from typing import Union
from dotenv import load_dotenv
from vercel.sandbox import Sandbox
from fastapi import FastAPI

app = FastAPI()

load_dotenv('.env.local')

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/sandbox")
def createSandbox():
    sandbox = Sandbox.create(
        ports=[3000], 
        source={"type": "git", "url":"https://github.com/nobelsu/expo-template"}
    )

    sandbox.run_command("npm", ["ci"])
    sandbox.run_command_detached("npx", ["expo", "start", "--web", "--port", "3000"])

    return {
        "sandboxID": sandbox.sandbox_id,
        "preview": sandbox.domain(3000),
    }