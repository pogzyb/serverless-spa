import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import cashflow
from api.config import get_config


logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


description = """
💰 <a href="https://github.com/peeriq/cashflow-challenge" target="_blank" rel="noreferrer">PeerIQ Cashflow Challenge</a> 💰
"""

def create_app() -> FastAPI:
    """
    Initializes the application.
    """
    cfg = get_config()
    
    app = FastAPI(
        title=cfg.app_name,
        debug=cfg.app_mode == "development",
        version=cfg.app_version,
        description=description
    )

    app.include_router(cashflow.cashflow, prefix="/cashflow")

    allow_origins=[
        "http://localhost",
        "http://localhost:3000"
    ]

    return CORSMiddleware(
        app,
        allow_origins=allow_origins, 
        allow_credentials=True, 
        allow_methods=["*"], 
        allow_headers=["*"],
        max_age=1200
    )


app = create_app()
