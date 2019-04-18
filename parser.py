import requests

class Parser():
    def __init__(self, input):
        self.parse_dict = {}
        self.name = ""
        self.role = ""
        self.server = ""
        self.region = ""
        #1 arg e.g. Feni
        self.name = input.split(" ")[0].capitalize()
        #2+ args e.g. Feni / Feni nagrand / Feni nagrand-EU / Feni nagrand-EU hps / Feni hps
        if len(input.split(" ")) > 1:
            #role e.g. Feni hps
            if input.split(" ")[1] in ["dps", "hps", "bossdps", "tankhps", "playerspeed"]:
                self.role = input.split(" ")[1]
            else:
                #two-part server name + region e.g. Spinlik defias-brotherhood-eu
                if len(input.split(" ")[1].split("-")) > 2:
                    self.server = input.split(" ")[1].split("-")[0] + "-" + input.split(" ")[1].split("-")[1]
                    self.region = input.split(" ")[1].split("-")[2]
                #one-part server + region e.g. Feni nagrand-eu
                elif len(input.split(" ")[1].split("-")) > 1:
                    if input.split(" ")[1].split("-")[1].lower() in ["eu", "us"]:
                        self.server = input.split(" ")[1].split("-")[0]
                        self.region = input.split(" ")[1].split("-")[1]
                    else:
                        self.server = input.split(" ")[1]
            #if server + role given
            if len(input.split(" ")) > 2:
                if input.split(" ")[2] in ["dps", "hps", "bossdps", "tankhps", "playerspeed"]:
                    self.role = input.split(" ")[2]
        if not self.role:
            self.role = "dps"
        if not self.server:
            self.server = "Nagrand"
        if not self.region:
            self.region = "EU"
        Parser.getParses(self, self.name, self.server, self.region, self.role, self.parse_dict)


    def getParses(self, name, server, region, role, dict):
        print(f"Retrieving data for {self.name}-{self.server} {self.region} for {self.role}")
        r = requests.get(f"https://www.warcraftlogs.com:443/v1/rankings/character/{self.name}/{self.server}/{self.region}?zone=21&metric={self.role}&api_key=e77e3ecb6ac0bcafe8a49c63dbe990e3")
        if r.status_code != requests.codes.ok:
            print("Unable to find parses for the data provided")
            return None
        print("Data retrieved")

        #can't be arsed using collections.defaultdict lel
        for i in r.json():
            name = i["encounterName"]
            if name not in self.parse_dict.keys():
                self.parse_dict[name] = {"rank":99999}

        for i in r.json():
            name = i["encounterName"]
            if self.parse_dict[name]["rank"] > i["rank"] and i["difficulty"] == 5:
                self.parse_dict[name] = {"rank":i["rank"],"outOf":i["outOf"],"percentile":i["percentile"]}

        print(f"{self.name}\'s top parses as {self.role} are: ")
        for k, v in self.parse_dict.items():
            if v['percentile'] > 90:
                print(f"{k} : rank {v['rank']} out of {v['outOf']}, {v['percentile']} percentile")

if __name__ == "__main__":
    print("Enter character name + role (dps, hps, bossdps, tankhps, playerspeed)\n")
    Parser(input())
