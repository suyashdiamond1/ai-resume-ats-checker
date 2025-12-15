#!/usr/bin/env python3
import warnings
warnings.filterwarnings('ignore')

print("Step 1: Testing imports step by step...", flush=True)

print("1.1: import re", flush=True)
import re
print("1.2: import typing", flush=True)
from typing import List, Dict, Tuple, Set
print("1.3: import collections", flush=True)
from collections import Counter
print("1.4: import sklearn TfidfVectorizer", flush=True)
from sklearn.feature_extraction.text import TfidfVectorizer
print("1.5: import sklearn cosine_similarity", flush=True)
from sklearn.metrics.pairwise import cosine_similarity
print("1.6: import numpy", flush=True)
import numpy as np

print("\nStep 2: Attempting to import ATSScorer...", flush=True)
from backend.services.ats_scorer import ATSScorer
print("SUCCESS - ATSScorer imported", flush=True)
