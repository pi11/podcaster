from sanic import Sanic
from tortoise.contrib.sanic import register_tortoise
from aerich import Command

from app.config import TORTOISE_ORM, SANIC_CONFIG
from app.routes.main import bp as main_bp

app = Sanic("podcaster")
app.config.update(SANIC_CONFIG)

# Register blueprints
app.blueprint(main_bp)

# Register Tortoise ORM
register_tortoise(app, config=TORTOISE_ORM, generate_schemas=True)


# Initialize Aerich
@app.listener("before_server_start")
async def init_aerich(app, loop):
    command = Command(tortoise_config=TORTOISE_ORM)
    await command.init()


if __name__ == "__main__":
    app.run(
        host=app.config.HOST,
        port=app.config.PORT,
        debug=app.config.DEBUG,
        auto_reload=app.config.DEBUG,
    )
