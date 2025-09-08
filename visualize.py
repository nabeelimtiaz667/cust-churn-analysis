import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QLabel,
    QTabWidget,
    QGridLayout,
    QScrollArea,
)
from PyQt5.QtCore import Qt
import numpy as np
from PyQt5.QtCore import Qt
import numpy as np


class ChurnAnalysisApp(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Customer Churn Analysis Dashboard")
        self.setGeometry(100, 100, 1200, 800)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create tabs
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Create different analysis tabs
        self.create_overview_tab()
        self.create_demographic_tab()
        self.create_service_tab()
        self.create_financial_tab()

        self.show()

    def create_overview_tab(self):
        overview_tab = QWidget()
        layout = QVBoxLayout(overview_tab)

        # Overall churn rate
        fig1 = plt.figure(figsize=(10, 5))
        churn_counts = self.data["Churn"].value_counts()
        plt.pie(
            churn_counts, labels=churn_counts.index, autopct="%1.1f%%", startangle=90
        )
        plt.title("Overall Churn Rate")
        canvas1 = FigureCanvas(fig1)

        # Churn by tenure
        fig2 = plt.figure(figsize=(10, 5))
        tenure_churn = self.data.groupby("tenure")["Churn"].apply(
            lambda x: (x == "Yes").mean() * 100
        )
        plt.plot(tenure_churn.index, tenure_churn.values)
        plt.xlabel("Tenure (months)")
        plt.ylabel("Churn Rate (%)")
        plt.title("Churn Rate by Tenure")
        plt.grid(True)
        canvas2 = FigureCanvas(fig2)

        # Add to layout
        layout.addWidget(canvas1)
        layout.addWidget(canvas2)

        self.tabs.addTab(overview_tab, "Overview")

    def create_demographic_tab(self):
        demographic_tab = QWidget()
        layout = QGridLayout(demographic_tab)

        # Churn by gender
        fig1 = plt.figure(figsize=(6, 4))
        gender_churn = self.data.groupby("gender")["Churn"].value_counts().unstack()
        gender_churn.plot(kind="bar", ax=plt.gca())
        plt.title("Churn by Gender")
        plt.ylabel("Count")
        plt.xticks(rotation=0)
        canvas1 = FigureCanvas(fig1)

        # Churn by senior citizen
        fig2 = plt.figure(figsize=(6, 4))
        senior_churn = (
            self.data.groupby("SeniorCitizen")["Churn"].value_counts().unstack()
        )
        senior_churn.plot(kind="bar", ax=plt.gca())
        plt.title("Churn by Senior Citizen Status")
        plt.ylabel("Count")
        plt.xticks([0, 1], ["Not Senior", "Senior"], rotation=0)
        canvas2 = FigureCanvas(fig2)

        # Churn by partner
        fig3 = plt.figure(figsize=(6, 4))
        partner_churn = self.data.groupby("Partner")["Churn"].value_counts().unstack()
        partner_churn.plot(kind="bar", ax=plt.gca())
        plt.title("Churn by Partner Status")
        plt.ylabel("Count")
        plt.xticks(rotation=0)
        canvas3 = FigureCanvas(fig3)

        # Churn by dependents
        fig4 = plt.figure(figsize=(6, 4))
        dependents_churn = (
            self.data.groupby("Dependents")["Churn"].value_counts().unstack()
        )
        dependents_churn.plot(kind="bar", ax=plt.gca())
        plt.title("Churn by Dependents")
        plt.ylabel("Count")
        plt.xticks(rotation=0)
        canvas4 = FigureCanvas(fig4)

        # Add to grid layout
        layout.addWidget(canvas1, 0, 0)
        layout.addWidget(canvas2, 0, 1)
        layout.addWidget(canvas3, 1, 0)
        layout.addWidget(canvas4, 1, 1)

        self.tabs.addTab(demographic_tab, "Demographics")

    def create_service_tab(self):
        # Make the tab scrollable
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        inner_widget = QWidget()
        layout = QGridLayout(inner_widget)
        # Set a minimum size for the inner widget to force scrolling
        inner_widget.setMinimumSize(1000, 1600)
        scroll_area.setMinimumSize(1000, 600)

        # Internet service vs churn
        fig1 = plt.figure(figsize=(6, 4))
        internet_churn = (
            self.data.groupby("InternetService")["Churn"].value_counts().unstack()
        )
        internet_churn.plot(kind="bar", ax=plt.gca())
        plt.title("Churn by Internet Service Type")
        plt.ylabel("Count")
        plt.xticks(rotation=0)
        canvas1 = FigureCanvas(fig1)

        # Contract type vs churn
        fig2 = plt.figure(figsize=(6, 4))
        contract_churn = self.data.groupby("Contract")["Churn"].value_counts().unstack()
        contract_churn.plot(kind="bar", ax=plt.gca())
        plt.title("Churn by Contract Type")
        plt.ylabel("Count")
        plt.xticks(rotation=0)
        canvas2 = FigureCanvas(fig2)

        # Payment method vs churn
        fig3 = plt.figure(figsize=(8, 5))
        payment_churn = (
            self.data.groupby("PaymentMethod")["Churn"].value_counts().unstack()
        )
        payment_churn.plot(kind="bar", ax=plt.gca())
        plt.title("Churn by Payment Method")
        plt.ylabel("Count")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        canvas3 = FigureCanvas(fig3)

        # Phone service vs churn
        fig4 = plt.figure(figsize=(6, 4))
        phone_churn = (
            self.data.groupby("PhoneService")["Churn"].value_counts().unstack()
        )
        phone_churn.plot(kind="bar", ax=plt.gca())
        plt.title("Churn by Phone Service")
        plt.ylabel("Count")
        plt.xticks(rotation=0)
        canvas4 = FigureCanvas(fig4)

        # Center-align the last widget (canvas4)

        center_widget = QWidget()
        center_layout = QHBoxLayout(center_widget)
        center_layout.addStretch(1)
        center_layout.addWidget(canvas4)
        center_layout.addStretch(1)

        # Add to grid layout
        layout.addWidget(canvas1, 0, 0)
        layout.addWidget(canvas2, 0, 1)
        layout.addWidget(canvas3, 1, 0, 1, 2)
        layout.addWidget(center_widget, 3, 0, 1, 2)

        scroll_area.setWidget(inner_widget)
        self.tabs.addTab(scroll_area, "Services")

    def create_financial_tab(self):
        financial_tab = QWidget()
        layout = QVBoxLayout(financial_tab)

        # Monthly charges distribution
        fig1 = plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        churn_yes = self.data[self.data["Churn"] == "Yes"]["MonthlyCharges"]
        churn_no = self.data[self.data["Churn"] == "No"]["MonthlyCharges"]
        plt.hist(
            [churn_yes, churn_no], bins=20, label=["Churned", "Not Churned"], alpha=0.7
        )
        plt.xlabel("Monthly Charges")
        plt.ylabel("Frequency")
        plt.title("Monthly Charges Distribution")
        plt.legend()

        # Total charges distribution
        plt.subplot(1, 2, 2)
        # Convert TotalCharges to numeric, handling empty strings
        self.data["TotalCharges"] = pd.to_numeric(
            self.data["TotalCharges"], errors="coerce"
        )
        churn_yes_total = self.data[self.data["Churn"] == "Yes"][
            "TotalCharges"
        ].dropna()
        churn_no_total = self.data[self.data["Churn"] == "No"]["TotalCharges"].dropna()
        plt.hist(
            [churn_yes_total, churn_no_total],
            bins=20,
            label=["Churned", "Not Churned"],
            alpha=0.7,
        )
        plt.xlabel("Total Charges")
        plt.ylabel("Frequency")
        plt.title("Total Charges Distribution")
        plt.legend()

        canvas1 = FigureCanvas(fig1)

        # Monthly charges vs churn rate
        fig2 = plt.figure(figsize=(10, 5))
        self.data["MonthlyChargesGroup"] = pd.cut(self.data["MonthlyCharges"], bins=10)
        monthly_churn_rate = self.data.groupby("MonthlyChargesGroup")["Churn"].apply(
            lambda x: (x == "Yes").mean() * 100
        )
        plt.bar(range(len(monthly_churn_rate)), monthly_churn_rate.values)
        plt.xlabel("Monthly Charges Groups")
        plt.ylabel("Churn Rate (%)")
        plt.title("Churn Rate by Monthly Charges Groups")
        plt.xticks(
            range(len(monthly_churn_rate)),
            [
                f"${int(interval.left)}-${int(interval.right)}"
                for interval in monthly_churn_rate.index
            ],
            rotation=45,
            ha="right",
        )
        canvas2 = FigureCanvas(fig2)

        layout.addWidget(canvas1)
        layout.addWidget(canvas2)

        self.tabs.addTab(financial_tab, "Financials")


def main():
    # Load and preprocess data
    data = pd.read_csv("customer-churn-table.csv.csv")

    # Convert TotalCharges to numeric, handling empty strings
    data["TotalCharges"] = pd.to_numeric(data["TotalCharges"], errors="coerce")
    data["TotalCharges"] = data["TotalCharges"].dropna()

    # Launch the application
    app = QApplication(sys.argv)
    ex = ChurnAnalysisApp(data)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
