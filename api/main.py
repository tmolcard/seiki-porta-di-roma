import logging
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from sources.config.experiment import DATA_PATH, SIMULATION_ID
from sources.domain.usecase.generate_visualizations import generate_visualizations
from sources.domain.usecase.get_portion_of_path import get_portion_of_path
from sources.infrastructure.local_filesystem_handler import LocalFilesystemHandler


class Prediction(BaseModel):
    floor: str
    beacon_pairs: list[tuple[str, str]]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "floor": "0",
                    "beacon_pairs": [
                        ["B1", "B3"],
                        ["B2", "B3"],
                        ["B1", "B6"],
                        ["B2", "B6"],
                        ["B4", "B3"],
                        ["B5", "B3"],
                        ["B1", "B1"],
                        ["B2", "B2"],
                        ["B3", "B3"],
                        ["B4", "B4"],
                        ["B5", "B5"],
                        ["B6", "B6"]
                    ]
                }
            ]
        }
    }


app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def root():
    html_content = """
    <html>
        <head>
            <title>API Home</title>
        </head>
        <body>
            <h1>Welcome to your beautiful API</h1>
            <ul>
                <li><a href="/predict">Predict (POST)</a></li>
                <li><a href="/viz">Visualizations (GET)</a></li>
                <li><a href="/docs">Doc</a></li>
            </ul>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.post("/predict")
def predict(prediction: Prediction):
    logging.info(f"Prediction called with parameters: prediction = {prediction}")

    floor = prediction.floor
    beacon_pairs = prediction.beacon_pairs

    if not floor or not beacon_pairs:
        return {"error": "Missing 'floor' or 'beacon_pairs' parameters."}

    local_filesystem_handler = LocalFilesystemHandler(DATA_PATH)

    n_true, total, proportion = get_portion_of_path(
        filesystem_handler=local_filesystem_handler,
        floor=floor,
        beacon_pairs=beacon_pairs,
        simulation_id=SIMULATION_ID
    )

    return {
        "n_true": n_true, "total": total, "proportion": proportion
    }


@app.get("/viz", response_class=HTMLResponse)
def read_items(floor: str = None):
    logging.info(f"Visualization called with parameter: floor = {floor}")
    local_filesystem_handler = LocalFilesystemHandler(DATA_PATH)

    html_content = generate_visualizations(local_filesystem_handler, simulation_id=SIMULATION_ID, floor=floor)

    return HTMLResponse(content=html_content, status_code=200)
