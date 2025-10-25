from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .schemas import PostCreate, Post
from .service import create_post_service, delete_post_service, create_hashtag_service, get_post_from_post_id_service, get_posts_from_hashtag_service, get_random_posts_service, get_user_posts_service, like_post_service, unlike_post_service,liked_users_post_service
from ..auth.service import get_current_user, existing_user
from ..auth.schemas import User


router = APIRouter(prefix="/posts", tags=["posts"])

#Create Post
@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, token: str, db: Session = Depends(get_db)):
    #Token kontrol
    user = await get_current_user(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Giriş yapmadan bu işlemi gerçekleştiremezsiniz."
        )

    #Post oluşturma
    db_post = await create_post_service(db, post, user.id)

    return db_post

#Get Current User Posts
@router.get("/user", response_model= list[Post])
async def get_current_user_posts(token: str, db: Session = Depends(get_db)):
    #Token kontrol
    user = await get_current_user(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Giriş yapmadan bu işlemi gerçekleştiremezsiniz."
        )
    return await get_user_posts_service(db, user.id)

#Get User Posts
@router.get("/user/{username}", response_model=list[Post])
async def get_user_posts(username: str, db: Session = Depends(get_db)):
    #Token kontrol
    user = await existing_user(db, username, "")

    return await get_user_posts_service(db, user.id)

#Get Posts from Hashtag
@router.get("/hashtag/{hashtag}")
async def get_posts_from_hashtag(hashtag: str, db: Session = Depends(get_db)):
    return await get_posts_from_hashtag_service(db, hashtag)

#Get Random Posts
@router.get("/feed")
async def get_random_posts(page: int=1, limit: int=5, hashtag: str = None, db: Session = Depends(get_db)):
    return await get_random_posts_service(db, page, limit, hashtag)

#Delete Post
@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(token: str, post_id: int, db: Session = Depends(get_db)):
    #Token kontrol
    user = await get_current_user(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Giriş yapmadan bu işlemi gerçekleştiremezsiniz."
        )
    post = await get_post_from_post_id_service(db, post_id)
    if post.author_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bu gönderiyi silmek için yetkiniz yok."
        )
    await delete_post_service(db, post_id)

#Like Post
@router.post("/like", status_code=status.HTTP_204_NO_CONTENT)
async def like_post(post_id: int, username: str, db: Session = Depends(get_db)):
    response, detail =  await like_post_service(db, post_id, username)
    if response == False:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )

#Unlike Post
@router.post("/unlike", status_code=status.HTTP_204_NO_CONTENT)
async def unlike_post(post_id: int, username: str, db: Session = Depends(get_db)):
    response, detail = await unlike_post_service(db, post_id, username)
    if response == False:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )
    
#Users Like Post
@router.get("/likes/{post_id}", response_model=list[User])
async def users_like_post(post_id: int, db: Session = Depends(get_db)):
    return await liked_users_post_service(db, post_id)


#Get Post
@router.get("{post_id}", response_model=Post)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    db_post = await get_post_from_post_id_service(db, post_id)
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Geçersiz Post ID."
        )
    return db_post
