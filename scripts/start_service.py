"""
GracefulOS Windows Service Entrypoint Script
"""

import sys
from pathlib import Path
import uvicorn

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config.settings import config

def main():
    print("=" * 60)
    print(f"Starting GracefulOS Control Plane on http://{config.host}:{config.port}")
    print("=" * 60)
    uvicorn.run("core.gateway.app:app", host=config.host, port=config.port, log_level="info")

if __name__ == "__main__":
    main()
