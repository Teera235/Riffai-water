"""
Integrate HydroLSTM pre-trained models into RIFFAI system
"""
import os
import shutil
from pathlib import Path

print("=" * 60)
print("🔗 Integrating HydroLSTM Models")
print("=" * 60)
print()

# Paths
hydro_path = Path("HydroLSTM")
ai_engine_path = Path("ai-engine/models/trained")

# Create target directories
basins = {
    "mekong_north": "model1",  # ED-LSTM
    "eastern_coast": "model2",  # NRM
    "southern_east": "model3",  # NRM-G
}

print("📦 Available HydroLSTM Models:")
print()

models_found = []

# Check Model 1 (ED-LSTM)
model1_path = hydro_path / "model1_results" / "521_model1_model.h5"
if model1_path.exists():
    print(f"✅ Model 1 (ED-LSTM): {model1_path}")
    print(f"   Size: {model1_path.stat().st_size / 1024:.1f} KB")
    models_found.append(("model1", model1_path))
else:
    print(f"❌ Model 1 not found: {model1_path}")

# Check Model 2 (NRM)
model2_path = hydro_path / "model2_results" / "521_model2_model.h5"
if model2_path.exists():
    print(f"✅ Model 2 (NRM): {model2_path}")
    print(f"   Size: {model2_path.stat().st_size / 1024:.1f} KB")
    models_found.append(("model2", model2_path))
else:
    print(f"❌ Model 2 not found: {model2_path}")

# Check Model 3 (NRM-G)
model3_path = hydro_path / "model3_results" / "NRM_generalized_basic.h5"
if model3_path.exists():
    print(f"✅ Model 3 (NRM-G): {model3_path}")
    print(f"   Size: {model3_path.stat().st_size / 1024:.1f} KB")
    models_found.append(("model3", model3_path))
else:
    print(f"❌ Model 3 not found: {model3_path}")

print()
print("=" * 60)
print("📋 Integration Plan")
print("=" * 60)
print()

for basin_id, model_name in basins.items():
    print(f"Basin: {basin_id:<20} → {model_name}")

print()
input("Press Enter to continue with integration...")
print()

# Copy models
print("=" * 60)
print("🔄 Copying Models")
print("=" * 60)
print()

copied = 0
for basin_id, model_name in basins.items():
    # Find the model
    model_file = None
    for m_name, m_path in models_found:
        if m_name == model_name:
            model_file = m_path
            break
    
    if not model_file:
        print(f"⚠️  Skipping {basin_id}: Model {model_name} not found")
        continue
    
    # Create target directory
    target_dir = ai_engine_path / basin_id
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy model file
    target_file = target_dir / "model.h5"
    shutil.copy2(model_file, target_file)
    
    print(f"✅ {basin_id}")
    print(f"   Source: {model_file}")
    print(f"   Target: {target_file}")
    print(f"   Size: {target_file.stat().st_size / 1024:.1f} KB")
    print()
    
    copied += 1

print("=" * 60)
print("📊 Summary")
print("=" * 60)
print()
print(f"Models copied: {copied}/{len(basins)}")
print()

if copied > 0:
    print("✅ Integration successful!")
    print()
    print("Next steps:")
    print("   1. Create scalers.pkl for each basin (if needed)")
    print("   2. Test models: python test-ai-models.py")
    print("   3. Run backend: cd backend && start-local.bat")
    print("   4. Test prediction API: POST /api/predict")
    print()
else:
    print("❌ No models were copied")
    print()
    print("Please check:")
    print("   - HydroLSTM folder exists")
    print("   - Model files are present")
    print("   - File permissions")
    print()
