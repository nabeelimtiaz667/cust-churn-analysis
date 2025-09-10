import joblib
import numpy as np
from typing import List, Optional, Any
from pydantic import BaseModel


class PredictionInput(BaseModel):
    Contract: str  # "Month-to-month", "One year", "Two year"
    InternetService: str  # "DSL", "Fibre optic", "No"
    MonthlyCharges: float
    tenure: int
    PaymentMethod: int


class PredictionOutput(BaseModel):
    probability: float
    prediction: int
    prediction_label: str  # Added for better interpretation
    features: Optional[Any] = None


class CalibratedModel:
    def __init__(self, model_path: str, binning_transformers_path: str):
        self.model = joblib.load(model_path)
        self.binning_transformers = joblib.load(binning_transformers_path)

    def _transform_features(self, raw_input: PredictionInput):
        """Transform raw input into model features"""
        # Contract encoding (same)
        contract_lower = raw_input.Contract.lower()
        if "month" in contract_lower:
            contract_long = 0
            contract_short = 1
        else:
            contract_long = 1
            contract_short = 0

        internet_lower = raw_input.InternetService.lower()
        if "no" in internet_lower:
            Has_Internet = 0
        else:
            Has_Internet = 1

        # Use the actual transformers for binning
        monthly_bin = (
            self.binning_transformers["monthly_binner"]
            .transform([[raw_input.MonthlyCharges]])[0][0]
            .astype(int)
        )
        tenure_bin = (
            self.binning_transformers["tenure_binner"]
            .transform([[raw_input.tenure]])[0][0]
            .astype(int)
        )

        # Convert bin numbers to one-hot encoding
        monthly_veryhigh = 1 if monthly_bin == 3 else 0
        monthly_medium = 1 if monthly_bin == 1 else 0
        monthly_low = 1 if monthly_bin == 0 else 0

        tenure_veryhigh = 1 if tenure_bin == 3 else 0
        tenure_high = 1 if tenure_bin == 2 else 0
        tenure_low = 1 if tenure_bin == 0 else 0

        return [
            raw_input.PaymentMethod,
            Has_Internet,
            contract_long,
            contract_short,
            monthly_veryhigh,
            monthly_medium,
            monthly_low,
            tenure_veryhigh,
            tenure_high,
            tenure_low,
        ]

    def predict(self, input_data: PredictionInput) -> PredictionOutput:
        # Convert named features to array in the correct order
        features = self._transform_features(input_data)

        # Convert to 2D array for sklearn
        features_array = np.array(features).reshape(1, -1)

        # Get probability
        probability = self.model.predict_proba(features_array)[0, 1]

        # Get prediction (you can adjust threshold if needed)
        prediction = 1 if probability >= 0.5 else 0

        # Get Prediction Label
        prediction_label = "Churn" if prediction == 1 else "No Churn"

        return PredictionOutput(
            probability=float(probability),
            prediction=prediction,
            prediction_label=prediction_label,
            features=features,
        )
