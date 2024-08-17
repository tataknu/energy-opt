import streamlit as st
import plotly.graph_objects as go
from optimize import EnergyOptimization

def main():
    st.set_page_config(page_title="Energy Optimization", page_icon=":sunny:")
    
    st.title("Solar Energy Storage Scheduling Optimization")
    
    st.write("""
             The goal of this project is to optimize the scheduling of energy storage systems (e.g., batteries) in conjunction with solar power generation to minimize energy costs. By storing excess solar energy during peak production hours and using it during periods of high demand or low solar output, we can reduce the reliance on grid electricity and maximize the utilization of renewable energy.
        
             This application uses Google OR-Tools' CP-SAT solver to find the optimal schedule for battery charging and discharging, minimizing the total energy cost over the optimization horizon.

             Most trivial assumption is that we take period as an integer value from 0 to 4 representing 5 points of time.
         """)
    
    st.markdown("Check out more in [link](%s)" % "https://github.com/tataknu/energy-opt")

    with st.expander("Key Concepts"):
        st.markdown("""
        ### Key Concepts
        - **Battery Capacity**: The maximum amount of energy that can be stored in the battery.
        - **Charging Efficiency**: The efficiency of the battery when charging, representing the percentage of energy that is successfully stored.
        - **Discharging Efficiency**: The efficiency of the battery when discharging, representing the percentage of stored energy that can be effectively utilized.
        - **Max Charging Rate**: The maximum rate at which the battery can be charged.
        - **Max Discharging Rate**: The maximum rate at which the battery can be discharged.
        - **Solar Energy**: The amount of energy generated by solar panels at each time step.
        - **Energy Demand**: The energy consumption pattern of the system or household at each time step.
        - **Grid Electricity Cost**: The cost of electricity from the grid at each time step.
        - **Solar Incentive**: Any incentives or credits provided for using solar energy at each time step.
        """)
    
    # Sidebar title    
    st.sidebar.title("Input Parameters:")

    # Input fields
    battery_capacity = st.sidebar.number_input("Battery Capacity", value=100)
    charging_efficiency = st.sidebar.number_input("Charging Efficiency", value=0.9)
    discharging_efficiency = st.sidebar.number_input("Discharging Efficiency", value=0.8)
    max_charging_rate = st.sidebar.number_input("Max Charging Rate", value=20)
    max_discharging_rate = st.sidebar.number_input("Max Discharging Rate", value=10)
    solar_energy = st.sidebar.text_input("Solar Energy (comma-separated)", value="30,40,50,60,70")
    energy_demand = st.sidebar.text_input("Energy Demand (comma-separated)", value="10,20,30,40,50")
    grid_electricity_cost = st.sidebar.text_input("Grid Electricity Cost (comma-separated)", value="0.1,0.2,0.3,0.4,0.5")
    solar_incentive = st.sidebar.text_input("Solar Incentive (comma-separated)", value="0.05,0.05,0.05,0.05,0.05")
    
    if st.sidebar.button("Optimize"):
        # Convert comma-separated strings to lists of floats
        solar_energy = [int(x) for x in solar_energy.split(",")]
        energy_demand = [int(x) for x in energy_demand.split(",")]
        grid_electricity_cost = [float(x) for x in grid_electricity_cost.split(",")]
        solar_incentive = [float(x) for x in solar_incentive.split(",")]
        
        # Create an instance of EnergyOptimization
        optimizer = EnergyOptimization(
            battery_capacity=battery_capacity,
            charging_efficiency=charging_efficiency,
            discharging_efficiency=discharging_efficiency,
            max_charging_rate=max_charging_rate,
            max_discharging_rate=max_discharging_rate,
            solar_energy=solar_energy,
            energy_demand=energy_demand,
            grid_electricity_cost=grid_electricity_cost,
            solar_incentive=solar_incentive
        )
        
        # Solve the optimization problem
        optimizer.solve()
        
        st.subheader("Optimization Results")
        if optimizer.solution is not None:
            # Extract data for plotting
            time_steps = [step['time_step'] for step in optimizer.solution]
            charge_values = [step['charge'] for step in optimizer.solution]
            discharge_values = [step['discharge'] for step in optimizer.solution]
            energy_stored_values = [step['energy_stored'] for step in optimizer.solution]
            
            # Create traces for the chart
            charge_trace = go.Bar(x=time_steps, y=charge_values, name='Charge')
            discharge_trace = go.Bar(x=time_steps, y=discharge_values, name='Discharge')
            energy_stored_trace = go.Scatter(x=time_steps, y=energy_stored_values, name='Energy Stored', mode='lines+markers')
            
            # Create the chart layout
            layout = go.Layout(
                title='Energy Storage Scheduling',
                xaxis=dict(title='Time Step'),
                yaxis=dict(title='Energy (kWh)'),
                barmode='stack'
            )
            
            # Create the figure and display the chart
            fig = go.Figure(data=[charge_trace, discharge_trace, energy_stored_trace], layout=layout)
            st.plotly_chart(fig)
        else:
            st.error("No optimal solution found.")

if __name__ == "__main__":
    main()