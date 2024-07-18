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
        self.add_ee_data()
        self.add_buttons(add_header=True)

    def add_ee_data(self):

        dataset = ee.Image("JRC/GSW1_4/GlobalSurfaceWater")
        image = dataset.select(["occurrence"])
        vis_params = {
            "min": 0.0,
            "max": 100.0,
            "palette": ["ffffff", "ffbbbb", "0000ff"],
        }
        self.addLayer(image, vis_params, "Occurrence")
        self.add_colorbar(
            vis_params, label="Water occurrence (%)", layer_name="Occurrence"
        )

    def add_buttons(self, position="topright", **kwargs):
        widget = widgets.VBox()
        layout = layout = widgets.Layout(width="auto")
        hist_btn = widgets.Button(description="Show histogram", layout=layout)
        bar_btn = widgets.Button(description="Show bar chart", layout=layout)
        reset_btn = widgets.Button(description="Reset", layout=layout)
        scale = widgets.IntSlider(min=30, max=1000, value=90, description="Scale")
        widget.children = [widgets.HBox([hist_btn, bar_btn, reset_btn]), scale]
        self.add_widget(widget, position=position, **kwargs)
        output = widgets.Output()
        self.add_widget(output, position="bottomleft", add_header=False)

        def hist_btn_click(b):
            region = self.user_roi
            if region is not None:
                image = ee.Image("JRC/GSW1_4/GlobalSurfaceWater").select(["occurrence"])
                self.default_style = {"cursor": "wait"}
                hist = geemap.image_histogram(
                    image,
                    region,
                    scale=60,
                    height=350,
                    width=550,
                    x_label="Water Occurrence (%)",
                    y_label="Pixel Count",
                    layout_args={
                        "title": dict(x=0.5),
                        "margin": dict(l=0, r=0, t=10, b=0),
                    },
                    return_df=False,
                )
                output.clear_output()
                with output:
                    display(hist)
                self.default_style = {"cursor": "default"}

        hist_btn.on_click(hist_btn_click)

        def reset_btn_click(b):
            self._draw_control.clear()
            output.clear_output()

        reset_btn.on_click(reset_btn_click)


@solara.component
def Page():
    with solara.Column(style={"min-width": "500px"}):
        Map.element(
            center=[20, -0],
            zoom=2,
            height="800px",
            zoom_ctrl=False,
            measure_ctrl=False,
        )
