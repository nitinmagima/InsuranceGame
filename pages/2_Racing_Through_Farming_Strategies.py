import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import json

st.set_page_config(
    page_title="Understanding Farming Strategies!",
    page_icon="🌾",
)

# --- App Title ---
st.title("🌟 Racing Through Farming Strategies 🌾")

st.markdown("""
So, you've taken on the Farming Challenge and made your choices—well done, farmer! 👩‍🌾👨‍🌾 But have you ever wondered how those decisions stack up against other strategies?  

This is your chance to explore how other farmers would have performed under different weather scenarios. Curious to see how the **Traditional Farmer** or the **Strategic Planner** handles extreme weather? Or maybe you're intrigued by the bold decisions of a high-risk taker versus the cautious approach of an insured farmer.  

Watch as different personas navigate the challenges of unpredictable weather, revealing how various choices impact their outcomes.  

Once you've explored your strategies here, don't forget to try the **Science Behind the Game** page to uncover the real-world implications of risk and insurance in farming!
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
if "global_year_types" not in st.session_state:
    st.session_state["global_year_types"] = []

# --- Define Personas ---
personas = [
    {"name": "Traditional_No_Insurance", "seed_type": "Traditional", "insurance": False},
    {"name": "Traditional_With_Insurance", "seed_type": "Traditional", "insurance": True},
    {"name": "High_Quality_No_Insurance", "seed_type": "High Quality", "insurance": False},
    {"name": "High_Quality_With_Insurance", "seed_type": "High Quality", "insurance": True},
]

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

# --- Instructions Section ---
with st.expander("Instructions", expanded=False):
    st.markdown("""
### 🌟 **Compare Different Farming Persona Strategies** 🌾

1. **Select Your Weather Risk:**  
   Decide how often extreme weather might strike using the return period selector on the left. 🌩️  
   *E.g.*, "once in 2 years" means a 50% chance annually.

2. **Meet the Farming Personas:**  
   - **👩‍🌾 Traditional Farmer (No Insurance):**  
     A low-risk, budget-friendly approach of using traditional seeds, but vulnerable to disasters.  
   - **👨‍🌾 Traditional Farmer (With Insurance):**  
     Plays safe with insurance for moderate protection while using traditional seeds.  
   - **🌾 High-Risk Taker (No Insurance):**  
     A bold approach with high-quality seeds but no fallback plan.  
   - **💼 Strategic Planner (With Insurance):**  
     Combines high investment of high quality seeds with risk management for steady profits.

3. **Run Multiple Simulations:**  
   Watch the race unfold and see who thrives under various conditions! Each simulation represents one farming season, where the outcomes depend on weather conditions and the farming persona's strategic decisions.

4. **Analyze Results:**  
   Check the leaderboard to identify the winning strategy and visualize the profit. Running multiple simulations allows you to see how strategies perform over time, helping you refine your approach and uncover patterns for success. 🏆🌾
    """)

    st.markdown("""
            To assist you in making informed decisions, refer to the table below, which outlines the costs and revenues associated with different seed types and insurance options. To change these default values for the simulations, please visit the **Customize Your Farming Adventure** page.
            """)

    st.markdown("""
            **Here are the current farming costs and revenues for your simulations:**  
        """)

    # Convert parameters DataFrame to a markdown-styled table
    styled_parameters = parameters_df.to_markdown(index=False, tablefmt="pretty")
    st.markdown(f"```\n{styled_parameters}\n```")

# --- Simulation Settings ---
with st.expander("Simulation Settings", expanded=True):
    return_period_options = {
        "Once in 2 years (50% chance per year)": 50,
        "Once in 5 years (20% chance per year)": 20,
        "Once in 10 years (10% chance per year)": 10,
        "Once in 20 years (5% chance per year)": 5,
        "Once in 50 years (2% chance per year)": 2,
        "Once in 100 years (1% chance per year)": 1,
    }
    selected_return_period = st.selectbox(
        "Select Return Period for Extreme Weather Events (Disasters):",
        options=list(return_period_options.keys()),
        help="""
            🌪️ **How Often Do Extreme Weather Events (Disasters) Strike?**  
            Extreme weather or a disaster is described as “once in N years.” For instance, a 1-in-5-year drought means a **20% chance** of it happening each year.  

            But here's the twist: a 20% chance doesn't mean it won't happen back-to-back—nature loves surprises! Similarly, a "1-in-100-year" disaster doesn't wait a century to occur. It has a **1% chance** of happening every single year, no matter when it last occurred.  
            Plan wisely and expect the unexpected! 🌦️
            """
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
    # Reset the global year types
    st.session_state["global_year_types"] = []
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

        # Store the global year type for this simulation
        st.session_state["global_year_types"].append(global_year_type)

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
        st.warning("Disaster struck this year! 😔 Bad weather affected everyone. Click 'Run Simulation' again to see what the weather holds for next year!")
    else:
        st.success("It was a great year! 🌞 Favorable weather brought good fortune to everyone. Click 'Run Simulation' again to discover next year's weather!")

    # Clear the feedback flag after displaying it
    st.session_state["show_simulation_feedback"] = False



# --- Visualization: Race for Net Profit ---
if any(st.session_state["persona_simulation_history"].values()):
    st.subheader("Net Profit Race 🏁")

    race_fig = go.Figure()
    persona_emojis = {
        "Traditional_No_Insurance": "🌱",
        "Traditional_With_Insurance": "🛡️",
        "High_Quality_No_Insurance": "💎",
        "High_Quality_With_Insurance": "🚀",
    }

    # Create x-axis labels
    x_labels = [f"{i + 1} ({year})" for i, year in enumerate(st.session_state['global_year_types'])]

    for persona in personas:
        name = persona["name"]
        history = st.session_state["persona_simulation_history"][name]

        # Calculate cumulative profit
        cumulative_profit = np.cumsum(history)

        # Add traces for each persona
        race_fig.add_trace(go.Scatter(
            x=x_labels,
            y=cumulative_profit,
            mode="lines+markers+text",
            marker=dict(size=10),
            name=f"{persona_emojis[name]} {name.replace('_', ' ')}",
            text=[""] * (len(cumulative_profit) - 1) + [persona_emojis[name]],
            textposition="top center"
        ))

    # # Update layout with categorical x-axis
    race_fig.update_layout(
        title="Farming Personas: Cumulative Profit",
        xaxis=dict(
            title="Simulation Number (Year Type)",
            type='category',
            tickangle=45,
        ),
        yaxis=dict(
            title="Cumulative Profit ($)",
        ),
        shapes=[
            # Add a persistent black line at y=0
            dict(
                type="line",
                xref="paper",  # Relative to the entire x-axis
                yref="y",  # Relative to the y-axis
                x0=0,  # Start at the left side
                x1=1,  # End at the right side
                y0=0,  # Line is at y=0
                y1=0,  # Line stays at y=0
                line=dict(color="darkslategray", width=2),  # Dark black line with thicker width
            )
        ],
        template="plotly_white"
    )

    # Display the chart
    st.plotly_chart(race_fig)


# --- Leaderboard ---
leaderboard = pd.DataFrame([
    {
        "Persona": persona["name"].replace("_", " "),
        # Calculate cumulative profit using np.sum to ensure consistency
        "Cumulative Profit": round(np.sum(st.session_state["persona_simulation_history"][persona["name"]]), 2)
        if st.session_state["persona_simulation_history"][persona["name"]] else 0
    }
    for persona in personas
]).sort_values(by="Cumulative Profit", ascending=False)

# Add rank and emojis based on positions
emoji_map = ["🥇", "🥈", "🥉", "🌱"]  # Emojis for ranking
leaderboard["Rank"] = range(len(leaderboard))  # Assign ranks
leaderboard["Emoji"] = leaderboard["Rank"].apply(lambda x: emoji_map[x] if x < len(emoji_map) else "🌾")
leaderboard = leaderboard[["Emoji", "Persona", "Cumulative Profit"]]  # Reorder columns

# Style the leaderboard as a fun and visually engaging Markdown table
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

