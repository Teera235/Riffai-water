"""
Google Earth Engine Service for Satellite Data
Production-ready implementation with error handling and fallback
"""
import ee
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json
import os


class EarthEngineService:
    """
    Service for fetching satellite data from Google Earth Engine
    
    Supports:
    - Sentinel-2 (optical imagery, 10m resolution)
    - Sentinel-1 (SAR imagery, 10m resolution)
    - NDVI, NDWI, MNDWI calculations
    - Water area detection
    """
    
    def __init__(self):
        self.initialized = False
        self.mock_mode = True
        self._initialize()
    
    def _initialize(self):
        """Initialize Earth Engine with authentication"""
        try:
            # Project ID
            project_id = os.getenv('GEE_PROJECT_ID', 'trim-descent-452802-t2')
            
            # Try to initialize with service account
            service_account = os.getenv('GEE_SERVICE_ACCOUNT')
            key_file = os.getenv('GEE_KEY_FILE')
            
            if service_account and key_file and os.path.exists(key_file):
                credentials = ee.ServiceAccountCredentials(service_account, key_file)
                ee.Initialize(credentials, project=project_id)
                self.initialized = True
                self.mock_mode = False
                print("✅ Earth Engine initialized with service account")
            else:
                # Try default authentication with project
                try:
                    ee.Initialize(project=project_id)
                    self.initialized = True
                    self.mock_mode = False
                    print(f"✅ Earth Engine initialized with project: {project_id}")
                except Exception as e:
                    print(f"⚠️  Earth Engine not authenticated: {e}")
                    print("    Running in MOCK mode")
                    print("    To enable: Run 'python authenticate-ee.py' or set GEE_SERVICE_ACCOUNT")
                    
        except Exception as e:
            print(f"⚠️  Earth Engine initialization failed: {e}")
            print("    Running in MOCK mode")
    
    def get_sentinel2_data(
        self,
        bbox: List[float],
        start_date: str,
        end_date: str,
        max_cloud_cover: float = 30.0
    ) -> Optional[Dict]:
        """
        Fetch Sentinel-2 data for a bounding box
        
        Args:
            bbox: [min_lon, min_lat, max_lon, max_lat]
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            max_cloud_cover: Maximum cloud coverage percentage
        
        Returns:
            Dictionary with satellite data and indices
        """
        if self.mock_mode:
            return self._get_mock_sentinel2_data(bbox, start_date, end_date)
        
        try:
            # Define area of interest
            aoi = ee.Geometry.Rectangle(bbox)
            
            # Load Sentinel-2 collection
            collection = (
                ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
                .filterBounds(aoi)
                .filterDate(start_date, end_date)
                .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', max_cloud_cover))
                .sort('CLOUDY_PIXEL_PERCENTAGE')
            )
            
            # Get the least cloudy image
            image = collection.first()
            
            if image is None:
                print(f"⚠️  No Sentinel-2 images found for {start_date} to {end_date}")
                return None
            
            # Get image info
            info = image.getInfo()
            properties = info.get('properties', {})
            
            # Calculate indices
            ndvi = self._calculate_ndvi(image)
            ndwi = self._calculate_ndwi(image)
            mndwi = self._calculate_mndwi(image)
            lswi = self._calculate_lswi(image)
            ndbi = self._calculate_ndbi(image)
            
            # Calculate water area
            water_mask = mndwi.gt(0.0)  # MNDWI > 0 indicates water
            water_area_sqm = water_mask.multiply(ee.Image.pixelArea()).reduceRegion(
                reducer=ee.Reducer.sum(),
                geometry=aoi,
                scale=10,
                maxPixels=1e9
            ).getInfo().get('MNDWI', 0)
            
            water_area_sqkm = water_area_sqm / 1_000_000
            
            # Get mean values
            ndvi_mean = ndvi.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=aoi,
                scale=10,
                maxPixels=1e9
            ).getInfo().get('NDVI', 0)
            
            ndwi_mean = ndwi.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=aoi,
                scale=10,
                maxPixels=1e9
            ).getInfo().get('NDWI', 0)
            
            mndwi_mean = mndwi.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=aoi,
                scale=10,
                maxPixels=1e9
            ).getInfo().get('MNDWI', 0)
            
            lswi_mean = lswi.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=aoi,
                scale=10,
                maxPixels=1e9
            ).getInfo().get('LSWI', 0)
            
            ndbi_mean = ndbi.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=aoi,
                scale=10,
                maxPixels=1e9
            ).getInfo().get('NDBI', 0)
            
            return {
                'source': 'sentinel-2',
                'acquisition_date': properties.get('system:time_start'),
                'cloud_coverage': properties.get('CLOUDY_PIXEL_PERCENTAGE', 0),
                'resolution_m': 10,
                'avg_ndvi': round(ndvi_mean, 4),
                'avg_ndwi': round(ndwi_mean, 4),
                'avg_mndwi': round(mndwi_mean, 4),
                'avg_lswi': round(lswi_mean, 4),
                'avg_ndbi': round(ndbi_mean, 4),
                'water_area_sqkm': round(water_area_sqkm, 2),
                'bbox': bbox,
                'image_id': info.get('id')
            }
            
        except Exception as e:
            print(f"❌ Error fetching Sentinel-2 data: {e}")
            return self._get_mock_sentinel2_data(bbox, start_date, end_date)
    
    def _calculate_ndvi(self, image: ee.Image) -> ee.Image:
        """Calculate Normalized Difference Vegetation Index"""
        nir = image.select('B8')
        red = image.select('B4')
        ndvi = nir.subtract(red).divide(nir.add(red)).rename('NDVI')
        return ndvi
    
    def _calculate_ndwi(self, image: ee.Image) -> ee.Image:
        """Calculate Normalized Difference Water Index"""
        green = image.select('B3')
        nir = image.select('B8')
        ndwi = green.subtract(nir).divide(green.add(nir)).rename('NDWI')
        return ndwi
    
    def _calculate_mndwi(self, image: ee.Image) -> ee.Image:
        """Calculate Modified Normalized Difference Water Index"""
        green = image.select('B3')
        swir = image.select('B11')
        mndwi = green.subtract(swir).divide(green.add(swir)).rename('MNDWI')
        return mndwi
    
    def _calculate_lswi(self, image: ee.Image) -> ee.Image:
        """Calculate Land Surface Water Index"""
        nir = image.select('B8')
        swir = image.select('B11')
        lswi = nir.subtract(swir).divide(nir.add(swir)).rename('LSWI')
        return lswi
    
    def _calculate_ndbi(self, image: ee.Image) -> ee.Image:
        """Calculate Normalized Difference Built-up Index"""
        swir = image.select('B11')
        nir = image.select('B8')
        ndbi = swir.subtract(nir).divide(swir.add(nir)).rename('NDBI')
        return ndbi
    
    def get_sentinel1_sar(
        self,
        bbox: List[float],
        start_date: str,
        end_date: str
    ) -> Optional[Dict]:
        """
        Fetch Sentinel-1 SAR data for water detection
        
        Args:
            bbox: [min_lon, min_lat, max_lon, max_lat]
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
        
        Returns:
            Dictionary with SAR data including VV, VH, ratio, and change detection
        """
        if self.mock_mode:
            return self._get_mock_sentinel1_data(bbox, start_date, end_date)
        
        try:
            # Define area of interest
            aoi = ee.Geometry.Rectangle(bbox)
            
            # Load Sentinel-1 GRD collection
            collection = (
                ee.ImageCollection('COPERNICUS/S1_GRD')
                .filterBounds(aoi)
                .filterDate(start_date, end_date)
                .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
                .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))
                .filter(ee.Filter.eq('instrumentMode', 'IW'))
                .select(['VV', 'VH'])
            )
            
            # Get most recent image
            image = collection.sort('system:time_start', False).first()
            
            if image is None:
                print(f"⚠️  No Sentinel-1 images found for {start_date} to {end_date}")
                return None
            
            # Get image info
            info = image.getInfo()
            properties = info.get('properties', {})
            
            # Get VV and VH bands
            vv = image.select('VV')
            vh = image.select('VH')
            
            # Calculate VV/VH ratio
            ratio = vv.divide(vh).rename('VV_VH_ratio')
            
            # Calculate mean values
            vv_mean = vv.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=aoi,
                scale=10,
                maxPixels=1e9
            ).getInfo().get('VV', 0)
            
            vh_mean = vh.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=aoi,
                scale=10,
                maxPixels=1e9
            ).getInfo().get('VH', 0)
            
            ratio_mean = ratio.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=aoi,
                scale=10,
                maxPixels=1e9
            ).getInfo().get('VV_VH_ratio', 0)
            
            # Water detection using VV threshold (typically < -15 dB for water)
            water_mask = vv.lt(-15)
            water_area_sqm = water_mask.multiply(ee.Image.pixelArea()).reduceRegion(
                reducer=ee.Reducer.sum(),
                geometry=aoi,
                scale=10,
                maxPixels=1e9
            ).getInfo().get('VV', 0)
            
            water_area_sqkm = water_area_sqm / 1_000_000
            
            # Change detection (compare with previous month)
            prev_start = (datetime.fromisoformat(start_date) - timedelta(days=30)).strftime('%Y-%m-%d')
            prev_end = start_date
            
            prev_collection = (
                ee.ImageCollection('COPERNICUS/S1_GRD')
                .filterBounds(aoi)
                .filterDate(prev_start, prev_end)
                .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
                .filter(ee.Filter.eq('instrumentMode', 'IW'))
                .select('VV')
            )
            
            prev_image = prev_collection.sort('system:time_start', False).first()
            
            change_detected = False
            change_area_sqkm = 0
            
            if prev_image:
                # Calculate difference
                diff = vv.subtract(prev_image.select('VV'))
                
                # Significant change threshold (> 3 dB change)
                change_mask = diff.abs().gt(3)
                change_area_sqm = change_mask.multiply(ee.Image.pixelArea()).reduceRegion(
                    reducer=ee.Reducer.sum(),
                    geometry=aoi,
                    scale=10,
                    maxPixels=1e9
                ).getInfo().get('VV', 0)
                
                change_area_sqkm = change_area_sqm / 1_000_000
                change_detected = change_area_sqkm > 1.0  # Significant if > 1 sqkm changed
            
            return {
                'source': 'sentinel-1-sar',
                'acquisition_date': properties.get('system:time_start'),
                'resolution_m': 10,
                'orbit_direction': properties.get('orbitProperties_pass', 'UNKNOWN'),
                'vv_mean_db': round(vv_mean, 2),
                'vh_mean_db': round(vh_mean, 2),
                'vv_vh_ratio': round(ratio_mean, 2),
                'water_area_sqkm': round(water_area_sqkm, 2),
                'change_detected': change_detected,
                'change_area_sqkm': round(change_area_sqkm, 2),
                'bbox': bbox,
                'image_id': info.get('id')
            }
            
        except Exception as e:
            print(f"❌ Error fetching Sentinel-1 data: {e}")
            return self._get_mock_sentinel1_data(bbox, start_date, end_date)
    
    def _get_mock_sentinel1_data(
        self,
        bbox: List[float],
        start_date: str,
        end_date: str
    ) -> Dict:
        """Generate mock Sentinel-1 SAR data"""
        import random
        
        try:
            date = datetime.fromisoformat(start_date)
        except:
            date = datetime.now()
        
        # Seasonal variation
        month = date.month
        is_wet_season = month in [5, 6, 7, 8, 9, 10]
        
        # SAR backscatter values (in dB)
        vv_mean = round(random.uniform(-18, -12) if is_wet_season else random.uniform(-14, -8), 2)
        vh_mean = round(random.uniform(-24, -18) if is_wet_season else random.uniform(-20, -14), 2)
        ratio = round(vv_mean / vh_mean if vh_mean != 0 else 1.0, 2)
        
        # Calculate approximate area
        lon_diff = abs(bbox[2] - bbox[0])
        lat_diff = abs(bbox[3] - bbox[1])
        approx_area_sqkm = lon_diff * lat_diff * 111 * 111
        
        water_area_factor = random.uniform(0.12, 0.20) if is_wet_season else random.uniform(0.03, 0.08)
        water_area_sqkm = round(approx_area_sqkm * water_area_factor, 2)
        
        change_detected = random.random() > 0.7  # 30% chance of change
        change_area_sqkm = round(random.uniform(1, 10), 2) if change_detected else 0
        
        return {
            'source': 'sentinel-1-sar-mock',
            'acquisition_date': date.isoformat(),
            'resolution_m': 10,
            'orbit_direction': random.choice(['ASCENDING', 'DESCENDING']),
            'vv_mean_db': vv_mean,
            'vh_mean_db': vh_mean,
            'vv_vh_ratio': ratio,
            'water_area_sqkm': water_area_sqkm,
            'change_detected': change_detected,
            'change_area_sqkm': change_area_sqkm,
            'bbox': bbox,
            'image_id': f'mock_s1_{date.strftime("%Y%m%d")}'
        }
    
    def get_time_series(
        self,
        bbox: List[float],
        start_date: str,
        end_date: str,
        interval_days: int = 5
    ) -> List[Dict]:
        """
        Get time series of satellite data
        
        Args:
            bbox: Bounding box
            start_date: Start date
            end_date: End date
            interval_days: Interval between images
        
        Returns:
            List of satellite data dictionaries
        """
        results = []
        
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        current = start
        
        while current <= end:
            next_date = current + timedelta(days=interval_days)
            
            data = self.get_sentinel2_data(
                bbox,
                current.strftime('%Y-%m-%d'),
                next_date.strftime('%Y-%m-%d')
            )
            
            if data:
                results.append(data)
            
            current = next_date
        
        return results
    
    def _get_mock_sentinel2_data(
        self,
        bbox: List[float],
        start_date: str,
        end_date: str
    ) -> Dict:
        """Generate mock Sentinel-2 data for testing"""
        import random
        
        # Parse date
        try:
            date = datetime.fromisoformat(start_date)
        except:
            date = datetime.now()
        
        # Seasonal variation
        month = date.month
        is_wet_season = month in [5, 6, 7, 8, 9, 10]  # May-October
        
        # Generate realistic values
        if is_wet_season:
            ndvi = round(random.uniform(0.25, 0.45), 4)
            ndwi = round(random.uniform(0.15, 0.40), 4)
            mndwi = round(random.uniform(0.10, 0.35), 4)
            water_area_factor = random.uniform(0.12, 0.20)
        else:
            ndvi = round(random.uniform(0.40, 0.70), 4)
            ndwi = round(random.uniform(-0.10, 0.15), 4)
            mndwi = round(random.uniform(-0.15, 0.10), 4)
            water_area_factor = random.uniform(0.03, 0.08)
        
        # Calculate approximate area from bbox
        lon_diff = abs(bbox[2] - bbox[0])
        lat_diff = abs(bbox[3] - bbox[1])
        approx_area_sqkm = lon_diff * lat_diff * 111 * 111  # Rough approximation
        water_area_sqkm = round(approx_area_sqkm * water_area_factor, 2)
        
        # LSWI and NDBI
        lswi = round(random.uniform(0.0, 0.3) if is_wet_season else random.uniform(-0.2, 0.1), 4)
        ndbi = round(random.uniform(-0.3, -0.1), 4)  # Negative for natural areas
        
        return {
            'source': 'sentinel-2-mock',
            'acquisition_date': date.isoformat(),
            'cloud_coverage': round(random.uniform(5, 30), 1),
            'resolution_m': 10,
            'avg_ndvi': ndvi,
            'avg_ndwi': ndwi,
            'avg_mndwi': mndwi,
            'avg_lswi': lswi,
            'avg_ndbi': ndbi,
            'water_area_sqkm': water_area_sqkm,
            'bbox': bbox,
            'image_id': f'mock_{date.strftime("%Y%m%d")}'
        }
    
    def test_connection(self) -> Dict:
        """Test Earth Engine connection"""
        if self.mock_mode:
            return {
                'status': 'mock',
                'message': 'Running in mock mode. To enable Earth Engine, authenticate first.',
                'instructions': [
                    '1. Install: pip install earthengine-api',
                    '2. Authenticate: earthengine authenticate',
                    '3. Or set service account: GEE_SERVICE_ACCOUNT and GEE_KEY_FILE env vars'
                ]
            }
        
        try:
            # Test with a simple query
            image = ee.Image('COPERNICUS/S2_SR_HARMONIZED/20200101T000000_20200101T000000_T01ABC')
            info = image.getInfo()
            
            return {
                'status': 'connected',
                'message': 'Earth Engine is connected and working',
                'initialized': self.initialized
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Earth Engine connection test failed: {str(e)}'
            }


# Singleton instance
_ee_service = None

def get_earth_engine_service() -> EarthEngineService:
    """Get singleton Earth Engine service instance"""
    global _ee_service
    if _ee_service is None:
        _ee_service = EarthEngineService()
    return _ee_service
