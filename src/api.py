from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from typing import Optional, List

app = FastAPI()

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = "data.csv"
df = pd.read_csv(DATA_PATH)
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")


def apply_filters(
    time_period: Optional[str] = None,
    segment: Optional[str] = None,
    service: Optional[str] = None,
    contract: Optional[str] = None,
):
    data = df.copy()
    # Time period filter (example: Last 30 days = tenure <= 1)
    if time_period:
        if time_period == "Last 30 days":
            data = data[data["tenure"] <= 1]
        elif time_period == "Last 90 days":
            data = data[data["tenure"] <= 3]
        elif time_period == "Last 6 months":
            data = data[data["tenure"] <= 6]
        elif time_period == "Last year":
            data = data[data["tenure"] <= 12]
    # Segment filter
    if segment and segment != "All Segments":
        if segment == "New Customers":
            data = data[data["tenure"] <= 6]
        elif segment == "Long-term Customers":
            data = data[data["tenure"] > 24]
        elif segment == "High-value Customers":
            data = data[data["MonthlyCharges"] > 80]
    # Service filter
    if service and service != "All Services":
        data = data[data["InternetService"] == service]
    # Contract filter
    if contract and contract != "All Contracts":
        data = data[data["Contract"] == contract]
    return data


# Testing route
@app.get("/test")
def test():
    return {"message": "Hello, FastAPI!"}


@app.get("/filters")
def get_filters():
    return {
        "time_periods": ["Last 30 days", "Last 90 days", "Last 6 months", "Last year"],
        "segments": [
            "All Segments",
            "New Customers",
            "Long-term Customers",
            "High-value Customers",
        ],
        "services": ["All Services"]
        + sorted(df["InternetService"].dropna().unique().tolist()),
        "contracts": ["All Contracts"]
        + sorted(df["Contract"].dropna().unique().tolist()),
    }


@app.get("/stats")
def get_stats(
    time_period: Optional[str] = None,
    segment: Optional[str] = None,
    service: Optional[str] = None,
    contract: Optional[str] = None,
):
    data = df.copy()
    data = apply_filters(time_period, segment, service, contract)
    total_customers = len(data)
    churn_rate = round((data["Churn"] == "Yes").mean() * 100, 2)
    avg_monthly = round(data["MonthlyCharges"].mean(), 2)
    avg_tenure = round(data["tenure"].mean(), 1)
    return {
        "total_customers": total_customers,
        "churn_rate": churn_rate,
        "avg_monthly": avg_monthly,
        "avg_tenure": avg_tenure,
    }


@app.get("/chart/{chart_name}")
def get_chart_data(
    chart_name: str,
    time_period: Optional[str] = None,
    segment: Optional[str] = None,
    service: Optional[str] = None,
    contract: Optional[str] = None,
):
    data = df.copy()
    data = apply_filters(time_period, segment, service, contract)
    if chart_name == "churnRate":
        churn_counts = data["Churn"].value_counts()
        return {
            "labels": churn_counts.index.tolist(),
            "values": churn_counts.values.tolist(),
        }
    elif chart_name == "tenureChurn":
        # Calculate churn rate for each tenure month (1-72)
        churn_rates = []
        for tenure in range(1, 73):
            group = data[data["tenure"] == tenure]
            if len(group) == 0:
                churn_rates.append(0)
            else:
                churn_rates.append(round((group["Churn"] == "Yes").mean() * 100, 2))
        return {
            "labels": list(range(1, 73)),
            "values": churn_rates,
        }
    elif chart_name == "genderChurn":
        grouped = data.groupby("gender")["Churn"].value_counts().unstack().fillna(0)
        return {
            "labels": grouped.index.tolist(),
            "churned": grouped.get("Yes", pd.Series([0] * len(grouped))).tolist(),
            "not_churned": grouped.get("No", pd.Series([0] * len(grouped))).tolist(),
        }
    elif chart_name == "seniorChurn":
        grouped = (
            data.groupby("SeniorCitizen")["Churn"].value_counts().unstack().fillna(0)
        )
        labels = ["Not Senior", "Senior"]
        return {
            "labels": labels,
            "churned": grouped.get("Yes", pd.Series([0] * len(grouped))).tolist(),
            "not_churned": grouped.get("No", pd.Series([0] * len(grouped))).tolist(),
        }
    elif chart_name == "partnerChurn":
        grouped = data.groupby("Partner")["Churn"].value_counts().unstack().fillna(0)
        labels = grouped.index.tolist()
        churned = grouped["Yes"].tolist() if "Yes" in grouped else [0] * len(labels)
        not_churned = grouped["No"].tolist() if "No" in grouped else [0] * len(labels)
        return {
            "labels": labels,
            "churned": churned,
            "not_churned": not_churned,
        }
    elif chart_name == "dependentsChurn":
        grouped = data.groupby("Dependents")["Churn"].value_counts().unstack().fillna(0)
        labels = grouped.index.tolist()
        churned = grouped["Yes"].tolist() if "Yes" in grouped else [0] * len(labels)
        not_churned = grouped["No"].tolist() if "No" in grouped else [0] * len(labels)
        return {
            "labels": labels,
            "churned": churned,
            "not_churned": not_churned,
        }
    elif chart_name == "internetChurn":
        grouped = (
            data.groupby("InternetService")["Churn"].value_counts().unstack().fillna(0)
        )
        labels = grouped.index.tolist()
        churned = grouped["Yes"].tolist() if "Yes" in grouped else [0] * len(labels)
        not_churned = grouped["No"].tolist() if "No" in grouped else [0] * len(labels)
        return {
            "labels": labels,
            "churned": churned,
            "not_churned": not_churned,
        }
    elif chart_name == "contractChurn":
        grouped = data.groupby("Contract")["Churn"].value_counts().unstack().fillna(0)
        labels = grouped.index.tolist()
        churned = grouped["Yes"].tolist() if "Yes" in grouped else [0] * len(labels)
        not_churned = grouped["No"].tolist() if "No" in grouped else [0] * len(labels)
        return {
            "labels": labels,
            "churned": churned,
            "not_churned": not_churned,
        }
    elif chart_name == "paymentChurn":
        grouped = (
            data.groupby("PaymentMethod")["Churn"].value_counts().unstack().fillna(0)
        )
        labels = grouped.index.tolist()
        churned = grouped["Yes"].tolist() if "Yes" in grouped else [0] * len(labels)
        not_churned = grouped["No"].tolist() if "No" in grouped else [0] * len(labels)
        return {
            "labels": labels,
            "churned": churned,
            "not_churned": not_churned,
        }
    elif chart_name == "phoneChurn":
        grouped = (
            data.groupby("PhoneService")["Churn"].value_counts().unstack().fillna(0)
        )
        labels = grouped.index.tolist()
        churned = grouped["Yes"].tolist() if "Yes" in grouped else [0] * len(labels)
        not_churned = grouped["No"].tolist() if "No" in grouped else [0] * len(labels)
        return {
            "labels": labels,
            "churned": churned,
            "not_churned": not_churned,
        }
    elif chart_name == "monthlyChargesDist":
        bins = [20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
        labels = [f"{bins[i]}-{bins[i+1]}" for i in range(len(bins) - 1)]
        churned = []
        not_churned = []
        for i in range(len(bins) - 1):
            group = data[
                (data["MonthlyCharges"] >= bins[i])
                & (data["MonthlyCharges"] < bins[i + 1])
            ]
            churned.append(len(group[group["Churn"] == "Yes"]))
            not_churned.append(len(group[group["Churn"] == "No"]))
        return {
            "labels": labels,
            "churned": churned,
            "not_churned": not_churned,
        }
    elif chart_name == "totalChargesDist":
        bins = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 999999]
        labels = [
            f"{bins[i]}-{bins[i+1]}" if bins[i + 1] != 999999 else "8000+"
            for i in range(len(bins) - 1)
        ]
        churned = []
        not_churned = []
        for i in range(len(bins) - 1):
            group = data[
                (data["TotalCharges"] >= bins[i]) & (data["TotalCharges"] < bins[i + 1])
            ]
            churned.append(len(group[group["Churn"] == "Yes"]))
            not_churned.append(len(group[group["Churn"] == "No"]))
        return {
            "labels": labels,
            "churned": churned,
            "not_churned": not_churned,
        }
    elif chart_name == "monthlyGroupsChurn":
        bins = [20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
        labels = [f"{bins[i]}-{bins[i+1]}" for i in range(len(bins) - 1)]
        churn_rates = []
        for i in range(len(bins) - 1):
            group = data[
                (data["MonthlyCharges"] >= bins[i])
                & (data["MonthlyCharges"] < bins[i + 1])
            ]
            if len(group) == 0:
                churn_rates.append(0)
            else:
                churn_rates.append(round((group["Churn"] == "Yes").mean() * 100, 2))
        return {
            "labels": labels,
            "values": churn_rates,
        }
    return {}


# Add similar endpoints for other charts as needed
