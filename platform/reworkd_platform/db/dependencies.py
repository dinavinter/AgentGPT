from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

#
# # This code creates and gets a database session for the current request.
# async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
#     """
#     Create and get database session.
#
#     :param request: current request.
#     :yield: database session.
#     """
#     session: AsyncSession = request.app.state.db_session_factory()
#
#     try:  # noqa: WPS501
#         yield session

async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """
    Create and get database session.

    :param request: current request.
    :yield: database session.
    """
    session: AsyncSession = request.app.state.db_session_factory()

    try:  # noqa: WPS501
        yield session
        await session.commit()
    finally:
        await session.close()
