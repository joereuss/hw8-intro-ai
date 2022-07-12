import random
import copy
class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']
    bestState = []

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    
    #this function determines if the game is in the drop phase
    def isDropPhase(self, state):
        count = 0
        #determines by counting the number of pieces on the board
        for row in state:
            count += row.count('b') + row.count('r')
        if (count < 8):
            return True
        else:
            return False

    #the successor function asked to implement, whether in drop phase or not
    def succ(self, state):
        piece = self.my_piece
        drop_phase = self.isDropPhase(state)
        legal = list()
        
        #if drop phase, almost every space is legal as long as it's empty
        if (drop_phase):
            #iterate thru board, all empty spaces are legal
            for row in range(5):
                for col in range(5):
                    if (state[row][col]) == ' ':
                        legal.append((row, col))
                    else:
                        continue

        #if not, then only empty adjacent pieces are legal
        if not (drop_phase):
            legal = list()
            #iterate thru board:
            for row in range(5):
                for col in range(5):
                    if state[row][col] == piece:
                        #check row of for legal spaces
                        if col - 1 >= 0 and state[row][col - 1] == ' ':
                            legal.append(((row, col - 1), (row, col)))
                        if col + 1 < 5 and state[row][col + 1] == ' ':
                            legal.append(((row, col + 1), (row, col)))
                        
                        #check row above for legal spaces
                        if row - 1 >= 0 and state[row - 1][col] == ' ':
                            legal.append(((row - 1, col), (row, col)))
                            if col - 1 >= 0 and state[row - 1][col - 1] == ' ':
                                legal.append(((row - 1, col - 1) , (row, col)))
                            if col + 1 < 5 and state[row - 1][col + 1] == ' ':
                                legal.append(((row - 1, col + 1), (row, col)))
                        
                        #check row below for legal spaces
                        if row + 1 < 5 and state[row + 1][col] == ' ':
                            legal.append(((row + 1, col), (row, col)))
                            if col - 1 >= 0 and state[row + 1][col - 1] == ' ':
                                legal.append(((row + 1, col - 1) , (row, col)))
                            if col + 1 < 5 and state[row + 1][col + 1] == ' ':
                                legal.append(((row + 1, col + 1), (row, col)))
        

        return legal

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        #check for drop phase
        drop_phase = self.isDropPhase(state)
     
        #set up a list containing the different indicies between the new and old states
        diff = list()
        
        
        if not drop_phase:

            # chooses a piece to move and remove it from the board
            # (You may move this condition anywhere, just be sure to handle it)
            # 
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase!
            move = []
            #run minimax
            value, bestState = self.max_value(state, 0)
            
            #create a temporary state of the old state
            tempState = copy.deepcopy(state)

            #find the different indicies and add them to our list
            for i in range(5):
                if tempState[i] != bestState[i]:
                    for j in range(5):
                        if tempState[i][j] != bestState[i][j]:
                            diff.append((i, j))
            
            
            #this chunk of code determines which indicies indicate the removed
            #piece or the new/moved place of the piece
            if tempState[diff[0][0]][diff[0][1]] == ' ':
                #indicate the removed row/col
                rrow = diff[0][0]
                rcol = diff[0][1]
                #indicate the moved row/col
                row = diff[1][0]
                col = diff[1][1]
            else:
                #else vise versa
                rrow = diff[1][0]
                rcol = diff[1][1]
                row = diff[0][0]
                col = diff[0][1]
            
            #insert to move and return
            move.insert(1, (row, col))
            move.insert(0, (rrow, rcol))
            
            return move
  
        # implemented a minimax algorithm to play better
        move = []
        #create tempoary state to hold old state
        tempState = copy.deepcopy(state)

        #run minimax
        value, bestState = self.max_value(state, 0)

       #find differences between new and old states
        for i in range(5):
            if tempState[i] != bestState[i]:
                for j in range(5):
                    if tempState[i][j] != bestState[i][j]:
                        diff.append((i, j))
        
        
        #add them to move and return
        move.insert(0, (diff[0][0], diff[0][1]))

        return move


    #the max-value portion of minimax, used with the lecture slides
    def max_value(self, state, depth):
        #create temporary state to hold "old" state
        tempState = state
        
        #check if new state is terminal
        if (self.game_value(state) != 0):
            return self.game_value(state), state
        
        #if depth reached, stop recursion and start returning
        if (depth >= 3):
            return self.heuristic_game_value(state), state
        
        
        else:
            alpha = float(-99999)
            #generate successors
            succ = self.succ(state)
            
            #if drop phase then successors only have 1 index
            if self.isDropPhase(state):
                for s in succ:
                    tempState = copy.deepcopy(state)
                    tempState[s[0]][s[1]] = self.my_piece
                    val = self.min_value(tempState, depth + 1)

                    if (val[0] > alpha):
                        alpha = val[0]

                return alpha, tempState
        
            #if not drop phase then becomes a list of lists for moves, so a bit different
            else:
                for s in succ:
                    tempState = copy.deepcopy(state)
                    tempState[s[0][0]][s[0][1]] = self.my_piece
                    tempState[s[1][0]][s[1][1]] = ' '
                    val = self.min_value(tempState, depth + 1)
                    if (val[0] > alpha):
                        alpha = val[0]

                return alpha, tempState
        
    #min-value in minimax, based on lecture slides
    def min_value(self, state, depth):
        tempState = state
        
        #check if state is terminal
        if (self.game_value(state) != 0):
            return self.game_value(state), state
        
        #if depth reached, end recursion 
        if (depth >= 3):
            return self.heuristic_game_value(state), state
        
        #the rest is similar to the max-value, just a bit of the opposite
        else:
            beta = float(99999)
            succ = self.succ(state)
            if self.isDropPhase(state):
                for s in succ:
                    tempState = copy.deepcopy(state)
                    tempState[s[0]][s[1]] = self.opp  

                    val = self.max_value(tempState, depth + 1)

                    if (val[0] < beta):
                        beta = val[0]

                return beta, tempState
            
            else:
                for s in succ:
                    tempState = copy.deepcopy(state)
                    tempState[s[0][0]][s[0][1]] = self.opp
                    tempState[s[1][0]][s[1][1]] = ' '
                    val = self.max_value(tempState, depth + 1)
                    if (val[0] < beta):
                        beta = val[0]


                return beta, tempState

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        I have completed checks for diagonal and box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if (state[i][col] != ' ' and state[i][col] == state[i+1][col]
                    == state[i+2][col] == state[i+3][col]):
                    return 1 if state[i][col]==self.my_piece else -1

        # check \ diagonal wins
        for row in range(2):
            for col in range(2):
                if (state[row][col] != ' ' and state[row][col] == 
                state[row + 1][col + 1] == state[row + 2][col + 2] == 
                state[row + 3][col + 3]):
                    return 1 if state[row][col]==self.my_piece else -1 
                    
        
        # check / diagonal wins
        for row in range(3, 5):
            for col in range(2):
                if (state[row][col] != ' ' and state[row][col] == 
                    state[row - 1][col + 1] == state[row - 2][col + 2] == 
                    state[row - 3][col + 3]):
                    return 1 if state[row][col]==self.my_piece else -1 
        
        # check box wins
        for row in range (1, 5):
            for col in range (1, 5):
                if (state[row][col] != ' ' and state[row][col] == 
                    state[row][col - 1] == state[row - 1][col] == 
                    state[row - 1][col - 1]):
                    return 1 if state[row][col]==self.my_piece else -1 

        return 0 # no winner yet
    
    def heuristic_game_value(self, state):
        # check if in terminal state
        val = self.game_value(state)
        if (val != 0):
            return val
        
        maxValue = -99999
        minValue = 99999
        
        # check the following win conditions and assign values
        
        # horizontal win
        
        #set up counters
        selfCounter = 0
        maxSelfCounter = 0
        oppCounter = 0
        maxOppCounter = 0

        #iterate thru state
        for i in range(5):
            for j in range(5):
                #check if ai pieces are close to horizontal win
                if state[i][j] == self.my_piece:
                    selfCounter += 1
                
                #check if opp pieces are close to horizontal win
                if state[i][j] == self.opp:
                    oppCounter += 1
                  
                #at end of col, find max counter and reset
            maxSelfCounter = max(maxSelfCounter, selfCounter)
                    
            selfCounter = 0
            maxOppCounter = max(maxOppCounter, oppCounter)
            oppCounter = 0
        # * .25 here since it takes 4 to win and the max can be 3 which is a .75
        maxValue = max(maxValue, maxSelfCounter * .25)
        minValue = min(minValue, maxOppCounter * -.25)

        
        
        # vertical win
        
        # reset counters
        selfCounter = 0
        oppCounter = 0
        maxSelfCounter = 0
        maxOppCounter = 0
        
        # iterate thru state
        for i in range(5):
            for j in range(5):
                
                #check if ai pieces are close to vertical win
                if state[j][i] == self.my_piece:
                    selfCounter += 1
                #check if opp pieces are close to vertical win
                if state[j][i] == self.opp:
                    oppCounter += 1
                
                #at end of rows, find max counter and reset counters

            maxSelfCounter = max(maxSelfCounter, selfCounter)
            selfCounter = 0
            maxOppCounter = max(maxOppCounter, oppCounter)
            oppCounter = 0
        maxValue = max(maxValue, maxSelfCounter * .25)
        minValue = min(minValue, maxOppCounter * -.25)
        
        # \ wins
        
        # reset counters
        selfCounter = 0
        oppCounter = 0
        maxSelfCounter = 0
        maxOppCounter = 0
        
        #iterate thru state
        for row in range(2):
            for col in range(2):
                # check ai pieces if close to \ win
                if state[row][col] == self.my_piece:
                    selfCounter += 1
                if state[row + 1][col + 1] == self.my_piece:
                    selfCounter += 1
                if state[row + 2][col + 2] == self.my_piece:
                    selfCounter += 1
                if state[row + 3][col + 3] == self.my_piece:
                    selfCounter += 1
                
                # check opp pices if close to \ win
                if state[row][col] == self.opp:
                    oppCounter += 1
                if state[row + 1][col + 1] == self.opp:
                    oppCounter += 1
                if state[row + 2][col + 2] == self.opp:
                    oppCounter += 1
                if state[row + 3][col + 3] == self.opp:
                    oppCounter += 1
                
                # at end of column, find max counter and reset counters
                
            maxSelfCounter = max(maxSelfCounter, selfCounter)
            selfCounter = 0
            maxOppCounter = max(maxOppCounter, oppCounter)
            oppCounter = 0 
        maxValue = max(maxValue, maxSelfCounter * .25)
        minValue = min(minValue, maxOppCounter * -.25)
        
        # / wins
        
        # reset counters
        selfCounter = 0
        oppCounter = 0
        maxSelfCounter = 0
        maxOppCounter = 0
        
        # iterate thru state
        for row in range(3, 5):
            for col in range(2):
                
                #check ai pieces if they are in / pattern
                if state[row][col] == self.my_piece:
                    selfCounter += 1
                if state[row - 1][col + 1] == self.my_piece:
                    selfCounter += 1
                if state[row - 2][col + 2] == self.my_piece:
                    selfCounter += 1
                if state[row - 3][col + 3] == self.my_piece:
                    selfCounter += 1
                
                #check opp pieces if they are in / pattern
                if state[row][col] == self.opp:
                    oppCounter += 1
                if state[row - 1][col + 1] == self.opp:
                    oppCounter += 1
                if state[row - 2][col + 2] == self.opp:
                    oppCounter += 1
                if state[row - 3][col + 3] == self.opp:
                    oppCounter += 1
                
                # at end of column, find max counter and reset counters

            maxSelfCounter = max(maxSelfCounter, selfCounter)
            selfCounter = 0
            maxOppCounter = max(maxOppCounter, oppCounter)
            oppCounter = 0 
        maxValue = max(maxValue, maxSelfCounter * .25)
        minValue = min(minValue, maxOppCounter * -.25)
                
        # box wins
        
        # reset counters
        selfCounter = 0
        oppCounter = 0
        maxSelfCounter = 0
        maxOppCounter = 0
        
        #iterate through state
        for row in range (1, 5):
            for col in range (1, 5):
                #check for ai pieces close to box
                if state[row][col] == self.my_piece:
                    selfCounter += 1
                if state[row][col - 1] == self.my_piece:
                    selfCounter += 1
                if state[row - 1][col] == self.my_piece:
                    selfCounter += 1
                if state[row - 1][col - 1] == self.my_piece:
                    selfCounter += 1
                
                #check for opp pieces close to box
                if state[row][col] == self.opp:
                    oppCounter += 1
                if state[row][col - 1] == self.opp:
                    oppCounter += 1
                if state[row - 1][col] == self.opp:
                    oppCounter += 1
                if state[row - 1][col - 1] == self.opp:
                    oppCounter += 1
                
                #at end of column, find max counter and reset counters

            maxSelfCounter = max(maxSelfCounter, selfCounter)
            selfCounter = 0
            maxOppCounter = max(maxOppCounter, oppCounter)
            oppCounter = 0 
        maxValue = max(maxValue, maxSelfCounter * .25)
        minValue = min(minValue, maxOppCounter * -.25)
        
        #print(minValue)      
        return maxValue + minValue
                
        

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
