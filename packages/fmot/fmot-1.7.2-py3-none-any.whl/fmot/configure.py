from typing import *
from dataclasses import dataclass, field, asdict
from contextlib import contextmanager

@dataclass
class FMOTConfig:
    """
    FMOTConfig can be used to change the behavior of
    model conversion, enabling/disabling certain optimizations
    and mappings.
    """

    # observers
    param_observer: str = 'min_max'
    default_observer: str = 'min_max'
    lstm_param_observer: str = 'min_max'
    minmax_headroom: int = 0

    # nn.Linear quantization mode
    pow2_linear_scale: bool = False
    perchannel_linear: bool = True

    # lookup table interpolation
    interpolate: bool = True
    sim_fixed_range_fp: bool = True
    ilut_requant: bool = False
    insert_fixed_range_observers: bool = True

    # rnn configuration
    rnn_mm_limits: bool = False

    # lstm config
    lstm_interpolate: bool = True    
    sequenced_lstm: bool = False
    fused_lstm: bool = True

    # tcn config
    # Plan: support legacy approach until femtomapper dev supports this,
    # then, deprecate the old feature.
    legacy_buffer_rotation: bool = False

    @contextmanager
    def configure(self, **kwargs):
        prev_state = asdict(self)

        for k, v in kwargs.items():
            setattr(self, k, v)
        try:
            yield
        finally:
            for k, v in prev_state.items():
                setattr(self, k, v)


CONFIG = FMOTConfig()

def configure_param_observer(obs_class: str='min_max'):
    """
    Configure the default parameter observer.

    Arguments:
        obs_class (str): Default 'min_max'. Options are: 
                'min_max': MinMaxObserver
                'moving_min_max': MovingAverageMinMaxObserver
                'gaussian': GaussianObserver
    """
    CONFIG.param_observer = obs_class

def configure_act_observer(obs_class: str='min_max'):
    """
    Configure the default activation observer.

    Arguments:
        obs_class (str, or class): Default 'min_max'. Options are: 
                'min_max': MinMaxObserver
                'moving_min_max': MovingAverageMinMaxObserver
                'gaussian': GaussianObserver
    """
    CONFIG.default_observer = obs_class
