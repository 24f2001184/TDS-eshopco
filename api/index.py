from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

df = pd.read_json("telemetry.json")


@app.post("/")
async def latency_metrics(payload: dict):

    regions = payload.get("regions", [])
    threshold = payload.get("threshold_ms", 180)

    result = {}

    for region in regions:

        region_df = df[df["region"] == region]

        if len(region_df) == 0:
            continue

        result[region] = {
            "avg_latency": round(
                float(region_df["latency_ms"].mean()), 2
            ),
            "p95_latency": round(
                float(np.percentile(region_df["latency_ms"], 95)), 2
            ),
            "avg_uptime": round(
                float(region_df["uptime_pct"].mean()), 2
            ),
            "breaches": int(
                (region_df["latency_ms"] > threshold).sum()
            )
        }

    return result
