# Designer Agent Backend

A FastAPI service for accessing Vercel sandboxes. It includes tools 

## Tech Stack

- Python3
- [FastAPI](https://fastapi.tiangolo.com/)
- [uv](https://github.com/astral-sh/uv)
- [Vercel Sandboxes](https://vercel.com/docs/vercel-sandbox)
- Uvicorn

## Prerequisites

Make sure you have the following installed:

- Python 
- pip 
- uv

## Setup & Installation

1. Clone the repository
```
git clone https://github.com/nobelsu/designer-backend
cd designer-backend
```
2. Activate virtual environment
```
uv venv
```
3. Install dependencies
```
uv pip install -r requirements.txt
```
4. Create a Vercel deployment
5. Setup environment variables (see below)
6. Run the server
``` 
fastapi dev main.py
```

## Environment Variables

This project uses environment variables for configuration.

1. Create an environment file

Create a file called .env.local in the project root

2. Add variables

Fill in the values as needed:
```
VERCEL_TOKEN=
VERCEL_TEAM_ID=
VERCEL_PROJECT_ID=
```
3. Note that these Vercel keys are from the deployment you created
