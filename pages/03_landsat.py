import os
import ee
import geemap
import ipywidgets as widgets
from IPython.display import display
import solara


class Map(geemap.Map):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_basemap("Esri.WorldImagery")
        self.add_gui_widget(add_header=True)

    def add_gui_widget(self, position="topright", **kwargs):

        widget = widgets.VBox(layout=widgets.Layout(padding="0px 5px 0px 5px"))
        pre_widget = widgets.HBox()
        post_widget = widgets.HBox()
        layout = widgets.Layout(width="auto")
        style = {"description_width": "initial"}
        padding = "0px 5px 0px 5px"
        pre_start_date = widgets.DatePicker(
            description="Start", layout=layout, style=style
        )
        pre_end_date = widgets.DatePicker(description="End", layout=layout, style=style)
        pre_cloud_cover = widgets.IntSlider(
            description="Cloud",
            min=0,
            max=100,
            value=25,
            step=1,
            style=style,
            layout=widgets.Layout(padding=padding, width="200px"),
        )
        pre_widget.children = [pre_start_date, pre_end_date, pre_cloud_cover]
        post_start_date = widgets.DatePicker(
            description="Start", layout=layout, style=style
        )
        post_end_date = widgets.DatePicker(
            description="End", layout=layout, style=style
        )
        post_cloud_cover = widgets.IntSlider(
            description="Cloud",
            min=0,
            max=100,
            value=30,
            step=1,
            style=style,
            layout=widgets.Layout(padding=padding, width="200px"),
        )
        post_widget.children = [post_start_date, post_end_date, post_cloud_cover]

        apply_btn = widgets.Button(description="Apply", layout=layout)
        split_btn = widgets.Button(description="Split", layout=layout)
        reset_btn = widgets.Button(description="Reset", layout=layout)
        close_btn = widgets.Button(description="Close", layout=layout)
        buttons = widgets.HBox([apply_btn, split_btn, reset_btn, close_btn])

        widget.children = [pre_widget, post_widget, buttons]
        self.add_widget(widget, position=position, **kwargs)


@solara.component
def Page():
    with solara.Column(style={"min-width": "500px"}):
        Map.element(
            center=[20, -0],
            zoom=2,
            height="750px",
            zoom_ctrl=False,
            measure_ctrl=False,
        )
