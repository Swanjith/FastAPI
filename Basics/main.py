try:
    from fastapi import FastAPI, HTTPException
except Exception as e:
    import sys
    print("Missing dependency 'fastapi'. Install with: pip install -r requirements.txt")
    print("Error:", e)
    sys.exit(1)

from pydantic import BaseModel
from logger import logger
from config import settings

# Pass config values when creating the FastAPI app
app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)
# Make settings available via app.state
app.state.settings = settings


@app.on_event("startup")
def startup_event():
    logger.info(
        f"Starting {settings.APP_NAME} (debug={settings.DEBUG}, log_level={settings.LOG_LEVEL})")


class Item(BaseModel):
    text: str
    is_done: bool = False


items: list[Item] = []


@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"message": "Hello World"}


@app.post("/items", response_model=list[Item])
def create_item(item: Item):
    items.append(item)
    logger.debug(f"Item created: {item}")
    return items


@app.get("/items", response_model=list[Item])
def list_items(limit: int | None = None):
    if limit is None:
        limit = settings.DEFAULT_LIMIT
    logger.debug(f"Listing items with limit={limit}")
    return items[0:limit]


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    if item_id < len(items):
        logger.debug(f"Returning item {item_id}")
        return items[item_id]
    logger.warning(f"Item {item_id} not found")
    raise HTTPException(status_code=404, detail="Item not found")


if __name__ == "__main__":
    # Allow running with: python main.py (for local development)
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
