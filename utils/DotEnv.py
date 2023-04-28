# search for .env file in the project directory
# and load it into the environment

import os

class DotEnv:
        def __init__(self):
            pass
    
        @staticmethod
        def load():
            file = os.path.join(os.path.dirname(__file__), '..', '.env')
            if os.path.isfile(file):
                print('Loading environment from .env file')
                with open(file) as f:
                    for line in f:
                        var = line.strip().split('=', 1)
                        if len(var) == 2:
                            os.environ[var[0]] = var[1]
            else:
                print('No .env file found')
    
        @staticmethod
        def get(key):
            return os.getenv(key)

        @staticmethod
        def get_by_prefix(prefix):
            return {k: v for k, v in os.environ.items() if k.startswith(prefix)}

