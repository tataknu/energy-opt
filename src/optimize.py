import csv
from ortools.sat.python import cp_model

class EnergyOptimization:
    def __init__(self, battery_capacity, charging_efficiency, discharging_efficiency,
                 max_charging_rate, max_discharging_rate, solar_energy, energy_demand,
                 grid_electricity_cost, solar_incentive):
        self.battery_capacity = int(battery_capacity)
        self.charging_efficiency = charging_efficiency
        self.discharging_efficiency = discharging_efficiency
        self.max_charging_rate = max_charging_rate
        self.max_discharging_rate = max_discharging_rate
        self.solar_energy = solar_energy
        self.energy_demand = energy_demand
        self.grid_electricity_cost = grid_electricity_cost
        self.solar_incentive = solar_incentive
        self.num_time_steps = len(solar_energy)
        self.solution = None

    def solve(self):
        model = cp_model.CpModel()

        # Scale the floating-point values to integers
        charging_efficiency = int(self.charging_efficiency * 100)
        discharging_efficiency = int(self.discharging_efficiency * 100)
        grid_electricity_cost = [int(cost * 100) for cost in self.grid_electricity_cost]
        solar_incentive = [int(incentive * 100) for incentive in self.solar_incentive]

        # Decision variables
        charge = [model.NewBoolVar(f'charge_{t}') for t in range(self.num_time_steps)]
        discharge = [model.NewBoolVar(f'discharge_{t}') for t in range(self.num_time_steps)]
        energy_stored = [model.NewIntVar(0, self.battery_capacity * 100, f'energy_stored_{t}') for t in range(self.num_time_steps)]

        # Constraints
        for t in range(self.num_time_steps):
            # Battery capacity constraint
            model.Add(energy_stored[t] <= self.battery_capacity * 100)

            # Energy balance constraint
            if t == 0:
                model.Add(energy_stored[t] == charge[t] * charging_efficiency * self.solar_energy[t] -
                          discharge[t] * discharging_efficiency - self.energy_demand[t] * 100)
            else:
                model.Add(energy_stored[t] == energy_stored[t-1] + charge[t] * charging_efficiency * self.solar_energy[t] -
                          discharge[t] * discharging_efficiency - self.energy_demand[t] * 100)

            # Battery charge/discharge rate constraints
            model.Add(charge[t] * self.max_charging_rate <= self.solar_energy[t])
            model.Add(discharge[t] * self.max_discharging_rate * 100 <= energy_stored[t])

            # Restriction: Battery cannot charge and discharge simultaneously
            model.Add(charge[t] + discharge[t] <= 1)

        # Objective function
        objective = sum(grid_electricity_cost[t] * (self.energy_demand[t] * 100 - discharge[t] * discharging_efficiency) -
                        solar_incentive[t] * self.solar_energy[t] for t in range(self.num_time_steps))
        model.Minimize(objective)

        # Solve the model
        solver = cp_model.CpSolver()
        status = solver.Solve(model)

        if status == cp_model.OPTIMAL:
            print("Optimal solution found!")
            self.solution = []
            for t in range(self.num_time_steps):
                self.solution.append({
                    'time_step': t,
                    'charge': solver.Value(charge[t]),
                    'discharge': solver.Value(discharge[t]),
                    'energy_stored': solver.Value(energy_stored[t]) / 100
                })
            print(f"Total cost: {solver.ObjectiveValue() / 10000}")
        else:
            print("No optimal solution found.")

    def export_to_csv(self, file_path):
        if self.solution is None:
            print("No solution available. Please run the solve() method first.")
            return

        fieldnames = ['time_step', 'charge', 'discharge', 'energy_stored']

        with open(file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.solution)

        print(f"Solution exported to {file_path}")


