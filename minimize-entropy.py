import numpy as np
from scipy.optimize import minimize

# Define the entropy generation equation (equation 10)
def entropy_generation(params, m1, m2, cp, R):
    T1_in, T2_out, P1_out, P2_out = params
    T1_out = T1_in  # Assuming inlet temperature of fluid 1 is equal to outlet temperature
    T2_in = T2_out  # Assuming inlet temperature of fluid 2 is equal to outlet temperature
    s_gen = m1 * cp * np.log(T1_out / T1_in) + m2 * cp * np.log(T2_out / T2_in) - m1 * R * np.log(P1_out) - m2 * R * np.log(P2_out)
    return s_gen

# Define the entropy generation number (equation 11)
def entropy_generation_number(s_gen, m2, cp):
    Ns = s_gen / (m2 * cp)
    return Ns

# Objective function to minimize
def objective(params, m1, m2, cp, R):
    s_gen = entropy_generation(params, m1, m2, cp, R)
    return s_gen

if __name__ == "__main__":
    # Given parameters
    m1 = 1.0  # mass flow rate of fluid 1 [kg/s]
    m2 = 1.0  # mass flow rate of fluid 2 [kg/s]
    cp = 1005  # specific heat at constant pressure [J/kg·K]
    R = 287.05  # specific gas constant [J/kg·K]

    # Initial guess for optimization
    initial_guess = [300, 400, 101325, 101325]  # [T1_in, T2_out, P1_out, P2_out]
    
    # Constraint: Pressure can't be negative
    constraints = (
    {'type': 'ineq', 'fun': lambda x: entropy_generation(x, m1, m2, cp, R)},
    {'type': 'ineq', 'fun': lambda x: x[2]},
    {'type': 'ineq', 'fun': lambda x: x[3]}
    )

    
    result = minimize(objective, initial_guess, args=(m1, m2, cp, R), constraints=constraints)

    optimal_parameters = result.x
    s_gen_optimal = entropy_generation(optimal_parameters, m1, m2, cp, R)
    Ns_optimal = entropy_generation_number(s_gen_optimal, m2, cp)

    print(f"Optimal parameters: T1_in={optimal_parameters[0]:.2f}K, T2_out={optimal_parameters[1]:.2f}K, P1_out={optimal_parameters[2]:.2f}Pa, P2_out={optimal_parameters[3]:.2f}Pa")
    print(f"Optimal entropy generation: {s_gen_optimal:.2f} J/K")
    print(f"Optimal entropy generation number: {Ns_optimal:.2f}")

