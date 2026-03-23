"""
Test AI service
"""
import pytest
from app.services.ai_service import AIService


def test_ai_service_predict():
    """Test AI service prediction"""
    service = AIService()
    
    # Mock data
    satellite_data = [
        (None, 0.5, 0.3, 0.2, 100.0),  # (date, ndvi, ndwi, mndwi, water_area)
        (None, 0.4, 0.35, 0.25, 120.0),
    ]
    water_data = [
        (None, 2.5),  # (datetime, level_m)
        (None, 2.8),
        (None, 3.0),
    ]
    rainfall_data = [
        (None, 10.0),  # (datetime, amount_mm)
        (None, 15.0),
        (None, 20.0),
    ]
    
    result = service.predict(
        basin_id="test_basin",
        satellite_data=satellite_data,
        water_data=water_data,
        rainfall_data=rainfall_data,
        days_ahead=30,
    )
    
    assert "flood_probability" in result
    assert "predicted_water_level" in result
    assert "affected_area_sqkm" in result
    assert "confidence" in result
    assert "model_version" in result
    
    assert 0 <= result["flood_probability"] <= 1
    assert result["confidence"] > 0
    assert result["model_version"] == "rule-based-v1"


def test_ai_service_high_risk():
    """Test AI service with high risk scenario"""
    service = AIService()
    
    # High risk data
    satellite_data = [(None, 0.3, 0.5, 0.4, 200.0)] * 5
    water_data = [(None, 4.8)] * 48  # High water level
    rainfall_data = [(None, 50.0)] * 72  # Heavy rain
    
    result = service.predict(
        basin_id="test_basin",
        satellite_data=satellite_data,
        water_data=water_data,
        rainfall_data=rainfall_data,
        days_ahead=7,
    )
    
    # Should predict high probability
    assert result["flood_probability"] > 0.5
