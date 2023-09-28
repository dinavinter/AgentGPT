import asyncio
from calendar import c
from math import e
from ssl import CERT_REQUIRED
from typing import AsyncGenerator
import aiomysql
from reworkd_platform.db.models.agent import AgentRun, AgentTask
from reworkd_platform.db.utils import create_database, drop_database
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from typing import Any, AsyncGenerator
from sqlalchemy import and_, func, select

from reworkd_platform.services.ssl import get_ssl_context
from reworkd_platform.settings import settings
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from reworkd_platform.db.dependencies import get_db_session
from reworkd_platform.db.utils import create_database, create_engine, drop_database
from reworkd_platform.settings import settings
from reworkd_platform.web.application import get_app


# print settings as json
print(str(settings.db_url))
print("db_echo: "+ str(settings.db_echo))
print("environment: "+ settings.environment)
print("db_base: "+ settings.db_base)
print("db_url: "+ str(settings.db_url))
print("db_host: "+ settings.db_host)
print("db_port: "+ str(settings.db_port))
print("db_user: "+ settings.db_user)
print("db_password: "+ settings.db_pass)



loop = asyncio.get_event_loop()

async def test_example():
    conn = await aiomysql.connect(host='db', port=3307,
                                  user='reworkd_platform', password='reworkd_platform', db='reworkd_platform',
                                  loop=loop)


    print(conn)
    cur = await conn.cursor()

    await cur.execute("SELECT * FROM agent_run")
    print(cur.description)
    r = await cur.fetchall()
    print(r)
    await cur.close()
    conn.close()


async def test_example2():
    # conn = await aiomysql.connect(host=settings.db_host, port=settings.db_port,
    #                               user=settings.db_user, password=settings.db_pass, db=settings.db_base,
    #                               loop=loop)
    from reworkd_platform.db.meta import meta  # noqa: WPS433

    # engine = create_async_engine(
    #     str(settings.db_url),
    #     echo=settings.db_echo,
    # )

    ssl_context = get_ssl_context(settings)
    ssl_context.verify_mode = CERT_REQUIRED
    connect_args = {"ssl": ssl_context}

    engine = create_async_engine(
        str(settings.db_url),
        echo=settings.db_echo,
        # connect_args=connect_args,
    )
    try:
        async with engine.begin() as conn:
            # await conn.run_sync(meta.create_all)

            print(str(conn))
            try:
                session_maker = async_sessionmaker(conn, expire_on_commit=False)
                session = session_maker()
                print(str(session))
                agent_run = await AgentRun.get(session, "059d96f9-8655-4063-a912-d130bb258d21")
                print(agent_run.goal)
            finally:
                await session.close()

    finally:
        await engine.dispose()




try:
    loop.run_until_complete(test_example2())
finally:
    loop.close()
#  {'host': 'db', 'db': 'reworkd_platform', 'user': 'reworkd_platform', 'password': 'reworkd_platform', 'port': 3307,



async def engine() -> AsyncGenerator[AsyncEngine, None]:
    """
    Create engine and databases.

    :yield: new engine.
    """
    from reworkd_platform.db.meta import meta  # noqa: WPS433
    from reworkd_platform.db.models import load_all_models  # noqa: WPS433

    load_all_models()

    await create_database()




    engine = create_async_engine(
            str(settings.db_url),
            echo=settings.db_echo,
        )
    async with engine.begin() as conn:
        await conn.run_sync(meta.create_all)

    try:
        yield engine
    finally:
        await engine.dispose()
        await drop_database()


async def dbsession(
    _engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    """
    Get session to database.

    Fixture that returns a SQLAlchemy session with a SAVEPOINT, and the rollback to it
    after the test completes.

    :param _engine: current engine.
    :yields: async session.
    """
    connection = await _engine.connect()
    trans = await connection.begin()

    session_maker = async_sessionmaker(
        connection,
        expire_on_commit=False,
    )
    session = session_maker()

    try:
        yield session
    finally:
        await session.close()
        await trans.rollback()
        await connection.close()

def fastapi_app(dbsession: AsyncSession) -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    application = get_app()
    application.dependency_overrides[get_db_session] = lambda: dbsession
    return application  # noqa: WPS331

async def client(
    fastapi_app: FastAPI, anyio_backend: Any
) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture that creates client for requesting server.

    :param fastapi_app: the application.
    :yield: client for the app.
    """
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


agent_loop = asyncio.get_event_loop()

# Run the test sequence
async def test_engine():
     async with engine() as e:
        async with dbsession(e) as session:
            app = fastapi_app(session)
            async with client(app) as ac:
                response = await ac.get("/agent/create")
                print(response.status_code)
                print(response.json())



# agent_loop.run_until_complete(test_engine())


async def run():
    async for e in engine():
        session = await dbsession(e)
        app = fastapi_app(session)
        async for ac in client(app):
            response = await ac.get("/agent/create")
            print(response.status_code)
            print(response.json())




# import asyncio
# loop = asyncio.get_event_loop()
# try:
#     loop.run_until_complete(run())
# finally:
#     loop.close()



