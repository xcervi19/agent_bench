from .alerts import router as alerts_router
from .events import router as events_router
from .insights import router as insights_router
from .profiles import router as profiles_router
from .reports import router as reports_router
from .search import router as search_router
from .setup import router as setup_router
from .signals import router as signals_router
from .tasks import router as tasks_router

ALL_ROUTERS = [
    setup_router,
    profiles_router,
    events_router,
    signals_router,
    insights_router,
    reports_router,
    alerts_router,
    search_router,
    tasks_router,
]

__all__ = ["ALL_ROUTERS"]
