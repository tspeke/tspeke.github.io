import math

# Total number of moles (constant since Stoichiometry is 2:2)

# Define conversion, X
# Should acheive roughly 98% conversion

class stream():
    def __init__(self, T, P, D_mole_flows):
        self.D_mole_flows = D_mole_flows
        self.T = T
        self.P = P
    
    @property
    def n_tot(self):
        flow_count = 0
        for flow in self.D_mole_flows.values():
            flow_count += flow
        
        return flow_count

    @property
    def D_y(self):
        return {key : (mole_flow / self.n_tot) for key, mole_flow in self.D_mole_flows.items()} # ".items()" returns both the key and value of each element
    
    @property
    def D_part_P(self):
        return {key : y*self.P for key, y in self.D_y.items()}

class reactor():
    def __init__(self, T, P, inlet, catalyst, m_catalyst):
        self.T = T
        self.P = P
        self.D_mole_flows = inlet
        self.catalyst = catalyst
        self.m_catalyst = m_catalyst
        
        self.D_r_stoich = {"CH4":0, "H2O":-1, "CO2":+1, "CO":-1, "H2":+1, "AR":0}
    
    # Kinetic Data
    @property
    def r(self): # in pound-moles converted per pound of catalyst per hour
        num = self.phi*self.k*(self.D_y["CO"]*self.D_y["H2O"] - (self.D_y["CO2"]*self.D_y["H2"])/(self.K))
        denom = 379*self.rho_cat
        return num / denom
    
    @property
    def rho_cat(self): # in lb/ft3
        if self.catalyst == "iron":
            return 126
        elif self.catalyst == "copper-zinc":
            return 155
    
    @property
    def K(self):
        return math.exp(4577.8/self.T - 4.33)
    
    @property
    def k(self):
        if self.catalyst == "iron":
            return math.exp(15.95 - 4900/self.T)
        elif self.catalyst == "copper-zinc":
            return math.exp(12.88 - 2002.6/self.T)
    
    @property
    def phi(self):
        if self.catalyst == "iron":
            if self.P <= 11.8:
                return 0.816 + (0.184 * self.P)
            elif self.P <= 20:
                return 1.53 + (0.123 * self.P)
            else:
                return 4
        
        elif self.catalyst == "copper-zinc":
            if self.P <= 24.8:
                return 0.86 + (0.14 * self.P)
            else:
                return 4.33
    
    # Calculating Outlet stream
    # Will output a stream type object
    @property
    def outlet(self):
        
        # Mass balance
        for k, v in self.D_r_stoich.items():
            self.D_mole_flows[k] += v * self.r
        
        # Energy balance
  
####################################################################################################

# Approximate expected molar flowrates (in kmol/h) from Aspen stream tables
input_molar_flows = {"CH4":0.57, "H2O":1.50, "CO2":12.83, "CO":87.59, "H2":189.83, "AR":1.86}

INPUT = stream(200, 100, input_molar_flows)

# Add H2O
INPUT.D_mole_flows["H2O"] += 100

HT_WGS_R = reactor(200, 100, INPUT, "iron")

print(INPUT.D_part_P)

def system_of_ODEs(W, X, T, P_T):
    """Defines the system of three coupled ODEs.

    Args:
        W: The independent variable (Mass of catalyst in pounds).
        X: The dependant variable

    Returns:
        A list or array containing the derivatives of the dependent variables
        [dX/dW, dT/dW, dP/dW].
    """

    # Define the equations for the derivatives
    dXdV = 1/(10.4)*(r_1(T, μ, P_T, X, S, phi)+r_2(T, μ, P_T, X, S, phi)+r_3(T, μ, P_T, X, S, phi))
    dSdV = 1/(10.4*X)*((1-S)*r_1(T, μ, P_T, X, S, phi)-S*r_2(T, μ, P_T, X, S, phi)-S*r_3(T, μ, P_T, X, S, phi))
    dphidV = 1/(10.4*X)*(-phi*r_1(T, μ, P_T, X, S, phi)+(1-phi)*r_2(T, μ, P_T, X, S, phi)-phi*r_3(T, μ, P_T, X, S, phi))

    return [dXdV, dSdV, dphidV]

