from envparse import Env

env = Env()

POSTGRES_DATABASE_URL = env.str("POSTGRES_DATABASE_URL", default="postgresql://postgres:postgres@0.0.0.0:5432/")
ELASTIC_URL = env.str("ELASTIC_URL", default="http://0.0.0.0:9200")
