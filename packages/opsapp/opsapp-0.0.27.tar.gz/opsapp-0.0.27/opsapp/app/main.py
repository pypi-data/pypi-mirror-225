# -*- coding: utf-8 -*-
'''
Created on 2020-11-6

@author: zhys513(254851907@qq.com)
'''   
import sys,os 
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from .settings import config 
from .core.response.BaseResponse import UnicornException
from .core.response.http_error import http_error_handler, unicorn_exception_handler
from .core.response.validation_error import http422_error_handler 
from .core.events.events import create_stop_app_handler, create_start_app_handler 
from .core.logging.logging import LoggerFactory 
from .core.router.router import router 
from .core.middleware.middleware import init_middlewares
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
import json,yaml    
from .core.openapi.converter import Converter   

# 初始化应用
application = FastAPI(title=config.PROJECT_NAME, version=config.VERSION, description=config.DESCRIPTION,docs_url=None, redoc_url=None)

@application.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    if config.DOCS == "True":
        return get_swagger_ui_html(
            openapi_url=application.openapi_url,
            title=application.title + " - Swagger UI",
            oauth2_redirect_url=application.swagger_ui_oauth2_redirect_url,
            swagger_js_url=f"/{config.SWAGGER}/swagger-ui-bundle.js",
            swagger_css_url=f"/{config.SWAGGER}/swagger-ui.css",
        )


@application.get(application.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    if config.DOCS == "True":
        return get_swagger_ui_oauth2_redirect_html()
        


@application.get("/redoc", include_in_schema=False)
async def redoc_html():
    if config.DOCS == "True":
        return get_redoc_html(
            openapi_url=application.openapi_url,
            title=application.title + " - ReDoc",
            redoc_js_url=f"/{config.SWAGGER}/redoc.standalone.js",
        ) 
        
# 注入
def get_application() -> FastAPI:
    # Log
    application.state.log = LoggerFactory('log').logger
    # 添加事件
    application.add_event_handler("startup", create_start_app_handler(application))
    application.add_event_handler("shutdown", create_stop_app_handler(application))
    # 中间件
    init_middlewares(application)
    # 路由
    application.include_router(router)
    # 添加错误处理
    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler) 
    application.add_exception_handler(UnicornException, unicorn_exception_handler) 
    # swagger 本地化
    swagger_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)),config.SWAGGER)
    application.mount(f"/{config.SWAGGER}", StaticFiles(directory=swagger_dir), name=f"/{config.SWAGGER}")
    application.openapi_version = "3.0.0"
    return application
    
def create_md_doc():  
    if not os.path.exists(config.STATIC_DIR):
        os.mkdir(config.STATIC_DIR)
        
    openapi = application.openapi()
    openapi_str = json.dumps(openapi, ensure_ascii=False)
    dyaml = yaml.load(openapi_str) 
    dyaml = yaml.dump(dyaml,default_flow_style=False)
    converter = Converter()
    text = converter.convert_content(dyaml)    
    with open(config.MDDOC_DIR, 'w', encoding='utf-8') as out:
        out.write(text)

def get_para(host = "0.0.0.0",port = 5000):
    #create_md_doc()    
    if len(sys.argv) != 1:
        for argv in sys.argv[1:]:
            if argv[:6] == "--port":
                port = int(argv.rsplit("=")[1])
            elif argv[:6] == "--host":
                host = argv.rsplit("=")[1]
    return host,port