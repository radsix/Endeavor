from fastapi import APIRouter, Request
from app.schemas import Customer as customerSchema
from app.models import Customer as customerModel
from app.dependency import endeavorSession
from app.helpers import getAll, getByUUID, createObject, deleteObject, updateObject
from .limiter import limiter, lim_rate
import uuid

router = APIRouter(
    prefix="/customer",
    tags=["Customer"],
    responses={404: {"description": "Not found"}},
)

# getting a list of customers
@router.get("/getCustomers", summary="Get a list of customers")
async def getCustomers(request: Request, session: endeavorSession):
    """
    Returns a customer
    """
    return await getAll(customerModel, session)

# getting a customer by its UUID
@router.get("/getCustomerByUUID", summary="Get a customer by its UUID")
async def getCustomerByUUID(UUID: uuid.UUID, request: Request, session: endeavorSession):
    """
    Returns a customer
    """
    return await getByUUID(UUID, customerModel, session)

# updating a customer by its UUID
@router.put("/updateCustomer", summary="Update a customer by its UUID")
@limiter.limit(lim_rate)
async def updateCustomerByUUID(UUID: uuid.UUID, customerUpdate: customerSchema, request: Request, session: endeavorSession):
    """
    Returns a customer
    """
    return await updateObject(UUID, customerUpdate, customerModel, session)

# creating a new customer
@router.post("/createCustomer", summary="Create a new customer")
@limiter.limit(lim_rate)
async def createCustomer(customerCreate: customerSchema, request: Request, session: endeavorSession) -> dict:
    """
    Returns a customer
    """
    return await createObject(customerCreate, customerModel, session)

# deleting a customer from the database by its UUID
@router.delete("/deleteCustomer", summary="Delete a customer by its UUID")
@limiter.limit(lim_rate)
async def deleteCustomerByUUID(UUID: uuid.UUID, request: Request, session: endeavorSession) -> dict:
    """
    Returns a customer
    """
    return await deleteObject(UUID, customerModel, session)