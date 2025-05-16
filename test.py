from player import roster
from player import Player,Goalie
import random


def resolveGK(Goalie,Attacker):
    for i in range(0,11):
        GoalieStat = random.choice([Goalie.POS, Goalie.REF, Goalie.DIV])
        total=Attacker.SHO+GoalieStat
        wheel=random.randint(1,total)
        if wheel<=Attacker.SHO:
                print("Attacker Wins")
        else:
             print("Goalie Wins")
        print(f"Wheel={wheel}")
        print(f"Att={Attacker.SHO}")
        print(f"Def={GoalieStat}")
        print("-" * 20)
    
def main():
    player= Player("Att","A","4",89,89,87,82,88,45,75)
    goalie= Goalie("Gk","G","111",89,85,89,76,90,46,88)
    resolveGK(goalie,player)


if __name__ == "__main__":
    main()