import os
import streamlit.components.v1 as components

_RELEASE = True
COMPONENT_NAME = 'review_component'

if not _RELEASE:
    _component_func = components.declare_component(
        COMPONENT_NAME,
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component(COMPONENT_NAME, path=build_dir)

def review_component(key=None, *args, **kwargs):
    component_value = _component_func(key=key, *args, **kwargs)
    return component_value

# app: `$ streamlit run review_component/__init__.py`
if not _RELEASE:
    review_component(
        name = "Person Name",
        image_src = "https://media.gettyimages.com/id/1198530320/vector/vector-illustration-of-panda-isolated-on-white-background.jpg?s=2048x2048&w=gi&k=20&c=r1yD-QUKrM4lrMgdGXPZlaEcw7tRv--IWpVunXGxGRU=",
        job_title = "Job Title",
        company = "Company Name",
        review = """
        Lorem ipsum dolor sit amet consectetur, adipisicing elit. 
        Id eum eaque esse saepe provident laudantium soluta dolore. 
        Alias a porro quis ut consectetur dolorum illum impedit, ullam voluptatum illo voluptate.
        """
    )
