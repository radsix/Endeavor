from fastapi import APIRouter, Request
from app.schemas import Board as boardSchema, updateBoard as updateSchema
from app.models import Board as boardModel, Project as projectModel
from app.dependency import endeavorSession
from app.helpers import getAll, getByUUID, getDescendantsByUUID, createObject, deleteObject, updateObject
from .limiter import limiter, lim_rate
import uuid

router = APIRouter(
    prefix="/board",
    tags=["Board"],
    responses={404: {"description": "Not found"}},
)

# getting a list of boards
@router.get("/getBoards", summary="Get a list of boards")
async def getBoards(request: Request, session: endeavorSession):
    """
    Returns all boards
    """
    return await getAll(boardModel, session)

# getting a list of boards from project UUID
@router.get("/getBoardsByProject", summary="Get a list of boards from project UUID")
async def getBoardsByProject(UUID: uuid.UUID, request: Request, session: endeavorSession):
    """
    Returns a board
    """
    return await getDescendantsByUUID(UUID, boardModel, session)

# getting a board from its UUID
@router.get("/getBoardByUUID", summary="Get a board from its UUID")
async def getBoardByUUID(UUID: uuid.UUID, request: Request, session: endeavorSession):
    """
    Returns a board
    """
    return await getByUUID(UUID, boardModel, session)

# updating a board by its UUID
@router.put("/updateBoard", summary="Update a board by its UUID")
@limiter.limit(lim_rate)
async def updateBoardByUUID(UUID: uuid.UUID, updateBoard: updateSchema, request: Request, session: endeavorSession):
    """
    Returns a board
    """
    return await updateObject(UUID, updateBoard, boardModel, session)

# creating a new board
@router.post("/createBoard", summary="Create a new board")
@limiter.limit(lim_rate)
async def createBoard(boardCreate: boardSchema, request: Request, session: endeavorSession):
    """
    Returns a board
    """
    await getByUUID(boardCreate.parentUUID, projectModel, session)
    return await createObject(boardCreate, boardModel, session)

# deleting a board from the database by its UUID
@router.delete("/deleteBoard", summary="Delete a board by its UUID")
@limiter.limit(lim_rate)
async def deleteBoardByUUID(UUID: uuid.UUID, request: Request, session: endeavorSession):
    """
    Returns a board
    """
    return await deleteObject(UUID, boardModel, session)