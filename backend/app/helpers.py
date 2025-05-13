from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, ProgrammingError
from uuid import UUID

from app.dependency import endeavorSession

async def getAll(getModel, session: endeavorSession):
    result = await session.execute(select(getModel))
    models = result.scalars().all()
    if not models:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No %s found" % getModel.__name__)
    return models

async def getAllByStr(name: str, getModel, session: endeavorSession):
    result = await session.execute(select(getModel).where(getModel.parentName == name))
    models = result.scalars().all()
    if not models:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No %s found" % getModel.__name__)
    return models

async def getByUUID(uuid: UUID, getModel, session: endeavorSession):
    result = await session.execute(select(getModel).where(getModel.UUID == uuid))
    model = result.scalars().first()
    if not model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No %s with that UUID found" % getModel.__name__)
    return model

async def getByStr(id: str, getModel, session: endeavorSession):
    result = await session.execute(select(getModel).where(getModel.name == id))
    model = result.scalars().first()
    if not model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No %s with that UUID found" % getModel.__name__)
    return model

async def getDescendantsByUUID(uuid: UUID, getModel, session: endeavorSession):
    result = await session.execute(select(getModel).where(getModel.parentUUID == uuid))
    models = result.scalars().all()
    if not models:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No %s found" % getModel.__name__)
    return models

async def getDescendantsByName(name: str, getModel, session: endeavorSession):
    result = await session.execute(select(getModel).where(getModel.parentName == name))
    models = result.scalars().all()
    if not models:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No %s found" % getModel.__name__)
    return models

async def updateObject(uuid: UUID, updateSchema, updateModel, session: endeavorSession):
    updateObj = await getByUUID(uuid, updateModel, session)
    try:
        for field, value in updateSchema.model_dump(exclude_unset=True).items():
            setattr(updateObj, field, value)
        await session.commit()
        await session.refresh(updateObj)
        modelResponse = type(updateSchema).model_validate(updateObj)
        return modelResponse.model_dump()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="A %s with this name already exists." % updateModel.__name__)
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error. Please try again later.")

async def createObject(createSchema, createModel, session: endeavorSession):
    try:
        model = createModel(**createSchema.model_dump())
        session.add(model)
        await session.commit()
        await session.refresh(model)
        modelResponse = type(createSchema).model_validate(model)
        return modelResponse.model_dump()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="A %s with this name already exists." % createModel.__name__)
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error. Please try again later.")

async def deleteObject(uuid: UUID, deleteModel, session:endeavorSession):
    delete = await getByUUID(uuid, deleteModel, session)
    try:
        await session.delete(delete)
        await session.commit()
        return {"deletedUUID": str(uuid)}
    except IntegrityError or ProgrammingError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Deletion Impossible")
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error. Please try again later.")