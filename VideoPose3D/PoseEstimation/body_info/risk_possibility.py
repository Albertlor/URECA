import math
import os
import json
import matplotlib.pyplot as plt
import time


class Risk:
    US_back = 6000 # in Newton
    US_shoulder = 115 # in Newton
    previous_cd_back = 1e-20
    previous_cd_shoulder = 1e-20
    p_back = 1.72
    q_back = 1.03
    p_shoulder = 0.573
    q_shoulder = 0.747

    def __init__(self, M_back, F_back, number_of_repetition, a):
        self.M_back = M_back
        self.F_back = F_back
        self.number_of_repetition = number_of_repetition
        self.a = a # a=10, b=0, a=10.7, b=450, a=9.7, b=250, a=8, b=500

    def risk(self):
        cd_threshold = 0.03
        accumulated_cd_back, S_back = Risk.cumulative_damage(self.M_back, self.F_back, self.a)

        Y_back = Risk.p_back + Risk.q_back * math.log(accumulated_cd_back + 1e-20) #add a very small number to ensure it's close to 0 but avoid ValueError
        r_back = math.exp(Y_back) / (1 + math.exp(Y_back))

        Y_back_threshold = Risk.p_back + Risk.q_back * math.log(cd_threshold + 1e-20) #add a very small number to ensure it's close to 0 but avoid ValueError
        r_back_threshold = math.exp(Y_back_threshold) / (1 + math.exp(Y_back_threshold))

        compressive_force_back = self.F_back + (self.M_back * self.a)

        return r_back, compressive_force_back, r_back_threshold, accumulated_cd_back, S_back
    
    @classmethod
    def cumulative_damage(cls, M_back, F_back, a):
        S_back = Risk.percentage_ultimate_strength(M_back, F_back, a)
        
        N_back = 902416 * math.exp((0-0.162) * S_back)
        cd_back = 1/N_back
        accumulated_cd_back = cd_back + cls.previous_cd_back
        cls.previous_cd_back = accumulated_cd_back

        return accumulated_cd_back, S_back
    
    @classmethod
    def percentage_ultimate_strength(cls, M_back, F_back, a):
        S_back = ( (F_back + (M_back * a)) / (cls.US_back) ) * 100

        print(f'S_back: {S_back}')

        return S_back
    
if __name__ == '__main__':
    dictionary1 = json.load(open('./cumulative_damage.json', 'r'))
    xAxis1 = [key for key, value in dictionary1.items() if int(key)%50==0 and int(key)!=0]
    yAxis1 = [value for key, value in dictionary1.items() if int(key)%50==0 and int(key)!=0]
    
    plt.grid(True)

    ## LINE GRAPH ##
    plt.plot(xAxis1,yAxis1, color='maroon', marker='o')
    plt.xlabel('Frame')
    plt.ylabel('Cumulative Damage')
        
    plt.show()

    plt.figure()
    dictionary2 = json.load(open('./stress_back.json', 'r'))
    xAxis2 = [key for key, value in dictionary2.items() if int(key)%50==0 and int(key)!=0]
    yAxis2 = [value for key, value in dictionary2.items() if int(key)%50==0 and int(key)!=0]
    
    plt.grid(True)

    ## LINE GRAPH ##
    plt.plot(xAxis2,yAxis2, color='maroon', marker='o')
    plt.xlabel('Frame')
    plt.ylabel('Ultimate Strength Percentile (%)')

    plt.show()
