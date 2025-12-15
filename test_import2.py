#!/usr/bin/env python3
import warnings
warnings.filterwarnings('ignore')

print("Step 1: Importing parsers...", flush=True)
try:
    from backend.parsers import PDFParser, DOCXParser, TextParser
    print("Step 2: Parsers imported successfully", flush=True)
except Exception as e:
    print(f"ERROR importing parsers: {e}", flush=True)
    import traceback
    traceback.print_exc()

print("Step 3: Importing ATSScorer...", flush=True)
try:
    from backend.services.ats_scorer import ATSScorer
    print("Step 4: ATSScorer imported successfully", flush=True)
except Exception as e:
    print(f"ERROR importing ATSScorer: {e}", flush=True)
    import traceback
    traceback.print_exc()

print("SUCCESS: All imports completed")
