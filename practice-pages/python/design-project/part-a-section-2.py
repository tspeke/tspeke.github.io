import math
from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt

# N.B. 
# T in K
# P in Pa

# --- CONSTANTS and CONVERSION FACTORS ---
R = 8.3145 # Ideal Gas Constant, J/(mol.K) or Pa.m^3/(mol.K)
ATM_TO_PA = 101325
KMOL_H_TO_MOL_S = 1000 / 3600
KJ_TO_J = 1000
LB_FT3_TO_KG_M3 = 16.0185
# Conversion for reaction rate from lbmol/(lb_cat.h) to mol/(kg_cat.s)
RATE_CONV_FACTOR = (453.592 / 3600) / 0.453592 # This simplifies to 1/3.6

# Assume viscosity ~ const throughout
MU = 1.8E-5 # Pa.s, Taken as viscosity of air for now

# Packing density - take as a default
VOIDAGE = 0.4

# Molar masses
D_Mr = {"CH4":16.04, "H2O":18.02, "CO2":44.01, "CO":28.01, "H2":2.02, "AR":39.95} # g/mol

# Shomate Equation parameters for Cp and H of species
# Gives:
# Cp, H = f(t), t = T (K) /1000

# Cp = A + B*t + C*t^2 + D*t^3 + E/t^2

# H(T) in kJ/mol = [A*t + B/2*t^2 + C/3*t^3 + D/4*t^4 - E/t + F] + H_formation
# The term in brackets is H(T) - H(298.15 K). H_formation is H(298.15 K).

# Units: 
# Cp in J/mol/K
# H in kJ/mol

# Shomate parameters [A, B, C, D, E, F, G, H] from NIST. H is ΔfH°(298.15 K) in kJ/mol.
CH4_par = [-0.70303, 108.477, -42.5216, 5.86279, 0.67857, -76.4838, 192.253, -74.8731]
H2O_par = [30.09200, 6.832514, 6.793435, -2.534480, 0.082139, -250.8810, 223.3967, -241.8264]
CO2_par = [24.99735, 55.18696, -33.69137, 7.948387, -0.136638, -403.6075, 228.2431, -393.5224]
CO_par  = [25.56759, 6.096130, 4.054656, -2.671301, 0.131021, -118.0089, 227.3665, -110.5271]
H2_par  = [33.066178, -11.363417, 11.432816, -2.772874, -0.158558, -9.980797, 172.707974, 0.0]
AR_par  = [20.78600, 0.0, 0.0, 0.0, 0.0, -6.19733, 154.846, 0.0]

D_par = {
    "CH4" : CH4_par, 
    "H2O" : H2O_par,
    "CO2" : CO2_par,
    "CO" : CO_par,
    "H2" : H2_par,
    "AR" : AR_par
}

# Total number of moles (constant since Stoichiometry is 2:2)

# Target:
# Should acheive roughly 98% conversion
# CO2 + CO --> H2 + CO2

####################################################################################################

# Classes

####################################################################################################

## Streams

class stream():
    def __init__(self, T, P, D_mole_flows):
        # Convert all inputs to a consistent SI unit system
        self.T = T # KELVIN
        self.P = P * ATM_TO_PA # P from atm to Pa
        # D_mole_flows from kmol/h to mol/s
        self.D_mole_flows = {k: v * KMOL_H_TO_MOL_S for k, v in D_mole_flows.items()}
    
    @property
    def M(self):
        # Returns total mass flow in kg/s
        total_mass_flow = 0
        for k, v in self.D_mole_flows.items():
            # v is in mol/s, D_Mr is in g/mol. Convert to kg/s
            total_mass_flow += v * (D_Mr[k] / 1000.0)
        
        return total_mass_flow
    
    @property
    def F(self):
        # Returns total molar flow in mol/s
        flow_count = 0
        for flow in self.D_mole_flows.values():
            flow_count += flow
        
        return flow_count

    # Use IGL
    @property
    def Q(self):
        # Returns volumetric flow rate in m^3/s
        return (self.F * R * self.T) / self.P
    
    # Use IGL
    @property
    def rho(self):
        # Returns density in kg/m^3
        return self.M / self.Q

    @property
    def D_y(self):
        return {key : (mole_flow / self.F) for key, mole_flow in self.D_mole_flows.items()} # ".items()" returns both the key and value of each element
    
    @property
    def D_part_P(self):
        return {key : y*self.P for key, y in self.D_y.items()}

####################################################################################################

## Reactors

class reactor():
    def __init__(self, inlet, reaction, m_catalyst, bed_diam):
        self.inlet = inlet

        self.r1 = reaction

        self.d = self.r1.catalyst.d # Otherwise clumsy to call

        self.W_T = m_catalyst
        self.D = bed_diam
        
    # Mechanical Data
    
    # Cross sectional area
    @property
    def A(self):
        return (self.D**2) / 4
    
    # Initial superficial velocity at inlet
    @property
    def u0(self):
        return self.inlet.Q / self.A

    # Calculate initial Re from inlet conditions of reactor
    # Re = d * u_superficial * rho / (mu * (1-voidage))   
    @property
    def Re0(self):
        return self.d * self.u0 * self.inlet.rho / (MU * (1 - VOIDAGE))
    
    def D_y_react(self, extent):
        D_mole_flows_react = self.r1.react(self.inlet.D_mole_flows, extent)

        flow_count = 0
        for flow in D_mole_flows_react.values():
            flow_count += flow
        
        return {k : n/flow_count for k, n in D_mole_flows_react.items()}

    def adiabatic_sys_ODEs(self, W, y):
        '''
        Defines the system of three coupled ODEs for the PFR.

        Args:
            W: The independent variable (Mass of catalyst / kg).
            y: A list or array containing the dependent variables [X, T, P_Pa].
               X: fractional conversion of CO (dimensionless)
               T: Temperature (K)
               P_Pa: Pressure (Pa)

        Returns:
            A list or array containing the derivatives of the dependent variables
            [dX/dW, dT/dW, dP/dW].
        '''
        
        X, T, P_Pa = y  # Unpack the dependent variables

        if P_Pa < 1: return [0, 0, 0]

        # --- Calculate instantaneous properties based on X, T, P ---

        # 1. Molar flows (mol/s)
        F_CO_in = self.inlet.D_mole_flows["CO"]
        extent = F_CO_in * X
        D_flows_inst = self.r1.react(self.inlet.D_mole_flows, extent)
        F_total_inst = sum(D_flows_inst.values())

        # 2. Mole fractions
        D_y_inst = {k: v / F_total_inst for k, v in D_flows_inst.items()}

        # --- Mass Balance (dX/dW) ---
        
        # Rate of reaction for CO (mol_CO_reacted / kg_cat / s)
        r1_inst = self.r1.r(T, P_Pa, D_y_inst)
        
        # dX/dW = r' / F_CO_in
        dXdW = r1_inst / F_CO_in
        
        # --- Energy Balance (dT/dW) ---

        # Enthalpy of reaction (J/mol)
        H_r1 = self.r1.H(T)

        # Mean heat capacity of mixture (J/mol/K)
        Cp_overall = Cp_tot(D_y_inst, T)
        
        # dT/dW = (-r_CO') * (-H_rxn) / (F_total * Cp_mean)
        # Note: r1_inst is rate of consumption (+), H_r1 is enthalpy of reaction (exothermic, so -)
        dTdW = (r1_inst * -H_r1) / (F_total_inst * Cp_overall)

        # --- Momentum Balance / Pressure Drop (dPdW) ---

        # Calculate local gas properties for Ergun equation
        # Mean molar mass (kg/mol)
        Mr_mean_inst = sum(D_y_inst[k] * (D_Mr[k] / 1000.0) for k in D_y_inst)
        # Density (kg/m^3) using Ideal Gas Law: rho = P*Mr / (R*T)
        rho_inst = (P_Pa * Mr_mean_inst) / (R * T)
        # Volumetric flow rate (m^3/s)
        Q_inst = (F_total_inst * R * T) / P_Pa
        # Superficial velocity (m/s)
        u_inst = Q_inst / self.A

        # Ergun equation for pressure drop per unit length (Pa/m)
        term1 = 150 * MU / (self.d**2) * ((1 - VOIDAGE)**2) / (VOIDAGE**3) * u_inst
        term2 = 1.75 * rho_inst / self.d * (1 - VOIDAGE) / (VOIDAGE**3) * (u_inst**2)
        dPdL = -(term1 + term2) # Negative for a pressure drop
        
        dLdW = 1 / (self.r1.catalyst.rho * (1 - VOIDAGE) * self.A)
        
        dPdW = dPdL * dLdW

        return [dXdW, dTdW, dPdW]

    def solve_ODEs(self):

        T_0 = self.inlet.T
        P_0 = self.inlet.P
        X_0 = 0.0
        y0 = [X_0, T_0, P_0] # Initial conditions vector [X, T, P]

        # Mass of catalyst (kg) over which reaction occurs
        W_span = (0, self.W_T)

        # Define points for the solver to return the solution at
        eval_points = np.linspace(W_span[0], W_span[1], 101)

        # Solve the system of ODEs
        # The function for solve_ivp must take (t, y) as arguments
        solution = solve_ivp(
            fun=self.adiabatic_sys_ODEs, 
            t_span=W_span, 
            y0=y0, 
            method='Radau', 
            t_eval=eval_points,
            rtol=1e-8,
            atol=1e-10,
            max_step=5.0
        )
        
        # Access the solution components
        W = solution.t
        
        # Ensure returned conversion is physically bounded between 0 and 1
        X = np.clip(solution.y[0], 0, 1)
        T = solution.y[1]
        P = solution.y[2]

        return W, X, T, P

    # Defining the Outlet stream object from the reactor
    def calc_profile(self):

        self.W, self.X, self.T, self.P = self.solve_ODEs()

        # --- Outlet Stream ---
        # Calculating the molar flows in outlet
        F_CO_in = self.inlet.D_mole_flows["CO"]
        extent = F_CO_in * self.X[-1]
        D_flows_outlet = self.r1.react(self.inlet.D_mole_flows, extent)
        
        # The solver returns P in Pa, but stream() expects atm.
        # D_flows_outlet is in mol/s, but stream() expects kmol/h.
        # We must convert both back to the input units for the stream class.
        D_flows_outlet_kmol_h = {k: v / KMOL_H_TO_MOL_S for k, v in D_flows_outlet.items()}
        
        self.outlet = stream(T=self.T[-1], P=self.P[-1]/ATM_TO_PA, D_mole_flows=D_flows_outlet_kmol_h)

####################################################################################################

## Reaction

class reaction():
    def __init__(self, D_stoich, catalyst):
        self.D_stoich = D_stoich
        self.catalyst = catalyst
    
    # Kinetic Data
    def r(self, T, P_Pa, D_y): # returns rate in mol_converted / (kg_catalyst * s)
        P_atm = P_Pa / ATM_TO_PA
        num = self.phi(P_atm)*self.k(T)*(D_y["CO"]*D_y["H2O"] - (D_y["CO2"]*D_y["H2"])/(self.K(T)))
        # Original rate 'num' is in lbmol/(lb_cat*h). Convert to mol/(kg_cat*s).
        denom = 379 * self.catalyst.rho
        return num / denom

    def K(self, T):
        return math.exp(4577.8/T - 4.33)
    
    def k(self, T):
        if self.catalyst.type == "iron":
            return math.exp(15.95 - 4900/T)
        elif self.catalyst.type == "copper-zinc":
            return math.exp(12.88 - 2002.6/T)
    
    def phi(self, P):
        # P here is expected in atm
        if self.catalyst.type == "iron":
            if P <= 11.8:
                return 0.816 + (0.184 * P)
            # This section is redefined to be continuous with the other two pieces.
            # It connects point (11.8, 2.9872) to (20, 4.0).
            elif P <= 20.0:
                return 2.9872 + ((4.0 - 2.9872) / (20.0 - 11.8)) * (P - 11.8)
            else:
                return 4.0
        elif self.catalyst.type == "copper-zinc":
            # The intercept is adjusted from 0.86 to 0.858 to make the function continuous at P=24.8 atm.
            if P <= 24.8:
                return 0.858 + (0.14 * P)
            else:
                return 4.33
    
    # Thermodynamic data
    
    # Calculation of H of given reaction
    def H(self, T):
        H_diff = 0
        for k, v in self.D_stoich.items():
            L_par = D_par[k]
            t = T / 1000
            # H_species(T) in kJ/mol = [H(T) - H(298)] + H(298)
            # [H(T) - H(298)] = A*t + B/2*t^2 + C/3*t^3 + D/4*t^4 - E/t + F
            # H(298) is the standard enthalpy of formation, the 8th parameter (L_par[7]).
            H_species = (L_par[0]*t + L_par[1]*(t**2)/2 + L_par[2]*(t**3)/3 + 
                         L_par[3]*(t**4)/4 - L_par[4]/t + L_par[5] + L_par[7])
            H_diff += v * H_species
        
        # H from Shomate is in kJ/mol, convert to J/mol for consistency
        return H_diff * KJ_TO_J
    
    # Reacting...

    # Returns dictionary of mol fractions after a certain amount of reaction has occured
    def react(self, D_moles, extent):
        return {k : n + extent * self.D_stoich[k] for k, n in D_moles.items()}

####################################################################################################

## Catalysts

class catalyst():
    def __init__(self, name, rho, particle_diam):
        self.type = name
        self.d = particle_diam / 1000 # in mm --> m
        self.rho = rho  # in lb/ft3

####################################################################################################

# Calculation of Cp of given composition
def Cp_tot(D_y, T):
    Cp_tot = 0
    for k, v in D_y.items():
        L_par = D_par[k]
        t = T / 1000
        # Cp =           A    +     B*t    +     C*t^2       +      D*t^3      +      E/t^2
        Cp_species = L_par[0] + L_par[1]*t + L_par[2]*(t**2) + L_par[3]*(t**3) + L_par[4]/(t**2)
        Cp_tot += v * Cp_species
    
    return Cp_tot

####################################################################################################



####################################################################################################

def helper_mole_to_y(D_mole_flows):
    n_tot = sum(D_mole_flows.values())
    
    return {k: n / n_tot for k, n  in D_mole_flows.values()}


####################################################################################################

# Process

####################################################################################################


# --- Catalysts ---
c_iron = catalyst("iron", 126, 3)
c_copper_zinc = catalyst("copper-zinc", 155, 2)

# --- Reactions ---

# Define WGS with Iron catalyst
r_wgs_iron = reaction(D_stoich={"CH4":0, "H2O":-1, "CO2":+1, "CO":-1, "H2":+1, "AR":0}, catalyst=c_iron)

# Define WGS with Copper-Zinc catalyst
r_wgs_copper_zinc = reaction(D_stoich={"CH4":0, "H2O":-1, "CO2":+1, "CO":-1, "H2":+1, "AR":0}, catalyst=c_copper_zinc)

# --- Define Inlet to Area ---

# Molar flowrates (in kmol/h) from Aspen stream tables
input_molar_flows = {"CH4": 0.57, "H2O": 1.50, "CO2": 12.83, "CO": 87.59, "H2": 189.83, "AR": 1.86}

# Add H2O for stoichiometry adjustment (e.g., 100 kmol/h) before creating the stream
input_molar_flows["H2O"] += 100

s_ht_wgs_in = stream(T=270+273.15, P=28, D_mole_flows=input_molar_flows)

R_ht_wgs = reactor(inlet=s_ht_wgs_in, reaction=r_wgs_iron, m_catalyst=2500, bed_diam=3)

R_ht_wgs.calc_profile()

s_ht_wgs_out = R_ht_wgs.outlet

# Second LT WGS reactor

# Create inlet for second reactor based on outlet of first
# We create a new stream object to avoid modifying the previous reactor's outlet reference
flows_intermediate = {k: v / KMOL_H_TO_MOL_S for k, v in s_ht_wgs_out.D_mole_flows.items()}
s_lt_wgs_in = stream(T=180, P=s_ht_wgs_out.P/ATM_TO_PA, D_mole_flows=flows_intermediate)

R_lt_wgs = reactor(inlet=s_lt_wgs_in, reaction=r_wgs_copper_zinc, m_catalyst=2500, bed_diam=3)

R_lt_wgs.calc_profile()

s_lt_wgs_out = R_lt_wgs.outlet

# --- Print Results ---
print(f"\n--- HT WGS INLET CONDITIONS ---")
print(f"Inlet Properties: T={s_ht_wgs_in.T:.1f} K, P={s_ht_wgs_in.P/ATM_TO_PA:.2f} atm")
print(f"Inlet Composition: {s_ht_wgs_in.D_y}")
print(f"\n--- HT WGS OUTLET CONDITIONS ---")
print(f"Outlet Properties: W_cat={R_ht_wgs.W_T:.1f} kg, X_CO={R_ht_wgs.X[-1]:.3f}, T={s_ht_wgs_out.T:.1f} K, P={s_ht_wgs_out.P/ATM_TO_PA:.2f} atm")

print(f"\n--- LT WGS INLET CONDITIONS ---")
print(f"Inlet Properties: T={s_lt_wgs_in.T:.1f} K, P={s_lt_wgs_in.P/ATM_TO_PA:.2f} atm")
print(f"\n--- LT WGS OUTLET CONDITIONS ---")
print(f"Outlet Properties: W_cat={R_lt_wgs.W_T:.1f} kg, X_CO={R_lt_wgs.X[-1]:.3f}, T={s_lt_wgs_out.T:.1f} K, P={s_lt_wgs_out.P/ATM_TO_PA:.2f} atm")
print(f"Outlet Composition: {s_lt_wgs_out.D_y}")

# Overall Conversion

X_overall = 1 - (s_lt_wgs_out.D_mole_flows["CO"] / s_ht_wgs_in.D_mole_flows["CO"])

print(f"\nOverall Conversion across plant: {X_overall:.4f} ({X_overall*100:.2f}%)")

#################################################################################################### 

# Sensitivity Analyses

####################################################################################################

# Wrapper function to simulate the entire plant area with variable parameters
def run_plant(T_ht, P_ht, W_ht, T_lt, W_lt, n_water_add):
    # 1. Setup Feed
    # Create a local copy of base flows to avoid modifying globals
    input_flows = {"CH4": 0.57, "H2O": 1.50, "CO2": 12.83, "CO": 87.59, "H2": 189.83, "AR": 1.86}
    flows = input_flows.copy()
    flows["H2O"] += n_water_add
    
    # 2. HT Reactor
    s1 = stream(T=T_ht, P=P_ht, D_mole_flows=flows)
    r1 = reactor(inlet=s1, reaction=r_wgs_iron, m_catalyst=W_ht, bed_diam=3)
    r1.calc_profile()
    
    # 3. Interstage (Cooling + Unit Conversion)
    s1_out = r1.outlet
    # Convert outlet mol/s back to kmol/h for new stream init
    flows_inter = {k: v / KMOL_H_TO_MOL_S for k, v in s1_out.D_mole_flows.items()}
    
    # 4. LT Reactor
    s2 = stream(T=T_lt, P=s1_out.P/ATM_TO_PA, D_mole_flows=flows_inter)
    r2 = reactor(inlet=s2, reaction=r_wgs_copper_zinc, m_catalyst=W_lt, bed_diam=3)
    r2.calc_profile()
    
    # 5. Calculate Overall Conversion
    CO_in_mol_s = s1.D_mole_flows["CO"]
    CO_out_mol_s = r2.outlet.D_mole_flows["CO"]
    
    # Clamp overall result to [0, 1]
    X_overall = np.clip(1 - (CO_out_mol_s / CO_in_mol_s), 0, 1)
    return X_overall, r1, r2

# --- Run Sensitivity Loops ---
print("\nStarting Sensitivity Analysis...")

# Base case values
base_T_ht = 270 + 273.15
base_P_ht = 28
base_W_ht = 2000
base_T_lt = 180 + 273.15
base_W_lt = 2000
base_n_water = 100

# Parameters to vary and their ranges (tuples of: label, unit, linspace)
tests = {
    "T_ht": ("HT Inlet T", "K", np.linspace(250, 350, 10) + 273.15),
    "P_ht": ("HT Inlet P", "atm", np.linspace(15, 40, 10)),
    "W_ht": ("HT Catalyst Mass", "kg", np.linspace(100, 1000, 10)),
    "T_lt": ("LT Inlet T", "K", np.linspace(160, 240, 10) + 273.15),
    "W_lt": ("LT Catalyst Mass", "kg", np.linspace(100, 1000, 10)),
    "n_water": ("Added Water", "kmol/h", np.linspace(50, 200, 10))
}

# Create a 2x3 grid of subplots
fig, axs = plt.subplots(2, 3, figsize=(15, 10))
axs = axs.flatten()

for i, (key, (label, unit, values)) in enumerate(tests.items()):
    results = []

    # For each parameter test, loop through its values and run a full simulation
    for val in values:
        # Start with a copy of the base case arguments
        args = [base_T_ht, base_P_ht, base_W_ht, base_T_lt, base_W_lt, base_n_water]

        # Update the specific parameter being tested in this loop
        idx_map = {"T_ht": 0, "P_ht": 1, "W_ht": 2, "T_lt": 3, "W_lt": 4, "n_water": 5}
        args[idx_map[key]] = val

        # Run the full two-reactor simulation and get the overall conversion
        x_res, _, _ = run_plant(*args)
        results.append(x_res)
    
    # Plot
    axs[i].plot(values, results, 'b-o', markersize=4)
    axs[i].set_title(f"Sensitivity: {label}")
    axs[i].set_xlabel(f"{label} ({unit})")
    axs[i].set_ylabel("Overall Conversion X")
    axs[i].grid(True)

plt.show()