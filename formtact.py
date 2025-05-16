import random
import os
os.system('cls')


def preplay():
    print("\n=== FAHAD AND LEMON FOOTBALL ===")


    print("\nCHOOSE YOUR TEAM:")
    print("A) REAL MADRID")
    print("B) LIVERPOOL")


    while True:
        ClubA = input("\nTeam : ").upper()
        if ClubA in ["A","B"]:
            break
        print("Invalid Team Choice!")


    ClubB = random.choice(["A","B"])
    while ClubB==ClubA:
        ClubB = random.choice(["A","B"])
        


    print("\nCHOOSE YOUR FORMATION:")
    print("A) 3-2-1 (Strong Defence)")
    print("B) 2-2-2 (Balanced formation)")
    print("C) 2-3-1 (High mid control)")

    while True:
        formation = input("\nFormation : ").upper()
        if formation in ["A", "B", "C"]:
            break
        print("Invalid Formation Choice!")
        
    ai_form = random.choice(["A", "B", "C"])

    print("\nCHOOSE YOUR DEFENCE TACTIC:")

    print("A) Backtrack")
    if formation=="A":
        print("B) Low Block")
    elif formation=="B":
        print("C) Switch Width")
    else:
        print("D) Holding Mid")

    while True:
        hometactd = input("\nTactic : ").upper()
        if formation=="A" and hometactd in ["A","B"]:
            break
        elif formation=="B" and hometactd in ["A","C"]:
            break
        elif formation=="C" and hometactd in ["A","D"]:
            break
        print("Invalid TACTIC Choice!")
        



    print("\nCHOOSE YOUR ATTACK TACTIC:")

    print("A) High Line")
    if formation=="A":
        print("B) Supporting Wingbacks")
    elif formation=="B":
        print("C) Shadow Striker")
    else:
        print("D) Hug The Line")
   

    while True:
        hometacta = input("\nTactic : ").upper()
        if formation=="A" and hometacta in ["A","B"]:
            break
        elif formation=="B" and hometacta in ["A","C"]:
            break
        elif formation=="C" and hometacta in ["A","D"]:
            break
        print("Invalid TACTIC Choice!")
        
    if ai_form=="A":
        awaytactd = random.choice(["A", "B"])
    elif ai_form=="B":
        awaytactd = random.choice(["A", "C"])
    else:
        awaytactd = random.choice(["A", "D"])

    if ai_form=="A":
        awaytacta = random.choice(["A", "B"])
    elif ai_form=="B":
        awaytacta = random.choice(["A", "C"])
    else:
        awaytacta = random.choice(["A", "D"])


    print("\nYOUR SETUP:")
    print(f"Formation: {'3-2-1' if formation == 'A' else '2-2-2' if formation == 'B' else '2-3-1'}")

    print("\nAI OPPONENT SETUP:")
    print(f"Formation: {'3-2-1' if ai_form == 'A' else '2-2-2' if ai_form == 'B' else '2-3-1'}")

    print("\nAi OPp SETUP:")
    print(f"TACT1 Ai: {'BT' if awaytactd == 'A' else 'LB' if awaytactd == 'B'  else 'SW' if awaytactd == 'C' else 'HM'}")

    print("\nAI OPPONENT SETUP:")
    print(f"TACT2 Ai: {'HL' if awaytacta == 'A' else 'SWB' if awaytacta == 'B'  else 'SS' if awaytacta == 'C' else 'HTL'}")

    return ClubA,ClubB,formation,ai_form,hometactd,hometacta,awaytacta,awaytactd


