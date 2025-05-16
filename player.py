from bs4 import BeautifulSoup
import requests
import os

roster = []
class Player:

    def __init__(self, Name, Pos, Kit, OVR, PAC, SHO, PAS, DRI, DEF, PHY):
        self.Name = Name
        self.Club = "Unknown"
        self.Kit = Kit
        self.Pos = Pos
        self.OVR = OVR
        self.PAC = PAC
        self.SHO = SHO
        self.PAS = PAS
        self.DRI = DRI
        self.DEF = DEF
        self.PHY = PHY

    def __str__(self):
        return f"{self.Name} - {self.Pos} - {self.Club} - {self.Kit} - OVR: {self.OVR} - PAC: {self.PAC} - SHO: {self.SHO} - PAS: {self.PAS} - DRI: {self.DRI} - DEF: {self.DEF} - PHY: {self.PHY}"

class Goalie:

    def __init__(self, Name, Pos, Kit, OVR, DIV, HAN, KIC, REF, SPD, POS):
        self.Name = Name
        self.Club = "Unknown"
        self.Kit = Kit
        self.Pos = Pos
        self.OVR = OVR
        self.DIV = DIV
        self.HAN = HAN
        self.KIC = KIC
        self.REF = REF
        self.SPD = SPD
        self.POS = POS

    def __str__(self):
        return f"{self.Name} - {self.Pos} - {self.Club} - {self.Kit} - OVR: {self.OVR} - DIV: {self.DIV} -HAN: {self.HAN} - KIC: {self.KIC} - REF: {self.REF} - SPD: {self.SPD} - POS: {self.POS}"

def scrape():
    with open('web.txt', 'r') as file:
        for line in file:
            url = line.strip()
            if not url:
                continue
            
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.text, 'lxml')

                name_div = soup.find('div', class_='card-25-name')
                fullname = name_div.text.strip() if name_div else "Unknown"

                if len(fullname) <= 8:
                    name = fullname  # Keep short names
                else:
                    # Split on last space or hyphen
                    name = fullname.replace('-', ' ').split()[-1]
                    
                    # Special case for compound last names"
                    if len(name) <= 3 and len(fullname.split()) > 1:
                        name = ' '.join(fullname.split()[-2:])

                pos_div = soup.find('div', class_='card-25-position')
                pos = pos_div.text.strip() if pos_div else "Unknown"

                ovr_div = soup.find('div', class_='card-25-rating')
                ovr = int(ovr_div.text.strip()) if ovr_div else 0

                # club_tag = soup.find('a', href=lambda href: href and '/club/' in href)
                # club = club_tag.text.strip() if club_tag else "Unknown"

                stats_container = soup.find('div', class_='card-25-atts')
                if stats_container:
                    stat_elements = stats_container.find_all('div', class_=lambda c: c and 'att' in c)
                    stats = [int(stat.text.strip()) for stat in stat_elements if stat.text.strip().isdigit()]
                else:
                    stats = []

                if len(stats) >= 6:
                    pac, sho, pas, dri, deff, phy = stats[:6]
                else:
                    pac = sho = pas = dri = deff = phy = 0

                kit=len(roster)
                if pos=="GK":
                    PL = Goalie(name, "G", kit, ovr, pac, sho, pas, dri, deff, phy)
                elif "B" in pos:
                    PL = Player(name, "D", kit, ovr, pac, sho, pas, dri, deff, phy)
                elif "M" in pos:
                    PL = Player(name, "M", kit, ovr, pac, sho, pas, dri, deff, phy)
                else:
                    PL = Player(name, "A", kit, ovr, pac, sho, pas, dri, deff, phy)


                roster.append(PL)
                path="roster.txt"
                
                with open(path,"a") as file:
                    file.write("\n" + str(PL))

            except Exception as e:
                print(f" Failed {url}: {str(e)}")
                continue
    print("Roster Loaded")

# def printrsoter():
#     for x in range(0,len(roster)):
#         print(roster[x].Name)

