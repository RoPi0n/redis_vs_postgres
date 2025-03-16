from quart import Quart
from .helpers.database import Postgres
from .helpers.redis_pool import RedisPool
from .controllers import module, tests
from config import Config

app = Quart('perfomance-test-app', template_folder=None, static_folder=None)
app.config.from_object(Config)
Postgres(app)
RedisPool(app)

app.register_blueprint(module)