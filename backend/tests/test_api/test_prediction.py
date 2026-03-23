"""
Test prediction API endpoints
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_predict_flood(client: AsyncClient, sample_basin):
    """Test flood prediction endpoint"""
    response = await client.post(
        "/api/predict/flood",
        params={"basin_id": sample_basin.id, "days_ahead": 30}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "prediction_id" in data
    assert "flood_probability" in data
    assert "risk_level" in data
    assert 0 <= data["flood_probability"] <= 1
    assert data["basin_id"] == sample_basin.id


@pytest.mark.asyncio
async def test_predict_invalid_basin(client: AsyncClient):
    """Test prediction with invalid basin"""
    response = await client.post(
        "/api/predict/flood",
        params={"basin_id": "invalid", "days_ahead": 30}
    )
    
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_prediction_history(client: AsyncClient, sample_basin):
    """Test prediction history endpoint"""
    # First create a prediction
    await client.post(
        "/api/predict/flood",
        params={"basin_id": sample_basin.id, "days_ahead": 30}
    )
    
    # Get history
    response = await client.get(f"/api/predict/history/{sample_basin.id}")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "predictions" in data
    assert len(data["predictions"]) > 0


@pytest.mark.asyncio
async def test_model_accuracy(client: AsyncClient):
    """Test model accuracy endpoint"""
    response = await client.get("/api/predict/accuracy")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "models" in data
