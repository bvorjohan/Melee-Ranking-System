'''
reference:
http://math.bu.edu/people/mg/ratings/rs/node5.html

'''

 DEFAULT_RATING = 1000
 DEFAULT_MATCHES = 10





class Player:
    def __init__(self, name, Nf=DEFAULT_MATCHES, R0=DEFAULT_RATING):
        self.Nf = Nf
        self.R0 = R0
        self.name = name

    def get_rank(self):
        return self.R0

    def adj_rank(self, diff):
        self.R0 += diff

    def get_matches(self):
        return self
'''
    def adj_rank(self, K_full, match_list, player_database):
        # assumes match_array == [player_name_1, player_name_2, ]
        player_dict = {}
        relevant_matches = []
        for match in match_list[]:
            if (match[0] == self.name or match[1] == self.name):
                relevant_matches.append(match)
        del match_list
        K = calc_K(K_full, self.Nf, len(relevant_matches)
        opponent_counter = {}
        S = 0
        E = 0
        for match in relevant_matches:
            if match[1] == self.name:
                match[1] == match[0]
                match[0] == self.name
            if match[0] == match[2]:
                S += 1
            elif match[1] == match[2]:
                S += 0
            elif match[2] == "draw":
                S += .5
            else:
                print("error")
            E += We(self.R0, match[0], player_database)

        self.R0 += K*(S-E)

        def We(rank_0, player_name, player_database):
            return 1.0/(1.0+10**(-(rank_0 - player_database.get_player(player_name).get_rank())/400.0))

        def calc_K(K_full, Nf, matches):
            if K_full:
                return 800.0/(Nf+matches)
            else:
                return 400.0/(Nf+matches/2.0)
'''



class Player_Database:
    '''
    ref for useful instance builder tips: https://stackoverflow.com/questions/141545/how-to-overload-init-method-based-on-argument-type
    '''
    def __init__(self):
        self.data = {}

    def __init__(self, data):
        # process data
        pass

    def __init__(self, players):
        self.players = players

    def add_player(self, player_name, R0= DEFAULT_RATING, matches = DEFAULT_MATCHES):
        player_info = [player_name, R0, matches]
        self.data[player_name] = player_info

    def delete_player(self, player_name):
        try:
            del self.data[player_name]
            break
        except KeyError as e:
            print(player_name + "not found in data")

    def get_player(self, player_name):
        try:
            return self.data[player_name]
        except KeyError as e:
            self.add_player(player_name)
            return self.data[player_name]

    def event_rank_adjust(self, match_list, K_full = True):

        def We(rank_0, player_name, player_database):
            return 1.0/(1.0+10**(-(rank_0 - player_database.get_player(player_name).get_rank())/400.0))

        def calc_K(K_full, Nf, matches):
            if K_full:
                return 800.0/(Nf+matches)
            else:
                return 400.0/(Nf+matches/2.0)

        new_rankings = {}

        for player in self.data:
            # assumes match_array == [player_name_1, player_name_2, ]
            player_dict = {}
            relevant_matches = []
            for match in match_list[]:
                if (match[0] == player.name or match[1] == player.name):
                    relevant_matches.append(match)
            K = calc_K(K_full, player.Nf, len(relevant_matches)
            opponent_counter = {}
            S = 0
            E = 0
            for match in relevant_matches:
                if match[1] == self.name:
                    match[1] == match[0]
                    match[0] == self.name
                if match[0] == match[2]:
                    S += 1
                elif match[1] == match[2]:
                    S += 0
                elif match[2] == "draw":
                    S += .5
                else:
                    print("error")
                E += We(self.R0, match[0], player_database)

            self.R0 += K*(S-E)





def main():
