import CoolProp.CoolProp as CP

def brayton_cycle(P1, T1, P2, T3_max, efficiency_compressor, efficiency_turbine):
    # Properties of supercritical CO2
    fluid = 'CO2'

    # 1-2: Isentropic Compression
    s1 = CP.PropsSI('S', 'P', P1, 'T', T1, fluid)
    h1 = CP.PropsSI('H', 'P', P1, 'T', T1, fluid)

    h2_s = CP.PropsSI('H', 'P', P2, 'S', s1, fluid)
    h2 = h1 + (h2_s - h1) / efficiency_compressor

    # 2-3: Heat addition in the recuperator and combustion chamber
    T2 = CP.PropsSI('T', 'P', P2, 'H', h2, fluid)
    h3 = CP.PropsSI('H', 'P', P2, 'T', T3_max, fluid)
    q_added = h3 - h2

    # 3-4: Isentropic Expansion
    s3 = CP.PropsSI('S', 'P', P2, 'H', h3, fluid)
    h4_s = CP.PropsSI('H', 'P', P1, 'S', s3, fluid)
    h4 = h3 - efficiency_turbine * (h3 - h4_s)

    # 4-1: Heat recovery in the recuperator
    T4 = CP.PropsSI('T', 'P', P1, 'H', h4, fluid)
    q_recuperated = (T4 - T2) * CP.PropsSI('C', 'P', P1, 'T', T4, fluid)

    # Net work and cycle efficiency
    w_net = (h3 - h4) - (h2 - h1)
    thermal_efficiency = w_net / q_added

    return thermal_efficiency, w_net, q_added, q_recuperated

if __name__ == "__main__":
    # Define cycle parameters
    P1 = 7.5e6  # Pa, initial pressure
    T1 = 300  # K, initial temperature
    P2 = 25e6  # Pa, max pressure after compression
    T3_max = 923  # K, max temperature after heat addition
    efficiency_compressor = 0.85
    efficiency_turbine = 0.90

    efficiency, w_net, q_added, q_recuperated = brayton_cycle(P1, T1, P2, T3_max, efficiency_compressor, efficiency_turbine)

    print(f"Cycle efficiency: {efficiency * 100:.2f}%")
    print(f"Net work: {w_net:.2f} J/kg")
    print(f"Heat added: {q_added:.2f} J/kg")
    print(f"Heat recuperated: {q_recuperated:.2f} J/kg")

