### README.md

# 🌾 **Agricultural Insurance Simulation Game** 🌾

Welcome to the **Agricultural Insurance Simulation Game**, a fun and interactive way to explore farming strategies, risk management, and the impact of climate change on agriculture. This game helps players understand how strategic decisions like investing in insurance and choosing seed types can influence farming profitability, even under extreme weather conditions.

---

## 🚀 **Overview**

The project is divided into four Python scripts, each representing a unique aspect of the simulation game. Here’s what each file does:

### **1. `1_The_Farming_Challenge.py`**
- This is the introductory game module where players select their farming strategies and navigate the challenges of extreme weather.
- **Features:**
  - **Persona Selection:** Choose between four farming personas:
    - 👩‍🌾 Traditional Farmer (No Insurance)
    - 👨‍🌾 Traditional Farmer (With Insurance)
    - 🌾 High-Risk Taker (No Insurance)
    - 💼 Strategic Planner (With Insurance)
  - **Weather Settings:** Adjust the return period for extreme weather events, such as droughts or floods.
  - **Goal:** Help players balance risks and rewards to maximize profitability.

---

### **2. `2_Racing_Through_Farming_Strategies.py`**
- This module visualizes the race between farming personas as they compete for cumulative profit over multiple simulations.
- **Features:**
  - **Net Profit Race Visualization:** A dynamic line chart showing the cumulative profit for each persona across simulations. 
  - **Year Type Feedback:** Displays whether a "Normal" or "Bad" weather year occurred for each simulation.
  - **Leaderboard:** A ranked table showcasing the top-performing personas with emojis for extra flair.

---

### **3. `3_The_Science_Behind_the_Game.py`**
- A deep dive into the science behind the game, this script educates users on:
  - The growing frequency of extreme weather events due to climate change.
  - The importance of agricultural insurance in managing farming risks.
  - Real-world examples of innovative insurance solutions, such as parametric insurance in Africa.
- **Goal:** Promote awareness about sustainable farming practices and the broader implications of food security.

---

### **4. `4_Customize_Your_Farming_Adventure.py`**
- This script allows users to customize their farming adventure by tweaking game parameters.
- **Features:**
  - Modify costs, revenues, and insurance details for each farming strategy.
  - Personalize the return period for extreme weather events to simulate different scenarios.
  - Save and reset settings to create new challenges.

---

### **Config File: `config.json`**

The `config.json` file is used to store all the default parameter values for the simulation, making it easier to manage and customize the game settings. This approach separates the configuration from the code, ensuring flexibility and maintainability.

#### Parameters in `config.json`:
- **`traditional_seed_cost`**: The cost of traditional seeds.
- **`high_quality_seed_cost`**: The cost of high-quality seeds, which are more expensive but offer higher rewards.
- **`traditional_yield_revenue`**: The revenue from traditional seeds under normal weather conditions.
- **`high_quality_yield_revenue`**: The revenue from high-quality seeds under normal weather conditions.
- **`insurance_payout`**: The compensation provided by insurance during bad weather years.
- **`insurance_premium`**: The cost of purchasing crop insurance.
- **`loan_interest_rate`**: The interest rate applied to loans for purchasing high-quality seeds.

## 🎮 **How to Play**

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/agricultural-insurance-simulation.git
   cd agricultural-insurance-simulation
   ```
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the scripts in Streamlit:
   ```bash
   streamlit run 1_The_Farming_Challenge.py
   ```

---

## 🔑 **Key Features**
- **Interactive Gameplay:** Choose strategies, simulate results, and visualize outcomes.
- **Dynamic Visualizations:** Graphs and tables make it easy to compare different farming strategies.
- **Real-World Insights:** Learn how climate change affects agriculture and the role of insurance in mitigating risks.
- **Customizable Scenarios:** Adjust parameters to test various farming conditions and strategies.

---

## 🌍 **Why It Matters**
Agriculture is one of the most vulnerable sectors to climate change. By engaging with this game, users can better understand the challenges farmers face and the critical role of insurance in ensuring food security and sustainable farming practices.

---

## 🤝 **Contributing**
Contributions are welcome! Feel free to open issues or submit pull requests to improve the game.

---

## 📄 **License**
This project is licensed under the MIT License. 

---

## 📩 **Contact**
For questions or suggestions, reach out to:
- **Nitin Magima** on [LinkedIn](https://www.linkedin.com/in/nitin-magima/).

---

Enjoy the game, and may your farming strategies lead to bountiful harvests! 🌟
```