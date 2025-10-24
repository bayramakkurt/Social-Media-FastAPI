#Business Logic = Service Katmanı

from fastapi import Depends
from sqlalchemy.orm import Session

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime

from .models import User
from .schemas import UserCreate, UserUpdate

bcrypt_context = CryptContext(schemes= ["bcrypt"], deprecated = "auto") #Şifreleri hashlemek için bağlam olarak bcrypt kullanıldı.
oauth2_bearer = OAuth2PasswordBearer(tokenUrl= "v1/auth/token") #Kullanıcı Bearer token almak için endpointe gitmeli ve giriş yapmalı
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINS = 60 * 24 * 30 #Token expire süresi 30 gün olacak.


#Mevcut Kullanıcıları Kontrol
async def existing_user(db: Session, username: str = None, email: str = None):
    """Kullanıcı adı veya email ile kullanıcı ara"""
    if username:
        db_user = db.query(User).filter(User.username == username).first()
        if db_user:
            return db_user
    
    if email:
        db_user = db.query(User).filter(User.email == email).first()
        if db_user:
            return db_user
    
    return None

#Token Oluşturma
async def create_access_token(username: str, id: int):
    expires = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINS)
    encode = {"sub": username, "id": id, "exp": expires}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

#Tokenden Kullanıcıyı Alma
async def get_current_user(db: Session, token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        id: str = payload.get("id")
        expires: datetime = payload.get("exp")
        if datetime.fromtimestamp(expires) < datetime.now():
            return None
        if username is None or id is None:
            return None
        return db.query(User).filter(User.id == id).first()
    except JWTError:
        return None
    
#Kullanıcı Bilgilerini Getirme
async def get_user_from_user_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

#Kullanıcı Oluşturma
async def create_user(db: Session, user: UserCreate):
    db_user = User(
        email = user.email.lower().strip(),
        username = user.username.lower().strip(),
        hashed_password = bcrypt_context.hash(user.password),
        birthDate = user.birthDate or None,
        gender = user.gender or None,
        biography = user.biography or None,
        location = user.location or None,
        profile_pic = user.profile_pic or None,
        name = user.name or None
    )
    db.add(db_user)
    db.commit()

    return db_user

#Authentication
async def authenticate(db: Session, username: str, password: str):
    """Kullanıcı adı veya email ile giriş"""
    # Önce username olarak kontrol et
    db_user = db.query(User).filter(User.username == username).first()
    
    # Bulunamadıysa email olarak kontrol et
    if not db_user:
        db_user = db.query(User).filter(User.email == username).first()
    
    # Hala bulunamadıysa None dön
    if not db_user:
        return None
    
    # Şifreyi kontrol et
    if not verify_password(password, db_user.hashed_password):
        return None
    
    return db_user

#Update User
async def update_user(db:Session, db_user: User, user_update: UserUpdate):
    db_user.biography = user_update.biography or db_user.biography
    db_user.birthDate = user_update.birthDate or db_user.birthDate
    db_user.name = user_update.name or db_user.name
    db_user.gender = user_update.gender or db_user.gender
    db_user.location = user_update.location or db_user.location
    db_user.profile_pic = user_update.profile_pic or db_user.profile_pic

    db.commit()