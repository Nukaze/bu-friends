import random
import sqlite3
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
    
def gen_qmark_list(_rangelimit):
    lastRange = 12
    questionMark = ["?,","?"]
    qLst = []
    for i in range(_rangelimit):
        rlm = _rangelimit
        if i+1 == _rangelimit:
            qLst.append(questionMark[1])
            break
        qLst.append(questionMark[0])
    qstr = "{}{}".format("?",", ?"*(rlm-1))
    return qLst, qstr
    
# quiz = get_MbtiQuizTH()
# selectist = [2, 3, 4, 5, 7, 9, 12, 14, 15, 19, 23, 25, 26, 27, 29, 31, 32, 33, 35, 36, 37]
# randLst = random.sample(range(len(selectist)),12)
# print(randLst)

# qstr = ""
# ql, qq= gen_qmark_list(12)
# print(ql)
# print(qq)
# print(len(qq))
