import os, traceback
from fastapi import Request, FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.globals import set_debug
from typing import Dict
from api.pose_identifier import router as pose_identifier_router
from api.related_poses import router as related_poses_router


if os.getenv("DEBUG", "False").lower() == "true":
    set_debug(True)

app = FastAPI(
    title="Yoga App Backend Server",
    version="0.1.0",
    description="POC Yoga Application",
)

# Commenting chains, going with simple llm calls until complexity needed 
# from chains.pose_identifier import PoseIdentifierChain
# pose_identifier = PoseIdentifierChain()


# Adds routes to the app for using the chain under:
# /invoke
# /batch
# /stream
# add_routes(
#     app, analyst_perspective.create_chain(), enable_feedback_endpoint=True, path="/api/v1/analyst-perspective"
# )
# add_routes(app, pose_identifier.create_chain(), path="/api/v1/pose-identifier")

app.include_router(pose_identifier_router)
app.include_router(related_poses_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    print("".join(traceback.TracebackException.from_exception(exc).format()))
    print("Request: ", request)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": f"{str(exc)}"},
    )
