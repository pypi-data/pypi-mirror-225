import os
import streamlit.components.v1 as components
import json

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "dilum_sentiment_basic",
        url="http://localhost:5173",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("dilum_sentiment_basic", path=build_dir)

def dilum_sentiment_basic(data, key=None):
    component_value = _component_func(data=data, key=key, default=0)
    return component_value

if not _RELEASE:
    import streamlit as st
    jsonData = """
                [
                {
                    "label": "positive",
                    "score": 0.4012986421585083
                },
                {
                    "label": "neutral",
                    "score": 0.37312614917755127
                },
                {
                    "label": "negative",
                    "score": 0.22557520866394043
                }
                ]
                """

    dictData= json.loads(jsonData)

    userText = dilum_sentiment_basic(dictData)
    if isinstance(userText, str):
        st.text('Text value is '+ userText)