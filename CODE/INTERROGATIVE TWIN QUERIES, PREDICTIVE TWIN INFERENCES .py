import time
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import numpy as np


@dataclass
class TelemetryRecord:
    timestamp: float
    temperature: float
    vibration: float
    rpm: float


class InterrogativeDigitalTwin:
    """
    Handles state retrieval, historical filtering, and health diagnostics.
    Answers: 'What is happening right now?' and 'What happened in the past?'
    """
    def __init__(self, asset_id: str):
        self.asset_id = asset_id
        self._history: List[TelemetryRecord] = []

    def ingest_telemetry(self, record: TelemetryRecord) -> None:
        """Ingest new sensor data into the twin's memory/store."""
        self._history.append(record)

    def get_current_state(self) -> Optional[TelemetryRecord]:
        """Query the latest operational state."""
        return self._history[-1] if self._history else None

    def query_historical_range(
        self, start_time: float, end_time: float
    ) -> List[TelemetryRecord]:
        """Query sensor readings within a specific time window."""
        return [
            r for r in self._history
            if start_time <= r.timestamp <= end_time
        ]

    def get_anomalies(
        self, temp_threshold: float = 85.0, vib_threshold: float = 4.5
    ) -> List[TelemetryRecord]:
        """Query historical instances where parameters breached thresholds."""
        return [
            r for r in self._history
            if r.temperature > temp_threshold or r.vibration > vib_threshold
        ]


class PredictiveDigitalTwin:
    """
    Handles forward forecasting, failure probability, and 'What-if' simulations.
    Answers: 'What will happen next?' and 'When will this asset fail?'
    """
    def __init__(self, asset_id: str):
        self.asset_id = asset_id

    def forecast_temperature(
        self, current_record: TelemetryRecord, steps_ahead: int = 5
    ) -> List[float]:
        """
        Simple linear trend forecast based on current state.
        (Replace with LSTM/Transformer or ROM physics models in production)
        """
        base_temp = current_record.temperature
        # Simulate slight thermal drift per time step
        drift_rate = 0.8  
        return [
            round(base_temp + (i * drift_rate), 2)
            for i in range(1, steps_ahead + 1)
        ]

    def predict_remaining_useful_life(
        self, current_record: TelemetryRecord, max_temp: float = 100.0
    ) -> Dict[str, Any]:
        """Predicts Remaining Useful Life (RUL) in operational hours."""
        if current_record.temperature >= max_temp:
            return {"rul_hours": 0.0, "status": "CRITICAL_FAILURE_IMMINENT"}

        temp_margin = max_temp - current_record.temperature
        # Degradation rate scaled by vibration intensity
        degradation_rate = 0.5 * (1 + current_record.vibration / 10.0)
        estimated_hours = round(temp_margin / degradation_rate, 2)

        return {
            "rul_hours": estimated_hours,
            "failure_risk": "HIGH" if estimated_hours < 10 else "LOW",
        }

    def simulate_what_if(
        self, current_record: TelemetryRecord, rpm_delta: float
    ) -> Dict[str, float]:
        """Evaluates system response to hypothetical control changes."""
        new_rpm = current_record.rpm + rpm_delta
        # Estimated linear thermal and vibration impact
        predicted_temp = current_record.temperature + (rpm_delta * 0.05)
        predicted_vib = current_record.vibration + (rpm_delta * 0.002)

        return {
            "simulated_rpm": new_rpm,
            "predicted_temperature": round(predicted_temp, 2),
            "predicted_vibration": round(predicted_vib, 2),
        }


# ==========================================
# Example Usage & Verification
# ==========================================
if __name__ == "__main__":
    asset_id = "TURBINE-001"
    
    # Initialize both roles for the same asset
    interrogative_twin = InterrogativeDigitalTwin(asset_id)
    predictive_twin = PredictiveDigitalTwin(asset_id)

    # 1. Simulate Telemetry Stream
    now = time.time()
    telemetry_samples = [
        TelemetryRecord(timestamp=now - 300, temperature=72.0, vibration=1.2, rpm=3000),
        TelemetryRecord(timestamp=now - 200, temperature=75.5, vibration=1.8, rpm=3100),
        TelemetryRecord(timestamp=now - 100, temperature=81.0, vibration=2.5, rpm=3300),
        TelemetryRecord(timestamp=now,       temperature=88.5, vibration=4.8, rpm=3600),
    ]

    for sample in telemetry_samples:
        interrogative_twin.ingest_telemetry(sample)

    # --- INTERROGATIVE TWIN QUERIES ---
    print("=== Interrogative Digital Twin Queries ===")
    current_state = interrogative_twin.get_current_state()
    print(f"Current Temperature: {current_state.temperature}°C, RPM: {current_state.rpm}")

    anomalies = interrogative_twin.get_anomalies(temp_threshold=85.0)
    print(f"Detected Anomalies: {len(anomalies)} breach(es) found.\n")

    # --- PREDICTIVE TWIN INFERENCES ---
    print("=== Predictive Digital Twin Inferences ===")
    if current_state:
        # Forecast future temperature
        forecast = predictive_twin.forecast_temperature(current_state, steps_ahead=3)
        print(f"Temperature Forecast (Next 3 steps): {forecast}")

        # Predict RUL
        rul_info = predictive_twin.predict_remaining_useful_life(current_state)
        print(f"Remaining Useful Life Prediction: {rul_info}")

        # "What-If" Simulation: Increasing RPM by +400
        sim_result = predictive_twin.simulate_what_if(current_state, rpm_delta=400)
        print(f"What-If Simulation (+400 RPM): {sim_result}")
