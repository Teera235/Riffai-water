"""
Pytest configuration and fixtures
"""
import asyncio
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.main import app
from app.models.database import Base, get_db
from app.config import get_settings

settings = get_settings()

# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://riffai:riffai123@localhost:5433/riffai_test"


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    """Create test database engine"""
    engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest.fixture
async def db_session(test_engine):
    """Create test database session"""
    async_session = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def client(db_session):
    """Create test client with database override"""
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture
async def auth_headers(client, db_session):
    """Create authenticated user and return headers"""
    from app.models.models import User
    from app.core.security import hash_password, create_access_token
    
    # Create test user
    user = User(
        email="test@riffai.org",
        name="Test User",
        password_hash=hash_password("test123"),
        role="admin",
        organization="Test Org",
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    # Create token
    token = create_access_token({"sub": user.id})
    
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
async def sample_basin(db_session):
    """Create sample basin for testing"""
    from app.models.models import Basin
    
    basin = Basin(
        id="test_basin",
        name="Test Basin",
        name_en="Test Basin",
        provinces=["Test Province"],
        area_sqkm=1000,
        bbox=[100.0, 13.0, 101.0, 14.0],
    )
    db_session.add(basin)
    await db_session.commit()
    await db_session.refresh(basin)
    
    return basin
