from .start import router as start_router
from .test import router as test_router
from .menu import router as menu_router
from .registration import router as registration_router

all_routers = [
    start_router,
    registration_router,
    test_router,
    menu_router,
]
