import main


class State:
    def __init__(self):
        self.transitions = None

    def run(self):
        assert 0, "Not implemented"

    def next(self, cmd):
        if cmd in self.transitions:
            return self.transitions[cmd]
        else:
            raise "Invalid input to state"

class StateMachine:
    def __init__(self, initial_state):
        self.current_state = initial_state
        self.current_state.run()

    def get_input(self):
        '''
        modify get_input to accept an argument to tell whether to get an input command?
        pass in custom input string (eg. "press any key to continue" instead of "Input:")
        '''
        exit = False
        while exit == False:
            cmd = input("Input: ")
            if(cmd == "exit"):
                exit = True
            self.current_state = self.current_state.next(cmd)
            self.current_state.run()

class Loading(State):
    def run(self):
        player_database = main.Player_Database()
        event_list = main.Event_List()

        # print("Press any key to continue.")

    def next(self, cmd):
        if not self.transitions:
            self.transitions = {"any": Main_Menu()}
        return State.next(self, "any")

class Main_Menu(State):
    def run(self):
        print("Please select an option:")
        print("1: Load existing player data")
        print("2: Clear loaded player data")
        print("3: Add known aliases / alternate tags / troll tags")
        print("4: Select tournaments for calulation")
        print("5: Run Elo ratings calculation")
        print("6: View Elo ratings")
        print("7: Save Elo ratings as player data")
        print("8: Close program")

    def next(self, cmd):
        if not self.transitions:
            self.transitions = {"1": Load_Player_Data(), "2": Clear_Player_Data(), "3": Modify_Alias_List(), "4": Select_Tournaments(), "5": Run_Calculation(), "6": Print_Elo_Ratings(), "7": Save_Elo_Ratings(), "8": Exit()}
        return State.next(self, cmd)

class Load_Player_Data(State):
    def run(self):
        # Here there be code to load a player database from players.roy
        print("Player data has been loaded (NOT)")

    def next(self, cmd):
        if not self.transitions:
            self.transitions = {"only": Main_Menu()}
        return State.next(self,"only")

class Clear_Player_Data(State):
    def run(self):
        # Here there be code to load a player database from players.roy
        print("Player data has been deleted (NOT)")

    def next(self, cmd):
        if not self.transitions:
            self.transitions = {"only": Main_Menu()}
        return State.next(self,"only")

class Modify_Alias_List(State):
    def run(self):
        print("This functionality is not yet supported")
        print("Modify alias list by manually editing aliases.roy")

    def next(self, cmd):
        if not self.transitions:
            self.transitions = {"only": Main_Menu()}
        return State.next(self,"only")

class Select_Tournaments(State):
    def run(self):
        print("Here are the tournaments currently in the queue")
        print("Please note: Elo calculations will always be run in chronological order")
        print("Here are the tournaments")
        print("1: Return to main menu")
        print("2: Add tournament")
        print("3: Delete tournament")

    def next(self, cmd):
        if not self.transitions:
            self.transitions = {"1": Main_Menu(), "2": Add_Tournament(), "3": Delete_Tournament()}
        return State.next(self, cmd)

class Add_Tournament(State):
    def run(self):
        print("Please enter the name of the tournament you would like to add")
        print("Here is the list of tournaments currently in the queue")

    def next(self, cmd):
        if not self.transitions:
            self.transitions = {"only": Select_Tournaments()}
        return State.next(self,"only")

class Delete_Tournament(State):
    def run(self):
        print("Please enter the name of the tournament you would like to add")
        print("Kere is a list of the tournaments currently in the queue")

    def next(self, cmd):
        if not self.transitions:
            self.transitions = {"only": Select_Tournaments()}
        return State.next(self,"only")

class Run_Calculation(State):
    def run(self):
        print("Running elo calculation...")
        print("Running...")
        print("Results have been calculated")

    def next(self,cmd):
        if not self.transitions:
            self.transitions = {"only": Main_Menu()}
        return State.next(self,"only")

class Print_Elo_Ratings(State):
    def run(self):
        print("Wow look at these DANK ratings")
        print("Player: I'mDirtyDan    Rating: Infinity")
        print("Player: R0y            Rating: Over 9000")
        print("Player: lucASS         Rating: Probably negative")

    def next(self, cmd):
        if not self.transitions:
            self.transitions = {"only": Main_Menu()}
        return State.next(self,"only")

class Save_Elo_Ratings(State):
    def run(self):
        print("Ayy we do that bitch a save")

    def next(self, cmd):
        if not self.transitions:
            self.transitions = {"only": Main_Menu()}
        return State.next(self,"only")

class Exit(State):
    def run(self):
        print("Kay bye-bye, now!")

    def next(self, cmd):
        if not self.transitions:
            self.transitions = {"only": Main_Menu()}
        return State.next(self,"only")

class Elo_Calculator(StateMachine):
    def __init__(self):
        player_database = None
        event_list = None
        StateMachine.__init__(self, Loading())

    def get_input(self):
        while True:
            if type(self.current_state) == type(Loading()):
                self.current_state = Main_Menu()
                self.current_state.run()
            elif type(self.current_state) == type(Exit()):
                break
            else:
                StateMachine.get_input(self)






Elo_Calculator().get_input()
