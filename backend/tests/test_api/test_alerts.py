"""
Test alerts API endpoints
"""
import pytest
from httpx import AsyncClient

from app.models.models import Alert, RiskLevel


@pytest.mark.asyncio
async def test_alerts_feed_empty(client: AsyncClient):
    response = await client.get("/api/alerts")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_alerts_feed_history_read_dismiss(client: AsyncClient, sample_basin, db_session):
    alert = Alert(
        basin_id=sample_basin.id,
        level=RiskLevel.WARNING,
        title="Test alert",
        message="Message",
        trigger_type="water_level",
        trigger_value=1.5,
        threshold_value=2.0,
    )
    db_session.add(alert)
    await db_session.commit()
    await db_session.refresh(alert)

    feed = await client.get("/api/alerts")
    assert feed.status_code == 200
    rows = feed.json()
    assert len(rows) == 1
    assert rows[0]["id"] == alert.id
    assert rows[0]["acknowledged"] is False
    assert rows[0]["is_active"] is True

    hist = await client.get("/api/alerts/history?days=30")
    assert hist.status_code == 200
    assert len(hist.json()["alerts"]) == 1

    read = await client.post(f"/api/alerts/{alert.id}/read")
    assert read.status_code == 200

    feed2 = await client.get("/api/alerts")
    row = next(r for r in feed2.json() if r["id"] == alert.id)
    assert row["acknowledged"] is True

    dismiss = await client.delete(f"/api/alerts/{alert.id}")
    assert dismiss.status_code == 200

    hist2 = await client.get("/api/alerts/history?days=30")
    hist_row = next(a for a in hist2.json()["alerts"] if a["id"] == alert.id)
    assert hist_row["is_active"] is False


@pytest.mark.asyncio
async def test_alert_resolve(client: AsyncClient, sample_basin, db_session):
    alert = Alert(
        basin_id=sample_basin.id,
        level=RiskLevel.WARNING,
        title="R",
        message="M",
        trigger_type="water_level",
        trigger_value=1.0,
        threshold_value=2.0,
    )
    db_session.add(alert)
    await db_session.commit()
    await db_session.refresh(alert)

    res = await client.put(f"/api/alerts/{alert.id}/resolve")
    assert res.status_code == 200
    await db_session.refresh(alert)
    assert alert.is_active is False


@pytest.mark.asyncio
async def test_tile_satellite_bad_id_returns_400(client: AsyncClient):
    r = await client.get("/api/map/tiles/not_a_tile_id/satellite")
    assert r.status_code == 400
    body = r.json()
    assert "detail" in body
