# Python implementation that demonstrates both the Interrogative and Predictive Digital Twin roles.

At a high level, this code **simulates a physical machine (e.g., an industrial turbine)** by creating a virtual representation called a **Digital Twin**.

Instead of cramming every single feature into one giant block of code, it splits the Digital Twin into **two specific operational roles**:

1. **Interrogative Role:** Reads and inspects what is happening **now** or what happened in the **past**.
2. **Predictive Role:** Calculates and forecasts what will happen in the **future**.

It then populates these twins with sample telemetry data (temperature, vibration, motor RPM) and demonstrates how to query real-time states and execute predictive calculations.

---

## 2. What is the Main Part of the Code?

The core architecture rests on **3 primary components**:

```
                       +-------------------------------+
                       |   1. TelemetryRecord (Data)   |
                       +-------------------------------+
                                       |
                       +---------------+---------------+
                       |                               |
                       v                               v
+------------------------------------+   +------------------------------------+
| 2. InterrogativeDigitalTwin Class  |   |   3. PredictiveDigitalTwin Class   |
|   (Historical & Real-time State)   |   |     (Future Trends & What-If)      |
+------------------------------------+   +------------------------------------+

```

1. **`TelemetryRecord` Data Model:** The standardized blueprint for holding raw sensor readings (`timestamp`, `temperature`, `vibration`, `rpm`).
2. **`InterrogativeDigitalTwin` Class:** The storage and retrieval engine. It manages the timeline of sensor data and handles queries.
3. **`PredictiveDigitalTwin` Class:** The analytics engine. It takes the latest state from the Interrogative twin and runs forecasting logic on top of it.

---

## 3. Step-by-Step Explanation of Each Class

### Step 1: Data Model — `TelemetryRecord`

```python
@dataclass
class TelemetryRecord:
    timestamp: float
    temperature: float
    vibration: float
    rpm: float

```

* **Role:** Acts as a clean container for single sensor snapshots.
* **Why it matters:** Every time a physical sensor reads data, it creates one `TelemetryRecord` containing the time it occurred and its measured values.

---

### Step 2: Class 1 — `InterrogativeDigitalTwin`

This class represents the memory of the Digital Twin.

#### 1. `__init__(self, asset_id: str)`

* **What it does:** Initializes the twin with a specific asset identifier (e.g., `"TURBINE-001"`) and creates an empty list `self._history` to store sensor records over time.

#### 2. `ingest_telemetry(self, record: TelemetryRecord)`

* **What it does:** Receives new sensor readings and appends them to `self._history`.
* **Purpose:** Keeps the Digital Twin synchronized with the real physical asset.

#### 3. `get_current_state(self)`

* **What it does:** Returns `self._history[-1]` (the last item in the list).
* **Purpose:** Answers the question: *"What are the current readings right now?"*

#### 4. `query_historical_range(self, start_time, end_time)`

* **What it does:** Iterates through `self._history` and returns records that fell between `start_time` and `end_time`.
* **Purpose:** Allows operators to review past operational windows (e.g., *"Show me sensor data between 2:00 PM and 3:00 PM"*).

#### 5. `get_anomalies(self, temp_threshold, vib_threshold)`

* **What it does:** Filters history for records where temperature or vibration exceeded designated safety limits.
* **Purpose:** Root-cause investigation and safety compliance auditing.

---

### Step 3: Class 2 — `PredictiveDigitalTwin`

This class contains the forward-looking logic and simulations.

#### 1. `__init__(self, asset_id: str)`

* **What it does:** Binds the predictive engine to the asset ID.

#### 2. `forecast_temperature(self, current_record, steps_ahead)`

* **What it does:** Takes the current temperature and projects it forward $N$ steps using a fixed thermal drift rate ($0.8^\circ\text{C}$ per step).
* **Purpose:** Predicts immediate future thermal conditions so systems can react before overheating occurs.

#### 3. `predict_remaining_useful_life(self, current_record, max_temp)`

* **What it does:**
1. Calculates remaining thermal headroom: $\text{max\_temp} - \text{current\_temp}$.
2. Calculates a degradation factor based on current vibration intensity.
3. Divides headroom by degradation rate to estimate remaining operating hours (RUL).


* **Purpose:** Enables **predictive maintenance**—fixing parts right before they fail rather than on a rigid calendar schedule.

#### 4. `simulate_what_if(self, current_record, rpm_delta)`

* **What it does:** Calculates hypothetical temperature and vibration outputs if the motor speed (RPM) were increased or decreased by `rpm_delta`.
* **Purpose:** Allows operators to test dangerous or demanding operating conditions in a virtual environment without risking physical machinery.

---

## 4. Deep-Dive: Queries vs. Inferences

The execution block in the script contrasts **Queries** against **Inferences**:

```python
# --- INTERROGATIVE TWIN QUERIES ---
current_state = interrogative_twin.get_current_state()
anomalies = interrogative_twin.get_anomalies(temp_threshold=85.0)

# --- PREDICTIVE TWIN INFERENCES ---
forecast = predictive_twin.forecast_temperature(current_state, steps_ahead=3)
rul_info = predictive_twin.predict_remaining_useful_life(current_state)
sim_result = predictive_twin.simulate_what_if(current_state, rpm_delta=400)

```

### Interrogative Twin Queries (Deterministic / Fact-Based)

* **Definition:** Direct database/memory lookups that retrieve known facts.
* **Operation:**
* `get_current_state()` looks up the latest timestamped entry ($88.5^\circ\text{C}, 3600\text{ RPM}$).
* `get_anomalies()` filters historical records to find that 1 entry crossed the $85.0^\circ\text{C}$ safety threshold.


* **Key Characteristic:** Zero math estimation involved; it simply reports what the sensors logged.

### Predictive Twin Inferences (Probabilistic / Model-Based)

* **Definition:** Math models and algorithms that calculate unobserved or future outcomes.
* **Operation:**
* `forecast_temperature()` projects that the next 3 intervals will reach $89.3^\circ\text{C}$, $90.1^\circ\text{C}$, and $90.9^\circ\text{C}$.
* `predict_remaining_useful_life()` estimates **15.54 hours** remaining before reaching the critical $100^\circ\text{C}$ ceiling.
* `simulate_what_if()` predicts that boosting motor speed by **+400 RPM** will push temperature to $108.5^\circ\text{C}$ and vibration to $5.6$.


* **Key Characteristic:** Uses current state data as an input to infer future behavior, enabling proactive automation.
