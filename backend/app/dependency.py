from typing import Annotated
from app.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

endeavorSession = Annotated[AsyncSession, Depends(get_db)]