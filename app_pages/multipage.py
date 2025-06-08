# app_pages/multipage.py
import streamlit as st


class MultiPage:
    """
    Simple container to register Streamlit page call-backs
    and display them via a sidebar menu.
    """

    def __init__(self, app_name: str = "Multi-Page App") -> None:
        self.pages = {}
        self.app_name = app_name

    # -------- public API --------
    def add_page(self, title: str, func) -> None:
        """Register a page.  *title* is the label shown in the sidebar,
        *func* is the function that draws the page."""
        self.pages[title] = func

    def run(self) -> None:
        st.set_page_config(page_title=self.app_name, layout="wide")
        st.sidebar.title(self.app_name)

        page_name = st.sidebar.radio("Navigation", list(self.pages.keys()))
        # Call the selected page’s draw function
        self.pages[page_name]()
