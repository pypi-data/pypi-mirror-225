"""
路由
""" 
from fastapi import APIRouter,Query
from fastapi.responses import HTMLResponse 
from ...settings import config 
router = APIRouter()

from starlette.responses import RedirectResponse  
# @router.get("/", summary="首页", include_in_schema=False)
# async def root():
#     return RedirectResponse('/docs')

@router.get("/d/{doc}", include_in_schema=False)
async def d(doc):   
    config.DOCS = doc 
    return RedirectResponse('/docs')

@router.get(config.MDDOC_URL, summary="生成 .MD 接口文档", response_class=HTMLResponse)
async def mddoc():   
    with open(config.MDDOC_DIR, 'r', encoding='utf-8') as f: 
        mddoc = f.read()
        return mddoc
