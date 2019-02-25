from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        pegs = []
        peg1 = []
        peg2 = []
        peg3 = []

        txt = self.kb.facts

        for f in txt:
            pred = f.statement.predicate
            if pred and pred == "on":
                fact = f.statement.terms
                if str(fact[1]) == "peg1":
                    disk = str(fact[0])
                    if disk == 'disk1':
                        peg1.append(1)
                    if disk == 'disk2':
                        peg1.append(2)
                    if disk == 'disk3':
                        peg1.append(3)
                elif str(fact[1]) == "peg2":
                    disk = str(fact[0])
                    if disk == 'disk1':
                        peg2.append(1)
                    if disk == 'disk2':
                        peg2.append(2)
                    if disk == 'disk3':
                        peg2.append(3)
                elif str(fact[1]) == "peg3":
                    disk = str(fact[0])
                    if disk == "disk1":
                        peg3.append(1)
                    if disk == "disk2":
                        peg3.append(2)
                    if disk == "disk3":
                        peg3.append(3)
                peg1.sort()
                peg2.sort()
                peg3.sort()
        pegs.append(tuple(peg1))
        pegs.append(tuple(peg2))
        pegs.append(tuple(peg3))

        return tuple(pegs)


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        txt = movable_statement.terms
        current_state = self.getGameState()

        old_fact_1 = ["on", txt[0], txt[1]]
        old_fact_2 = ["top", txt[0], txt[1]]

        self.kb.kb_retract(Fact(old_fact_1))
        self.kb.kb_retract(Fact(old_fact_2))

        new_fact_1 = ["on", txt[0], txt[2]]
        new_fact_2 = ["top", txt[0], txt[2]]

        self.kb.kb_assert(Fact(new_fact_1))
        self.kb.kb_assert(Fact(new_fact_2))



        #change top and intial
        initial = str(txt[1])
        initial_peg = 0
        if initial == "peg1":
            initial_peg = 1
        elif initial == "peg2":
            initial_peg = 2
        else:
            initial_peg = 3

        peg = current_state[initial_peg - 1]

        if len(peg) == 0 or len(peg) == 1:
            new_fact = ["empty", txt[1]]
            self.kb.kb_assert(Fact(new_fact))
        else:
            new_top = "disk" + str(peg[1])
            new_fact = ["top", Term(new_top), txt[1]]
            self.kb.kb_assert(Fact(new_fact))


        # change top and target
        target = str(txt[2])
        target_peg = 0
        if target == "peg1":
            target_peg = 1
        elif target == "peg2":
            target_peg = 2
        else:
            target_peg = 3

        pegs = current_state[target_peg - 1]

        if len(pegs) == 0:
            new_fact = ["empty", txt[2]]
            self.kb.kb_retract(Fact(new_fact))
        else:
            old_top = "disk" + str(pegs[0])
            new_fact = ["top", Term(old_top), txt[2]]
            self.kb.kb_retract(Fact(new_fact))




    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here

        # fact: (position tile1 pos1 pos1)

        rows = []
        row1 = []
        row2 = []
        row3 = []

        txt = self.kb.facts
        empty_index = -1

        for f in txt:
            pred = f.statement.predicate
            if pred == "empty":
                empty_index = int(str(fact[0])[-1])
                fact = f.statement.terms
                if str(fact[1]) == "pos1":
                    row1.append(-1)
                if str(fact[1]) == "pos2":
                    row2.append(-1)
                if str(fact[1]) == "pos3":
                    row3.append(-1)
            if pred == "position":
                fact = f.statement.terms
                if str(fact[2]) == "pos1":
                    disk = str(fact[0])
                    if disk == 'tile1':
                        row1.append(1)
                    if disk == 'tile2':
                        row1.append(2)
                    if disk == 'tile3':
                        row1.append(3)
                    if disk == 'tile4':
                        row1.append(4)
                    if disk == 'tile5':
                        row1.append(5)
                    if disk == 'tile6':
                        row1.append(6)
                    if disk == 'tile7':
                        row1.append(7)
                    if disk == 'tile8':
                        row1.append(8)
                if str(fact[2]) == "pos2":
                    disk = str(fact[0])
                    if disk == 'tile1':
                        row2.append(1)
                    if disk == 'tile2':
                        row2.append(2)
                    if disk == 'tile3':
                        row2.append(3)
                    if disk == 'tile4':
                        row2.append(4)
                    if disk == 'tile5':
                        row2.append(5)
                    if disk == 'tile6':
                        row2.append(6)
                    if disk == 'tile7':
                        row2.append(7)
                    if disk == 'tile8':
                        row2.append(8)
                if str(fact[2]) == "pos3":
                    disk = str(fact[0])
                    if disk == 'tile1':
                        row3.append(1)
                    if disk == 'tile2':
                        row3.append(2)
                    if disk == 'tile3':
                        row3.append(3)
                    if disk == 'tile4':
                        row3.append(4)
                    if disk == 'tile5':
                        row3.append(5)
                    if disk == 'tile6':
                        row3.append(6)
                    if disk == 'tile7':
                        row3.append(7)
                    if disk == 'tile8':
                        row3.append(8)
        rows.append(tuple(row1))
        rows.append(tuple(row2))
        rows.append(tuple(row3))

        return tuple(rows)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        txt = movable_statement.terms
        tile = txt[0]

        adjacents = []

        for f in self.kb.facts:
            pred = f.statement.predicate
            if pred == "adjacent":
                terms = f.statement.terms
                if terms[0] == tile:
                    adjacents.append(terms[1])
                if terms[1] == tile:
                    adjacents.append(terms[0])

        for a in adjacents:
            fact1 = ["adjacent", a, tile]
            fact2 = ["adjacent", tile, a]
            self.kb.kb_retract(Fact(fact1))
            self.kb.kb_retract(Fact(fact2))

        old_fact_1 = ["position", txt[0], txt[1], txt[2]]
        old_fact_2 = ["empty", txt[3], txt[4]]

        self.kb.kb_retract(Fact(old_fact_1))
        self.kb.kb_retract(Fact(old_fact_2))

        new_fact_1 = ["position", txt[0], txt[3], txt[4]]
        new_fact_2 = ["empty", txt[1], txt[2]]

        self.kb.kb_assert(Fact(new_fact_1))
        self.kb.kb_assert(Fact(new_fact_2))


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
