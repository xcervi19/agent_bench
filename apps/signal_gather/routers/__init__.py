from .events import router as events_router
from .insights import router as insights_router
from .signals import router as signals_router
from .tasks import router as tasks_router

ALL_ROUTERS = [events_router, signals_router, insights_router, tasks_router]

__all__ = ["ALL_ROUTERS"]
