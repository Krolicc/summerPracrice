from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Item, User_Item
from datetime import timedelta
from schemas import ItemCreate, UserItemCreate

import crud, schemas, auth

app = FastAPI()

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/items/", response_model=ItemCreate)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(name=item.name, price=item.price)
    db.add(db_item)
    db.commit()
    db.refresh(db_item) 
    return db_item


@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = db.query(Item).offset(skip).limit(limit).all()
    return items

@app.post("/token", response_model=auth.Token)
def login(form_data: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.get_user(db, username=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username, "id": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/user/items")
async def get_user_items(token: str = Depends(auth.oauth2_scheme), db: Session = Depends(get_db)):
    payload = auth.verify_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    existing_user_items = crud.get_user_items(payload["id"], db)
    if not existing_user_items:
        raise HTTPException(status_code=404, detail="User items not found")
    
    item_idx = [user_item.item_id for user_item in existing_user_items]

    items = db.query(Item).filter(Item.id.in_(item_idx)).all()

    result = []
    for item in items:
        count = next((ui.count for ui in existing_user_items if ui.item_id == item.id), 0)
        result.append({
            "id": item.id,
            "name": item.name,
            "price": item.price,
            "count": count
        })

    return result


@app.post("/user/items", response_model=UserItemCreate | None)
def create_user_items(item: UserItemCreate, db: Session = Depends(get_db)):
    db_item = db.query(User_Item).filter(User_Item.user_id == item.user_id, User_Item.item_id == item.item_id).first()

    if not db_item:
        db_user_item = User_Item(user_id=item.user_id, item_id=item.item_id, count=item.count)
        db.add(db_user_item)
        db.commit()
        db.refresh(db_user_item) 
        return db_user_item


@app.delete("/user/items/{item_id}")
def create_user_items(item_id: int, token: str = Depends(auth.oauth2_scheme), db: Session = Depends(get_db)):
    payload = auth.verify_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    db_user_item = db.query(User_Item).filter(User_Item.user_id == payload["id"], User_Item.item_id == item_id).first()
    if not db_user_item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(db_user_item)
    db.commit()

    existing_user_items = crud.get_user_items(payload["id"], db)
    if not existing_user_items:
        raise HTTPException(status_code=404, detail="User items not found")
    
    item_idx = [user_item.item_id for user_item in existing_user_items]

    items = db.query(Item).filter(Item.id.in_(item_idx)).all()

    result = []
    for item in items:
        count = next((ui.count for ui in existing_user_items if ui.item_id == item.id), 0)
        result.append({
            "id": item.id,
            "name": item.name,
            "price": item.price,
            "count": count
        })

    return {"items": result}

@app.put("/user/items/{item_id}/{count}")
def update_item(item_id: int, count: int, token: str = Depends(auth.oauth2_scheme), db: Session = Depends(get_db)):
    payload = auth.verify_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    item = db.query(User_Item).filter(User_Item.user_id == payload["id"], User_Item.item_id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item.count = count
    db.commit()
    db.refresh(item)

    existing_user_items = crud.get_user_items(payload["id"], db)
    if not existing_user_items:
        raise HTTPException(status_code=404, detail="User items not found")
    
    item_idx = [user_item.item_id for user_item in existing_user_items]

    items = db.query(Item).filter(Item.id.in_(item_idx)).all()

    result = []
    for item in items:
        count = next((ui.count for ui in existing_user_items if ui.item_id == item.id), 0)
        result.append({
            "id": item.id,
            "name": item.name,
            "price": item.price,
            "count": count
        })

    return {"items": result}


@app.post("/register", response_model=schemas.UserCreate)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user(db, username=user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


# Пример защищенного маршрута
@app.get("/protected_route")
async def protected_route(token: str = Depends(auth.oauth2_scheme)):
    payload = auth.verify_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    return {"message": "Authorized", "user": payload}