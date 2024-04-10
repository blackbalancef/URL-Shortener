from pathlib import Path

import uvicorn
from dotenv import load_dotenv

if __name__ == "__main__":
    # it is important to load application, after environment loaded
    load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
