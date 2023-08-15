# -*- coding: utf-8 -*-
import os
from ...settings import config

def get_prefix_uri(_file_,pre = config.API_PREFIX):
    basename = os.path.basename(_file_)
    pname = os.path.splitext(basename)[0]
    ves = os.path.abspath(os.path.dirname(_file_)).split('/')[-1].split('\\')[-1]
    uri = '/'.join([pre,ves,pname]) 
    uri_not_pre = '/'.join(['',ves,pname]) 
    return uri,uri_not_pre,ves,pname