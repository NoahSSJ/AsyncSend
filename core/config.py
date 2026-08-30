from pathlib import Path
from pprint import pprint

import yaml

class MyConfig():
    def __init__(self, yaml_Path: Path):
        self.yaml_path = yaml_Path

    def get_loader(self):
        yaml_str = Path(self.yaml_path).read_text(encoding='utf-8')
        config = yaml.safe_load(yaml_str)
        pprint(config)


a = MyConfig(yaml_Path=Path(__file__).parent.parent.joinpath('config.yaml'))
a.get_loader()