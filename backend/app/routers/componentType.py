from fastapi import APIRouter, Request, HTTPException
from sqlalchemy.exc import IntegrityError, ProgrammingError
from app.schemas import ComponentType as componentSchema
from app.models import ComponentType as componentModel
from app.dependency import endeavorSession
from app.helpers import getAll, getByStr, createObject
from .limiter import limiter, lim_rate

router = APIRouter(
    prefix="/type",
    tags=["Component Type"],
    responses={404: {"description": "Not found"}},
)

# getting a list of component types
@router.get("/getTypes", summary="Get a list of component types")
async def getTypes(request: Request, session: endeavorSession):
    """
    Returns a list of component types
    """
    return await getAll(componentModel, session)

# creating a new component type
@router.post("/createType", summary="Create a new component type")
@limiter.limit(lim_rate)
async def createType(componentTypeCreate: componentSchema, request: Request, session: endeavorSession) -> dict:
    """
    Returns a component type
    """
    return await createObject(componentTypeCreate, componentModel, session)

# deleting a component type from the database by its UUID
@router.delete("/deleteType", summary="Delete a component type by its UUID")
@limiter.limit(lim_rate)
async def deleteTypeByName(name: str, request: Request, session: endeavorSession) -> dict:
    """
    Returns a component type
    """
    delete = await getByStr(name, componentModel, session)
    try:
        await session.delete(delete)
        await session.commit()
        return {"deletedName": name}
    except IntegrityError or ProgrammingError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Deletion Impossible")
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error. Please try again later.")