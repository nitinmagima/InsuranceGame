import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import json

st.set_page_config(
    page_title="Agricultural Insurance Simulation Game",
    page_icon="🌾",
)

# Set up the Streamlit app
st.title("Welcome to the Agricultural Insurance Simulation Game! 🌾")

import streamlit as st

st.markdown(
    """
    Embark on an interactive journey that explores the fascinating dynamics of farming, risk management, and climate change. Here's what awaits you:  

    - **The Farming Challenge**  
      Customize your farming setup by choosing seed types, insurance options, and return periods for extreme weather. Experiment with different strategies to find the perfect balance between risk and reward!  

    - **Racing Through Farming Strategies**  
      Once you've completed the farming challenge here, head over to the **Racing Through Farming Strategies** page to understand how your decisions compare to others under various weather conditions!  

    - **The Science Behind the Game**  
      Explore the **The Science Behind the Game** page to dive into the real-world implications of risk and insurance in agriculture. Learn how disasters and return periods affect farming strategies and profitability.  

    - **Customize Your Farming Adventure**  
      Visit the **Customize Your Farming Adventure** page to take control of the simulation. Adjust costs, revenues, and other parameters to explore how various factors impact farming outcomes.  
    """
)


# Collapsible Welcome Message
with st.expander("**Instructions!**", expanded=False):
    st.markdown("""
    
    ### 🌟 **How to Play** 🌾
    
    Step into the shoes of a farmer and navigate the exciting world of agriculture, where your decisions can lead to bountiful harvests or challenging seasons. This interactive experience lets you balance potential profits against the unpredictable forces of nature.

    **How to Play:**
    
    Make your decisions using the options below. 

    1. **Choose Your Seeds** - Decide between traditional seeds (lower cost, standard yield) or high-quality seeds (higher cost, requires a loan, but offers greater potential).

    2. **Decide on Insurance** - Will you safeguard your crops with insurance or take the risk without it?

    3. **Understand how often disasters like droughts or floods might strike your farm.**

    4. **Run the Simulation!**

    ### 🧩 **Your Goal**  

    Navigate the challenges of farming by balancing risk and reward! Will you prioritize safety, take bold risks, or find the perfect strategy? The choice is yours. 
    
    Run multiple simulations to test strategies, adapt to challenges, and discover the best approach to thrive in any condition! Each simulation represents one farming season, where you test your chosen strategy against the unpredictability of weather conditions and market dynamics to evaluate how well your decisions balance risk, reward, and profitability. Running multiple simulations allows you to observe how your chosen strategy performs over time, under varying weather conditions, and helps you identify patterns, strengths, and weaknesses in your approach, ultimately aiding in refining your decision-making for long-term success. 
    
    **Farming Personas**
    - 👩‍🌾 Traditional Farmer (Traditional Seeds With No Insurance)
    - 👨‍🌾 Traditional Farmer (Traditional Seeds With Insurance)
    - 🌾 High-Risk Taker (High-Quality Seeds With No Insurance)
    - 💼 Strategic Planner (High-Quality Seeds With Insurance)
    
    Good luck, and may your crops grow tall! 🌱
    """)

# Initialize session state variables with default values if they don't exist
# --- Default Parameters ---
# Load configuration from JSON file
def load_config(file_path="config.json"):
    with open(file_path, "r") as file:
        return json.load(file)

# Load default parameters from the config file
default_params = load_config()

for key, value in default_params.items():
    if key not in st.session_state:
        st.session_state[key] = value


# --- Farming Parameters ---
# Load parameters into a DataFrame
parameters_df = pd.DataFrame([
    {
        "Setting": "Traditional Seed Cost",
        "Value": f"${st.session_state['traditional_seed_cost']}"
    },
    {
        "Setting": "High Quality Seed Cost",
        "Value": f"${st.session_state['high_quality_seed_cost']}"
    },
    {
        "Setting": "Traditional Yield Revenue",
        "Value": f"${st.session_state['traditional_yield_revenue']}"
    },
    {
        "Setting": "High Quality Yield Revenue",
        "Value": f"${st.session_state['high_quality_yield_revenue']}"
    },
    {
        "Setting": "Insurance Payout",
        "Value": f"${st.session_state['insurance_payout']}"
    },
    {
        "Setting": "Insurance Premium",
        "Value": f"${st.session_state['insurance_premium']}"
    },
    {
        "Setting": "Loan Interest Rate (%)",
        "Value": f"{st.session_state['loan_interest_rate']}%"
    }
])

# User Instructions and Inputs
with st.expander("**Make your Decisions!**", expanded=False):
    st.markdown("""

        ### 🚜 **Ready to embark on this farming adventure? Make your choices and see if you can beat the odds!**

        To assist you in making informed decisions, refer to the table below, which outlines the costs and revenues associated with different seed types and insurance options. To change these default values for the simulations, please visit the **Customize Your Farming Adventure** page.
        """)

    st.markdown("""
        **Here are the current farming costs and revenues for your simulations:**  
    """)

    # Convert parameters DataFrame to a markdown-styled table
    styled_parameters = parameters_df.to_markdown(index=False, tablefmt="pretty")
    st.markdown(f"```\n{styled_parameters}\n```")

    # User inputs
    seed_type = st.selectbox(
        "**Choose Seed Type:**",
        ("Traditional", "High Quality"),
        help="Pick 'Traditional' for a safe bet with lower costs, or go big with 'High Quality', it—requires a loan but it comes with the promise of bigger yields! 🌽💪"
    )

    # Display loan information if High Quality seeds are selected
    if seed_type == "High Quality":
        st.markdown("**Note:** High Quality seeds require a loan.")
        st.markdown(f"**Loan Interest Rate:** {st.session_state['loan_interest_rate']}%")

    st.divider()

    # Checkbox for purchasing insurance
    purchase_insurance = st.checkbox(
        "**Will you invest in insurance to safeguard your crops against unforeseen events?**",
        help=(
            "Protect your crops or take a risk and see if not taking insurance is worth the gamble this season! 🌦️\n\n"
            "**Premium**: The amount you pay to obtain a crop insurance policy.\n\n"
            "**Payout**: The compensation you receive from the insurance provider if your crops suffer losses due to covered events."
        )
    )

    # If insurance is purchased, use the insurance premium from session state
    if purchase_insurance:
        insurance_premium = st.session_state['insurance_premium']
        insurance_payout = st.session_state['insurance_payout']
        st.markdown(
            f"""
            You've secured your crops with insurance!  
            **Premium:** `${insurance_premium}`  
            **Payout:** `${insurance_payout}` 🌦️✅
            """
        )
    else:
        insurance_premium = 0.0
        st.markdown(f"No safety net this season—you're farming without insurance! 😨")

    st.divider()

    # Define return period options
    return_period_options = [
        ("Once in 2 years (50% chance per year)", 50),
        ("Once in 5 years (20% chance per year)", 20),
        ("Once in 10 years (10% chance per year)", 10),
        ("Once in 20 years (5% chance per year)", 5),
        ("Once in 50 years (2% chance per year)", 2),
        ("Once in 100 years (1% chance per year)", 1)
    ]

    # Create a dictionary for easy lookup
    return_period_dict = {label: prob for label, prob in return_period_options}

    # Select return period
    selected_return_period = st.selectbox(
        "**Select Return Period for Extreme Weather Events:**",
        list(return_period_dict.keys()),
        help="""
        🌪️ **How Often Do Extreme Weather Events (Disasters) Strike?**  
        Extreme weather or a disaster is described as “once in N years.” For instance, a 1-in-5-year drought means a **20% chance** of it happening each year.  

        But here's the twist: a 20% chance doesn't mean it won't happen back-to-back—nature loves surprises! Similarly, a "1-in-100-year" disaster doesn't wait a century to occur. It has a **1% chance** of happening every single year, no matter when it last occurred.  
        Plan wisely and expect the unexpected! 🌦️
        """
    )


# Calculate the probability of a bad year
bad_year_probability = return_period_dict[selected_return_period] / 100
normal_year_probability = 1 - bad_year_probability


# Initialize session state to store simulation history
if 'simulation_history' not in st.session_state:
    st.session_state['simulation_history'] = []

# Function to simulate a single season
def simulate_season():
    # Determine the type of year (Normal or Bad) based on probabilities
    year_type = np.random.choice(
        ["Normal", "Bad"],  # Possible outcomes
        p=[normal_year_probability, bad_year_probability]  # Probabilities for each outcome
    )

    # Calculate costs and revenue based on the chosen seed type
    if seed_type == "Traditional":
        # For traditional seeds, cost is fixed, and revenue depends on the year type
        costs = st.session_state['traditional_seed_cost']
        revenue = st.session_state['traditional_yield_revenue'] if year_type == "Normal" else 0
    else:
        # For high-quality seeds, include the loan interest in the cost
        costs = st.session_state['high_quality_seed_cost'] * (1 + st.session_state['loan_interest_rate'] / 100)
        # Revenue depends on the year type
        revenue = st.session_state['high_quality_yield_revenue'] if year_type == "Normal" else 0

    # Adjust costs and revenue if the year is "Bad" and insurance is purchased
    if year_type == "Bad" and purchase_insurance:
        revenue += st.session_state['insurance_payout']  # Add insurance payout to revenue
        costs += insurance_premium  # Add insurance premium to costs
    elif purchase_insurance:
        costs += insurance_premium  # Add insurance premium even if the year is not "Bad"

    # Calculate net profit
    profit = revenue - costs

    # Append results to simulation history
    st.session_state['simulation_history'].append({
        "Year Type": year_type,
        "Revenue": round(revenue, 2),
        "Costs": round(costs, 2),
        "Net Profit": round(profit, 2)
    })

    # Return the results of the simulation
    return year_type, revenue, costs, profit

st.markdown("""
    **Run Simulation**: Click the 'Run Simulation' button to simulate the farming season and view your financial outcomes.
    """)

# Function to reset simulation history
def reset_simulation_history():
    st.session_state['simulation_history'] = []
    if "simulation_result" in st.session_state:
        del st.session_state["simulation_result"]  # Clear the simulation result
    st.success("Simulation history has been reset. Start fresh and simulate again!")


# Function to display the reset confirmation message
def show_reset_message():
    st.success("Simulation history has been reset. Start fresh and simulate again!")

# Create three columns with specified width ratios
col1, col2, col3 = st.columns([2, 4, 2])

# Place the "Reset Simulation History" button in the first column (left-aligned)
with col3:
    if st.button("Reset Simulation", key="reset_button"):
        reset_simulation_history()

# Place the "Run Simulation" button in the third column (right-aligned)
with col1:
    if st.button("Run Simulation", key="run_button"):
        year_type, revenue, costs, profit = simulate_season()
        st.session_state["simulation_result"] = {
            "year_type": year_type,
            "revenue": revenue,
            "costs": costs,
            "profit": profit
        }

# Display the simulation outcome outside the columns
if "simulation_result" in st.session_state:
    st.subheader("Simulation Outcome!")
    result = st.session_state["simulation_result"]
    if result["profit"] < 0:
        st.warning("Warning: You incurred a loss this season. Click 'Run Simulation' again to see if next season turns things around!")
    else:
        st.success("Success: You made a profit this season! Click 'Run Simulation' again to see how your strategy fares in the next season!")

if st.session_state['simulation_history']:
    history_df = pd.DataFrame(st.session_state['simulation_history'])

    # --- Simulation Summary ---
    total_revenue = history_df["Revenue"].sum()
    total_costs = history_df["Costs"].sum()
    total_net_profit = history_df["Net Profit"].sum()

    st.markdown(f"""
        ### 💰 Simulation Summary
        - **Total Revenue:** ${total_revenue}
        - **Total Costs:** ${total_costs}
        - **Total Net Profit:** ${total_net_profit}
    """)

    # Define columns for the visualizations
    col1, col2 = st.columns(2)

    # --- 1. Breakdown of Costs vs. Revenue (Pie Chart) ---
    with col1:
        st.subheader("Breakdown of Costs vs. Revenue")
        pie_fig = go.Figure(
            data=[go.Pie(
                labels=["Total Costs", "Total Revenue"],
                values=[total_costs, total_revenue],
                textinfo='label+percent',
                marker=dict(colors=["#FF9999", "#99FF99"])  # Soft red and green
            )]
        )
        pie_fig.update_layout(title=" ", title_x=0.5, title_font=dict(size=16, family="Arial"))
        st.plotly_chart(pie_fig)

    # --- 2. Year Type Analysis (Bar Chart) ---
    with col2:
        st.subheader("Year Type Analysis")
        year_counts = history_df["Year Type"].value_counts()
        bar_fig = go.Figure(
            data=[go.Bar(
                x=year_counts.index,
                y=year_counts.values,
                marker=dict(color=["#FF6666", "#99CCFF"])  # Soft blue and red
            )]
        )
        bar_fig.update_layout(
            title=" ",
            xaxis_title="Year Type",
            yaxis_title="Count",
            title_x=0.5,
            title_font=dict(size=16, family="Arial"),
        )
        st.plotly_chart(bar_fig)

    # --- 3. Net Profit Over Simulations (Bar Chart) ---
    st.subheader("Net Profit Over Simulations")
    colors = ['#99FF99' if x >= 0 else '#FF9999' for x in history_df["Net Profit"]]  # Green for profit, red for loss
    net_profit_fig = go.Figure(
        data=[go.Bar(
            x=[f"Sim {i+1}" for i in range(len(history_df))],
            y=history_df["Net Profit"],
            marker=dict(color=colors),
            text=history_df["Net Profit"],
            textposition='auto'
        )]
    )
    net_profit_fig.update_layout(
        title=" ",
        xaxis_title="Simulation Number",
        yaxis_title="Net Profit ($)",
        title_x=0.5,
        title_font=dict(size=16, family="Arial"),
        shapes=[dict(type="line", x0=-0.5, x1=len(history_df)-0.5, y0=0, y1=0, line=dict(color="black", width=1, dash="dash"))]  # Reference line at 0
    )
    st.plotly_chart(net_profit_fig)

    # Simulation History Table (below the chart)
    st.subheader("Simulation History")

    # Style rows based on the Year Type column
    def highlight_rows(row):
        if row["Year Type"] == "Normal":
            return ['background-color: #DFF2BF'] * len(row)  # Light Green for Normal years
        elif row["Year Type"] == "Bad":
            return ['background-color: #FFBABA'] * len(row)  # Light Red for Bad years
        else:
            return [''] * len(row)  # No styling for others

    styled_df = history_df.style.apply(highlight_rows, axis=1)
    st.dataframe(styled_df)  # Display the styled DataFrame

# Add a copyright line at the bottom of the page
st.markdown(
    "<div style='text-align: center; margin-top: 50px; font-size: 12px; color: gray;'>"
    "© The National Center for Disaster Preparedness (NCDP) Columbia Climate School, at Columbia University. All rights reserved."
    "</div>",
    unsafe_allow_html=True
)