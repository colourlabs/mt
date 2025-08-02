import os
import yaml

class Config:
    def __init__(self, path="./config.yml"):
        with open(path) as f:
            data = yaml.safe_load(f)

        self.port = int(os.getenv("PORT", data.get("port", 8080)))
        self.replica_timeout = float(data.get("replica_timeout", 60))
        self.host = os.getenv("HOST", data.get("host", "127.0.0.1"))