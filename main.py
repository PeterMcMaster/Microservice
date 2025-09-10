from __future__ import annotations

import os
import socket
from datetime import datetime

from typing import Dict, List
from uuid import UUID

from fastapi import FastAPI, HTTPException
from fastapi import Query, Path
from typing import Optional

from models.person import PersonCreate, PersonRead, PersonUpdate
from models.address import AddressCreate, AddressRead, AddressUpdate
from models.classes import ClassCreate, ClassRead, ClassUpdate
from models.account import AccountCreate, AccountRead, AccountUpdate
from models.health import Health

port = int(os.environ.get("FASTAPIPORT", 8000))

# -----------------------------------------------------------------------------
# Fake in-memory "databases"
# -----------------------------------------------------------------------------
persons: Dict[UUID, PersonRead] = {}
addresses: Dict[UUID, AddressRead] = {}
classes: Dict[UUID, ClassRead] = {}
accounts: Dict[UUID, AccountRead] = {}

app = FastAPI(
    title="Person/Address/Class/Account API",
    description="Demo FastAPI app using Pydantic v2 models for Person, Address, Class, and Account.",
    version="0.1.0",
)

# -----------------------------------------------------------------------------
# Address endpoints
# -----------------------------------------------------------------------------

def make_health(echo: Optional[str], path_echo: Optional[str]=None) -> Health:
    return Health(
        status=200,
        status_message="OK",
        timestamp=datetime.utcnow().isoformat() + "Z",
        ip_address=socket.gethostbyname(socket.gethostname()),
        echo=echo,
        path_echo=path_echo
    )

@app.get("/health", response_model=Health)
def get_health_no_path(echo: str | None = Query(None, description="Optional echo string")):
    # Works because path_echo is optional in the model
    return make_health(echo=echo, path_echo=None)

@app.get("/health/{path_echo}", response_model=Health)
def get_health_with_path(
    path_echo: str = Path(..., description="Required echo in the URL path"),
    echo: str | None = Query(None, description="Optional echo string"),
):
    return make_health(echo=echo, path_echo=path_echo)

@app.post("/addresses", response_model=AddressRead, status_code=201)
def create_address(address: AddressCreate):
    if address.id in addresses:
        raise HTTPException(status_code=400, detail="Address with this ID already exists")
    addresses[address.id] = AddressRead(**address.model_dump())
    return addresses[address.id]

@app.get("/addresses", response_model=List[AddressRead])
def list_addresses(
    street: Optional[str] = Query(None, description="Filter by street"),
    city: Optional[str] = Query(None, description="Filter by city"),
    state: Optional[str] = Query(None, description="Filter by state/region"),
    postal_code: Optional[str] = Query(None, description="Filter by postal code"),
    country: Optional[str] = Query(None, description="Filter by country"),
):
    results = list(addresses.values())

    if street is not None:
        results = [a for a in results if a.street == street]
    if city is not None:
        results = [a for a in results if a.city == city]
    if state is not None:
        results = [a for a in results if a.state == state]
    if postal_code is not None:
        results = [a for a in results if a.postal_code == postal_code]
    if country is not None:
        results = [a for a in results if a.country == country]

    return results

@app.get("/addresses/{address_id}", response_model=AddressRead)
def get_address(address_id: UUID):
    if address_id not in addresses:
        raise HTTPException(status_code=404, detail="Address not found")
    return addresses[address_id]

@app.patch("/addresses/{address_id}", response_model=AddressRead)
def update_address(address_id: UUID, update: AddressUpdate):
    if address_id not in addresses:
        raise HTTPException(status_code=404, detail="Address not found")
    stored = addresses[address_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    addresses[address_id] = AddressRead(**stored)
    return addresses[address_id]

# -----------------------------------------------------------------------------
# Person endpoints
# -----------------------------------------------------------------------------
@app.post("/persons", response_model=PersonRead, status_code=201)
def create_person(person: PersonCreate):
    # Each person gets its own UUID; stored as PersonRead
    person_read = PersonRead(**person.model_dump())
    persons[person_read.id] = person_read
    return person_read

@app.get("/persons", response_model=List[PersonRead])
def list_persons(
    uni: Optional[str] = Query(None, description="Filter by Columbia UNI"),
    first_name: Optional[str] = Query(None, description="Filter by first name"),
    last_name: Optional[str] = Query(None, description="Filter by last name"),
    email: Optional[str] = Query(None, description="Filter by email"),
    phone: Optional[str] = Query(None, description="Filter by phone number"),
    birth_date: Optional[str] = Query(None, description="Filter by date of birth (YYYY-MM-DD)"),
    city: Optional[str] = Query(None, description="Filter by city of at least one address"),
    country: Optional[str] = Query(None, description="Filter by country of at least one address"),
):
    results = list(persons.values())

    if uni is not None:
        results = [p for p in results if p.uni == uni]
    if first_name is not None:
        results = [p for p in results if p.first_name == first_name]
    if last_name is not None:
        results = [p for p in results if p.last_name == last_name]
    if email is not None:
        results = [p for p in results if p.email == email]
    if phone is not None:
        results = [p for p in results if p.phone == phone]
    if birth_date is not None:
        results = [p for p in results if str(p.birth_date) == birth_date]

    # nested address filtering
    if city is not None:
        results = [p for p in results if any(addr.city == city for addr in p.addresses)]
    if country is not None:
        results = [p for p in results if any(addr.country == country for addr in p.addresses)]

    return results

@app.get("/persons/{person_id}", response_model=PersonRead)
def get_person(person_id: UUID):
    if person_id not in persons:
        raise HTTPException(status_code=404, detail="Person not found")
    return persons[person_id]

@app.patch("/persons/{person_id}", response_model=PersonRead)
def update_person(person_id: UUID, update: PersonUpdate):
    if person_id not in persons:
        raise HTTPException(status_code=404, detail="Person not found")
    stored = persons[person_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    persons[person_id] = PersonRead(**stored)
    return persons[person_id]

# -----------------------------------------------------------------------------
# Class endpoints
# -----------------------------------------------------------------------------
@app.post("/classes", response_model=ClassRead, status_code=201)
def create_class(cls: ClassCreate):
    # Each class gets its own UUID; stored as ClassRead
    class_read = ClassRead(**cls.model_dump())
    classes[class_read.id] = class_read
    return class_read

@app.get("/classes", response_model=List[ClassRead])
def list_classes(
    name: Optional[str] = Query(None, description="Filter by class name"),
    description: Optional[str] = Query(None, description="Filter by class description"), 
):
    results = list(classes.values())

    if name is not None:
        results = [c for c in results if c.name == name]
    if description is not None:
        results = [c for c in results if c.description == description]

    return results

@app.get("/classes/{class_id}", response_model=ClassRead)
def get_class(class_id: UUID):
    if class_id not in classes:
        raise HTTPException(status_code=404, detail="Class not found")
    return classes[class_id]

@app.patch("/classes/{class_id}", response_model=ClassRead)
def update_class(class_id: UUID, update: ClassUpdate):
    if class_id not in classes:
        raise HTTPException(status_code=404, detail="Class not found")
    stored = classes[class_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    classes[class_id] = ClassRead(**stored)
    return classes[class_id]

# -----------------------------------------------------------------------------
# Account endpoints
# -----------------------------------------------------------------------------
@app.post("/accounts", response_model=AccountRead, status_code=201)
def create_account(account: AccountCreate):
    # Each account gets its own UUID; stored as AccountRead
    account_read = AccountRead(**account.model_dump())
    accounts[account_read.id] = account_read
    return account_read

@app.get("/accounts", response_model=List[AccountRead])
def list_accounts(
    username: Optional[str] = Query(None, description="Filter by username"),
    number_id: Optional[int] = Query(None, description="Filter by number ID"),
    amount: Optional[float] = Query(None, description="Filter by amount"),
):
    results = list(accounts.values())

    if username is not None:
        results = [a for a in results if a.username == username]
    if number_id is not None:
        results = [a for a in results if a.number_id == number_id]
    if amount is not None:
        results = [a for a in results if a.amount == amount]

    return results

@app.get("/accounts/{account_id}", response_model=AccountRead)
def get_account(account_id: UUID):
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    return accounts[account_id] 

@app.patch("/accounts/{account_id}", response_model=AccountRead)
def update_account(account_id: UUID, update: AccountUpdate):
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    stored = accounts[account_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    accounts[account_id] = AccountRead(**stored)
    return accounts[account_id]

# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Person/Address API. See /docs for OpenAPI UI."}

# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
