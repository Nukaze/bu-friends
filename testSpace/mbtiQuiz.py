import random
def get_MbtiQuizEN():
    return [["I","E","Expend energy, enjoy groups or b. conserve energy, enjoy one-on-one"],
            ["I","E","Are u out-going?"],
            ["I","E","Are u out-going?"],
            ["I","E","Are u out-going?"],
            ["I","E","Are u out-going?"],
            ["I","E","Are u out-going?"],
            ["I","E","Are u out-going?"],
            
            ["N","S","Which one you trust Present or Future?"],
            ["N","S","Which one you trust Present or Future?"],
            ["N","S","Which one you trust Present or Future?"],
            ["N","S","Which one you trust Present or Future?"],
            ["N","S","Which one you trust Present or Future?"],
            ["N","S","Which one you trust Present or Future?"],
            ["N","S","Which one you trust Present or Future?"],
            
            ["F","T","When someone make mistake what you do to help?"],
            ["F","T","When someone make mistake what you do to help?"],
            ["F","T","When someone make mistake what you do to help?"],
            ["F","T","When someone make mistake what you do to help?"],
            ["F","T","When someone make mistake what you do to help?"],
            ["F","T","When someone make mistake what you do to help?"],
            ["F","T","When someone make mistake what you do to help?"],
            
            ["P","J","Have you wake-up instanly when alarm is clocking"],
            ["P","J","Have you wake-up instanly when alarm is clocking"],
            ["P","J","Have you wake-up instanly when alarm is clocking"],
            ["P","J","Have you wake-up instanly when alarm is clocking"],
            ["P","J","Have you wake-up instanly when alarm is clocking"],
            ["P","J","Have you wake-up instanly when alarm is clocking"],
            ["P","J","Have you wake-up instanly when alarm is clocking"]    
]
def get_MbtiQuizTH():
     return [["I","E","1 เพลิดเพลินกับเพื่อนกลุ่มใหญ่ หรือเพลิดเพลินแบบเพื่อนกลุ่มเล็ก ๆ "],
            ["I","E","2 Are u out-going?"],
            ["I","E","3 Are u out-going?"],
            ["I","E","4 Are u out-going?"],
            ["I","E","5 Are u out-going?"],
            ["I","E","6 Are u out-going?"],
            ["I","E","7 Are u out-going?"],
            
            ["N","S","8 Which one you trust Present or Future?"],
            ["N","S","9 Which one you trust Present or Future?"],
            ["N","S","10 Which one you trust Present or Future?"],
            ["N","S","11 Which one you trust Present or Future?"],
            ["N","S","12 Which one you trust Present or Future?"],
            ["N","S","13 Which one you trust Present or Future?"],
            ["N","S","14 Which one you trust Present or Future?"],
            
            ["F","T","15 When someone make mistake what you do to help?"],
            ["F","T","16 When someone make mistake what you do to help?"],
            ["F","T","17 When someone make mistake what you do to help?"],
            ["F","T","18 When someone make mistake what you do to help?"],
            ["F","T","19 When someone make mistake what you do to help?"],
            ["F","T","20 When someone make mistake what you do to help?"],
            ["F","T","21 When someone make mistake what you do to help?"],
            
            ["P","J","22 Have you wake-up instanly when alarm is clocking"],
            ["P","J","23 Have you wake-up instanly when alarm is clocking"],
            ["P","J","24 Have you wake-up instanly when alarm is clocking"],
            ["P","J","25 Have you wake-up instanly when alarm is clocking"],
            ["P","J","26 Have you wake-up instanly when alarm is clocking"],
            ["P","J","27 Have you wake-up instanly when alarm is clocking"],
            ["P","J","28 Have you wake-up instanly when alarm is clocking"]    
]
    
    
lst = [1,2,3,4,5,6]    
quiz = get_MbtiQuizTH()
randLst = random.sample(range(len(quiz)),len(quiz))
