from src.fault_injector.fault_configurations.fault_configuration import FaultConfiguration
from src.fault_injector.fault_types.fault import Fault
import random

class RegularFaultStrategy:

    def should_inject(tick: int, fault: Fault) -> bool:
        return fault.configuration.start_tick == tick and not fault.injected
    
    def should_resolve(tick: int, fault: Fault) -> bool:
        return fault.configuration.end_tick == tick and fault.injected


class RandomFaultStrategy:

    def should_inject(tick: int, fault: Fault) -> bool:
        return random.random() < fault.configuration.inject_probability and not fault.injected
    
    def should_resolve(tick: int, fault: Fault) -> bool:
        return random.random() < fault.configuration.resolve_probability and fault.injected