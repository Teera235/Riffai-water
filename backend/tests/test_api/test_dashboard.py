"""
Test dashboard API endpoints
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_dashboard_overview(client: AsyncClient):
    """Test dashboard overview endpoint"""
    response = await client.get("/api/dashboard/overview")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "timestamp" in data
    assert "active_alerts" in data
    assert "basins" in data
    assert "summary" in data
    assert isinstance(data["basins"], list)


@pytest.mark.asyncio
async def test_dashboard_basin_stats(client: AsyncClient, sample_basin):
    """Test basin statistics endpoint"""
    response = await client.get(f"/api/dashboard/stats/{sample_basin.id}")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["basin_id"] == sample_basin.id
    assert "water_level" in data
    assert "rainfall" in data
    assert "alerts" in data


@pytest.mark.asyncio
async def test_dashboard_invalid_basin(client: AsyncClient):
    """Test dashboard with invalid basin ID"""
    response = await client.get("/api/dashboard/stats/invalid_basin")
    
    assert response.status_code == 404
