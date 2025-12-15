#!/usr/bin/env python3
"""Debug: Test imports and run analysis, then start server"""
import sys
print("Step 1: Test imports")
try:
    from backend.main import app
    print("  ✓ Backend imports OK")
except Exception as e:
    print(f"  ✗ Backend import failed: {e}")
    sys.exit(1)

print("\nStep 2: Start server")
try:
    import uvicorn
    print("  Starting uvicorn...")
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="warning"
    )
except KeyboardInterrupt:
    print("\n  Server stopped by user")
except Exception as e:
    print(f"  ✗ Server error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
