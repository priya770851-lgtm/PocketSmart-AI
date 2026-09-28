import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="PocketSmart AI",
    page_icon="💰",
    layout="wide"
)

st.title("💰 PocketSmart AI")
st.subheader("Smart Budget & Recommendation Assistant")

st.write(
    "Manage your income, track expenses, analyze your spending "
    "and get smart recommendations."
)

st.divider()

# Sidebar
st.sidebar.header("💰 Financial Details")

income = st.sidebar.number_input(
    "Enter Monthly Income (₹)",
    min_value=0.0,
    step=500.0
)

st.sidebar.subheader("➕ Add Expense")

expense_category = st.sidebar.selectbox(
    "Expense Category",
    [
        "Food",
        "Travel",
        "Shopping",
        "Education",
        "Entertainment",
        "Bills",
        "Other"
    ]
)

expense_amount = st.sidebar.number_input(
    "Expense Amount (₹)",
    min_value=0.0,
    step=100.0
)

add_expense = st.sidebar.button("Add Expense")

# Store expenses
if "expenses" not in st.session_state:
    st.session_state.expenses = []

if add_expense and expense_amount > 0:
    st.session_state.expenses.append({
        "Category": expense_category,
        "Amount": expense_amount
    })

# Calculate total expenses
total_expenses = sum(
    expense["Amount"]
    for expense in st.session_state.expenses
)

balance = income - total_expenses

# Dashboard
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "💵 Monthly Income",
        f"₹{income:,.0f}"
    )

with col2:
    st.metric(
        "💸 Total Expenses",
        f"₹{total_expenses:,.0f}"
    )

with col3:
    st.metric(
        "🏦 Available Balance",
        f"₹{balance:,.0f}"
    )

st.divider()

# Expense history
st.header("📋 Expense History")

if st.session_state.expenses:

    for i, expense in enumerate(st.session_state.expenses, 1):
        st.write(
            f"**{i}. {expense['Category']}** — "
            f"₹{expense['Amount']:,.0f}"
        )

else:
    st.info(
        "👋 No expenses added yet. "
        "Use the sidebar to add your first expense."
    )

    # Spending Analysis
if st.session_state.expenses:

    st.divider()

    st.header("📊 Spending Analysis")

    # Convert expenses into DataFrame
    expense_df = pd.DataFrame(st.session_state.expenses)

    # Category-wise total
    category_totals = (
        expense_df
        .groupby("Category")["Amount"]
        .sum()
        .reset_index()
    )

    col1, col2 = st.columns(2)

    # Pie Chart
    with col1:
        st.subheader("🥧 Expense Distribution")

        fig = px.pie(
            category_totals,
            names="Category",
            values="Amount",
            title="Where Your Money Goes"
        )

        st.plotly_chart(fig, use_container_width=True)

    # Bar Chart
    with col2:
        st.subheader("📊 Category-wise Spending")

        fig = px.bar(
            category_totals,
            x="Category",
            y="Amount",
            title="Spending by Category"
        )

        st.plotly_chart(fig, use_container_width=True)

    # Spending percentages
    st.subheader("📌 Spending Summary")

    total = category_totals["Amount"].sum()

    for _, row in category_totals.iterrows():

        percentage = (row["Amount"] / total) * 100

        st.write(
            f"**{row['Category']}**: "
            f"₹{row['Amount']:,.0f} "
            f"({percentage:.1f}%)"
        )

# Balance warning
if income > 0 and balance < 0:
    st.error(
        "🚨 Warning! Your expenses are higher than your income."
    )

elif income > 0:
    st.success(
        f"🎉 You have ₹{balance:,.0f} remaining this month."
    )

    # AI Recommendation Engine
if st.session_state.expenses and income > 0:

    st.divider()
    st.header("🤖 PocketSmart AI Recommendations")

    expense_df = pd.DataFrame(st.session_state.expenses)

    category_totals = (
        expense_df
        .groupby("Category")["Amount"]
        .sum()
        .reset_index()
    )

    total_spending = category_totals["Amount"].sum()
    savings = income - total_spending
    savings_percentage = (savings / income) * 100

    # Suggested spending limits
    suggested_limits = {
        "Food": 0.15,
        "Travel": 0.10,
        "Shopping": 0.10,
        "Education": 0.15,
        "Entertainment": 0.10,
        "Bills": 0.20,
        "Other": 0.10
    }

    recommendations = []

    # 1. Analyze every category
    for _, row in category_totals.iterrows():

        category = row["Category"]
        amount = row["Amount"]

        # Get suggested percentage
        suggested_percentage = suggested_limits.get(category, 0.10)

        suggested_budget = income * suggested_percentage

        # Amount above suggested budget
        excess = amount - suggested_budget

        if excess > 0:

            reduction_target = amount * 0.20
            possible_saving = min(reduction_target, excess)

            weekly_limit = suggested_budget / 4

            recommendations.append({
                "category": category,
                "amount": amount,
                "budget": suggested_budget,
                "saving": possible_saving,
                "weekly": weekly_limit,
                "type": "high"
            })

        else:

            recommendations.append({
                "category": category,
                "amount": amount,
                "budget": suggested_budget,
                "saving": 0,
                "weekly": suggested_budget / 4,
                "type": "normal"
            })

    # 2. Display recommendations
    st.subheader("💡 Personalized Suggestions")

    total_possible_saving = 0

    for rec in recommendations:

        category = rec["category"]
        amount = rec["amount"]
        budget = rec["budget"]
        saving = rec["saving"]
        weekly = rec["weekly"]

        if rec["type"] == "high":

            total_possible_saving += saving

            st.warning(
                f"⚠️ **{category} spending is high**\n\n"
                f"You spent **₹{amount:,.0f}**.\n\n"
                f"Suggested monthly budget: **₹{budget:,.0f}**.\n\n"
                f"🎯 Try reducing this expense by around "
                f"**₹{saving:,.0f}**.\n\n"
                f"💰 Possible monthly saving: "
                f"**₹{saving:,.0f}**.\n\n"
                f"📅 Suggested weekly limit: "
                f"**₹{weekly:,.0f}**."
            )

        else:

            st.success(
                f"✅ **{category} spending is within the "
                f"suggested range.**\n\n"
                f"Spent: **₹{amount:,.0f}** | "
                f"Suggested budget: **₹{budget:,.0f}**"
            )

    # 3. Overall savings recommendation
    st.subheader("💰 Savings Analysis")

    if savings_percentage < 10:

        st.error(
            f"🚨 Your current savings rate is only "
            f"**{savings_percentage:.1f}%**.\n\n"
            f"Current savings: **₹{savings:,.0f}**.\n\n"
            f"Try reducing high-spending categories "
            f"and increase your monthly savings."
        )

    elif savings_percentage < 20:

        st.warning(
            f"💡 Your current savings rate is "
            f"**{savings_percentage:.1f}%**.\n\n"
            f"Current savings: **₹{savings:,.0f}**.\n\n"
            f"Consider increasing your savings gradually."
        )

    else:

        st.success(
            f"🎉 Your current savings rate is "
            f"**{savings_percentage:.1f}%**.\n\n"
            f"You are currently saving **₹{savings:,.0f}**."
        )

    # 4. Potential savings
    if total_possible_saving > 0:

        st.info(
            f"🚀 **Potential Improvement**\n\n"
            f"By reducing high-spending categories, "
            f"you could potentially save around "
            f"**₹{total_possible_saving:,.0f} more per month**."
        )