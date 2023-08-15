from typing import Union
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

 
# 启动uvicorn服务，默认端口8000
if __name__ == '__main__': 
    uvicorn.run(app='__main__:app', host='0.0.0.0', port=5000, reload=True)