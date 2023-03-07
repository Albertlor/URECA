import math


class Risk:
    US_axial = 6000 #Newton
    US_bending = 51.7 #Nm
    a = 0.5
    b = 0.5
    accumulated_risk_back = 0
    p_back = 1.72
    q_back = 1.03
    p_shoulder = 0.573
    q_shoulder = 0.747

    def __init__(self, M_back, F_back, M_shoulder, F_shoulder, number_of_repetition):
        self.M_back = M_back
        self.F_back = F_back
        self.M_shoulder = M_shoulder
        self.F_shoulder = F_shoulder
        self.number_of_repetition = number_of_repetition

    def risk(self):
        cd_back, cd_shoulder = Risk.cumulative_damage(self.M_back, self.F_back, self.M_shoulder, self.F_shoulder, self.number_of_repetition)
        
        Y_back = Risk.p_back + Risk.q_back * math.log(cd_back + 1e-10) #add a very small number to ensure it's close to 0 but avoid ValueError
        r_back = math.exp(Y_back) / (1 + math.exp(Y_back))

        Y_shoulder = Risk.p_shoulder + Risk.q_shoulder * math.log(cd_shoulder + 1e-10)
        r_shoulder = math.exp(Y_shoulder) / (1 + math.exp(Y_shoulder))

        Risk.accumulated_risk_back += r_back

        return r_back, Risk.accumulated_risk_back, r_shoulder
    
    @staticmethod
    def cumulative_damage(M_back, F_back, M_shoulder, F_shoulder, number_of_repetition):
        S_back, S_shoulder = Risk.percentage_ultimate_strength(M_back, F_back, M_shoulder, F_shoulder)
        
        N_back = 902416 * math.exp((0-0.162) * S_back)
        cd_back = 1/N_back * number_of_repetition

        N_shoulder = 10 ** ((101.25 - S_shoulder) / 14.83)
        cd_shoulder = 1/N_shoulder * number_of_repetition

        return cd_back, cd_shoulder
    
    @classmethod
    def percentage_ultimate_strength(cls, M_back, F_back, M_shoulder, F_shoulder):
        percentage_US_axial_back = F_back / cls.US_axial
        percentage_US_bending_back = M_back / cls.US_bending

        percentage_US_axial_shoulder = F_shoulder / cls.US_axial
        percentage_US_bending_shoulder = M_shoulder / cls.US_bending

        S_back = cls.a * percentage_US_axial_back + cls.b * percentage_US_bending_back
        S_shoulder = cls.a * percentage_US_axial_shoulder + cls.b * percentage_US_bending_shoulder

        return S_back * 100, S_shoulder * 100
        