import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------

st.set_page_config(
    page_title="PocketSmart AI",
    page_icon="💰",
    layout="wide"
)

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------

if "expenses" not in st.session_state:
    st.session_state.expenses = []

if "income" not in st.session_state:
    st.session_state.income = 0.0


# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

st.sidebar.title("💰 PocketSmart AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "📊 Spending Insights",
        "🔮 What-If Simulator",
        "🎯 Goal Planner",
        "🤖 AI Money Coach"
    ]
)


# -------------------------------------------------
# DASHBOARD
# -------------------------------------------------

if page == "🏠 Dashboard":

    st.title("💰 PocketSmart AI")
    st.subheader("Smart Budget & Recommendation Assistant")

    st.write(
        "Track your money, understand your spending "
        "and make smarter financial decisions."
    )

    st.divider()

    st.header("💵 Monthly Financial Details")

    income = st.number_input(
        "Monthly Income (₹)",
        min_value=0.0,
        value=float(st.session_state.income),
        step=500.0
    )

    st.session_state.income = income

    st.subheader("➕ Add Expense")

    col1, col2, col3 = st.columns(3)

    with col1:
        category = st.selectbox(
            "Category",
            [
                "Food",
                "Travel",
                "Shopping",
                "Education",
                "Entertainment",
                "Bills",
                "Health",
                "Other"
            ]
        )

    with col2:
        amount = st.number_input(
            "Amount (₹)",
            min_value=0.0,
            step=100.0
        )

    with col3:
        st.write("")
        st.write("")
        add_expense = st.button(
            "➕ Add Expense",
            use_container_width=True
        )

    if add_expense and amount > 0:

        st.session_state.expenses.append({
            "Category": category,
            "Amount": amount
        })

        st.success(
            f"Added ₹{amount:,.0f} to {category}."
        )

    # -------------------------------------------------
    # CALCULATIONS
    # -------------------------------------------------

    total_expenses = sum(
        expense["Amount"]
        for expense in st.session_state.expenses
    )

    balance = income - total_expenses

    if income > 0:
        savings_rate = (balance / income) * 100
    else:
        savings_rate = 0

    st.divider()

    # -------------------------------------------------
    # FINANCIAL SUMMARY
    # -------------------------------------------------

    st.header("📊 Financial Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "💵 Income",
            f"₹{income:,.0f}"
        )

    with col2:
        st.metric(
            "💸 Expenses",
            f"₹{total_expenses:,.0f}"
        )

    with col3:
        st.metric(
            "🏦 Balance",
            f"₹{balance:,.0f}"
        )

    with col4:
        st.metric(
            "📈 Savings Rate",
            f"{savings_rate:.1f}%"
        )

    # -------------------------------------------------
    # EXPENSE HISTORY
    # -------------------------------------------------

    st.divider()

    st.header("📋 Recent Expenses")

    if st.session_state.expenses:

        expense_df = pd.DataFrame(
            st.session_state.expenses
        )

        st.dataframe(
            expense_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No expenses added yet. "
            "Add your first expense above."
        )


# -------------------------------------------------
# SPENDING INSIGHTS
# -------------------------------------------------

elif page == "📊 Spending Insights":

    st.title("📊 Spending Insights")

    if not st.session_state.expenses:

        st.info(
            "Add some expenses from the Dashboard "
            "to see your spending insights."
        )

    else:

        expense_df = pd.DataFrame(
            st.session_state.expenses
        )

        category_totals = (
            expense_df
            .groupby("Category")["Amount"]
            .sum()
            .reset_index()
        )

        total = category_totals["Amount"].sum()

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("🥧 Expense Distribution")

            pie = px.pie(
                category_totals,
                names="Category",
                values="Amount",
                title="Where Your Money Goes"
            )

            st.plotly_chart(
                pie,
                use_container_width=True
            )

        with col2:

            st.subheader("📊 Category Spending")

            bar = px.bar(
                category_totals,
                x="Category",
                y="Amount",
                title="Spending by Category"
            )

            st.plotly_chart(
                bar,
                use_container_width=True
            )

        st.divider()

        st.subheader("🧠 Spending Pattern")

        highest = category_totals.loc[
            category_totals["Amount"].idxmax()
        ]

        percentage = (
            highest["Amount"] / total
        ) * 100

        st.info(
            f"Your highest spending category is "
            f"**{highest['Category']}**, accounting for "
            f"**{percentage:.1f}%** of your expenses."
        )


# -------------------------------------------------
# WHAT-IF SIMULATOR
# -------------------------------------------------

elif page == "🔮 What-If Simulator":

    st.title("🔮 What-If Simulator")

    st.write(
        "Explore how small spending changes could affect "
        "your monthly and yearly savings."
    )

    if not st.session_state.expenses:

        st.info(
            "Add expenses from the Dashboard first."
        )

    else:

        expense_df = pd.DataFrame(
            st.session_state.expenses
        )

        category_totals = (
            expense_df
            .groupby("Category")["Amount"]
            .sum()
        )

        selected_category = st.selectbox(
            "Choose an expense category",
            category_totals.index
        )

        current_amount = category_totals[
            selected_category
        ]

        reduction = st.slider(
            "Reduce this expense by (%)",
            min_value=0,
            max_value=100,
            value=10,
            step=5
        )

        saving = current_amount * (
            reduction / 100
        )

        new_amount = current_amount - saving

        st.divider()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Current Spending",
                f"₹{current_amount:,.0f}"
            )

        with col2:
            st.metric(
                "New Spending",
                f"₹{new_amount:,.0f}"
            )

        with col3:
            st.metric(
                "Monthly Saving",
                f"₹{saving:,.0f}"
            )

        st.success(
            f"💰 Reducing {selected_category} spending "
            f"by {reduction}% could save approximately "
            f"**₹{saving:,.0f} per month**."
        )

        st.info(
            f"📅 Over one year, that could become "
            f"**₹{saving * 12:,.0f}**."
        )


# -------------------------------------------------
# GOAL PLANNER
# -------------------------------------------------

elif page == "🎯 Goal Planner":

    st.title("🎯 Financial Goal Planner")

    st.write(
        "Plan how much you need to save every month "
        "to reach a financial goal."
    )

    col1, col2 = st.columns(2)

    with col1:

        goal_name = st.text_input(
            "Goal Name",
            placeholder="Example: New Laptop"
        )

        target_amount = st.number_input(
            "Target Amount (₹)",
            min_value=0.0,
            step=1000.0
        )

    with col2:

        current_savings = st.number_input(
            "Current Savings (₹)",
            min_value=0.0,
            step=500.0
        )

        months = st.number_input(
            "Target Period (Months)",
            min_value=1,
            value=6,
            step=1
        )

    if target_amount > current_savings:

        remaining = target_amount - current_savings

        monthly_required = remaining / months

        st.divider()

        st.subheader("🎯 Your Goal Plan")

        st.write(
            f"Goal: **{goal_name or 'My Goal'}**"
        )

        st.metric(
            "Amount Remaining",
            f"₹{remaining:,.0f}"
        )

        st.metric(
            "Required Monthly Saving",
            f"₹{monthly_required:,.0f}"
        )

        st.success(
            f"Save approximately **₹{monthly_required:,.0f} "
            f"per month** for {months} months "
            f"to reach your goal."
        )

    elif target_amount > 0:

        st.success(
            "🎉 You have already reached your goal!"
        )


# -------------------------------------------------
# AI MONEY COACH
# -------------------------------------------------

elif page == "🤖 AI Money Coach":

    st.title("🤖 PocketSmart AI Money Coach")

    st.write(
        "Get personalized insights based on your "
        "current financial data."
    )

    if not st.session_state.expenses:

        st.info(
            "Add expenses from the Dashboard first."
        )

    else:

        expense_df = pd.DataFrame(
            st.session_state.expenses
        )

        total_expenses = expense_df["Amount"].sum()

        income = st.session_state.income

        balance = income - total_expenses

        if income > 0:

            savings_rate = (
                balance / income
            ) * 100

        else:

            savings_rate = 0

        st.subheader("🧠 Your Financial Snapshot")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Spending",
                f"₹{total_expenses:,.0f}"
            )

        with col2:
            st.metric(
                "Balance",
                f"₹{balance:,.0f}"
            )

        with col3:
            st.metric(
                "Savings Rate",
                f"{savings_rate:.1f}%"
            )

        st.divider()

        st.subheader("💡 Recommendations")

        if balance < 0:

            st.error(
                "🚨 Your expenses are currently higher "
                "than your income. Review your largest "
                "expense categories."
            )

        elif savings_rate < 10:

            st.warning(
                "💡 Your current savings rate is below 10%. "
                "Try reducing non-essential spending."
            )

        elif savings_rate < 20:

            st.info(
                "📈 Your finances are positive, but you "
                "could increase your savings gradually."
            )

        else:

            st.success(
                "🎉 Your current savings rate is above 20%."
            )

        category_totals = (
            expense_df
            .groupby("Category")["Amount"]
            .sum()
        )

        highest_category = category_totals.idxmax()

        highest_amount = category_totals.max()

        st.info(
            f"🔎 Your largest expense category is "
            f"**{highest_category}** "
            f"with spending of **₹{highest_amount:,.0f}**."
        )