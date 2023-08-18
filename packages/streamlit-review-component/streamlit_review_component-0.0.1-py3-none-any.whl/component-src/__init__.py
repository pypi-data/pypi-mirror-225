import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        name="review_component",
        url="http://localhost:3001"
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend-react/build")
    _component_func = components.declare_component("review_component", path=build_dir)


if not _RELEASE:

    def review_component(key=None, *args, **kwargs):
        return _component_func(
            key=key,
            *args, 
            **kwargs
        )

    review_component(
        name="Name",
        image_src="https://cdn.vectorstock.com/i/1000x1000/67/33/flat-square-icon-of-a-cute-giant-panda-vector-1886733.webp",
        job_title="Job Title",
        company="Company",
        review="Lorem ipsum dolor sit amet consectetur, adipisicing elit. Nisi, exercitationem rerum quisquam voluptatum ea facere suscipit officiis at sit facilis veniam sint iusto, et in aperiam tempora expedita quia illo."
    )