import numpy as np
import gradio as gr
import time

from src.Database import Database
from src.Algorithm import Algorithm

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

database = None


def submit(k_value: int, algorithm: str, agg_function: str, agg_fields: list[str], normalized: bool):
    k_value = int(k_value)

    if not algorithm:
        raise gr.Error("Algorithm must be selected!")

    if not agg_function:
        raise gr.Error("Aggregate function must be selected!")

    if not agg_fields:
        raise gr.Error("Aggregate fields must be selected!")

    if len(agg_fields) < 1:
        raise gr.Error("At least 2 fields must be selected!")

    if k_value < 1:
        raise gr.Error("K must be greater than 0!")

    start_time = time.time()

    if algorithm == "Naive":
        data, access_count = Algorithm.top_k_naive(k_value, agg_function, agg_fields, database, normalized)
    elif algorithm == "Fagin":
        data, access_count = Algorithm.top_k_fagin(k_value, agg_function, agg_fields, database, normalized)
    else:
        raise gr.Error("Invalid algorithm")

    end_time = time.time()
    total_time = f"Time spent: {end_time - start_time:.10f}s"
    access_count = f"Access count: {access_count}"

    return (data, total_time, access_count)


def load_db(csv_select, progress=gr.Progress()):
    global database
    database = Database("data/" + csv_select, progress=progress)
    return {db_label: gr.update(value=csv_select), submit_btn: gr.update(interactive=True)}


with gr.Blocks(css=css, theme=theme) as interface:
    gr.HTML(header)

    gr.Markdown("## Select database")
    with gr.Row().style(equal_height=True):
        with gr.Column(scale=1, min_width=180):
            csv_select = gr.Dropdown(
                label="CSV File",
                info="Select CSV file to load into database",
                choices=["mouse.csv", "test.random.csv"],
                value="mouse.csv",
            )
            db_btn = gr.Button("Load database")

        with gr.Column(scale=1, min_width=180):
            db_label = gr.Textbox(label="Loaded database", readonly=True, placeholder="Nothing loaded yet...", lines=4)

    # Spacer
    gr.HTML("<br/><br/>")

    gr.Markdown("## Select query parameters")
    with gr.Row().style(equal_height=True):
        with gr.Column(scale=1, min_width=180):
            algorithm = gr.Dropdown(
                label="Algorithm",
                info="Algorithm used for querying top-k",
                choices=["Naive", "Fagin"],
                value="Naive",
            )
        with gr.Column(scale=1, min_width=180):
            agg_function = gr.Dropdown(
                label="Aggregation function",
                info="Select aggregation function to use",
                choices=["Min", "Max", "Sum", "Avg"],
                value="Avg",
            )
        with gr.Column(scale=1, min_width=180):
            k_value = gr.Number(label="K", info="Number of top-k results to return", value=10)

        with gr.Column(scale=2):
            agg_fields = gr.CheckboxGroup(
                label="Fields",
                info="Select fields to aggregate",
                choices=["Weight", "Accuracy", "DPI", "Price"],
                value=["Accuracy", "Price"],
            )

    with gr.Row().style(equal_height=True):
        with gr.Column(scale=9):
            submit_btn = gr.Button("Submit", variant="primary", interactive=False)

        with gr.Column(scale=1, min_width=80):
            normalized = gr.Checkbox(label="Normalized", value=False)

    # Spacer
    gr.HTML("<br/><br/>")

    gr.Markdown("## Results")
    output = gr.Matrix(
        datatype=["str", "number", "number", "number", "number", "number"],
        headers=["Name", "Weight", "Accuracy", "DPI", "Price", "Aggregation"],
        row_count=5,
    )
    time_spent = gr.Markdown(f"Time spent: {0:.10f}s")
    access_count = gr.Markdown(f"Access count: {0}")

    db_btn.click(load_db, inputs=csv_select, outputs=[db_label, submit_btn])

    submit_btn.click(
        submit,
        inputs=[k_value, algorithm, agg_function, agg_fields, normalized],
        outputs=[output, time_spent, access_count],
    )


# Only for development to have live-reload using `gradio main.py`
# because it requires entrypoint to be called `demo`
# demo = interface


def main():
    interface.queue()
    interface.launch()

    return
    db = Database("./data/mouse.csv")

    print("\n-------------- [ Sorted by accuracy ] --------------")
    print(*db.get_sorted_accuracy(), sep="\n")

    print("\n-------------- [ Sorted by weight ] --------------")
    print(*db.get_sorted_weight(), sep="\n")

    print("\n-------------- [ Sorted by DPI ] --------------")
    print(*db.get_sorted_dpi(), sep="\n")

    print("\n-------------- [ Sorted by price ] --------------")
    print(*db.get_sorted_price(), sep="\n")
