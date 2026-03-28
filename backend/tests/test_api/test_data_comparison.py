"""Test data comparison endpoint"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_data_comparison(client: AsyncClient, sample_basin):
    r = await client.get(
        f"/api/data/comparison/{sample_basin.id}",
        params={"year1": 2020, "year2": 2021},
    )
    assert r.status_code == 200
    d = r.json()
    assert d["basin_id"] == sample_basin.id
    assert d["year1"]["year"] == 2020
    assert d["year2"]["year"] == 2021
    assert "total_rainfall_mm" in d["year1"]
