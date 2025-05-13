from fastapi import APIRouter, Request
from .limiter import limiter, lim_rate
from app.schemas import Project as projectSchema, updateProject as updateSchema
from app.models import Project as projectModel, Customer as customerModel
from app.helpers import getAll, getByUUID, getDescendantsByUUID, createObject, deleteObject, updateObject
from app.dependency import endeavorSession
import uuid

router = APIRouter(
    prefix="/project",
    tags=["Project"],
    responses={404: {"description": "Not found"}},
)

# getting a list of projects
@router.get("/getProjects", summary="Get a list of projects")
async def getProjects(request: Request, session: endeavorSession):
    """
    Returns a project
    """
    return await getAll(projectModel, session)

# getting a list of projects from customer UUID
@router.get("/getProjectsByCustomer", summary="Get a list of projects from customer UUID")
async def getProjectByCustomerUUID(UUID: uuid.UUID, request: Request, session: endeavorSession):
    """
    Returns a project
    """
    return await getDescendantsByUUID(UUID, projectModel, session)

# getting a project from its UUID
@router.get("/getProjectByUUID", summary="Get a project from its UUID")
async def getProjectByUUID(UUID: uuid.UUID, request: Request, session: endeavorSession):
    """
    Returns a project
    """
    return await getByUUID(UUID, projectModel, session)

# updating a project by its UUID
@router.put("/updateProject", summary="Update a project by its UUID")
@limiter.limit(lim_rate)
async def updateProjectByUUID(UUID: uuid.UUID, projectUpdate: updateSchema, request: Request, session: endeavorSession):
    """
    Returns a project
    """
    return await updateObject(UUID, projectUpdate, projectModel, session)

# creating a new project
@router.post("/createProject", summary="Create a new project")
@limiter.limit(lim_rate)
async def createProject(projectCreate: projectSchema, request: Request, session: endeavorSession):
    """
    Returns a project
    """
    await getByUUID(projectCreate.parentUUID, customerModel, session)
    return await createObject(projectCreate, projectModel, session)

# deleting a project from the database by its UUID
@router.delete("/deleteProject", summary="Delete a project by its UUID")
@limiter.limit(lim_rate)
async def deleteProjectByUUID(UUID: uuid.UUID, request: Request, session: endeavorSession):
    """
    Returns a project
    """
    return await deleteObject(UUID, projectModel, session)
