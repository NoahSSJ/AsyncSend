from datetime import datetime
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
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
log_dir = root_dir / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
log_path = log_dir.joinpath(f"run_{timestamp}.log")
logging.basicConfig(
    filename=log_path,
    format="%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s",
    level=logging.INFO,
    encoding='utf-8'
)

log = logging.getLogger("project")