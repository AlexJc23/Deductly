
from fastapi import APIRouter
from app.api.v1.endpoints import health, user, auth, trip, income, expense



api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(user.router)
api_router.include_router(auth.router)
api_router.include_router(trip.router)
api_router.include_router(income.router)
api_router.include_router(expense.router)
