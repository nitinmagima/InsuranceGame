import streamlit as st

st.title("Customize Your Farming Adventure ⚙️")

st.markdown("""
## 
Welcome to the **Customize Your Farming Adventure Page**, where you have the power to fine-tune your simulation parameters and customize your farming experience. Here's what you can do:

1. **Adjust Costs and Revenues**:
   - Set the costs for traditional and high-quality seeds.
   - Define the expected revenue from both types of seeds.

2. **Modify Loan Parameters**:
   - Set the interest rate for loans required to purchase high-quality seeds.

3. **Insurance Parameters**:
   - Specify the **insurance payout** amount in case of crop failure.
   - Adjust the **insurance premium** to determine the cost of purchasing insurance.

4. **Reset to Defaults**:
   - Quickly revert all parameters to their original default values using the **Reset to Defaults** button.

Take control of your simulation and create the scenario that suits your farming strategy! 🌱🌾
""")


# Default parameter values
default_params = {
    'traditional_seed_cost': 80,           # Lower cost to reflect affordability of traditional seeds
    'high_quality_seed_cost': 120,         # High-quality seeds are more expensive but not excessively so
    'traditional_yield_revenue': 150,      # Revenue from traditional seeds should be modest but sustainable
    'high_quality_yield_revenue': 350,     # Higher potential revenue to make high-quality seeds attractive
    'insurance_payout': 120,               # Insurance payout should sufficiently offset losses in bad years
    'insurance_premium': 15,               # A fair cost for insurance that isn't too high for players to avoid
    'loan_interest_rate': 7.0              # Slightly higher interest rate to reflect real-world loan conditions
}


# Store initial values to compare later and initialize session state
for key, value in default_params.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Reset button functionality
if st.sidebar.button("Reset to Defaults"):
    for key, value in default_params.items():
        st.session_state[key] = value
    st.success("Settings have been reset to default values.")

# Sidebar sliders for settings
st.session_state['traditional_seed_cost'] = st.sidebar.slider(
    "Traditional Seed Cost ($):",
    min_value=0,
    max_value=100,
    value=st.session_state['traditional_seed_cost'],
    help="Set the cost of traditional seeds."
)

st.session_state['traditional_yield_revenue'] = st.sidebar.slider(
    "Traditional Yield Revenue ($):",
    min_value=0,
    max_value=500,
    value=st.session_state['traditional_yield_revenue'],
    help="Set the revenue from traditional yield."
)

st.session_state['high_quality_seed_cost'] = st.sidebar.slider(
    "High Quality Seed Cost ($):",
    min_value=0,
    max_value=200,
    value=st.session_state['high_quality_seed_cost'],
    help="Set the cost of high-quality seeds."
)

st.session_state['loan_interest_rate'] = st.sidebar.slider(
    "Loan Interest Rate (%):",
    min_value=0.0,
    max_value=20.0,
    value=st.session_state['loan_interest_rate'],
    step=0.1,
    help="Set the interest rate for loans taken to purchase high-quality seeds."
)

st.session_state['high_quality_yield_revenue'] = st.sidebar.slider(
    "High Quality Yield Revenue ($):",
    min_value=0,
    max_value=1000,
    value=st.session_state['high_quality_yield_revenue'],
    help="Set the revenue from high-quality yield."
)

st.session_state['insurance_premium'] = st.sidebar.slider(
    "Insurance Premium ($):",
    min_value=0,
    max_value=100,
    value=st.session_state['insurance_premium'],
    help="Set the cost of purchasing insurance for the season."
)


st.session_state['insurance_payout'] = st.sidebar.slider(
    "Insurance Payout ($):",
    min_value=0,
    max_value=500,
    value=st.session_state['insurance_payout'],
    help="Set the insurance payout amount."
)


# Check if any value has changed
settings_changed = any(
    st.session_state[key] != default_params[key]
    for key in default_params
)

# Show success message only if settings have changed
if settings_changed:
    st.success("Parameters updated! Navigate back to the Home page to see the changes.")

# Add a copyright line at the bottom of the page
st.markdown(
    "<div style='text-align: center; margin-top: 50px; font-size: 12px; color: gray;'>"
    "© The National Center for Disaster Preparedness (NCDP) Columbia Climate School, at Columbia University. All rights reserved."
    "</div>",
    unsafe_allow_html=True
)