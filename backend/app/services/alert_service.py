from google.cloud import pubsub_v1
from datetime import datetime
import json

from app.config import get_settings
from app.models.models import RiskLevel

settings = get_settings()


class AlertService:
    def __init__(self):
        try:
            self.publisher = pubsub_v1.PublisherClient()
            self.topic_path = self.publisher.topic_path(
                settings.GCP_PROJECT_ID, "riffai-alerts"
            )
        except Exception:
            self.publisher = None
            self.topic_path = None
    
    def evaluate_risk(
        self,
        water_level: float = None,
        rainfall_mm: float = None,
        ndwi: float = None,
        flood_probability: float = None,
    ) -> RiskLevel:
        """ประเมินระดับความเสี่ยงจากข้อมูลหลายแหล่ง"""
        
        scores = []
        
        if water_level is not None:
            if water_level > settings.ALERT_WATER_LEVEL_CRITICAL:
                scores.append(4)
            elif water_level > settings.ALERT_WATER_LEVEL_WARNING:
                scores.append(3)
            elif water_level > settings.ALERT_WATER_LEVEL_WARNING * 0.8:
                scores.append(2)
            else:
                scores.append(1)
        
        if rainfall_mm is not None:
            if rainfall_mm > 200:
                scores.append(4)
            elif rainfall_mm > settings.ALERT_RAINFALL_WARNING:
                scores.append(3)
            elif rainfall_mm > 50:
                scores.append(2)
            else:
                scores.append(1)
        
        if ndwi is not None:
            if ndwi > 0.5:
                scores.append(4)
            elif ndwi > settings.ALERT_NDWI_WARNING:
                scores.append(3)
            elif ndwi > 0.2:
                scores.append(2)
            else:
                scores.append(1)
        
        if flood_probability is not None:
            if flood_probability > 0.8:
                scores.append(4)
            elif flood_probability > 0.6:
                scores.append(3)
            elif flood_probability > 0.4:
                scores.append(2)
            else:
                scores.append(1)
        
        if not scores:
            return RiskLevel.NORMAL
        
        max_score = max(scores)
        return {
            1: RiskLevel.NORMAL,
            2: RiskLevel.WATCH,
            3: RiskLevel.WARNING,
            4: RiskLevel.CRITICAL,
        }[max_score]
    
    async def publish_alert(self, alert_data: dict):
        """ส่ง alert ผ่าน Pub/Sub"""
        if not self.publisher:
            print(f"[Alert Local] {alert_data}")
            return
        
        message = json.dumps(alert_data, default=str).encode("utf-8")
        future = self.publisher.publish(self.topic_path, message)
        return future.result()
