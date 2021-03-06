from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from app.routes.patient import router as PatientRouter
from app.routes.staff import router as StaffRouter
from app.routes.group import router as GroupRouter
from app.routes.room import router as RoomRouter
from app.routes.auth import router as AuthRouter
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


API_PREFIX = "/api"
PROJECT_NAME = "GANO API"
DEBUG = False
VERSION = "0.1"

origins = [
    "http://react.facerain.club",
    "http://localhost",
    "http://localhost:8080",
]


def get_application() -> FastAPI:
    app = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)
    app.include_router(PatientRouter, tags=["Patient"], prefix="/patient")
    app.include_router(StaffRouter, tags=["Staff"], prefix="/staff")
    app.include_router(GroupRouter, tags=["Group"], prefix="/group")
    app.include_router(RoomRouter, tags=["Room"], prefix="/room")
    app.include_router(AuthRouter, tags=["Auth"], prefix="/auth")
    app.add_middleware(CORSMiddleware, allow_origins=origins,
                       allow_credentials=True,
                       allow_methods=["*"],
                       allow_headers=["*"],)
    return app


app = get_application()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


@app.get("/", tags=["Root"])
async def read_root():
    return {"Message": "Access Successfully!"}
