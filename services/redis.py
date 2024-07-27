import redis


class RedisClient:
    def __init__(self, host: str, port: int, db: int = 0):
        self.host = host
        self.port = port
        self.db = db
        self.client = None

    def connect(self):
        self.client = redis.Redis(host=self.host, port=self.port, db=self.db)
        try:
            self.client.ping()
            print(f"Connected to Redis at {self.host}:{self.port}")
        except redis.ConnectionError as e:
            print(f"Failed to connect to Redis: {e}")
            self.client = None

    def get_client(self):
        if not self.client:
            self.connect()
        return self.client


redis_client = RedisClient(host='redis', port=6379)
