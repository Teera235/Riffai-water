"""
Test script for comprehensive satellite indices
Tests NDVI, NDWI, MNDWI, LSWI, NDBI and SAR features
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.satellite_service import SatelliteService
from datetime import datetime, timedelta
import json


def test_optical_indices():
    """Test Sentinel-2 optical indices"""
    print("=" * 60)
    print("🛰️  Testing Sentinel-2 Optical Indices")
    print("=" * 60)
    
    service = SatelliteService()
    
    # Test for Mekong North basin
    basin_id = "mekong_north"
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
    
    print(f"\n📍 Basin: {basin_id}")
    print(f"📅 Date range: {start_date} to {end_date}")
    print("\nFetching data...")
    
    result = service.fetch_sentinel2(basin_id, start_date, end_date)
    
    if result.get("status") == "success":
        print("\n✅ SUCCESS - Optical Indices Retrieved:")
        print(f"   Source: {result.get('source')}")
        print(f"   Acquisition: {result.get('acquisition_date')}")
        print(f"   Cloud Coverage: {result.get('cloud_coverage')}%")
        print(f"   Resolution: {result.get('resolution_m')}m")
        print("\n📊 Indices:")
        print(f"   NDVI (Vegetation): {result.get('avg_ndvi'):.4f}")
        print(f"   NDWI (Water): {result.get('avg_ndwi'):.4f}")
        print(f"   MNDWI (Modified Water): {result.get('avg_mndwi'):.4f}")
        print(f"   LSWI (Land Surface Water): {result.get('avg_lswi'):.4f}")
        print(f"   NDBI (Built-up): {result.get('avg_ndbi'):.4f}")
        print(f"\n💧 Water Area: {result.get('water_area_sqkm')} km²")
        
        # Interpretation
        print("\n🔍 Interpretation:")
        ndvi = result.get('avg_ndvi', 0)
        ndwi = result.get('avg_ndwi', 0)
        mndwi = result.get('avg_mndwi', 0)
        lswi = result.get('avg_lswi', 0)
        
        if ndvi > 0.6:
            print("   🌳 High vegetation density")
        elif ndvi > 0.3:
            print("   🌿 Moderate vegetation")
        else:
            print("   🏜️  Low vegetation / bare soil")
        
        if mndwi > 0.3:
            print("   💧 High water presence")
        elif mndwi > 0.0:
            print("   💦 Moderate water presence")
        else:
            print("   🏞️  Low water presence")
        
        if lswi > 0.2:
            print("   🌊 High surface water / wetland")
        elif lswi > 0.0:
            print("   💧 Moderate surface moisture")
        
    else:
        print(f"\n❌ ERROR: {result.get('message', 'Unknown error')}")
    
    return result


def test_sar_features():
    """Test Sentinel-1 SAR features"""
    print("\n" + "=" * 60)
    print("📡 Testing Sentinel-1 SAR Features")
    print("=" * 60)
    
    service = SatelliteService()
    
    basin_id = "mekong_north"
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
    
    print(f"\n📍 Basin: {basin_id}")
    print(f"📅 Date range: {start_date} to {end_date}")
    print("\nFetching SAR data...")
    
    result = service.fetch_sentinel1_sar(basin_id, start_date, end_date)
    
    if result.get("status") == "success":
        print("\n✅ SUCCESS - SAR Features Retrieved:")
        print(f"   Source: {result.get('source')}")
        print(f"   Acquisition: {result.get('acquisition_date')}")
        print(f"   Resolution: {result.get('resolution_m')}m")
        print(f"   Orbit: {result.get('orbit_direction')}")
        print("\n📡 SAR Backscatter:")
        print(f"   VV polarization: {result.get('vv_mean_db')} dB")
        print(f"   VH polarization: {result.get('vh_mean_db')} dB")
        print(f"   VV/VH ratio: {result.get('vv_vh_ratio')}")
        print(f"\n💧 Water Area: {result.get('water_area_sqkm')} km²")
        print(f"\n🔄 Change Detection:")
        print(f"   Change detected: {'Yes ⚠️' if result.get('change_detected') else 'No ✓'}")
        if result.get('change_detected'):
            print(f"   Changed area: {result.get('change_area_sqkm')} km²")
        
        # Interpretation
        print("\n🔍 Interpretation:")
        vv = result.get('vv_mean_db', 0)
        
        if vv < -15:
            print("   💧 Strong water signature (smooth surface)")
        elif vv < -10:
            print("   🌊 Moderate water / wet surface")
        else:
            print("   🏞️  Dry surface / vegetation")
        
        if result.get('change_detected'):
            print("   ⚠️  Significant surface change detected!")
            print("      → Possible flooding or water level change")
        
    else:
        print(f"\n❌ ERROR: {result.get('message', 'Unknown error')}")
    
    return result


def test_time_series():
    """Test time series data"""
    print("\n" + "=" * 60)
    print("📈 Testing Time Series Data")
    print("=" * 60)
    
    service = SatelliteService()
    
    basin_id = "mekong_north"
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d")
    
    print(f"\n📍 Basin: {basin_id}")
    print(f"📅 Date range: {start_date} to {end_date}")
    print(f"📊 Interval: 10 days")
    print("\nFetching time series...")
    
    results = service.get_water_coverage_timeseries(basin_id, start_date, end_date, 10)
    
    if results:
        print(f"\n✅ SUCCESS - Retrieved {len(results)} data points")
        print("\n📊 Time Series Summary:")
        print(f"{'Date':<12} {'NDVI':<8} {'NDWI':<8} {'MNDWI':<8} {'LSWI':<8} {'NDBI':<8} {'Water %':<8}")
        print("-" * 70)
        
        for item in results:
            date = item['date'][:10]
            ndvi = item.get('ndvi', 0)
            ndwi = item.get('ndwi', 0)
            mndwi = item.get('mndwi', 0)
            lswi = item.get('lswi', 0)
            ndbi = item.get('ndbi', 0)
            water_frac = item.get('water_fraction', 0) * 100
            
            print(f"{date:<12} {ndvi:<8.4f} {ndwi:<8.4f} {mndwi:<8.4f} {lswi:<8.4f} {ndbi:<8.4f} {water_frac:<8.2f}")
        
        # Calculate trends
        ndwi_values = [item.get('ndwi', 0) for item in results]
        water_values = [item.get('water_fraction', 0) for item in results]
        
        if len(ndwi_values) >= 2:
            ndwi_trend = ndwi_values[-1] - ndwi_values[0]
            water_trend = water_values[-1] - water_values[0]
            
            print("\n📈 Trends:")
            print(f"   NDWI change: {ndwi_trend:+.4f} {'📈 Increasing' if ndwi_trend > 0 else '📉 Decreasing'}")
            print(f"   Water coverage change: {water_trend*100:+.2f}% {'💧 Increasing' if water_trend > 0 else '🏜️ Decreasing'}")
    else:
        print("\n❌ No time series data available")
    
    return results


def main():
    print("\n" + "=" * 60)
    print("🛰️  RIFFAI Satellite Indices Test Suite")
    print("=" * 60)
    print("\nTesting comprehensive satellite data retrieval:")
    print("  • Sentinel-2: NDVI, NDWI, MNDWI, LSWI, NDBI")
    print("  • Sentinel-1: VV, VH, ratio, change detection")
    print("\n")
    
    try:
        # Test optical indices
        optical_result = test_optical_indices()
        
        # Test SAR features
        sar_result = test_sar_features()
        
        # Test time series
        ts_results = test_time_series()
        
        # Summary
        print("\n" + "=" * 60)
        print("📋 Test Summary")
        print("=" * 60)
        
        optical_ok = optical_result.get("status") == "success"
        sar_ok = sar_result.get("status") == "success"
        ts_ok = len(ts_results) > 0 if ts_results else False
        
        print(f"\n✓ Optical Indices (Sentinel-2): {'✅ PASS' if optical_ok else '❌ FAIL'}")
        print(f"✓ SAR Features (Sentinel-1): {'✅ PASS' if sar_ok else '❌ FAIL'}")
        print(f"✓ Time Series: {'✅ PASS' if ts_ok else '❌ FAIL'}")
        
        if optical_ok and sar_ok and ts_ok:
            print("\n🎉 All tests passed!")
            print("\n💡 Next steps:")
            print("   1. Authenticate Earth Engine: earthengine authenticate")
            print("   2. Run backend: cd backend && .\\start-local.bat")
            print("   3. Test API: http://localhost:8000/api/pipeline/test-ee")
        else:
            print("\n⚠️  Some tests failed (running in mock mode)")
            print("   This is normal if Earth Engine is not authenticated")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
