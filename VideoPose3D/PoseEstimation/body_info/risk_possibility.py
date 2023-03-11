import math


class Risk:
    US = 6000 #Newton
    a = 0.12 #hyperparameter decided by the ergonomics specialists
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
        cd_back, accumulated_cd_back, cd_shoulder_per_repetition, cd_shoulder = Risk.cumulative_damage(self.M_back, self.F_back, self.M_shoulder, self.F_shoulder)
        
        Y_back_per_repetition = Risk.p_back + Risk.q_back * math.log(cd_back + 1e-20) #add a very small number to ensure it's close to 0 but avoid ValueError
        r_back_per_repetition = math.exp(Y_back_per_repetition) / (1 + math.exp(Y_back_per_repetition))
        Y_back = Risk.p_back + Risk.q_back * math.log(accumulated_cd_back + 1e-20) #add a very small number to ensure it's close to 0 but avoid ValueError
        r_back = math.exp(Y_back) / (1 + math.exp(Y_back))

        Y_shoulder_per_repetition = Risk.p_shoulder + Risk.q_shoulder * math.log(cd_shoulder_per_repetition + 1e-20)
        r_shoulder_per_repetition = math.exp(Y_shoulder_per_repetition) / (1 + math.exp(Y_shoulder_per_repetition))
        Y_shoulder = Risk.p_shoulder + Risk.q_shoulder * math.log(cd_shoulder + 1e-20)
        r_shoulder = math.exp(Y_shoulder) / (1 + math.exp(Y_shoulder))

        compressive_force = self.F_back + self.M_back / Risk.a

        return r_back_per_repetition, r_back, r_shoulder_per_repetition, r_shoulder, compressive_force
    
    @classmethod
    def cumulative_damage(cls, M_back, F_back, M_shoulder, F_shoulder):
        S_back, S_shoulder = Risk.percentage_ultimate_strength(M_back, F_back, M_shoulder, F_shoulder)
        
        N_back = 902416 * math.exp((0-0.162) * S_back)
        cd_back = 1/N_back
        accumulated_cd_back = cd_back + cls.previous_cd_back
        cls.previous_cd_back = accumulated_cd_back

        N_shoulder = 10 ** ((101.25 - S_shoulder) / 14.83)
        cd_shoulder = 1/N_shoulder
        accumulated_cd_shoulder = cd_shoulder + cls.previous_cd_shoulder
        cls.previous_cd_shoulder = accumulated_cd_shoulder

        return cd_back, accumulated_cd_back, cd_shoulder, accumulated_cd_shoulder
    
    @classmethod
    def percentage_ultimate_strength(cls, M_back, F_back, M_shoulder, F_shoulder):
        S_back = ((F_back + (M_back/cls.a)) / (cls.US)) * 100
        S_shoulder = ((F_shoulder + (M_shoulder/cls.a)) / (cls.US)) * 100

        print(f'S: {S_back}')

        return S_back, S_shoulder
        