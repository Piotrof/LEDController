from fastapi import APIRouter

router = APIRouter()

@router.get("/hello")
async def say_hello():
    """
    A simple asynchronous endpoint returning a greeting.
    """
    return {"message": "Hello from your async endpoint!"}

@router.get("/items/{item_id}")
async def read_item(item_id: int):
    """
    A simple endpoint that takes a path parameter and returns a mock item.
    """
    return {"item_id": item_id, "item_name": f"Item {item_id}"}
