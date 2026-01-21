from fastapi import FastAPI, HTTPException, Form
from pydantic import BaseModel
from typing import  Optional, List, Dict


class User(BaseModel):
    id:int
    name: str
    age: int


class Post(BaseModel):
    id: int
    title: str
    body: str
    author: User


class PostCreate(BaseModel):
    title: str
    body: str
    author_id:int



users = [
    {"id": 1, "name": "John", "age": 25},
    {"id": 2, "name": "Mike", "age": 35},
    {"id": 3, "name": "Flinn", "age": 45}
]

posts = [
    {"id": 1, "title": "Post 1", "body": "This is a body text of the Post 1","author": users[1]},
    {"id": 2, "title": "Post 2", "body": "This is a body text of the Post 2","author": users[0]},
    {"id": 3, "title": "Post 3", "body": "This is a body text of the Post 3","author": users[2]}
]


app = FastAPI()

@app.get("/")
async def index():
    return "This is a homepage"


@app.get("/items")
async def items() -> List[Post]:
    return [Post(**post) for post in posts]


@app.get("/items/{id}")
async def items(id: int) -> Dict:
    for post in posts:
        if post['id'] == id:
            return Post(**post)
    
    raise HTTPException(status_code=404, detail="The post number {id} is not available")

@app.post("/items/add")
async def add_item(post: PostCreate) -> Post:
    author = next((user for user in users if user["id"] == post.author_id) , None)
    if not author:
        raise HTTPException(status_code=404, detail='User not found')
    new_post_id = len(posts) + 1
    new_post = {"id": new_post_id, "title": post.title, "body": post.body, "author": author}
    posts.append(new_post)
    return Post(**new_post)


@app.get("/search")
async def search(post_id: Optional[int] = None) -> dict:
    if post_id:
        for post in posts:
            if post["id"] == post_id:
                return post
        raise HTTPException(status_code=404, detail="Post not found")
    else:
        return {"data": "No post provided"}