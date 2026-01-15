from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import  Optional, List, Dict


class Post(BaseModel):
    id: int
    title: str
    body: str


posts = [
    {"id":1, "title":"Post 1", "body":"This is a body text of the Post 1"},
    {"id":2, "title":"Post 2", "body":"This is a body text of the Post 2"},
    {"id":3, "title":"Post 3", "body":"This is a body text of the Post 3"}
]


app = FastAPI()


@app.get("/items")
async def items() -> List[Post]:
    return [Post(**post) for post in posts]


@app.get("/items/{id}")
async def items(id: int) -> Dict:
    for post in posts:
        if post['id'] == id:
            return Post(**post)
    
    raise HTTPException(status_code=404, detail="The post number {id} is not available")


@app.get("/search")
async def search(post_id: Optional[int] = None) -> dict:
    if post_id:
        for post in posts:
            if post["id"] == post_id:
                return post
        raise HTTPException(status_code=404, detail="Post not found")
    else:
        return {"data": "No post provided"}