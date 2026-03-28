"""
Test dashboard API endpoints
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_dashboard_summary(client: AsyncClient):
    """Test dashboard summary aggregates for analytics"""
    response = await client.get("/api/dashboard/summary?days=7")
    assert response.status_code == 200
    data = response.json()
    assert data["period_days"] == 7
    assert "avgWaterLevel" in data
    assert "totalRainfall" in data
    assert isinstance(data["avgWaterLevel"], (int, float))
    assert isinstance(data["totalRainfall"], (int, float))


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
    assert "water_levels" in data
    assert "rainfall" in data
    assert "satellite_indices" in data


@pytest.mark.asyncio
async def test_dashboard_invalid_basin(client: AsyncClient):
    """Invalid basin still returns 200 with empty series (no basin guard on stats route)"""
    response = await client.get("/api/dashboard/stats/invalid_basin")

    assert response.status_code == 200
    data = response.json()
    assert data["basin_id"] == "invalid_basin"
