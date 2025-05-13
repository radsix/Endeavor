from fastapi import APIRouter, Request
from .limiter import limiter, lim_rate
from app.schemas import ComponentMFR as componentMFRSchema, updateComponentMFR as updateSchema
from app.models import ComponentMFR as componentMFRModel, Component as componentModel
from app.helpers import getByUUID, getDescendantsByUUID, createObject, deleteObject, updateObject
from app.dependency import endeavorSession
import uuid

router = APIRouter(
    prefix="/componentMFR",
    tags=["Manufacturer Component"],
    responses={404: {"description": "Not found"}},
)

# getting a list of manufactured parts that match the component
@router.get("/getMFRsByComponent", summary="Get a list of projects from customer UUID")
async def getMFRByComponentUUID(UUID: uuid.UUID, request: Request, session: endeavorSession):
    """
    Returns a manufacturer component
    """
    return await getDescendantsByUUID(UUID, componentMFRModel, session)

# getting a manufacturer component from its UUID
@router.get("/getComponentMFRByUUID", summary="Get a manufacturer component from its UUID")
async def getComponentMFRByUUID(UUID: uuid.UUID, request: Request, session: endeavorSession):
    """
    Returns a manufacturer component
    """
    return await getByUUID(UUID, componentMFRModel, session)

# updating a manufacturer component by its UUID
@router.put("/updateMFR", summary="Update a manufacturer component by its UUID")
@limiter.limit(lim_rate)
async def updateComponentMFRByUUID(UUID: uuid.UUID, projectUpdate: updateSchema, request: Request, session: endeavorSession):
    """
    Returns a manufacturer component
    """
    return await updateObject(UUID, projectUpdate, componentMFRModel, session)

# creating a new manufactured component
@router.post("/createMFR", summary="Create a new project")
@limiter.limit(lim_rate)
async def createComponentMFR(projectCreate: componentMFRSchema, request: Request, session: endeavorSession):
    """
    Returns a manufacturer component
    """
    await getByUUID(projectCreate.parentUUID, componentModel, session)
    return await createObject(projectCreate, componentMFRModel, session)

# deleting a manufacturer component from the database by its UUID
@router.delete("/deleteMFR", summary="Delete a manufacturer component by its UUID")
@limiter.limit(lim_rate)
async def deleteComponentMFRByUUID(UUID: uuid.UUID, request: Request, session: endeavorSession):
    """
    Returns a manufacturer component
    """
    return await deleteObject(UUID, componentMFRModel, session)
