import numpy as np
import gradio as gr
import time

from src.Database import Database

header = """
<div class="header">
    <h1>BI-VWM Semestral Project</h1>
    <h2>Fagin Top-K Algorithm</h2>
    <span>Jan Černý, 2023</span>
</div>
"""

css = """
footer {visibility: hidden;}
.header {text-align: center; padding: 20px;}
"""

theme = gr.themes.Soft(primary_hue=gr.themes.colors.emerald).set(
    block_shadow="0px 0px 5px 0px rgba(0,0,0,0.1)",
    background_fill_primary="#f5f6f7",
)


def submit(algorithm: str, agg_function: str, agg_fields: list[str]):
    if not algorithm or not agg_function or not agg_fields:
        raise gr.Error("Inputs cannot be empty")

    if len(agg_fields) < 2:
        raise gr.Error("At least 2 fields must be selected")

    start_time = time.time()

    # Pause between 1s and 3s to simulate long running query
    time.sleep(np.random.randint(1, 3))

    database = Database("./data/mouse.csv")
    data = {
        "data": [["John", 21, "Male"]],
        "headers": ["Name", "Age", "Gender"],
    }

    end_time = time.time()
    total_time = f"Time spent: {end_time - start_time:.10f}s"

    return (database.as_dict(), total_time)


with gr.Blocks(css=css, theme=theme) as interface:
    gr.HTML(header)

    with gr.Row().style(equal_height=True):
        with gr.Column(scale=1):
            algorithm = gr.Dropdown(
                label="Algorithm",
                info="Algorithm used for querying top-k",
                choices=["Naive", "Fagin"],
                # value="Fagin",
            )
        with gr.Column(scale=1):
            agg_function = gr.Dropdown(
                label="Aggregation function",
                info="Select aggregation function to use",
                choices=["Min", "Max", "Sum"],
                # value="Max",
            )
        with gr.Column(scale=3):
            agg_fields = gr.CheckboxGroup(
                label="Fields",
                info="Select fields to aggregate",
                choices=["Weight", "Accuracy", "DPI", "Price"],
            )

    submit_btn = gr.Button("Submit", variant="primary")

    output = gr.Matrix(
        datatype=["str", "number", "number", "number", "number"],
        headers=["Name", "Weight", "Accuracy", "DPI", "Price"],
        row_count=5,
    )
    time_spent = gr.Markdown(f"Time spent: {0:.10f}s")

    submit_btn.click(
        submit,
        inputs=[algorithm, agg_function, agg_fields],
        outputs=[output, time_spent],
    )


# Only for development to have live-reload using `gradio main.py`
# because it requires entrypoint to be called `demo`
# demo = interface


def main():
    # interface.launch()
    db = Database("./data/mouse.csv")
    print(*db.get_data(), sep="\n")
    print(*db.get_data_sorted(), sep="\n")
    print(*db.get_column_sorted(0), sep="\n")
