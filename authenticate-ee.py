"""
Authenticate Google Earth Engine
"""
import ee

print("=" * 60)
print("🌍 Google Earth Engine Authentication")
print("=" * 60)
print()

try:
    print("Starting authentication process...")
    print()
    print("📝 Instructions:")
    print("   1. A browser window will open")
    print("   2. Sign in with your Google account")
    print("   3. Grant Earth Engine permissions")
    print("   4. Copy the authorization code")
    print("   5. Paste it back here")
    print()
    
    # Authenticate
    ee.Authenticate()
    
    print()
    print("=" * 60)
    print("✅ Authentication Successful!")
    print("=" * 60)
    print()
    
    # Test initialization with project
    print("Testing Earth Engine connection...")
    project_id = 'trim-descent-452802-t2'
    print(f"Using project: {project_id}")
    
    try:
        ee.Initialize(project=project_id)
    except Exception as e:
        print(f"⚠️  Could not initialize with project: {e}")
        print("Trying without project...")
        ee.Initialize()
    
    # Test with a simple query
    image = ee.Image('USGS/SRTMGL1_003')
    info = image.getInfo()
    
    print("✅ Earth Engine is working!")
    print()
    print("📊 Test Query Result:")
    print(f"   Image ID: {info.get('id')}")
    print(f"   Type: {info.get('type')}")
    print()
    print("=" * 60)
    print("🎉 Setup Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("   1. Run: python test-satellite-indices.py")
    print("   2. Or start backend: cd backend && start-local.bat")
    print("   3. Test API: http://localhost:8000/api/pipeline/test-ee")
    print()
    
except Exception as e:
    print()
    print("=" * 60)
    print("❌ Authentication Failed")
    print("=" * 60)
    print()
    print(f"Error: {e}")
    print()
    print("Troubleshooting:")
    print("   1. Make sure you have a Google account")
    print("   2. Sign up for Earth Engine: https://earthengine.google.com/signup/")
    print("   3. Check internet connection")
    print("   4. Try again")
    print()
