from . import tools as tools
from .cfa_simulation_smoother import CFASimulationSmoother as CFASimulationSmoother
from .kalman_smoother import KalmanSmoother as KalmanSmoother
from typing import Any

SIMULATION_STATE: int
SIMULATION_DISTURBANCE: int
SIMULATION_ALL: Any

class SimulationSmoother(KalmanSmoother):
    simulation_outputs: Any
    simulation_smooth_results_class: Any
    prefix_simulation_smoother_map: Any
    def __init__(self, k_endog, k_states, k_posdef: Any | None = ..., simulation_smooth_results_class: Any | None = ..., simulation_smoother_classes: Any | None = ..., **kwargs) -> None: ...
    def get_simulation_output(self, simulation_output: Any | None = ..., simulate_state: Any | None = ..., simulate_disturbance: Any | None = ..., simulate_all: Any | None = ..., **kwargs): ...
    def simulation_smoother(self, simulation_output: Any | None = ..., method: str = ..., results_class: Any | None = ..., prefix: Any | None = ..., **kwargs): ...

class SimulationSmoothResults:
    model: Any
    prefix: Any
    dtype: Any
    def __init__(self, model, simulation_smoother) -> None: ...
    @property
    def simulation_output(self): ...
    @simulation_output.setter
    def simulation_output(self, value) -> None: ...
    @property
    def simulate_state(self): ...
    @simulate_state.setter
    def simulate_state(self, value) -> None: ...
    @property
    def simulate_disturbance(self): ...
    @simulate_disturbance.setter
    def simulate_disturbance(self, value) -> None: ...
    @property
    def simulate_all(self): ...
    @simulate_all.setter
    def simulate_all(self, value) -> None: ...
    @property
    def generated_measurement_disturbance(self): ...
    @property
    def generated_state_disturbance(self): ...
    @property
    def generated_obs(self): ...
    @property
    def generated_state(self): ...
    @property
    def simulated_state(self): ...
    @property
    def simulated_measurement_disturbance(self): ...
    @property
    def simulated_state_disturbance(self): ...
    def simulate(self, simulation_output: int = ..., disturbance_variates: Any | None = ..., initial_state_variates: Any | None = ..., pretransformed_variates: bool = ...) -> None: ...
