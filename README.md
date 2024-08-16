# Solar Energy Storage Scheduling Optimization using Google OR-Tools' CP-SAT Solver

## Problem Definition

The goal of this project is to optimize the scheduling of energy storage systems (e.g., batteries) in conjunction with solar power generation to minimize energy costs. By storing excess solar energy during peak production hours and using it during periods of high demand or low solar output, we can reduce the reliance on grid electricity and maximize the utilization of renewable energy. 

### Decision Variables

- Binary variables:
  - `charge[t]`: Indicates whether the battery is charging at time step `t`.
  - `discharge[t]`: Indicates whether the battery is discharging at time step `t`.
- Continuous variables:
  - `energy_stored[t]`: Represents the energy stored in the battery at time step `t`.

### Constraints

- Battery capacity:
  - The total energy stored in the battery cannot exceed its maximum capacity.
  - `energy_stored[t] <= battery_capacity` for all time steps `t`.
- Energy balance:
  - The energy stored, generated, and consumed must be balanced at each time step.
  - `energy_stored[t] = energy_stored[t-1] + charge[t] * charging_efficiency * solar_energy[t] - discharge[t] * discharging_efficiency - energy_demand[t]` for all time steps `t`.
- Battery charge/discharge rates:
  - The rate at which the battery can be charged or discharged is limited.
  - `charge[t] * charging_rate <= max_charging_rate` for all time steps `t`.
  - `discharge[t] * discharging_rate <= max_discharging_rate` for all time steps `t`.
- Solar energy availability:
  - The amount of solar energy generated varies based on time of day and weather conditions.
  - `solar_energy[t]` is given as input data for each time step `t`.
- Energy demand:
  - The energy consumption pattern of the system or household varies over time.
  - `energy_demand[t]` is given as input data for each time step `t`.

### Objective Function

The objective is to minimize the total cost of energy over the optimization horizon, considering the cost of grid electricity and any incentives for solar energy usage. 

`minimize(sum(grid_electricity_cost[t] * (energy_demand[t] - discharge[t] * discharging_efficiency) - solar_incentive[t] * solar_energy[t]) for all time steps t)`

## Solution Approach

1. Collect and preprocess historical data on solar energy generation, energy consumption, and electricity prices.
2. Forecast solar energy generation and energy demand for the optimization horizon using techniques like time series analysis or machine learning.
3. Formulate the problem using the defined decision variables, constraints, and objective function.
4. Implement the model using Google OR-Tools' CP-SAT solver in Python.
5. Configure the solver parameters and run the optimization process.
6. Analyze the optimal solution and visualize the results to showcase the energy storage and usage patterns.
7. Perform sensitivity analysis by varying input parameters to evaluate the impact on the optimal solution and cost savings.

## Expected Results

The optimization model will provide an optimal schedule for battery charging and discharging, minimizing the total energy cost over the optimization horizon. The results will demonstrate the potential cost savings and the effective utilization of solar energy through optimal storage scheduling. 

This project aims to showcase the application of Google OR-Tools' CP-SAT solver in solving real-world optimization problems related to solar energy management. The code and documentation will be made available on GitHub for reference and further development.
