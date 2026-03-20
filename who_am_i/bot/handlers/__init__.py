from .start import router as start_router
from .test import router as test_router
from .menu import router as menu_router
from .registration import router as registration_router
from .stats import router as stats_router

all_routers = [
    start_router,
    test_router,
    menu_router,
    registration_router,
    stats_router,
]
