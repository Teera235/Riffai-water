"""
API endpoints for grid-based tile system
"""
from fastapi import APIRouter, Query
from typing import Optional, List
from app.data.grid_tiles import (
    generate_thailand_tiles,
    get_tiles_by_risk,
    get_tile_by_id,
    get_tile_history,
    get_tiles_summary,
)

router = APIRouter()


@router.get("/tiles")
async def get_tiles(
    risk_level: Optional[str] = Query(None, regex="^(safe|normal|watch|warning|critical)$"),
):
    """
    Get all tiles or filter by risk level
    
    ⚠️ NOTE: Currently using simulated data for demonstration
    
    Risk levels:
    - safe: No risk
    - normal: Normal conditions
    - watch: Monitor closely
    - warning: High risk
    - critical: Immediate danger
    """
    if risk_level:
        tiles = get_tiles_by_risk(risk_level)
    else:
        tiles = generate_thailand_tiles()
    
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "id": tile["id"],
                "properties": {
                    **tile,
                    "bounds": None,  # Remove from properties
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [tile["bounds"][0][1], tile["bounds"][0][0]],  # SW
                        [tile["bounds"][1][1], tile["bounds"][0][0]],  # SE
                        [tile["bounds"][1][1], tile["bounds"][1][0]],  # NE
                        [tile["bounds"][0][1], tile["bounds"][1][0]],  # NW
                        [tile["bounds"][0][1], tile["bounds"][0][0]],  # Close
                    ]],
                },
            }
            for tile in tiles
        ],
        "meta": {
            "dataSource": "simulated",
            "warning": "This data is simulated for demonstration purposes",
            "note": "Production version will use real-time data from monitoring stations"
        }
    }


@router.get("/tiles/summary")
async def get_summary():
    """
    Get summary statistics of all tiles
    
    ⚠️ NOTE: Currently using simulated data for demonstration
    """
    summary = get_tiles_summary()
    summary["meta"] = {
        "dataSource": "simulated",
        "warning": "This data is simulated for demonstration purposes"
    }
    return summary


@router.get("/tiles/{tile_id}")
async def get_tile(tile_id: str):
    """Get detailed information for a specific tile"""
    tile = get_tile_by_id(tile_id)
    
    if not tile:
        return {"error": "Tile not found"}, 404
    
    return tile


@router.get("/tiles/{tile_id}/history")
async def get_history(
    tile_id: str,
    days: int = Query(default=7, ge=1, le=30),
):
    """Get historical data for a tile"""
    history = get_tile_history(tile_id, days)
    
    return {
        "tileId": tile_id,
        "days": days,
        "history": history,
    }


@router.get("/tiles/{tile_id}/satellite")
async def get_tile_satellite_data(tile_id: str):
    """
    Get satellite data for a specific tile
    
    Returns NDVI, NDWI, MNDWI, LSWI, NDBI indices and water area analysis
    """
    from app.services.earth_engine_service import get_earth_engine_service
    from datetime import datetime, timedelta
    
    # Parse tile ID to get coordinates
    # Format: tile_LAT_LON (e.g., tile_15.5_100.5)
    try:
        parts = tile_id.split("_")
        lat = float(parts[1])
        lon = float(parts[2])
    except:
        return {"error": "Invalid tile ID format"}, 400
    
    # Create bounding box (0.5 degree tile)
    tile_size = 0.5
    bbox = [lon, lat, lon + tile_size, lat + tile_size]
    
    # Get data for last 7 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    ee_service = get_earth_engine_service()
    data = ee_service.get_sentinel2_data(
        bbox,
        start_date.strftime('%Y-%m-%d'),
        end_date.strftime('%Y-%m-%d')
    )
    
    if not data:
        return {
            "error": "No satellite data available",
            "tileId": tile_id,
            "bbox": bbox
        }
    
    return {
        "tileId": tile_id,
        "bbox": bbox,
        "center": [lat + tile_size/2, lon + tile_size/2],
        "ndvi": data.get("avg_ndvi", 0),
        "ndwi": data.get("avg_ndwi", 0),
        "mndwi": data.get("avg_mndwi", 0),
        "lswi": data.get("avg_lswi", 0),
        "ndbi": data.get("avg_ndbi", 0),
        "waterArea": data.get("water_area_sqkm", 0),
        "date": data.get("acquisition_date", datetime.now().isoformat()),
        "cloudCoverage": data.get("cloud_coverage", 0),
        "source": data.get("source", "unknown"),
        "resolution": data.get("resolution_m", 10),
        "meta": {
            "dataSource": "sentinel-2" if not ee_service.mock_mode else "simulated",
            "warning": "This data is simulated for demonstration purposes" if ee_service.mock_mode else None
        }
    }
