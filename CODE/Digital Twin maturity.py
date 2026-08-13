import time
import math
from dataclasses import dataclass
from typing import Dict, Any, List, Optional


# =====================================================================
# Telemetry Data Schema
# =====================================================================
@dataclass
class AssetTelemetry:
    timestamp: float
    bearing_temp: float      # Component-level metric (Partial DT scope)
    vibration: float         # System-level metric (DT Clone scope)
    motor_rpm: float         # System-level metric (DT Clone scope)
    ambient_temp: float      # External environment metric (Augmented DT scope)


# =====================================================================
# Level 1: Partial Digital Twin
# =====================================================================
class PartialDigitalTwin:
    """
    Scope: Single component / isolated variable.
    Capability: Basic monitoring and threshold alerts for a targeted sub-system.
    """
    def __init__(self, asset_id: str, temp_limit: float = 80.0):
        self.asset_id = asset_id
        self.temp_limit = temp_limit
        self.last_bearing_temp: Optional[float] = None

    def ingest_bearing_data(self, temp: float) -> Dict[str, Any]:
        """Ingests only the specific metric it is built to monitor."""
        self.last_bearing_temp = temp
        status = "NORMAL" if temp <= self.temp_limit else "OVERHEATING_WARNING"
        
        return {
            "maturity_level": "Level 1: Partial DT",
            "monitored_metric": "bearing_temp",
            "value": temp,
            "status": status
        }


# =====================================================================
# Level 2: Digital Twin Clone
# =====================================================================
class DigitalTwinClone:
    """
    Scope: Full 1:1 physical entity reflection.
    Capability: Real-time bi-directional state synchronization and closed-loop feedback.
    """
    def __init__(self, asset_id: str):
        self.asset_id = asset_id
        self.current_state: Optional[AssetTelemetry] = None
        self.cooling_fan_active: bool = False

    def sync_state(self, telemetry: AssetTelemetry) -> Dict[str, Any]:
        """Synchronizes complete 1:1 real-time state across all internal sensors."""
        self.current_state = telemetry
        
        # Bi-directional control response (Actuation signal back to physical asset)
        if telemetry.bearing_temp > 80.0 and not self.cooling_fan_active:
            self.cooling_fan_active = True
        elif telemetry.bearing_temp <= 75.0 and self.cooling_fan_active:
            self.cooling_fan_active = False

        return {
            "maturity_level": "Level 2: DT Clone",
            "synced_telemetry": {
                "bearing_temp": telemetry.bearing_temp,
                "vibration": telemetry.vibration,
                "motor_rpm": telemetry.motor_rpm
            },
            "control_outputs": {
                "cooling_fan_active": self.cooling_fan_active
            }
        }


# =====================================================================
# Level 3: Augmented Digital Twin
# =====================================================================
class AugmentedDigitalTwin:
    """
    Scope: Full asset + environmental context + ML/Physics analytics.
    Capability: Forecasting, Remaining Useful Life (RUL), and 'What-If' simulations.
    """
    def __init__(self, asset_id: str):
        self.asset_id = asset_id

    def evaluate_augmented_state(
        self, 
        telemetry: AssetTelemetry, 
        grid_load_factor: float
    ) -> Dict[str, Any]:
        """Fuses live telemetry with external ambient data & predictive algorithms."""
        
        # 1. Thermal हेडरूम Assessment considering external ambient context
        effective_thermal_stress = telemetry.bearing_temp + (0.15 * telemetry.ambient_temp)
        
        # 2. Predictive Maintenance: Remaining Useful Life (RUL) estimation
        # Baseline Max Safe Temp = 105°C
        headroom = max(0.0, 105.0 - effective_thermal_stress)
        wear_factor = 1.0 + (telemetry.vibration / 5.0) + (grid_load_factor * 0.2)
        rul_hours = round(headroom / (0.4 * wear_factor), 1)

        # 3. "What-If" Counterfactual Simulation Engine
        simulated_rpm_increase = telemetry.motor_rpm + 500
        simulated_temp = telemetry.bearing_temp + (500 * 0.012) + (telemetry.ambient_temp * 0.05)

        return {
            "maturity_level": "Level 3: Augmented DT",
            "fused_inputs": {
                "bearing_temp": telemetry.bearing_temp,
                "ambient_temp": telemetry.ambient_temp,
                "external_grid_load": grid_load_factor
            },
            "predictive_analytics": {
                "effective_thermal_stress": round(effective_thermal_stress, 2),
                "estimated_rul_hours": rul_hours,
                "health_index": "CRITICAL" if rul_hours < 10 else "HEALTHY"
            },
            "what_if_simulation": {
                "scenario": "+500 RPM under current ambient conditions",
                "predicted_temp": round(simulated_temp, 2)
            }
        }


# =====================================================================
# Verification and Demonstration Execution
# =====================================================================
if __name__ == "__main__":
    asset_id = "TURBINE-M01"
    
    # Instantiate Twins across the 3 maturity levels
    partial_dt = PartialDigitalTwin(asset_id)
    clone_dt = DigitalTwinClone(asset_id)
    augmented_dt = AugmentedDigitalTwin(asset_id)

    # Simulated sensor reading from the physical environment
    sample_data = AssetTelemetry(
        timestamp=time.time(),
        bearing_temp=83.5,    # Over temp limit (>80°C)
        vibration=3.2,
        motor_rpm=3200.0,
        ambient_temp=38.0     # External high ambient heat
    )

    print("==================================================")
    print(f"   DIGITAL TWIN MATURITY PIPELINE [{asset_id}]   ")
    print("==================================================\n")

    # 1. Level 1 Output
    l1_res = partial_dt.ingest_bearing_data(sample_data.bearing_temp)
    print(f"--- [LEVEL 1] PARTIAL DT ---")
    print(f"Status: {l1_res['status']} (Monitored Metric: {l1_res['value']}°C)\n")

    # 2. Level 2 Output
    l2_res = clone_dt.sync_state(sample_data)
    print(f"--- [LEVEL 2] DT CLONE ---")
    print(f"Synced State: {l2_res['synced_telemetry']}")
    print(f"Closed-Loop Actuation: {l2_res['control_outputs']}\n")

    # 3. Level 3 Output
    l3_res = augmented_dt.evaluate_augmented_state(
        telemetry=sample_data, 
        grid_load_factor=1.2  # High external grid stress
    )
    print(f"--- [LEVEL 3] AUGMENTED DT ---")
    print(f"Fused Analytics: {l3_res['predictive_analytics']}")
    print(f"What-If Simulation: {l3_res['what_if_simulation']}\n")
