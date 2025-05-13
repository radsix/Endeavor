from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import relationship, backref, Mapped, mapped_column as mappedColumn
from sqlalchemy_utils import CountryType, PhoneNumberType, EmailType, ChoiceType
from app.database import Base
import uuid

class Customer(Base):
    __tablename__ = "customers"

    UUID: Mapped[uuid.UUID] = mappedColumn(primary_key=True, default=uuid.uuid4) # needs to have its own UUID
    name: Mapped[str] = mappedColumn(nullable=False, unique=True)

    address1: Mapped[str]
    address2: Mapped[str]
    city: Mapped[str]
    state: Mapped[str]
    country: Mapped[str]
    zip: Mapped[str]

    contact: Mapped[str]
    contactPosition: Mapped[str]
    phone: Mapped[str]
    email: Mapped[str]

    comments: Mapped[str]

class Project(Base):
    __tablename__ = "projects"

    UUID: Mapped[uuid.UUID] = mappedColumn(primary_key=True, default=uuid.uuid4) # needs to have its own UUID
    parentUUID: Mapped[uuid.UUID] = mappedColumn(ForeignKey('customers.UUID'), nullable=False, index=True)
    customer = relationship('Customer', backref=backref('projects', cascade='all, delete-orphan'))

    name: Mapped[str] = mappedColumn(nullable=False, unique=True)
    description: Mapped[str]
    startDate: Mapped[str]
    application: Mapped[str]
    status = Mapped[Boolean]

    estPrototypeDate: Mapped[str]
    estProuctionDate: Mapped[str]
    estAnnualUsage: Mapped[str]
    estProjectLengthWeeks: Mapped[str]

class Board(Base):
    __tablename__ = "boards"

    UUID: Mapped[uuid.UUID] = mappedColumn(primary_key=True, default=uuid.uuid4) # needs to have its own UUID
    parentUUID: Mapped[uuid.UUID] = mappedColumn(ForeignKey('projects.UUID'), nullable=False)
    project = relationship('Project', backref=backref('boards', cascade='all, delete-orphan'))

    name: Mapped[str] = mappedColumn(nullable=False, unique=True)
    version: Mapped[str]
    revision: Mapped[str]
    MFRRepFirm: Mapped[str]
    MFRRepContact: Mapped[str]
    MFRRepContactPhone: Mapped[str]

class BoardComponent(Base):
    __tablename__ = "boardComponents"

    boardUUID: Mapped[uuid.UUID] = mappedColumn(ForeignKey('boards.UUID'), nullable=False, primary_key=True)
    board = relationship('Board', backref=backref('boardComponents', cascade='all, delete-orphan'))

    componentUUID: Mapped[uuid.UUID] = mappedColumn(ForeignKey('components.UUID'), nullable=False)
    component = relationship('Component', backref=backref('boardComponents', cascade='all, delete-orphan'))

class ComponentType(Base):
    __tablename__ = "componentTypes"

    name: Mapped[str] = mappedColumn(primary_key=True, unique=True)

class Component(Base):
    __tablename__ = "components"

    UUID: Mapped[uuid.UUID] = mappedColumn(primary_key=True, default=uuid.uuid4) # needs to have its own UUID
    parentName: Mapped[str] = mappedColumn(ForeignKey('componentTypes.name'), nullable=False)
    componentType = relationship('ComponentType', backref=backref('components', cascade='all, delete-orphan'))
    
    name: Mapped[str] = mappedColumn(unique=True)

class ComponentMFR(Base):
    __tablename__ = "componentMFRs"

    UUID: Mapped[uuid.UUID] = mappedColumn(primary_key=True, default=uuid.uuid4) # needs to have its own UUID
    parentUUID: Mapped[uuid.UUID] = mappedColumn(ForeignKey('components.UUID'), nullable=False)
    component = relationship('Component', backref=backref('componentMFRs', cascade='all, delete-orphan'))

    MFRPartNumber: Mapped[str] = mappedColumn(unique=True)
    MFRDescription: Mapped[str]
    version: Mapped[str]
    tags: Mapped[str]

    comment: Mapped[str]