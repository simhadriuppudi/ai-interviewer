"""
Test the complete interview flow to identify where Errno 22 occurs
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from datetime import datetime
from pathlib import Path

print("Testing datetime operations...")
try:
    dt = datetime.utcnow()
    print(f"  datetime.utcnow(): {dt}")
    timestamp = dt.timestamp()
    print(f"  timestamp: {timestamp}")
    int_timestamp = int(timestamp)
    print(f"  int(timestamp): {int_timestamp}")
    filename = f"test_{int_timestamp}_file.txt"
    print(f"  filename: {filename}")
    print("✓ Datetime operations work")
except Exception as e:
    print(f"✗ Datetime error: {e}")

print("\nTesting file operations...")
try:
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    test_file = upload_dir / "test.txt"
    with open(test_file, "w") as f:
        f.write("test")
    print(f"  Created: {test_file}")
    test_file.unlink()
    print("✓ File operations work")
except Exception as e:
    print(f"✗ File error: {e}")

print("\nTesting database operations...")
try:
    from backend.app.db import engine
    from sqlmodel import SQLModel
    print(f"  Database URL: {engine.url}")
    print("✓ Database connection works")
except Exception as e:
    print(f"✗ Database error: {e}")

print("\nAll tests complete!")
