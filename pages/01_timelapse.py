import os
import ee
import geemap
import ipywidgets as widgets
from IPython.display import display
import solara


class Map(geemap.Map):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        url = "https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}"
        self.add_tile_layer(url, name="Google Satellite", attribution="Google")
        self.add_gui("timelapse", basemap=None)


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
