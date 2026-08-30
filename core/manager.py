import asyncio
import httpx
import logging
from pathlib import Path

def get_root_dir():
    current_path = Path(__file__).resolve()
    while True:
        flag_path = current_path.joinpath('pyproject.toml')
        if not flag_path.is_file():
            current_path = current_path.parent
        else:
            return current_path

root_dir = get_root_dir()
save_dir = root_dir / "images"
save_dir.mkdir(parents=True, exist_ok=True)

class SendManager():
    def __init__(self):
        self.sites = []
        
    
    
