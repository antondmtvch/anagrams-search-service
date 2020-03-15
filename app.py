import sys
import aioredis

from aiohttp import web
from loguru import logger
from aiohttp_apispec import validation_middleware
from aiohttp_apispec import setup_aiohttp_apispec

from api.routes import setup_routes
from settings import load_settings


async def setup_redis(app: web.Application, db: int) -> aioredis.ConnectionsPool:

    try:
        pool = await aioredis.create_pool((
            app['settings']['redis']['REDIS_HOST'],
            app['settings']['redis']['REDIS_PORT']
        ),
            db=db
        )
    except (OSError, KeyError) as e:
        logger.error(e)
        sys.exit(1)

    async def close_redis(app: web.Application):
        pool.close()
        await pool.wait_closed()

    app.on_cleanup.append(close_redis)
    app['redis-pool'] = pool

    return pool


async def init_app(settings: dict, db: int, **kwargs) -> web.Application:

    app = web.Application(**kwargs)

    app['settings'] = settings

    setup_routes(app)

    setup_aiohttp_apispec(app)

    app.middlewares.append(validation_middleware)

    await setup_redis(app, db)

    logger.debug(app['settings'])

    return app


def main():
    settings = load_settings()
    app = init_app(settings, db=settings['redis']['REDIS_DB'])
    try:
        web.run_app(app, host=settings['app']['APP_HOST'], port=settings['app']['APP_PORT'])
    except KeyError as e:
        logger.error(e)


if __name__ == '__main__':
    main()
