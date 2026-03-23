"""
Training script for HydroLSTM model
Connects to production database and trains models for each basin
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from models.hydro_lstm import HydroLSTM
import argparse
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, and_


# Database connection
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://riffai:riffai123@34.21.160.173/riffai"
)

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def load_data_from_db(basin_id: str, days_back: int = 365):
    """
    Load training data from production database
    
    Args:
        basin_id: Basin ID
        days_back: Number of days to load
    
    Returns:
        DataFrame with features
    """
    print(f"\n{'='*60}")
    print(f"Loading data for basin: {basin_id}")
    print(f"Days back: {days_back}")
    print(f"{'='*60}\n")
    
    async with async_session() as db:
        # Import models
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))
        from app.models.models import Station, WaterLevel, Rainfall
        
        # Get stations in basin
        result = await db.execute(
            select(Station).where(
                Station.basin_id == basin_id,
                Station.is_active == True
            )
        )
        stations = result.scalars().all()
        
        if not stations:
            print(f"❌ No stations found for basin {basin_id}")
            return None
        
        print(f"Found {len(stations)} stations:")
        for s in stations:
            print(f"  - {s.name} ({s.station_type})")
        
        # Get water level data
        water_stations = [s.id for s in stations if s.station_type == "water_level"]
        rain_stations = [s.id for s in stations if s.station_type == "rainfall"]
        
        cutoff = datetime.utcnow() - timedelta(days=days_back)
        
        # Load water levels
        water_data = []
        if water_stations:
            result = await db.execute(
                select(WaterLevel).where(
                    WaterLevel.station_id.in_(water_stations),
                    WaterLevel.datetime >= cutoff
                ).order_by(WaterLevel.datetime)
            )
            water_records = result.scalars().all()
            
            for w in water_records:
                water_data.append({
                    'datetime': w.datetime,
                    'station_id': w.station_id,
                    'water_level_m': w.level_m,
                    'flow_rate': w.flow_rate
                })
            
            print(f"✅ Loaded {len(water_data)} water level records")
        
        # Load rainfall
        rain_data = []
        if rain_stations:
            result = await db.execute(
                select(Rainfall).where(
                    Rainfall.station_id.in_(rain_stations),
                    Rainfall.datetime >= cutoff
                ).order_by(Rainfall.datetime)
            )
            rain_records = result.scalars().all()
            
            for r in rain_records:
                rain_data.append({
                    'datetime': r.datetime,
                    'station_id': r.station_id,
                    'rainfall_mm': r.amount_mm
                })
            
            print(f"✅ Loaded {len(rain_data)} rainfall records")
        
        if not water_data and not rain_data:
            print(f"❌ No data found for basin {basin_id}")
            return None
        
        # Combine data into hourly DataFrame
        df_water = pd.DataFrame(water_data) if water_data else pd.DataFrame()
        df_rain = pd.DataFrame(rain_data) if rain_data else pd.DataFrame()
        
        # Create hourly time series
        if not df_water.empty:
            df_water['datetime'] = pd.to_datetime(df_water['datetime'])
            df_water = df_water.groupby('datetime').agg({
                'water_level_m': 'mean',
                'flow_rate': 'mean'
            }).reset_index()
        
        if not df_rain.empty:
            df_rain['datetime'] = pd.to_datetime(df_rain['datetime'])
            df_rain = df_rain.groupby('datetime').agg({
                'rainfall_mm': 'sum'
            }).reset_index()
        
        # Merge on datetime
        if not df_water.empty and not df_rain.empty:
            data = pd.merge(df_water, df_rain, on='datetime', how='outer')
        elif not df_water.empty:
            data = df_water
        else:
            data = df_rain
        
        data = data.sort_values('datetime').reset_index(drop=True)
        
        # Fill missing values
        data = data.fillna(method='ffill').fillna(0)
        
        # Add ET (mock for now - should come from weather API)
        data['et_mm'] = 3.0  # Average ET for Thailand
        
        print(f"\n📊 Data Summary:")
        print(f"  Date range: {data['datetime'].min()} to {data['datetime'].max()}")
        print(f"  Total records: {len(data)}")
        print(f"  Columns: {list(data.columns)}")
        print(f"\n{data.describe()}\n")
        
        return data


def prepare_features(data: pd.DataFrame):
    """
    Prepare features for training
    
    Args:
        data: DataFrame with raw data
    
    Returns:
        X: Input features
        y: Target values
    """
    # Ensure we have required columns
    required_cols = ['water_level_m', 'rainfall_mm', 'et_mm']
    
    for col in required_cols:
        if col not in data.columns:
            if col == 'water_level_m':
                data[col] = 2.0  # Default water level
            elif col == 'rainfall_mm':
                data[col] = 0.0
            elif col == 'et_mm':
                data[col] = 3.0
    
    # Features: rainfall, water_level, et, previous water_level (as proxy for discharge)
    X = data[['rainfall_mm', 'water_level_m', 'et_mm', 'water_level_m']].values
    
    # Target: future water level
    y = data['water_level_m'].values
    
    return X, y


async def train_basin_model(basin_id: str, epochs: int = 100, batch_size: int = 32):
    """
    Train model for a specific basin
    
    Args:
        basin_id: Basin ID
        epochs: Number of training epochs
        batch_size: Batch size
    """
    print(f"\n{'='*60}")
    print(f"🤖 Training HydroLSTM for Basin: {basin_id}")
    print(f"{'='*60}\n")
    
    # Load data
    data = await load_data_from_db(basin_id, days_back=365)
    
    if data is None or len(data) < 100:
        print(f"❌ Insufficient data for training (need at least 100 records)")
        return None, None
    
    # Prepare features
    X, y = prepare_features(data)
    print(f"Features shape: {X.shape}")
    print(f"Target shape: {y.shape}")
    
    # Initialize model
    model = HydroLSTM(
        input_timesteps=24,  # Use past 24 hours
        output_timesteps=24,  # Predict next 24 hours
        n_features=4,
        encoder_units=128,
        decoder_units=128,
        dropout=0.2
    )
    
    # Prepare sequences
    print("\n📦 Preparing sequences...")
    X_seq, y_seq = model.prepare_sequences(X, y)
    print(f"Sequence X shape: {X_seq.shape}")
    print(f"Sequence y shape: {y_seq.shape}")
    
    if len(X_seq) < 50:
        print(f"❌ Insufficient sequences for training (need at least 50)")
        return None, None
    
    # Split train/validation
    split_idx = int(len(X_seq) * 0.8)
    X_train, X_val = X_seq[:split_idx], X_seq[split_idx:]
    y_train, y_val = y_seq[:split_idx], y_seq[split_idx:]
    
    print(f"\n📊 Data Split:")
    print(f"  Train samples: {len(X_train)}")
    print(f"  Validation samples: {len(X_val)}")
    
    # Build and train
    print(f"\n🏗️  Building model...")
    model.build_model()
    model.model.summary()
    
    print(f"\n🚀 Training for {epochs} epochs...")
    history = model.train(
        X_train, y_train,
        X_val, y_val,
        epochs=epochs,
        batch_size=batch_size,
        verbose=1
    )
    
    # Evaluate
    print("\n📈 Evaluating model...")
    metrics = model.evaluate(X_val, y_val)
    print(f"\n✅ Validation Metrics:")
    print(f"  MSE:  {metrics['mse']:.4f}")
    print(f"  MAE:  {metrics['mae']:.4f}")
    print(f"  RMSE: {metrics['rmse']:.4f}")
    print(f"  R²:   {metrics['r2']:.4f}")
    
    # Save model
    model_dir = os.path.join(os.path.dirname(__file__), '..', 'models', 'trained', basin_id)
    os.makedirs(model_dir, exist_ok=True)
    
    model_path = os.path.join(model_dir, 'model.h5')
    scaler_path = os.path.join(model_dir, 'scalers.pkl')
    
    print(f"\n💾 Saving model to {model_path}")
    model.save(model_path, scaler_path)
    
    # Save metrics
    metrics_path = os.path.join(model_dir, 'metrics.txt')
    with open(metrics_path, 'w') as f:
        f.write(f"Basin: {basin_id}\n")
        f.write(f"Trained: {datetime.now()}\n")
        f.write(f"Epochs: {epochs}\n")
        f.write(f"Batch size: {batch_size}\n")
        f.write(f"Training samples: {len(X_train)}\n")
        f.write(f"Validation samples: {len(X_val)}\n")
        f.write(f"\nMetrics:\n")
        f.write(f"  MSE:  {metrics['mse']:.4f}\n")
        f.write(f"  MAE:  {metrics['mae']:.4f}\n")
        f.write(f"  RMSE: {metrics['rmse']:.4f}\n")
        f.write(f"  R²:   {metrics['r2']:.4f}\n")
    
    print(f"\n{'='*60}")
    print(f"✅ Training completed for {basin_id}")
    print(f"{'='*60}\n")
    
    return model, metrics


async def main():
    parser = argparse.ArgumentParser(description='Train HydroLSTM model')
    parser.add_argument('--basin', type=str, help='Basin ID (or "all" for all basins)')
    parser.add_argument('--epochs', type=int, default=50, help='Number of epochs')
    parser.add_argument('--batch-size', type=int, default=32, help='Batch size')
    
    args = parser.parse_args()
    
    if args.basin and args.basin != 'all':
        await train_basin_model(args.basin, args.epochs, args.batch_size)
    else:
        # Train for all basins
        basins = ['mekong_north', 'eastern_coast', 'southern_east']
        for basin in basins:
            try:
                await train_basin_model(basin, epochs=args.epochs, batch_size=args.batch_size)
            except Exception as e:
                print(f"❌ Error training {basin}: {e}")
                continue


if __name__ == "__main__":
    asyncio.run(main())
