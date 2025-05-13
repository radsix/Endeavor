from fastapi import APIRouter, Request
from app.schemas import Component as componentSchema, updateComponent as updateSchema
from app.models import Component as componentModel, ComponentType as typeModel
from app.dependency import endeavorSession
from app.helpers import getAllByStr, getByUUID, getByStr, createObject, deleteObject, updateObject
from .limiter import limiter, lim_rate
import uuid

router = APIRouter(
    prefix="/component",
    tags=["Component"],
    responses={404: {"description": "Not found"}},
)

# getting a list components by type
@router.get("/getComponentsByType", summary="Get components by their type")
async def getComponentsByType(name: str, request: Request, session: endeavorSession):
    """
    Returns a list of components
    """
    return await getAllByStr(name, componentModel, session)

# getting a component by its UUID
@router.get("/getComponentByUUID", summary="Get a component by its UUID")
async def getComponentByUUID(UUID: uuid.UUID, request: Request, session: endeavorSession):
    """
    Returns a component
    """
    return await getByUUID(UUID, componentModel, session)

# updating a component by its UUID
@router.put("/updateComponent", summary="Update a component by its UUID")
@limiter.limit(lim_rate)
async def updateComponentByUUID(UUID: uuid.UUID, updateComponent: updateSchema, request: Request, session: endeavorSession):
    """
    Returns a component
    """
    return await updateObject(UUID, updateComponent, componentModel, session)

# creating a new component
@router.post("/createComponent", summary="Create a new component")
@limiter.limit(lim_rate)
async def createComponent(createComponent: componentSchema, request: Request, session: endeavorSession):
    """
    Returns a component
    """
    await getByStr(createComponent.parentName, typeModel, session)
    return await createObject(createComponent, componentModel, session)

# deleting a component from the database by its UUID
@router.delete("/deleteComponent", summary="Delete a component by its UUID")
@limiter.limit(lim_rate)
async def deleteComponentByUUID(UUID: uuid.UUID, request: Request, session: endeavorSession):
    """
    Returns a component
    """
    return await deleteObject(UUID, componentModel, session)