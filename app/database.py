from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


from app.models.user import Base

SQLALCHEMY_DATABASE_URL = (
    "postgresql+asyncpg://postgres:kaikeviss4896@localhost:5432/db_filelens"
)

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def shutdown_db():
    await engine.dispose()

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db
