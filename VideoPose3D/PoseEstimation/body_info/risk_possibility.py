import math
import cv2



class Risk:
    US_back = 6000 # in Newton
    US_shoulder = 115 # in Newton
    previous_cd_back = 1e-20
    previous_cd_shoulder = 1e-20
    p_back = 1.72
    q_back = 1.03
    p_shoulder = 0.573
    q_shoulder = 0.747

    def __init__(self, M_back, F_back, M_shoulder, F_shoulder, number_of_repetition, a, b, c, d):
        self.M_back = M_back
        self.F_back = F_back
        self.M_shoulder = M_shoulder
        self.F_shoulder = F_shoulder
        self.number_of_repetition = number_of_repetition
        self.a = a # a=10, b=0, a=10.7, b=450, a=9.7, b=250, a=8, b=500
        self.b = b
        self.c = c
        self.d = d

    def risk(self):
        cd_threshold = 0.03
        accumulated_cd_back, accumulated_cd_shoulder, S_shoulder = Risk.cumulative_damage(self.M_back, self.F_back, self.M_shoulder, self.F_shoulder, self.a, self.b, self.c, self.d)

        Y_back = Risk.p_back + Risk.q_back * math.log(accumulated_cd_back + 1e-20) #add a very small number to ensure it's close to 0 but avoid ValueError
        r_back = math.exp(Y_back) / (1 + math.exp(Y_back))

        Y_back_threshold = Risk.p_back + Risk.q_back * math.log(cd_threshold + 1e-20) #add a very small number to ensure it's close to 0 but avoid ValueError
        r_back_threshold = math.exp(Y_back_threshold) / (1 + math.exp(Y_back_threshold))

        Y_shoulder = Risk.p_shoulder + Risk.q_shoulder * math.log(accumulated_cd_shoulder + 1e-20)
        r_shoulder = math.exp(Y_shoulder) / (1 + math.exp(Y_shoulder))

        Y_shoulder_threshold = Risk.p_shoulder + Risk.q_shoulder * math.log(cd_threshold + 1e-20) #add a very small number to ensure it's close to 0 but avoid ValueError
        r_shoulder_threshold = math.exp(Y_shoulder_threshold) / (1 + math.exp(Y_shoulder_threshold))

        compressive_force_back = self.F_back + (self.M_back * self.a + self.b)
        compressive_force_shoulder = self.F_shoulder + (self.M_shoulder * self.c - self.d)

        return r_back, r_shoulder, compressive_force_back, compressive_force_shoulder, r_back_threshold, r_shoulder_threshold, S_shoulder
    
    @classmethod
    def cumulative_damage(cls, M_back, F_back, M_shoulder, F_shoulder, a, b, c, d):
        S_back, S_shoulder = Risk.percentage_ultimate_strength(M_back, F_back, M_shoulder, F_shoulder, a, b, c, d)
        
        N_back = 902416 * math.exp((0-0.162) * S_back)
        cd_back = 1/N_back
        accumulated_cd_back = cd_back + cls.previous_cd_back
        cls.previous_cd_back = accumulated_cd_back

        N_shoulder = 10 ** ((101.25 - S_shoulder) / 14.83)
        cd_shoulder = 1/N_shoulder
        accumulated_cd_shoulder = cd_shoulder + cls.previous_cd_shoulder
        cls.previous_cd_shoulder = accumulated_cd_shoulder

        return accumulated_cd_back, accumulated_cd_shoulder, S_shoulder
    
    @classmethod
    def percentage_ultimate_strength(cls, M_back, F_back, M_shoulder, F_shoulder, a, b, c , d):
        S_back = ( (F_back + (M_back * a + b)) / (cls.US_back) ) * 100
        S_shoulder = ( (F_shoulder + (M_shoulder * c - d)) / (cls.US_shoulder) ) * 100

        print(f'S_back: {S_back}')
        print(f'S_shoulder: {S_shoulder}')

        return S_back, S_shoulder
        