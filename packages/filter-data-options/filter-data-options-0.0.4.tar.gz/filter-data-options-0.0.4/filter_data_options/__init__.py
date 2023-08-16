import os
import streamlit.components.v1 as components
import streamlit as st

_RELEASE = True

if not _RELEASE:
    _filter_data_options = components.declare_component(
      
        "filter_data_options",
         url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _filter_data_options = components.declare_component("filter_data_options", path=build_dir)

def filter_data_options(data=None, legendData=None, showLegend=False,styles=None, submitBtnName=None, deleteBtnName=None, selectAllBtnName=None, deSelectAllBtnName=None, key=None):

    component_value = _filter_data_options(data=data, legendData=legendData, showLegend=showLegend, styles=styles, submitBtnName=submitBtnName, deleteBtnName=deleteBtnName, selectAllBtnName=selectAllBtnName, deSelectAllBtnName=deSelectAllBtnName, key=key, default=0)

    return component_value


if not _RELEASE:
    import streamlit as st

    data = [
        {"index":0, "category":"Physical Atk", "condition":"greater than", "userSelect":"2000", "add":True, "remove":False, "active":False, "style":{"background-color":"green"}},
        {"index":1, "category":"Defense", "condition":"greater than", "userSelect":"150", "add":True, "remove":False, "active":False, "style":{}},
        {"index":2, "category":"Physical Atk", "condition":"equals", "userSelect":"200", "add":True, "remove":False, "active":False, "style":{}},
        {"index":3, "category":"Movement Speed", "condition":"greater than", "userSelect":"40", "add":True, "remove":False, "active":False, "style":{}},
        {"index":4, "category":"Movement Speed", "condition":"greater than", "userSelect":"40", "add":True, "remove":False, "active":False, "style":{}},
        {"index":5, "category":"Movement Speed", "condition":"greater than", "userSelect":"40", "add":True, "remove":False, "active":False, "style":{}},
    ]

    colorKey = [
        {"index":0, "title":"Primary", "style":{"background-color":"black", "width":"6px", "height":"4px", "padding":"10px", "border-radius":"50%", }, },
        {"index":1, "title":"Secondary", "style":{"background-color":"#ffa9a9", "width":"6px", "height":"4px", "padding":"10px", "border-radius":"50%",  }}
    ]

    submitBtnName = "OPTIMIZE"
    deleteBtnName = "DELETE ALL"
    selectAllBtnName = "SELECT ALL"
    deSelectAllBtnName = "UNSELECT ALL"

    component_res = filter_data_options(data=data, submitBtnName=submitBtnName, deleteBtnName=deleteBtnName, selectAllBtnName=selectAllBtnName, deSelectAllBtnName=deSelectAllBtnName)