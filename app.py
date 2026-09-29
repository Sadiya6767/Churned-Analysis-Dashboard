import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Customer Churn Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")

    # Convert TotalCharges to numeric
    df["TotalCharges"] = pd.to_numeric(
        df["TotalCharges"],
        errors="coerce"
    )

    return df


df = load_data()


# =========================================================
# TITLE
# =========================================================

st.title("📊 Customer Churn Analysis Dashboard")

st.markdown(
    "This dashboard analyzes customer churn patterns based on "
    "contract, internet service, payment method, monthly charges "
    "and customer characteristics."
)


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.header("🔍 Dashboard Filters")

# Contract filter
contract_options = ["All"] + sorted(df["Contract"].dropna().unique().tolist())

selected_contract = st.sidebar.selectbox(
    "Contract",
    contract_options
)


# Internet Service filter
internet_options = ["All"] + sorted(
    df["InternetService"].dropna().unique().tolist()
)

selected_internet = st.sidebar.selectbox(
    "Internet Service",
    internet_options
)


# Payment Method filter
payment_options = ["All"] + sorted(
    df["PaymentMethod"].dropna().unique().tolist()
)

selected_payment = st.sidebar.selectbox(
    "Payment Method",
    payment_options
)


# Senior Citizen filter
senior_options = ["All", "Yes", "No"]

selected_senior = st.sidebar.selectbox(
    "Senior Citizen",
    senior_options
)


# Partner filter
partner_options = ["All", "Yes", "No"]

selected_partner = st.sidebar.selectbox(
    "Partner",
    partner_options
)


# Dependents filter
dependent_options = ["All", "Yes", "No"]

selected_dependent = st.sidebar.selectbox(
    "Dependents",
    dependent_options
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df.copy()


if selected_contract != "All":
    filtered_df = filtered_df[
        filtered_df["Contract"] == selected_contract
    ]


if selected_internet != "All":
    filtered_df = filtered_df[
        filtered_df["InternetService"] == selected_internet
    ]


if selected_payment != "All":
    filtered_df = filtered_df[
        filtered_df["PaymentMethod"] == selected_payment
    ]


if selected_senior != "All":
    senior_value = 1 if selected_senior == "Yes" else 0

    filtered_df = filtered_df[
        filtered_df["SeniorCitizen"] == senior_value
    ]


if selected_partner != "All":
    filtered_df = filtered_df[
        filtered_df["Partner"] == selected_partner
    ]


if selected_dependent != "All":
    filtered_df = filtered_df[
        filtered_df["Dependents"] == selected_dependent
    ]


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_customers = filtered_df["customerID"].nunique()

churned_customers = filtered_df[
    filtered_df["Churn"] == "Yes"
]["customerID"].nunique()


if total_customers > 0:
    churn_rate = (
        churned_customers / total_customers
    ) * 100
else:
    churn_rate = 0


avg_monthly_charges = filtered_df["MonthlyCharges"].mean()


# =========================================================
# KPI CARDS
# =========================================================

st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Total Customers",
        f"{total_customers:,}"
    )


with col2:
    st.metric(
        "Churned Customers",
        f"{churned_customers:,}"
    )


with col3:
    st.metric(
        "Churn Rate",
        f"{churn_rate:.2f}%"
    )


with col4:
    st.metric(
        "Avg Monthly Charges",
        f"${avg_monthly_charges:.2f}"
    )


st.divider()


# =========================================================
# CHURN BY CONTRACT
# =========================================================

st.subheader("📄 Churn by Contract")

contract_churn = pd.crosstab(
    filtered_df["Contract"],
    filtered_df["Churn"],
    normalize="index"
) * 100

fig, ax = plt.subplots(figsize=(8, 4))

contract_churn.plot(
    kind="bar",
    ax=ax
)

ax.set_xlabel("Contract")
ax.set_ylabel("Churn Percentage (%)")
ax.set_title("Churn by Contract")
ax.legend(title="Churn")

plt.xticks(rotation=0)
plt.tight_layout()

st.pyplot(fig)

st.divider()


# =========================================================
# CHURN BY INTERNET SERVICE
# =========================================================

st.subheader("🌐 Churn by Internet Service")

internet_churn = pd.crosstab(
    filtered_df["InternetService"],
    filtered_df["Churn"],
    normalize="index"
) * 100

fig, ax = plt.subplots(figsize=(8, 4))

internet_churn.plot(
    kind="bar",
    ax=ax
)

ax.set_xlabel("Internet Service")
ax.set_ylabel("Churn Percentage (%)")
ax.set_title("Churn by Internet Service")
ax.legend(title="Churn")

plt.xticks(rotation=0)
plt.tight_layout()

st.pyplot(fig)

st.divider()


# =========================================================
# CHURN BY PAYMENT METHOD
# =========================================================

st.subheader("💳 Churn by Payment Method")

payment_churn = pd.crosstab(
    filtered_df["PaymentMethod"],
    filtered_df["Churn"],
    normalize="index"
) * 100

fig, ax = plt.subplots(figsize=(10, 5))

payment_churn.plot(
    kind="bar",
    ax=ax
)

ax.set_xlabel("Payment Method")
ax.set_ylabel("Churn Percentage (%)")
ax.set_title("Churn by Payment Method")
ax.legend(title="Churn")

plt.xticks(rotation=30, ha="right")
plt.tight_layout()

st.pyplot(fig)

st.divider()


# =========================================================
# CHURN BY MONTHLY CHARGES
# =========================================================

st.subheader("💰 Churn by Monthly Charges")

fig, ax = plt.subplots(figsize=(9, 5))

sns.boxplot(
    data=filtered_df,
    x="Churn",
    y="MonthlyCharges",
    ax=ax
)

ax.set_xlabel("Churn")
ax.set_ylabel("Monthly Charges")
ax.set_title("Monthly Charges Distribution by Churn")

plt.tight_layout()

st.pyplot(fig)

st.divider()


# =========================================================
# CHURN BY SENIOR CITIZEN
# =========================================================

st.subheader("👴 Churn by Senior Citizen")

senior_churn = pd.crosstab(
    filtered_df["SeniorCitizen"],
    filtered_df["Churn"],
    normalize="index"
) * 100

senior_churn.index = senior_churn.index.map(
    {0: "No", 1: "Yes"}
)

fig, ax = plt.subplots(figsize=(7, 4))

senior_churn.plot(
    kind="bar",
    ax=ax
)

ax.set_xlabel("Senior Citizen")
ax.set_ylabel("Churn Percentage (%)")
ax.set_title("Churn by Senior Citizen")
ax.legend(title="Churn")

plt.xticks(rotation=0)
plt.tight_layout()

st.pyplot(fig)

st.divider()


# =========================================================
# CHURN BY PARTNER
# =========================================================

st.subheader("👫 Churn by Partner")

partner_churn = pd.crosstab(
    filtered_df["Partner"],
    filtered_df["Churn"],
    normalize="index"
) * 100

fig, ax = plt.subplots(figsize=(7, 4))

partner_churn.plot(
    kind="bar",
    ax=ax
)

ax.set_xlabel("Partner")
ax.set_ylabel("Churn Percentage (%)")
ax.set_title("Churn by Partner")
ax.legend(title="Churn")

plt.xticks(rotation=0)
plt.tight_layout()

st.pyplot(fig)

st.divider()


# =========================================================
# CHURN BY DEPENDENTS
# =========================================================

st.subheader("👨‍👩‍👧 Churn by Dependents")

dependent_churn = pd.crosstab(
    filtered_df["Dependents"],
    filtered_df["Churn"],
    normalize="index"
) * 100

fig, ax = plt.subplots(figsize=(7, 4))

dependent_churn.plot(
    kind="bar",
    ax=ax
)

ax.set_xlabel("Dependents")
ax.set_ylabel("Churn Percentage (%)")
ax.set_title("Churn by Dependents")
ax.legend(title="Churn")

plt.xticks(rotation=0)
plt.tight_layout()

st.pyplot(fig)

st.divider()


# =========================================================
# BUSINESS INSIGHTS
# =========================================================

st.subheader("💡 Business Insights")

st.markdown("""
### Key areas to monitor

- **Contract:** Compare churn percentages across different contract types.
- **Internet Service:** Identify internet service categories with relatively higher churn.
- **Payment Method:** Compare churn behavior across payment methods.
- **Monthly Charges:** Examine whether customers with higher monthly charges show different churn patterns.
- **Senior Citizen:** Compare churn behavior between senior and non-senior customers.
- **Partner:** Compare churn between customers with and without partners.
- **Dependents:** Compare churn between customers with and without dependents.

> Final business recommendations should be based on the actual values observed in the dataset.
""")


# =========================================================
# DATA PREVIEW
# =========================================================

with st.expander("📋 View Filtered Dataset"):
    st.dataframe(
        filtered_df,
        use_container_width=True
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Customer Churn Analysis Dashboard | "
    "Built with Python, Pandas, Matplotlib, Seaborn and Streamlit"
)