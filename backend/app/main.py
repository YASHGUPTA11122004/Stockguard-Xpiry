from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from . import models, schemas, database, auth, utils

from fastapi.middleware.cors import CORSMiddleware

# ---------------- INIT ----------------
app = FastAPI(title="StockGuard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=database.engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# ---------------- GET CURRENT USER ----------------
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        user_id = int(payload.get("sub"))
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


# ---------------- AUTH ----------------
@app.post("/signup", response_model=schemas.UserOut)
def signup(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = utils.hash(user.password)

    # ✅ FIXED FIELD NAME
    new_user = models.User(
        email=user.email,
        hashed_password=hashed
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.post("/login", response_model=schemas.Token)
def login(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    # ✅ FIXED FIELD NAME
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = auth.create_access_token({"sub": str(db_user.id)})

    return {"access_token": token}


# ---------------- ITEMS ----------------
@app.post("/items", response_model=schemas.ItemOut)
def create_item(
    item: schemas.ItemCreate,
    db: Session = Depends(database.get_db),
    current_user=Depends(get_current_user),
):
    new_item = models.Item(**item.dict(), owner_id=current_user.id)

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


@app.get("/items", response_model=list[schemas.ItemOut])
def get_items(
    db: Session = Depends(database.get_db),
    current_user=Depends(get_current_user),
):
    items = db.query(models.Item).filter(
        models.Item.owner_id == current_user.id
    ).all()

    items = sorted(
        items,
        key=lambda x: utils.calculate_urgency(x.category, x.expiry_date),
        reverse=True,
    )

    return items
