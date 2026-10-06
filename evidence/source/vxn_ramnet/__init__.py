"""VXN-RAMNet camera-based visual route-memory research prototype.

The package implements constrained offline route research. The presentation's
Pi/Android object-detection test is team-reported and outside this source tree.
Mobile route integration, IMU fusion and live route guidance remain unvalidated.
"""

from .config.models import PipelineConfig
from .core.version import __version__
from .pipeline.runner import PipelineResult, VxnPipeline, run_pipeline
from .recognition import RouteRecognizer, learn_route_memory

__all__ = [
    "PipelineConfig",
    "PipelineResult",
    "VxnPipeline",
    "run_pipeline",
    "RouteRecognizer",
    "learn_route_memory",
    "__version__",
]
