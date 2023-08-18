from fastapi import APIRouter

from .dome import router as dome_router

router = APIRouter(
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

router.include_router(dome_router)
