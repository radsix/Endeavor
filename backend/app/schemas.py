from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
import uuid

class Customer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str

    address1: Optional[str] = None
    address2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    zip: Optional[str] = None

    contact: Optional[str] = None
    contactPosition: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

    comments: Optional[str] = None

class Project(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    parentUUID: uuid.UUID
    description: Optional[str] = None
    startDate: Optional[str] = None
    application: Optional[str] = None
    status: Optional[bool] = False

    estPrototypeDate: Optional[str] = None
    estProuctionDate: Optional[str] = None
    estAnnualUsage: Optional[str] = None
    estProjectLengthWeeks: Optional[str] = None

class updateProject(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: Optional[str] = None
    startDate: Optional[str] = None
    application: Optional[str] = None
    status: Optional[bool] = False

    estPrototypeDate: Optional[str] = None
    estProuctionDate: Optional[str] = None
    estAnnualUsage: Optional[str] = None
    estProjectLengthWeeks: Optional[str] = None

class Board(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    parentUUID: uuid.UUID
    version: Optional[str] = None
    revision: Optional[str] = None

    MFRRepFirm: Optional[str] = None
    MFRRepContact: Optional[str] = None
    MFRRepContactPhone: Optional[str] = None

class updateBoard(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    version: Optional[str] = None
    revision: Optional[str] = None

    MFRRepFirm: Optional[str] = None
    MFRRepContact: Optional[str] = None
    MFRRepContactPhone: Optional[str] = None

class BoardComponent(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    boardUUID: uuid.UUID
    componentUUID: uuid.UUID

class ComponentType(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str

class Component(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    parentName: str
    name: str

class updateComponent(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str

class ComponentMFR(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    parentUUID: uuid.UUID

    MFRPartNumber: str
    MFRDescription: Optional[str] = None
    version: Optional[str] = None
    tags: Optional[str] = None

    comment: Optional[str] = None

class updateComponentMFR(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    MFRPartNumber: Optional[str] = None
    MFRDescription: Optional[str] = None
    version: Optional[str] = None
    tags: Optional[str] = None

    comment: Optional[str] = None