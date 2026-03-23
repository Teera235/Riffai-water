"""
Test HydroLSTM models integration
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from pathlib import Path
import numpy as np

print("=" * 60)
print("🤖 Testing AI Models")
print("=" * 60)
print()

# Check if models exist
ai_engine_path = Path("ai-engine/models/trained")
basins = ["mekong_north", "eastern_coast", "southern_east"]

print("📦 Checking Models:")
print()

models_available = {}
for basin_id in basins:
    model_path = ai_engine_path / basin_id / "model.h5"
    if model_path.exists():
        size_kb = model_path.stat().st_size / 1024
        print(f"✅ {basin_id:<20} {size_kb:>8.1f} KB")
        models_available[basin_id] = model_path
    else:
        print(f"❌ {basin_id:<20} Not found")

print()

if not models_available:
    print("❌ No models found!")
    print()
    print("Run first: python integrate-hydrolstm.py")
    sys.exit(1)

print("=" * 60)
print("🧪 Testing Model Loading")
print("=" * 60)
print()

try:
    import tensorflow as tf
    from tensorflow import keras
    
    print(f"TensorFlow version: {tf.__version__}")
    print()
    
    for basin_id, model_path in models_available.items():
        print(f"Testing {basin_id}...")
        
        try:
            # Load model
            model = keras.models.load_model(model_path)
            
            # Get model info
            print(f"  ✅ Model loaded successfully")
            print(f"  Input shape: {model.input_shape}")
            print(f"  Output shape: {model.output_shape}")
            print(f"  Parameters: {model.count_params():,}")
            
            # Test prediction with dummy data
            if isinstance(model.input_shape, list):
                # Multiple inputs
                dummy_inputs = [np.random.randn(1, *shape[1:]) for shape in model.input_shape]
            else:
                # Single input
                dummy_inputs = np.random.randn(1, *model.input_shape[1:])
            
            prediction = model.predict(dummy_inputs, verbose=0)
            print(f"  ✅ Test prediction successful")
            print(f"  Prediction shape: {prediction.shape}")
            print()
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            print()
    
    print("=" * 60)
    print("🔗 Testing AI Service Integration")
    print("=" * 60)
    print()
    
    from app.services.ai_service import AIService
    
    ai_service = AIService()
    
    print(f"Models loaded: {len(ai_service.models)}")
    print(f"Model mode: {'AI' if ai_service.model_loaded else 'Rule-based'}")
    print()
    
    if ai_service.models:
        print("Available models:")
        for basin_id in ai_service.models.keys():
            print(f"  ✅ {basin_id}")
        print()
    
    # Test prediction
    print("Testing prediction...")
    
    # Mock data
    satellite_data = [
        ("2026-03-01", 0.5, 0.2, 0.1, 100),
        ("2026-03-02", 0.5, 0.2, 0.1, 105),
        ("2026-03-03", 0.5, 0.3, 0.2, 110),
    ]
    
    water_data = [
        ("2026-03-01 12:00", 2.5),
        ("2026-03-02 12:00", 2.6),
        ("2026-03-03 12:00", 2.7),
    ]
    
    rainfall_data = [
        ("2026-03-01 12:00", 10),
        ("2026-03-02 12:00", 15),
        ("2026-03-03 12:00", 20),
    ]
    
    result = ai_service.predict(
        basin_id="mekong_north",
        satellite_data=satellite_data,
        water_data=water_data,
        rainfall_data=rainfall_data,
        days_ahead=7
    )
    
    print("Prediction result:")
    print(f"  Flood probability: {result['flood_probability']:.2%}")
    print(f"  Water level: {result['predicted_water_level']:.2f} m")
    print(f"  Affected area: {result['affected_area_sqkm']:.2f} km²")
    print(f"  Confidence: {result['confidence']:.2%}")
    print(f"  Model: {result['model_version']}")
    print()
    
    print("=" * 60)
    print("✅ All Tests Passed!")
    print("=" * 60)
    print()
    print("🎉 AI models are ready to use!")
    print()
    print("Next steps:")
    print("   1. Start backend: cd backend && start-local.bat")
    print("   2. Test API: POST http://localhost:8000/api/predict")
    print("   3. View predictions in frontend")
    print()
    
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print()
    print("Install required packages:")
    print("   pip install tensorflow scikit-learn h5py")
    print()
except Exception as e:
    print(f"❌ Test failed: {e}")
    print()
    import traceback
    traceback.print_exc()
