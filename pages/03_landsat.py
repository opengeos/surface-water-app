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
            description="Start",
            style=style,
            layout=widgets.Layout(padding=padding, width="160px"),
        )
        pre_end_date = widgets.DatePicker(
            description="End",
            style=style,
            layout=widgets.Layout(padding=padding, width="160px"),
        )
        pre_cloud_cover = widgets.IntSlider(
            description="Cloud",
            min=0,
            max=100,
            value=25,
            step=1,
            readout=False,
            style=style,
            layout=widgets.Layout(padding=padding, width="130px"),
        )
        pre_cloud_label = widgets.Label(value=str(pre_cloud_cover.value))
        geemap.jslink_slider_label(pre_cloud_cover, pre_cloud_label)
        pre_widget.children = [
            pre_start_date,
            pre_end_date,
            pre_cloud_cover,
            pre_cloud_label,
        ]
        post_start_date = widgets.DatePicker(
            description="Start",
            style=style,
            layout=widgets.Layout(padding=padding, width="160px"),
        )
        post_end_date = widgets.DatePicker(
            description="End",
            style=style,
            layout=widgets.Layout(padding=padding, width="160px"),
        )
        post_cloud_cover = widgets.IntSlider(
            description="Cloud",
            min=0,
            max=100,
            value=30,
            step=1,
            readout=False,
            style=style,
            layout=widgets.Layout(padding=padding, width="130px"),
        )
        post_cloud_label = widgets.Label(value=str(post_cloud_cover.value))
        geemap.jslink_slider_label(post_cloud_cover, post_cloud_label)
        post_widget.children = [
            post_start_date,
            post_end_date,
            post_cloud_cover,
            post_cloud_label,
        ]

        apply_btn = widgets.Button(description="Apply", layout=layout)
        split_btn = widgets.Button(description="Split", layout=layout)
        reset_btn = widgets.Button(description="Reset", layout=layout)
        close_btn = widgets.Button(description="Close", layout=layout)
        buttons = widgets.HBox([apply_btn, split_btn, reset_btn, close_btn])
        output = widgets.Output()

        widget.children = [pre_widget, post_widget, buttons, output]
        self.add_widget(widget, position=position, **kwargs)

        def apply_btn_click(b):

            if self.user_roi is None:
                output.clear_output()
                output.append_stdout("Please draw a ROI first.")
            elif (
                pre_start_date.value is None
                or pre_end_date.value is None
                or post_start_date.value is None
                or post_end_date.value is None
            ):
                output.clear_output()
                output.append_stdout("Please select start and end dates.")

            elif self.user_roi is not None:
                output.clear_output()
                output.append_stdout("Computing... Please wait.")
                roi = ee.FeatureCollection(self.user_roi)
                pre_col = (
                    ee.ImageCollection("NASA/HLS/HLSL30/v002")
                    .filterBounds(roi)
                    .filterDate(
                        pre_start_date.value.strftime("%Y-%m-%d"),
                        pre_end_date.value.strftime("%Y-%m-%d"),
                    )
                    .filter(ee.Filter.lt("CLOUD_COVERAGE", pre_cloud_cover.value))
                )
                post_col = (
                    ee.ImageCollection("NASA/HLS/HLSL30/v002")
                    .filterBounds(roi)
                    .filterDate(
                        post_start_date.value.strftime("%Y-%m-%d"),
                        post_end_date.value.strftime("%Y-%m-%d"),
                    )
                    .filter(ee.Filter.lt("CLOUD_COVERAGE", post_cloud_cover.value))
                )

                pre_img = pre_col.median().clip(roi)
                post_img = post_col.median().clip(roi)
                vis_params = {"bands": ["B6", "B5", "B4"], "min": 0, "max": 0.4}
                self.add_layer(pre_img, vis_params, "Pre-event Image")
                self.add_layer(post_img, vis_params, "Post-event Image")
                output.clear_output()

        apply_btn.on_click(apply_btn_click)


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
