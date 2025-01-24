import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="Understanding Farming Strategies!",
    page_icon="🌾",
)

# --- App Title ---
st.title("🌟 Farming Personas: Compete for Profitability! 🌟")

# --- Instructions Section ---
with st.expander("Instructions", expanded=False):
    st.markdown("""
        ### 🌟 **How to Play** 🌾

        1. **Select Your Weather Risk:**  
           Decide how often extreme weather might strike using the return period selector on the left. 🌩️  
           *E.g.*, "once in 2 years" means a 50% chance annually.

        2. **Meet the Farming Personas:**  
           - **👩‍🌾 Traditional Farmer (No Insurance):**  
             A low-risk, budget-friendly approach, but vulnerable to disasters.  
           - **👨‍🌾 Traditional Farmer (With Insurance):**  
             Plays safe with insurance for moderate protection.  
           - **🌾 High-Risk Taker (No Insurance):**  
             A bold approach with high-quality seeds but no fallback plan.  
           - **💼 Strategic Planner (With Insurance):**  
             Combines high investment with risk management for steady profits.

        3. **Run the Simulation:**  
           Watch the race unfold and see who thrives under various conditions!

        4. **Analyze Results:**  
           Check the leaderboard to identify the winning strategy and visualize the profit race. 🏆
    """)

# --- Initialize Session State ---
if "persona_simulation_history" not in st.session_state:
    st.session_state["persona_simulation_history"] = {
        "Traditional_No_Insurance": [],
        "Traditional_With_Insurance": [],
        "High_Quality_No_Insurance": [],
        "High_Quality_With_Insurance": [],
    }
if "years_record" not in st.session_state:
    st.session_state["years_record"] = {
        "Traditional_No_Insurance": [],
        "Traditional_With_Insurance": [],
        "High_Quality_No_Insurance": [],
        "High_Quality_With_Insurance": [],
    }

# --- Define Personas ---
personas = [
    {"name": "Traditional_No_Insurance", "seed_type": "Traditional", "insurance": False},
    {"name": "Traditional_With_Insurance", "seed_type": "Traditional", "insurance": True},
    {"name": "High_Quality_No_Insurance", "seed_type": "High Quality", "insurance": False},
    {"name": "High_Quality_With_Insurance", "seed_type": "High Quality", "insurance": True},
]

# --- Default Parameters ---
default_params = {
    'traditional_seed_cost': 80,
    'high_quality_seed_cost': 120,
    'traditional_yield_revenue': 150,
    'high_quality_yield_revenue': 350,
    'insurance_payout': 120,
    'insurance_premium': 15,
    'loan_interest_rate': 7.0,
}

for key, value in default_params.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- Sidebar Settings ---
st.sidebar.header("Simulation Settings")
return_period_options = {
    "Once in 2 years (50% chance per year)": 50,
    "Once in 5 years (20% chance per year)": 20,
    "Once in 10 years (10% chance per year)": 10,
    "Once in 20 years (5% chance per year)": 5,
    "Once in 50 years (2% chance per year)": 2,
    "Once in 100 years (1% chance per year)": 1,
}
selected_return_period = st.sidebar.selectbox(
    "Select Return Period for Extreme Weather Events:",
    options=list(return_period_options.keys()),
    help="🌪️ Decide how frequently extreme weather events like droughts occur."
)
bad_year_probability = return_period_options[selected_return_period] / 100
normal_year_probability = 1 - bad_year_probability


# --- Simulation Logic ---
def simulate_season(persona, year_type):
    # Costs and revenue logic
    if persona["seed_type"] == "Traditional":
        costs = st.session_state['traditional_seed_cost']
        revenue = st.session_state['traditional_yield_revenue'] if year_type == "Normal" else 0
    else:
        costs = st.session_state['high_quality_seed_cost'] * (1 + st.session_state['loan_interest_rate'] / 100)
        revenue = st.session_state['high_quality_yield_revenue'] if year_type == "Normal" else 0

    # Insurance adjustments
    if persona["insurance"]:
        costs += st.session_state['insurance_premium']
        if year_type == "Bad":
            revenue += st.session_state['insurance_payout']

    # Calculate net profit
    net_profit = revenue - costs

    # Update history
    persona_name = persona["name"]
    cumulative_profit = net_profit + (st.session_state["persona_simulation_history"][persona_name][-1] if
                                      st.session_state["persona_simulation_history"][persona_name] else 0)
    st.session_state["persona_simulation_history"][persona_name].append(cumulative_profit)


# --- Reset Logic ---
def reset_simulation_history():
    for key in st.session_state["persona_simulation_history"]:
        st.session_state["persona_simulation_history"][key] = []
        st.session_state["years_record"][key] = []
    st.success("Simulation reset successfully!")


# --- Layout Buttons ---
col1, col2, col3 = st.columns([2, 4, 2])

with col1:
    if st.button("Run Simulation"):
        st.session_state["show_simulation_feedback"] = False  # Reset feedback flag

        # Determine the year type once for all personas
        global_year_type = np.random.choice(
            ["Normal", "Bad"], p=[normal_year_probability, bad_year_probability]
        )

        # Run the simulation for all personas using the global year type
        for persona in personas:
            simulate_season(persona, global_year_type)  # Pass the shared year type

        # Set the flag to show feedback
        st.session_state["show_simulation_feedback"] = True

with col3:
    if st.button("Reset Simulation"):
        reset_simulation_history()

# Display user feedback outside the column
if "show_simulation_feedback" in st.session_state and st.session_state["show_simulation_feedback"]:
    st.subheader("Simulation Outcome!")

    # Provide feedback based on the global year type
    if global_year_type == "Bad":
        st.warning("Disaster struck this year! 😔 It was a bad weather year for everyone.")
    else:
        st.success("It was a normal year. 🌞 Everyone enjoyed favorable weather!")

    # Clear the feedback flag after displaying it
    st.session_state["show_simulation_feedback"] = False

# --- Visualization: Race for Net Profit ---
if any(st.session_state["persona_simulation_history"].values()):
    st.subheader("Net Profit Race 🏁")

    race_fig = go.Figure()
    persona_emojis = {"Traditional_No_Insurance": "🌱", "Traditional_With_Insurance": "🛡️",
                      "High_Quality_No_Insurance": "💎", "High_Quality_With_Insurance": "🚀"}
    year_colors = {"Normal": "green", "Bad": "red"}

    for persona in personas:
        name = persona["name"]
        history = st.session_state["persona_simulation_history"][name]
        years = st.session_state["years_record"][name]
        color_sequence = [year_colors[year] for year in years]

        race_fig.add_trace(go.Scatter(
            x=list(range(1, len(history) + 1)),
            y=history,
            mode="lines+markers+text",
            marker=dict(color=color_sequence, size=10),
            name=f"{persona_emojis[name]} {name.replace('_', ' ')}",
            text=[""] * (len(history) - 1) + [persona_emojis[name]],
            textposition="top center"
        ))

    race_fig.update_layout(
        title="Farming Personas: Profit Race",
        xaxis_title="Simulation Number",
        yaxis_title="Cumulative Profit ($)",
        template="plotly_white"
    )
    st.plotly_chart(race_fig)

# --- Leaderboard ---
leaderboard = pd.DataFrame([
    {"Persona": persona["name"].replace("_", " "),
     "Cumulative Profit": st.session_state["persona_simulation_history"][persona["name"]][-1] if
     st.session_state["persona_simulation_history"][persona["name"]] else 0}
    for persona in personas
]).sort_values(by="Cumulative Profit", ascending=False)

# Add rank and emojis based on positions
emoji_map = ["🥇", "🥈", "🥉", "🌱"]  # Emojis for ranking
leaderboard["Rank"] = range(len(leaderboard))  # Assign ranks
leaderboard["Emoji"] = leaderboard["Rank"].apply(lambda x: emoji_map[x] if x < len(emoji_map) else "🌾")
leaderboard = leaderboard[["Emoji", "Persona", "Cumulative Profit"]]  # Reorder columns

# Style the leaderboard as a fun and visually engaging markdown table
st.subheader("🏆 🌟 The Farming Leaderboard 🌟")
st.markdown("""
    **Which farmer is performing the best?**  
""")

# Convert leaderboard to a markdown-styled table
styled_leaderboard = leaderboard.to_markdown(index=False, tablefmt="pretty")
st.markdown(f"```\n{styled_leaderboard}\n```")

# Add a copyright line at the bottom of the page
st.markdown(
    "<div style='text-align: center; margin-top: 50px; font-size: 12px; color: gray;'>"
    "© The National Center for Disaster Preparedness (NCDP) Columbia Climate School, at Columbia University. All rights reserved."
    "</div>",
    unsafe_allow_html=True
)

