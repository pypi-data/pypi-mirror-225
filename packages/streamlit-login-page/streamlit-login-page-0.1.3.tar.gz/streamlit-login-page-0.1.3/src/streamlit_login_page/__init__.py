from pathlib import Path
from typing import Optional

import streamlit as st
import streamlit.components.v1 as components

# Tell streamlit that there is a component called streamlit_login_page,
# and that the code to display that component is in the "frontend" folder
frontend_dir = (Path(__file__).parent / "frontend").absolute()
_component_func = components.declare_component(
	"streamlit_login_page", path=str(frontend_dir)
)

# Create the python function that will be called
def streamlit_login_page(
    key: Optional[str] = None,
    height:Optional[int]=830
):
    """
    Add a descriptive docstring
    """
    component_value = _component_func(
        key=key,height=height
    )

    return component_value


def main():
    st.markdown('''
        <style>
        .stApp header{
            display:none;
        }
        .main .block-container{
            max-width: unset;
            padding-left: 5em;
            padding-right: 5em;
            padding-top: 0em;
            padding-bottom: 1em;
            }
        [data-testid="stMetricDelta"] > div:nth-child(2){
            justify-content: center;
        }
        </style>
    ''', unsafe_allow_html=True)

    value = streamlit_login_page()

    st.write(value)


# if __name__ == "__main__":
#     main()
