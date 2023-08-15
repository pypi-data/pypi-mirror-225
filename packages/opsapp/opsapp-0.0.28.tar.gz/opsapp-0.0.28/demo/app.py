#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import os,sys,random,string
base_dir = os.path.dirname(__file__)
sys.path.append(base_dir) 
from fastapi import APIRouter
from opsapp.app.core.response.BaseResponse import success, fail   
from fastapi import Query, File, UploadFile, Response 
from opsapp.utils.utils import save_file 
from pydantic import BaseModel
from opsapp.app.core.logging.logging import LoggerFactory
from opsapp.app.core.aip import get_prefix_uri   
import numpy as np

logger = LoggerFactory().logger 
router = APIRouter()     
URI,API_PREFIX,VES,PNAME = get_prefix_uri(__file__)
API_SUMMARY = 'DEMO' 
API_TAG = '-'.join([API_SUMMARY,VES])
 
# -------------------- Business --------------------     
 

class Item(BaseModel):
    det_file: str = Query(
        './models/yolox.onnx',
        description="检测模型文件地址",
        deprecated=True
    )
    rec_file: str = Query(
        './models/rec_ocr.onnx',
        description="识别模型文件地址",
        deprecated=True
    ) 
    confthre: float = Query(
        0.25,
        description="检测框的过滤阈值",
        deprecated=True
    )
    nmsthre: float = Query(
        0.65,
        description="NMS的阈值",
        deprecated=True
    ) 
    input_shape: str = Query(
        '640,640',
        description="输入图片大小",
        deprecated=True
    ) 
    bar_code: bool = Query(
        "False",
        description="开启条形码识别，默认关闭",
        deprecated=True
    ) 
   
 
@router.post(API_PREFIX + '_init',tags=[API_TAG], summary='模型初始化')
async def init(item: Item):   
    global det_session , rec_session ,nmsthre,confthre,input_shape,bar_code,lcode
    det_file = item.dict()['det_file'] 
    rec_file = item.dict()['rec_file'] 
    confthre = item.dict()['confthre'] 
    nmsthre = item.dict()['nmsthre'] 
    input_shape = item.dict()['input_shape'] 
    bar_code = item.dict()['bar_code'] 
    result = {} 
    result["det_file"] = det_file
    result["rec_file"] = rec_file
    result["confthre"] = confthre
    result["nmsthre"] = nmsthre
    result["input_shape"] = input_shape
    result["bar_code"] = bar_code
  
    return success(result)  
  