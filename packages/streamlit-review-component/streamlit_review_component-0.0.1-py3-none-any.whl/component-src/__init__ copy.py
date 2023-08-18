import os
import streamlit.components.v1 as components

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = False

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("review_component"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "review_component",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend-react/build")
    _component_func = components.declare_component("review_component", path=build_dir)


# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def review_component(
        name,
        link,
        image_src,
        job_title,
        company,
        review,
        key=None
):
    """Create a new instance of "review_component".

    Parameters
    ----------
    name: str
        The name of the thing we're saying hello to. The component will display
        the text "Hello, {name}!"
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    int
        The number of times the component's "Click Me" button has been clicked.
        (This is the value passed to `Streamlit.setComponentValue` on the
        frontend.)

    """
    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.
    component_value = _component_func(
        name = name,
        link = link,
        image_src = image_src,
        job_title = job_title,
        company = company,
        review = review,
        key=key, 
        default=0
    )

    # We could modify the value returned from the component if we wanted.
    # There's no need to do this in our simple example - but it's an option.
    return component_value


# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run review_component/__init__.py`
if not _RELEASE:

    review_component(
        name="Gokul Prasad",
        link="https://www.linkedin.com/in/gokul-prasad/",
        image_src="https://media.licdn.com/dms/image/D5635AQHJti-G3j2NJw/profile-framedphoto-shrink_800_800/0/1685830341237?e=1692907200&v=beta&t=7lM9xocM05Vd1fa3FpcOg204qzmYjo1fLYIUW2cQF8k",
        job_title="Data Scientist",
        company="AI Camp",
        review="Faculty Finder is an excellent tool, providing an easy-to-use method to interface with the collected data to derive previously-unseen actionable trends. This goes above and beyond what was expected!"
    )

    review_component(
        name="Blake Martin",
        link="https://www.linkedin.com/in/blakemartin314/",
        image_src="https://media.licdn.com/dms/image/D5603AQFvnkpSK6oXuA/profile-displayphoto-shrink_200_200/0/1665723473233?e=1697673600&v=beta&t=v3l9R37hq1Za1i4vZokKbZVja0nPwhnfn1mNw17g5To",
        job_title="Data Scientist",
        company="AI Camp",
        review="The project was impressive, and their victory was undoubtedly well-deserved. They managed to secure a significantly larger number of contacts compared to any other team, showcasing the remarkable effectiveness of their chosen methodology. The interactive data dashboard developed by the team added a commendable touch, with the inclusion of a chatbot feature seamlessly integrated into the dashboard."
    )