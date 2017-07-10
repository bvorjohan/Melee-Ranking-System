import math
import challonge
# import inspect
import datetime
import pytz

utc = pytz.UTC
challonge.set_credentials("roy696969", "jTdkaINmF3ppeBZRYPZeccGLEiYunE4uBXnU7W4Y")
# # help(challonge.participants)
# tourney = challonge.matches.index("runback-43")
# # print(tourney[0])
# print(tourney[0]["player1-id"])
# player1 = challonge.participants.show("runback-45",56495007)
# print(player1)
# print()
# print(player1["name"])
# Tell pychallonge about your [CHALLONGE! API credentials](http://api.challonge.com/v1).
# challonge.set_credentials("roy696969", "jTdkaINmF3ppeBZRYPZeccGLEiYunE4uBXnU7W4Y")

# Retrieve a tournament by its id (or its url).
# tournament = challonge.tournaments.show("runback-43")

# Tournaments, matches, and participants are all represented as normal Python dicts.
# print(tournament["id"]) # 3272
# print(tournament["name"]) # My Awesome Tournament
# print(tournament["started-at"]) # None
'''
    # Retrieve the participants for a given tournament.
    participants = challonge.participants.index(tournament["id"])
    print(len(participants)) # 13

    # Start the tournament and retrieve the updated information to see the effects
    # of the change.
    challonge.tournaments.start(tournament["id"])
    tournament = challonge.tournaments.show(tournament["id"])
    print(tournament["started-at"]) # 2011-07-31 16:16:02-04:00
'''


DEFAULT_RATING = 1000
DEFAULT_MATCHES = 0
MAX_NAME_LENGTH = 15
PREFIXES = ["|","KH","FX", "SG7", "Uncle", "_", " ", "HTLB"]
# ALIASES = {"imdirtydan": "I'mDirtyDan", "luca$$": "Lucid", "tal": "Caligula", "Calligula": "Caligula"}

class Player:
    def __init__(self, name, Nf=DEFAULT_MATCHES, R0=DEFAULT_RATING):
        self.Nf = Nf
        self.R0 = R0
        self.name = name

    def __str__(self):
	    return "Name: " + self.name +" "*(15-len(self.name)) + " Rating: " + str(int(self.R0)) + " "*(4-int(math.log10(self.R0+1))) + " Matches: " + str(self.Nf)

    def We(self, other):
        #other = player_database.get_player(player_name)
        return 1.0/(1.0+10**(-(self.R0 - other.get_rank())/400.0))

    def get_rank(self):
        return self.R0

    def adj_rank(self, diff):
        self.R0 += diff

    def get_matches(self):
        return self

    def add_matches(self, num_matches):
        self.Nf += num_matches

class Player_Database:
    '''
    ref for useful instance builder tips: https://stackoverflow.com/questions/141545/how-to-overload-init-method-based-on-argument-type
    '''
    def __init__(self):
        self.data = {}
        self.aliases = self.open_aliases(filename = "aliases.roy")


    def strip_prefixes(self, match_data, prefixes):
        matches = match_data[:]
        for match in range(len(matches)):
            # print(self.formatted_match_data[match])
            for player_name in range(len(matches[match])):
                for prefix in prefixes:
                    # print(prefix, "|||", self.formatted_match_data[match][player_name], "|||", self.formatted_match_data[match][player_name][0:len(prefix)])
                    if match_data[match][player_name][0:len(prefix)] == prefix:
                        # print("Truuuuuuu")
                        match_data[match][player_name] = match_data[match][player_name][len(prefix):]
        return match_data

    def remove_troll_tags(self, match_data):
        for match in range(len(match_data)):
            # print(match)
            for player in range(len(match_data[match])):
                # print("Player to be stripped: " + player)
                for alias in self.aliases:
                    if match_data[match][player].lower() == alias.lower():
                        # print("Swapped '" + player + "' with '" + self.aliases[alias] + "'")
                        # input()
                        match_data[match][player] = self.aliases[alias]
        return match_data

    def sterilize_match_data(self, match_data, prefixes = PREFIXES):
        for _ in range(3):
            match_data = self.strip_prefixes(match_data, prefixes)
        match_data = self.remove_troll_tags(match_data)

        return match_data

    def add_player(self, player_name, R0= DEFAULT_RATING, matches = DEFAULT_MATCHES):
        player = Player(player_name, matches, R0)
        # print(player)
        if player_name in self.data:
            print("Player already in database!")
        else:
            self.data[player_name] = player

    def add_players(self, player_name_list):
        for player_name in player_name_list:
            self.add_player(player_name)

    def delete_player(self, player_name):
        try:
            del self.data[player_name]
        except KeyError as e:
            print(player_name + "not found in data")

    def get_player(self, player_name):
        try:
            return self.data[player_name]
        except KeyError as e:
            for player in self.data:
                if player.lower() == player_name.lower():
                    return self.data[player]
            self.add_player(player_name)
            return self.data[player_name]

    def save_aliases(self, alias_dictionary, filename = "aliases.roy"):
        with open(filename, "w") as file:
            for alias in alias_dictionary:
                file.write( alias + "%" + alias_dictionary[alias] + "\n")

    def open_aliases(self, filename = "aliases.roy"):
        alias_dictionary = {}
        with open(filename, "r") as file:
            for line in file:
                aliases = line.split("%")
                # print(aliases)
                alias_dictionary[aliases[0].strip()] = aliases[1].strip()
        return alias_dictionary

    def event_rank_adjust(self, match_list, K_full = True):

        def calc_K(K_full, Nf, matches):
            if Nf+matches == 0:
                return 0
            elif K_full:
                return 800.0/(Nf+matches)
            else:
                return 400.0/(Nf+matches/2.0)
        # print("Calculating a new event...")
        ranking_adj = {}
        # print(self.data)
        for match in match_list:
            for i in range(2):
                if not(match[i] in self.data):
                    # print(match[i])
                    # input("Press enter...")
                    self.add_player(match[i])

        for player_name in self.data.copy():
            # print(player_name)
            player = self.data[player_name]
            # assumes match_array == [player_name_1, player_name_2, winning_player_name]
            # print(player)
            player_dict = {}
            relevant_matches = []
            for match in match_list:
                if (match[0] == player.name or match[1] == player.name):
                    relevant_matches.append(match)
            K = calc_K(K_full, player.Nf, len(relevant_matches))
            opponent_counter = {}
            S = 0
            E = 0
            # print(player.name)
            for match in relevant_matches:
                # print(match)
                # print(match[1],player.name)
                if match[1] == player.name:
                    match[1] = match[0]
                    match[0] = player.name
                # print(match)
                if match[0] == match[2]:
                    S += 1
                elif match[1] == match[2]:
                    S += 0
                elif match[2] == "draw":
                    S += .5
                else:
                    print("error")
                    pass
                E += player.We(self.get_player(match[1]))
                try:
                    opponent_counter[match[1]] += 1
                except KeyError as e:
                    opponent_counter[match[1]] = 1
                '''
                more_than_once = False
                if opponent_counter.max() > 1:
                    more_than_once = True
                '''

                adj_factor = 0 # change per chess method
            # print(player.name, E)
            adj_factor = 0
            ranking_adj[player.name] = K*(S-E) + adj_factor
            player.add_matches(len(relevant_matches))

        for player_name in self.data:
            player = self.data[player_name]
            try:
                player.R0 += ranking_adj[player.name]
            except KeyError:
                pass

    def multi_event_rank_adjust(self, event_list, K_full = True):
        for event in event_list:
            print("Running event: " + event.id)
            match_data = self.sterilize_match_data(event.match_data)
            self.event_rank_adjust(event.match_data, K_full = K_full)

    def event_list_rank_adjust(self, event_list, K_full = True):
        sorted_list = []
        event_list_copy = dict(event_list.events)
        earliest_date = datetime.datetime.now()
        earliest_event = Event("",earliest_date,[[]])

        while len(event_list_copy) > 0:
            for event_name in event_list_copy:
                event = event_list_copy[event_name]
                if utc.localize(event.date) < utc.localize(earliest_date):
                    earliest_date = event.date
                    earliest_event = event
                    earliest_event_name = event.id
            sorted_list.append(earliest_event)
            del event_list_copy[earliest_event_name]
            earliest_date = datetime.datetime.now()
            earliest_event = Event("",earliest_date,[[]])

        self.multi_event_rank_adjust(sorted_list)

    def list_all_players(self):
        for player in self.data:
            print("Player: " + player)

    def list_player_stats(self, player_name):
        try:
            print(self.data[player_name])
        except KeyError as e:
            print("Player not found")

    def list_all_player_stats(self):
        data_copy = self.data.copy()
        while len(data_copy) > 0:
            temp_max_elo = 0
            temp_max_player_name = ""
            for player_name in data_copy:
                if data_copy[player_name].R0 > temp_max_elo:
                    temp_max_elo = data_copy[player_name].R0
                    temp_max_player_name = player_name

            print(data_copy[temp_max_player_name])
            del data_copy[temp_max_player_name]

    def save_player_data(self, filename = "players.roy"):
        file = open(filename, "w")
        for player_name in self.data:
            player = self.data[player_name]
            file.write(str(player)+ "\n")
        file.close()

    def load_player_data(self, filename = "players.roy"):
        loaded_player_data = {}
        with open(filename, "r") as file:
            lines = file.readlines()
        for line in lines:
            # print("Line: " + line)
            # Extra whitespace
            line = line + " "*6
            try:
                name_index = line.index("Name:")
                rating_index = line.index("Rating:")
                matches_index = line.index("Matches:")
            except ValueError as e:
                # No Data
                pass
            else:
                try:
                    name = line[name_index+6:name_index+6+MAX_NAME_LENGTH].strip()
                    # print("Name: " + name)
                    rating = int(line[rating_index+8:rating_index+12].strip())
                    matches = int(line[rating_index+9:rating_index + 14].strip())
                except ValueError as e:
                    # Unreadable Data
                    pass
                else:
                    # Updates data in dataframe (adds new players, updates repeated players, retains unchanged players)
                    self.data.update({name:Player(name, matches, rating)})
                    # print()

class Event:
    def __init__(self, name, date, data):
        if len(name)>0:
            print("Loading event '" + name + "'")
        self.id = name
        self.date = date
        self.match_data = data
        '''
        self.strip_prefixes()
        self.strip_prefixes()
        self.strip_prefixes()
        self.get_rid_of_troll_tags() # should be moved to player database
        '''

    @classmethod
    def from_challonge(cls,tourney_id):
        print("Pulling Challonge data for " + tourney_id)
        # self.id = tourney_id
        date = challonge.tournaments.show(tourney_id)["started-at"]
        raw_match_data = challonge.matches.index(tourney_id)
        # self.formatted_match_data = []
        formatted_match_data = cls.parse_match_data(raw_match_data,tourney_id)
        # self.strip_prefixes()
        # self.strip_prefixes()
        # self.strip_prefixes()
        # self.get_rid_of_troll_tags()
        del raw_match_data
        # del self.raw_participants
        return cls(tourney_id, date, formatted_match_data)

    def get_rid_of_troll_tags(self, alias_dict):
        for match in range(len(self.match_data)):
            for player_name in range(len(self.match_data[match])):
                if self.match_data[match][player_name].lower() in ALIASES:
                    # print("----Replacing " + self.formatted_match_data[match][player_name])
                    self.match_data[match][player_name] = ALIASES[self.match_data[match][player_name].lower()]


    def strip_prefixes(self):
        for match in range(len(self.match_data)):
            # print(self.formatted_match_data[match])
            for player_name in range(len(self.match_data[match])):
                for prefix in PREFIXES:
                    # print(prefix, "|||", self.formatted_match_data[match][player_name], "|||", self.formatted_match_data[match][player_name][0:len(prefix)])
                    if self.match_data[match][player_name][0:len(prefix)] == prefix:
                        # print("Truuuuuuu")
                        self.match_data[match][player_name] = self.match_data[match][player_name][len(prefix):]

    def save_event(self):
        pass

    def load_event(self):
        pass

    def get_matches(self):
        return self.match_data


    def print_all_matches(self):
        print("-----------------------------------")
        for match in self.match_data:
            print(match)

    @classmethod
    def parse_match_data(cls, raw_match_data, id):
        stripped_data = []
        known_player_ids = {}
        formatted_match_data = []
        for match in range(len(raw_match_data)):
            # if(match<6):
                # print("---------------------------------")
                # print(self.raw_match_data[match])
            formatted_match_data.append([])
            player_0_id = raw_match_data[match]["player1-id"]
            player_1_id = raw_match_data[match]["player2-id"]
            # print(match)
            # print(formatted_match_data[match])
            # print(player_0_id)
            # print(player_1_id)
            # break
            if player_0_id in known_player_ids:
                formatted_match_data[match].append(known_player_ids[player_0_id])
            else:
                formatted_match_data[match].append(challonge.participants.show(id, player_0_id)["display-name"])
                known_player_ids[player_0_id] = formatted_match_data[match][0]


            if player_1_id in known_player_ids:
                formatted_match_data[match].append(known_player_ids[player_1_id])
            else:
                formatted_match_data[match].append(challonge.participants.show(id, player_1_id)["display-name"])
                known_player_ids[player_1_id] = formatted_match_data[match][1]
            formatted_match_data[match].append(known_player_ids[raw_match_data[match]["winner-id"]])
            # print(self.formatted_match_data[match])
        return formatted_match_data


    def get_match_data(self):
        stripped_data = []
        known_player_ids = {}
        for match in range(len(self.raw_match_data)):
            # if(match<6):
                # print("---------------------------------")
                # print(self.raw_match_data[match])
            self.formatted_match_data.append([])
            player_0_id = self.raw_match_data[match]["player1-id"]
            player_1_id = self.raw_match_data[match]["player2-id"]

            # print(player_0_id)
            # print(player_1_id)
            # break
            if player_0_id in known_player_ids:
                self.formatted_match_data[match].append(known_player_ids[player_0_id])
            else:
                self.formatted_match_data[match].append(challonge.participants.show(self.id, player_0_id)["display-name"])
                known_player_ids[player_0_id] = self.formatted_match_data[match][0]


            if player_1_id in known_player_ids:
                self.formatted_match_data[match].append(known_player_ids[player_1_id])
            else:
                self.formatted_match_data[match].append(challonge.participants.show(self.id, player_1_id)["display-name"])
                known_player_ids[player_1_id] = self.formatted_match_data[match][1]
            self.formatted_match_data[match].append(known_player_ids[self.raw_match_data[match]["winner-id"]])
            # print(self.formatted_match_data[match])

    def get_id(self):
        return self.id

class Event_List:
    loaded_events = {}
    def __init__(self):
        self.events = {}
        # print(len(self.loaded_events))
        if len(self.loaded_events) == 0:
            # print("Truuuuuuuuuu")
            Event_List.load_events_class()

    @classmethod
    def load_events_class(cls, filename = "events.roy"):
        with open(filename, "r") as file:
            lines = file.readlines()
            events = {}
            state = 0
            name = ""
            date = None
            matches = []
            # print(matches)
            for line in lines:
                # print("State: " + str(state))
                if state == 0: # find name state
                    try:
                        name_index = line.index("Event: ")
                    except ValueError as e:
                        # no event
                        pass
                    else:
                        name = line[name_index+7:].strip()
                        state = 1

                elif state == 1:
                    try: date_index = line.index("Date: ")
                    except ValueError as e:
                    #no event
                        pass
                    else:
                        date = datetime.datetime.strptime(line[date_index+6:date_index+24], "%Y-%m-%d %H:%M:%S")
                        state = 2

                elif state == 2:
                    try:
                        name0_index = line.index("Player 1: ")
                        name1_index = line.index("Player 2: ")
                        winner_index = line.index("Winner: ")
                        # print(name0_index)
                    except ValueError as e:
                        # no valid match data:
                        pass
                    else:
                        name0 = line[9:10+MAX_NAME_LENGTH].strip()
                        name1 = line[19+MAX_NAME_LENGTH:20+MAX_NAME_LENGTH*2].strip()
                        winner = line[28+MAX_NAME_LENGTH*2:29+MAX_NAME_LENGTH*3].strip()
                        # print(matches)
                        # print("----------------------------")
                        # print("First name: " + name0)
                        matches.append([name0,name1,winner])

                if line[0] == "-":
                    try:
                        cls.loaded_events.update({name:Event(name,date,matches)})
                    except:
                        pass
                    else:
                        pass
                    finally:
                        state = 0
                        matches = []

    @classmethod
    def add_event_class(cls, event):
        cls.loaded_events[event.id] = event

    def add_event(self, event):
        self.events[event.id] = event
        if event.id not in self.loaded_events:
            Event_List.add_event_class()

    def add_event_by_id(self, event_id):
        if event_id in self.loaded_events:
            print("Loading event '" + event_id + "' from local memory")
            self.events[event_id] = self.loaded_events[event_id]
        else:
            print("Loading event '" + event_id + "' from Challonge")
            self.events[event_id] = Event.from_challonge(event_id)
            self.loaded_events[event_id] = self.events[event_id]

    def add_events(self, events):
        for event in events:
            self.add_event(event)

    def load_events(self, filename = "events.roy"):
        with open(filename, "r") as file:
            lines = file.readlines()
            events = {}
            state = 0
            name = ""
            date = None
            matches = []
            # print(matches)
            for line in lines:
                # print("State: " + str(state))
                if state == 0: # find name state
                    try:
                        name_index = line.index("Event: ")
                    except ValueError as e:
                        # no event
                        pass
                    else:
                        name = line[name_index+7:].strip()
                        state = 1

                elif state == 1:
                    try: date_index = line.index("Date: ")
                    except ValueError as e:
                    #no event
                        pass
                    else:
                        date = datetime.datetime.strptime(line[date_index+6:date_index+24], "%Y-%m-%d %H:%M:%S")
                        state = 2

                elif state == 2:
                    try:
                        name0_index = line.index("Player 1: ")
                        name1_index = line.index("Player 2: ")
                        winner_index = line.index("Winner: ")
                        # print(name0_index)
                    except ValueError as e:
                        # no valid match data:
                        pass
                    else:
                        name0 = line[9:10+MAX_NAME_LENGTH].strip()
                        name1 = line[19+MAX_NAME_LENGTH:20+MAX_NAME_LENGTH*2].strip()
                        winner = line[28+MAX_NAME_LENGTH*2:29+MAX_NAME_LENGTH*3].strip()
                        # print(matches)
                        # print("----------------------------")
                        # print("First name: " + name0)
                        matches.append([name0,name1,winner])

                if line[0] == "-":
                    try:
                        self.events.update({name:Event(name,date,matches)})
                    except:
                        pass
                    else:
                        pass
                    finally:
                        state = 0
                        matches = []

    def print_event_names(self):
        for event in self.events:
            print(event)

    def save_events(self, filename = "events.roy"):
        pass # ILLEGAL METHOD - DO NOT USE FOR RISK OF LOSING LOCAL DATA
        with open(filename, "w") as file:
            for event in self.events:
                file.write("Event: " + self.events[event].get_id() + "\n")
                file.write("Date: " + str(self.events[event].date) + "\n")
                for match in self.events[event].get_matches():
                    file.write("Player 1: " + match[0] +" "*(15-len(match[0])) + "Player 2: " + match[1] +" "*(15-len(match[1])) + "Winner: " + match[2] +" "*(15-len(match[2])) + " "*6 + "\n")
                file.write("---------------------------------------\n")

    @classmethod
    def save_events_class(cls, filename = "events.roy"):
        with open(filename, "w") as file:
            for event in cls.loaded_events:
                file.write("Event: " + cls.loaded_events[event].get_id() + "\n")
                file.write("Date: " + str(cls.loaded_events[event].date) + "\n")
                for match in cls.loaded_events[event].get_matches():
                    file.write("Player 1: " + match[0] +" "*(15-len(match[0])) + "Player 2: " + match[1] +" "*(15-len(match[1])) + "Winner: " + match[2] +" "*(15-len(match[2])) + " "*6 + "\n")
                file.write("---------------------------------------\n")





def main():
    print()
    print()
    print("-----------------------------------------------------------------")



    df = Player_Database()
    # # df.add_player("Mijo")
    # # df.add_players(["LK","I'mDirtyDan"])
    # # Runbacc_0 = [["Mijo","I'mDirtyDan","I'mDirtyDan"],["LK","I'mDirtyDan","LK"],["Mijo","I'mDirtyDan","Mijo"],["Mijo","LK","LK"],["Felzarn","Mijo","Mijo"],["Felzarn","LK","LK"]]
    # # Runbacc_1 = [["Mijo","r0y","Mijo"],["LK","Mijo","LK"],["r0y","Felzarn","r0y"],["Mijo","LK","LK"],["Felzarn","Mijo","Mijo"],["r0y","Mijo","Mijo"]]
    # # print()
    # # print("Printing all player stats...")
    # # df.list_all_player_stats()
    # # print()
    # # df.event_rank_adjust(Runbacc_0)
    # # df.list_all_player_stats()
    # # print()
    # # for i in range(2000):
    # #     df.event_rank_adjust(Runbacc_1)
    # # df.list_all_player_stats()
    # # df.save_player_data("text.roy")
    # # df.open_player_data("text.roy")
    # #
    #
    # event_0 = Event("runback-42")
    # event_1 = Event("runback-43")
    # event_2 = Event("runback-44")
    # event_3 = Event("runback-45")
    # event_4 = Event("runback-46")
    # event_5 = Event("runback-47")
    # event_6 = Event("runback-48")
    # event_7 = Event("runback-49")
    #
    # # event_0.get_match_data()
    # # event_0.strip_prefixes()
    # # event_0.strip_prefixes()
    # # event_0.strip_prefixes()
    # # event_0.get_rid_of_troll_tags()
    # # event_0.print_all_matches()
    #
    # df.event_rank_adjust(event_0.formatted_match_data)
    # df.event_rank_adjust(event_1.formatted_match_data)
    # df.event_rank_adjust(event_2.formatted_match_data)
    # df.event_rank_adjust(event_3.formatted_match_data)
    # df.event_rank_adjust(event_4.formatted_match_data)
    # df.event_rank_adjust(event_5.formatted_match_data)
    # df.event_rank_adjust(event_6.formatted_match_data)
    # df.event_rank_adjust(event_7.formatted_match_data)
    #
    # df.list_all_player_stats()
    #
    # # df.save_aliases(ALIASES, "aliases.roy")
    # # print(df.aliases)
    # df.save_player_data()


    event_list = Event_List()


    # event_list.add_events([Event.from_challonge("runback-45"), Event.from_challonge("runback-43")])
    # event_list.save_events()
    # df.load_player_data()
    # df.list_all_player_stats()


    # event_list.load_events()

    # df.list_all_player_stats()
    event_list.add_event_by_id("runback-42")
    event_list.add_event_by_id("runback-43")
    event_list.add_event_by_id("runback-44")
    event_list.add_event_by_id("runback-45")
    event_list.add_event_by_id("runback-46")
    event_list.add_event_by_id("runback-47")
    event_list.add_event_by_id("runback-48")
    event_list.add_event_by_id("runback-49")
    event_list.save_events_class()
    df.event_list_rank_adjust(event_list)
    df.list_all_player_stats()
    df.save_player_data()

















if __name__ == "__main__":
    main()
