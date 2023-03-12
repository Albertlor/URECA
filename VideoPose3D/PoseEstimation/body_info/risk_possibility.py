import math


class Risk:
    US_back = 6000 # in Newton
    US_shoulder = 100e6 # in Pascal
    a = 11 #hyperparameter decided by the ergonomics specialists
    b = -800
    previous_cd_back = 1e-20
    previous_cd_shoulder = 1e-20
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
        cd_threshold = 0.03
        accumulated_cd_back, accumulated_cd_shoulder = Risk.cumulative_damage(self.M_back, self.F_back, self.M_shoulder, self.F_shoulder)

        Y_back = Risk.p_back + Risk.q_back * math.log(accumulated_cd_back + 1e-20) #add a very small number to ensure it's close to 0 but avoid ValueError
        r_back = math.exp(Y_back) / (1 + math.exp(Y_back))

        Y_back_threshold = Risk.p_back + Risk.q_back * math.log(cd_threshold + 1e-20) #add a very small number to ensure it's close to 0 but avoid ValueError
        r_back_threshold = math.exp(Y_back_threshold) / (1 + math.exp(Y_back_threshold))

        Y_shoulder = Risk.p_shoulder + Risk.q_shoulder * math.log(accumulated_cd_shoulder + 1e-20)
        r_shoulder = math.exp(Y_shoulder) / (1 + math.exp(Y_shoulder))

        compressive_force_back = self.F_back + self.M_back * Risk.a + Risk.b
        compressive_force_shoulder = self.F_shoulder + self.M_shoulder

        return r_back, r_shoulder, compressive_force_back, compressive_force_shoulder, r_back_threshold
    
    @classmethod
    def cumulative_damage(cls, M_back, F_back, M_shoulder, F_shoulder):
        S_back, S_shoulder = Risk.percentage_ultimate_strength(M_back, F_back, M_shoulder, F_shoulder)
        
        N_back = 902416 * math.exp((0-0.162) * S_back)
        cd_back = 1/N_back
        accumulated_cd_back = cd_back + cls.previous_cd_back
        cls.previous_cd_back = accumulated_cd_back

        N_shoulder = 10 ** ((101.25 - S_shoulder) / 14.83)
        cd_shoulder = 1/N_shoulder
        print(cd_shoulder)
        accumulated_cd_shoulder = cd_shoulder + cls.previous_cd_shoulder
        cls.previous_cd_shoulder = accumulated_cd_shoulder

        return accumulated_cd_back, accumulated_cd_shoulder
    
    @classmethod
    def percentage_ultimate_strength(cls, M_back, F_back, M_shoulder, F_shoulder):
        S_back = ( (F_back + (M_back * cls.a + cls.b)) / (cls.US_back) ) * 100
        S_shoulder = ( ((F_shoulder + (M_shoulder)) / 2.91e-6) / (cls.US_shoulder) ) * 100

        print(f'S_back: {S_back}')
        print(f'S_shoulder: {S_shoulder}')

        return S_back, S_shoulder
        