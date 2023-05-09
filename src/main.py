import numpy as np
import gradio as gr
import time

from Database import Database

header = """
        <h1 style="text-align: center">BI-VWM Semestral Project</h1>
        <h2>Fagin Top-K Algorithm</h2>
        <span>Jan Černý, 2023</span>
        """

css = "footer {visibility: hidden}"


def submit():
    start_time = time.time()

    # Pause for 5 seconds to simulate long computation
    # time.sleep(5)
    database = Database("./data/mouse.csv")
    data = {
        "data": [["John", 21, "Male"]],
        "headers": ["Name", "Age", "Gender"],
    }

    end_time = time.time()
    total_time = f"Time spent: {end_time - start_time:.10f}s"

    return (database.as_dict(), total_time)


with gr.Blocks(css=css, theme=gr.themes.Soft(primary_hue=gr.themes.colors.emerald)) as interface:
    gr.HTML(header)

    with gr.Row().style(equal_height=True):
        with gr.Column(scale=1):
            agg_function = gr.Dropdown(
                label="Aggregation function",
                info="Select aggregation function to use",
                choices=["Min", "Max", "Sum"],
            )
        with gr.Column(scale=3):
            agg_fields = gr.CheckboxGroup(
                label="Fields",
                info="Select fields to aggregate",
                choices=["Size", "Price", "Speed", "Weight", "Capacity"],
            )

    submit_btn = gr.Button("Submit", variant="primary")

    output = gr.Matrix(datatype=["str", "number", "number", "number", "number"], type="array")
    time_spent = gr.Markdown(f"Time spent: {0:.10f}s")

    submit_btn.click(
        submit,
        inputs=None,
        outputs=[output, time_spent],
    )


# Only for development to have live-reload using `gradio main.py`
# because it requires entrypoint to be called `demo`
# demo = interface

if __name__ == "__main__":
    # database = Database("./data/mouse.csv")
    interface.launch()
