"""
HydroLSTM Model for Flood Prediction
Based on: https://github.com/uihilab/HydroLSTM
Adapted for RiffAI Platform
"""
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import LSTM, Dense, Input, RepeatVector, TimeDistributed
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler
import pickle


class HydroLSTM:
    """
    Encoder-Decoder LSTM for streamflow/flood prediction
    
    Architecture:
    - Encoder: LSTM layers to encode input sequence
    - Decoder: LSTM layers to decode and predict future sequence
    
    Input features:
    - Precipitation (mm)
    - Water level (m)
    - Evapotranspiration (mm/month)
    - Previous discharge (m3/s)
    
    Output:
    - Future discharge/water level predictions
    """
    
    def __init__(
        self,
        input_timesteps=24,
        output_timesteps=24,
        n_features=4,
        encoder_units=128,
        decoder_units=128,
        dropout=0.2
    ):
        self.input_timesteps = input_timesteps
        self.output_timesteps = output_timesteps
        self.n_features = n_features
        self.encoder_units = encoder_units
        self.decoder_units = decoder_units
        self.dropout = dropout
        
        self.model = None
        self.scaler_X = MinMaxScaler()
        self.scaler_y = MinMaxScaler()
        
    def build_model(self):
        """Build Encoder-Decoder LSTM architecture"""
        
        # Encoder
        encoder_inputs = Input(shape=(self.input_timesteps, self.n_features))
        encoder = LSTM(
            self.encoder_units,
            return_state=True,
            dropout=self.dropout
        )
        encoder_outputs, state_h, state_c = encoder(encoder_inputs)
        encoder_states = [state_h, state_c]
        
        # Decoder
        decoder_inputs = RepeatVector(self.output_timesteps)(encoder_outputs)
        decoder = LSTM(
            self.decoder_units,
            return_sequences=True,
            dropout=self.dropout
        )
        decoder_outputs = decoder(decoder_inputs, initial_state=encoder_states)
        
        # Output layer
        decoder_dense = TimeDistributed(Dense(1))
        decoder_outputs = decoder_dense(decoder_outputs)
        
        # Define model
        self.model = Model(encoder_inputs, decoder_outputs)
        self.model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )
        
        return self.model
    
    def prepare_sequences(self, data, target):
        """
        Prepare sequences for training
        
        Args:
            data: Input features (n_samples, n_features)
            target: Target values (n_samples,)
        
        Returns:
            X: Input sequences (n_sequences, input_timesteps, n_features)
            y: Target sequences (n_sequences, output_timesteps, 1)
        """
        X, y = [], []
        
        for i in range(len(data) - self.input_timesteps - self.output_timesteps):
            X.append(data[i:i + self.input_timesteps])
            y.append(target[i + self.input_timesteps:i + self.input_timesteps + self.output_timesteps])
        
        return np.array(X), np.array(y).reshape(-1, self.output_timesteps, 1)
    
    def train(
        self,
        X_train,
        y_train,
        X_val=None,
        y_val=None,
        epochs=100,
        batch_size=32,
        verbose=1
    ):
        """
        Train the model
        
        Args:
            X_train: Training input sequences
            y_train: Training target sequences
            X_val: Validation input sequences (optional)
            y_val: Validation target sequences (optional)
            epochs: Number of training epochs
            batch_size: Batch size
            verbose: Verbosity mode
        
        Returns:
            history: Training history
        """
        if self.model is None:
            self.build_model()
        
        # Normalize data
        n_samples = X_train.shape[0]
        X_train_reshaped = X_train.reshape(-1, self.n_features)
        X_train_scaled = self.scaler_X.fit_transform(X_train_reshaped)
        X_train_scaled = X_train_scaled.reshape(n_samples, self.input_timesteps, self.n_features)
        
        y_train_scaled = self.scaler_y.fit_transform(y_train.reshape(-1, 1))
        y_train_scaled = y_train_scaled.reshape(n_samples, self.output_timesteps, 1)
        
        validation_data = None
        if X_val is not None and y_val is not None:
            n_val = X_val.shape[0]
            X_val_reshaped = X_val.reshape(-1, self.n_features)
            X_val_scaled = self.scaler_X.transform(X_val_reshaped)
            X_val_scaled = X_val_scaled.reshape(n_val, self.input_timesteps, self.n_features)
            
            y_val_scaled = self.scaler_y.transform(y_val.reshape(-1, 1))
            y_val_scaled = y_val_scaled.reshape(n_val, self.output_timesteps, 1)
            
            validation_data = (X_val_scaled, y_val_scaled)
        
        # Train
        history = self.model.fit(
            X_train_scaled,
            y_train_scaled,
            validation_data=validation_data,
            epochs=epochs,
            batch_size=batch_size,
            verbose=verbose
        )
        
        return history
    
    def predict(self, X):
        """
        Make predictions
        
        Args:
            X: Input sequences (n_sequences, input_timesteps, n_features)
        
        Returns:
            predictions: Predicted values (n_sequences, output_timesteps)
        """
        if self.model is None:
            raise ValueError("Model not trained yet")
        
        # Normalize input
        n_samples = X.shape[0]
        X_reshaped = X.reshape(-1, self.n_features)
        X_scaled = self.scaler_X.transform(X_reshaped)
        X_scaled = X_scaled.reshape(n_samples, self.input_timesteps, self.n_features)
        
        # Predict
        y_pred_scaled = self.model.predict(X_scaled)
        
        # Denormalize
        y_pred = self.scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1))
        y_pred = y_pred.reshape(n_samples, self.output_timesteps)
        
        return y_pred
    
    def save(self, model_path, scaler_path):
        """Save model and scalers"""
        if self.model is None:
            raise ValueError("Model not trained yet")
        
        self.model.save(model_path)
        
        with open(scaler_path, 'wb') as f:
            pickle.dump({
                'scaler_X': self.scaler_X,
                'scaler_y': self.scaler_y
            }, f)
    
    def load(self, model_path, scaler_path):
        """Load model and scalers"""
        self.model = tf.keras.models.load_model(model_path)
        
        with open(scaler_path, 'rb') as f:
            scalers = pickle.load(f)
            self.scaler_X = scalers['scaler_X']
            self.scaler_y = scalers['scaler_y']
    
    def evaluate(self, X_test, y_test):
        """
        Evaluate model performance
        
        Returns:
            metrics: Dictionary with MSE, MAE, R2
        """
        y_pred = self.predict(X_test)
        y_true = y_test.reshape(-1, self.output_timesteps)
        
        mse = np.mean((y_true - y_pred) ** 2)
        mae = np.mean(np.abs(y_true - y_pred))
        
        # R2 score
        ss_res = np.sum((y_true - y_pred) ** 2)
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
        r2 = 1 - (ss_res / ss_tot)
        
        return {
            'mse': float(mse),
            'mae': float(mae),
            'r2': float(r2),
            'rmse': float(np.sqrt(mse))
        }
