#!/usr/bin/env python3
import warnings
warnings.filterwarnings('ignore')

print("Step 1: Importing FastAPI...", flush=True)
from fastapi import FastAPI
print("Step 2: FastAPI imported", flush=True)

print("Step 3: Importing routes...", flush=True)
from backend.api.routes import router
print("Step 4: Routes imported", flush=True)

print("Step 5: Creating app...", flush=True)
app = FastAPI()
print("Step 6: App created", flush=True)

print("SUCCESS: All imports completed")
print(f"App object: {app}")
