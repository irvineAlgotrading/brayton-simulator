import tkinter as tk
from tkinter import ttk
import CoolProp.CoolProp as CP

class BraytonCycleGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Brayton Cycle Simulator")
        self.geometry("400x400")

        # Parameters initialization
        self.P1 = tk.DoubleVar(value=7.5e6)
        self.P2 = tk.DoubleVar(value=25e6)
        self.T1 = 300
        self.T3_max = 923
        self.efficiency_compressor = 0.85
        self.efficiency_turbine = 0.90

        ttk.Label(self, text="Initial Pressure (Pa):").grid(column=0, row=0, sticky=tk.W)
        ttk.Spinbox(self, from_=1e6, to_=50e6, increment=0.1e6, textvariable=self.P1, command=self.calculate).grid(column=1, row=0)

        ttk.Label(self, text="Max Pressure (Pa):").grid(column=0, row=1, sticky=tk.W)
        ttk.Spinbox(self, from_=5e6, to_=100e6, increment=0.1e6, textvariable=self.P2, command=self.calculate).grid(column=1, row=1)

        self.results_var = tk.StringVar(value="Press Start to run the simulation.")
        ttk.Label(self, textvariable=self.results_var, wraplength=350).grid(column=0, row=2, columnspan=2)

        ttk.Button(self, text="Start", command=self.calculate).grid(column=0, row=3, columnspan=2)

    def calculate(self):
        efficiency, w_net, q_added, q_recuperated = self.brayton_cycle(self.P1.get(), self.T1, self.P2.get(), self.T3_max, self.efficiency_compressor, self.efficiency_turbine)
        result_text = f"""
        Cycle efficiency: {efficiency * 100:.2f}%
        Net work: {w_net:.2f} J/kg
        Heat added: {q_added:.2f} J/kg
        Heat recuperated: {q_recuperated:.2f} J/kg
        """
        self.results_var.set(result_text)

    def brayton_cycle(self, P1, T1, P2, T3_max, efficiency_compressor, efficiency_turbine):
        fluid = 'CO2'
        s1 = CP.PropsSI('S', 'P', P1, 'T', T1, fluid)
        h1 = CP.PropsSI('H', 'P', P1, 'T', T1, fluid)

        h2_s = CP.PropsSI('H', 'P', P2, 'S', s1, fluid)
        h2 = h1 + (h2_s - h1) / efficiency_compressor
        T2 = CP.PropsSI('T', 'P', P2, 'H', h2, fluid)
        h3 = CP.PropsSI('H', 'P', P2, 'T', T3_max, fluid)
        q_added = h3 - h2

        s3 = CP.PropsSI('S', 'P', P2, 'H', h3, fluid)
        h4_s = CP.PropsSI('H', 'P', P1, 'S', s3, fluid)
        h4 = h3 - efficiency_turbine * (h3 - h4_s)
        T4 = CP.PropsSI('T', 'P', P1, 'H', h4, fluid)
        q_recuperated = (T4 - T2) * CP.PropsSI('C', 'P', P1, 'T', T4, fluid)

        w_net = (h3 - h4) - (h2 - h1)
        thermal_efficiency = w_net / q_added

        return thermal_efficiency, w_net, q_added, q_recuperated

if __name__ == "__main__":
    app = BraytonCycleGUI()
    app.mainloop()
