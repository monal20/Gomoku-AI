#Winning Condition

from Game_Mode import*

#Class that analyzes the state of the board
class CheckForWin(object):

    #Slightly adapted from: https://www.cs.cmu.edu/~112/notes/2d-list-case-studies.html
    @staticmethod
    def wordSearch(board, word, piecesInARow, countTarget):
        (rows, cols) = (len(board), len(board[0]))
        for row in range(rows):
            for col in range(cols):
                result = CheckForWin.wordSearchFromCell(board, word, row, col,piecesInARow, countTarget)
                if (result != None):
                    return result
        return None

    #Slightly adapted from: https://www.cs.cmu.edu/~112/notes/2d-list-case-studies.html
    @staticmethod
    def wordSearchFromCell(board, word, startRow, startCol, piecesInARow, countTarget):
        count = 0
        possibleDirections = 8 # 3^2 - 1
        for dir in range(possibleDirections):
            result = CheckForWin.wordSearchFromCellInDirection(board, word,
                                                startRow, startCol, dir, piecesInARow)
            if (result != None):
                count += 1
            if (count == countTarget):
                return result
        return None

    #Slightly adapted from: https://www.cs.cmu.edu/~112/notes/2d-list-case-studies.html
    @staticmethod
    def wordSearchFromCellInDirection(board, word, startRow, startCol, dir, piecesInARow):
        (rows, cols) = (len(board), len(board[0]))
        dirs = [ (-1, -1), (-1, 0), (-1, +1),
                ( 0, -1),          ( 0, +1),
                (+1, -1), (+1, 0), (+1, +1) ]
        (drow,dcol) = dirs[dir]    
        winStreak = piecesInARow
        for i in range(winStreak):
            row = startRow + i*drow
            col = startCol + i*dcol
            if ((row < 0) or (row >= rows) or
                (col < 0) or (col >= cols) or
                (board[row][col] != word)):
                return None
        return word


    #Inspired from: https://www.cs.cmu.edu/~112/notes/2d-list-case-studies.html
    #function that takes returns 1) the longest run of two players, with the abilty
    #of the current cell being sandwiched, and 2) the number connecting 
    #pieces with respect to that cell
    #Ex: oo_oo is counted as 5 in a row
    @staticmethod
    def countPiecesFromCellInTwoDir(board, player1, player2, startRow, startCol):
        #player1
        countP1 = 0
        longestRunP1 = 0
        #player2
        countP2 = 0
        longestRunP2 = 0
        possibleOrientations = 4
        for dirOr in range(possibleOrientations):
            longestRunP1, countP1 = CheckForWin.countPiecesFromCellInTwoDirHelper(board,
                        player1, longestRunP1,countP1, startRow, startCol, dirOr)
            longestRunP2, countP2 = CheckForWin.countPiecesFromCellInTwoDirHelper(board,
                        player2, longestRunP2,countP2, startRow, startCol, dirOr)
        return longestRunP1, countP1, longestRunP2, countP2

    #Helper function that combines the possible pieces in a row of any directional
    #orientation
    @staticmethod
    def countPiecesFromCellInTwoDirHelper(board, player, playerRun, playerCount, 
                                    startRow, startCol, dirOr):
        run1, run2 = CheckForWin.countPiecesInTwoDirOr(board, player,
                                                startRow, startCol, dirOr)
        playerRun = max(playerRun, (run1 + run2)-1)
        playerCount += playerRun//2
        return playerRun, playerCount

    #Inspired from: https://www.cs.cmu.edu/~112/notes/2d-list-case-studies.html
    @staticmethod
    def countPiecesInTwoDirOr(board, player, startRow, startCol, dirOr):
        """
        (-1, -1), (-1, 0), (-1, +1),
        ( 0, -1),  Piece,  ( 0, +1),
        (+1, -1), (+1, 0), (+1, +1) ]"""
        #Based on above directions,check in respective directinal oreinetation: 
        #     decreasing diagonals   increasing horizontal
        dirs = [[(-1,-1),(1,1)],           [(1,-1),(-1,1)] , 
        #       vertical                   horizontal
                [(-1,0),(1,0)],           [(0,-1),(0,1)]]
        orientation = dirs[dirOr]
        (drow1,dcol1) = dirs[dirOr][0]
        run1 = CheckForWin.countPiecesInTwoDir(board, player, 
                                            startRow, startCol, drow1,dcol1)
        (drow2,dcol2) = dirs[dirOr][1]
        run2 = CheckForWin.countPiecesInTwoDir(board, player, 
                                            startRow, startCol, drow2,dcol2)
        return run1, run2

    #Inspired from: https://www.cs.cmu.edu/~112/notes/2d-list-case-studies.html
    @staticmethod
    def countPiecesInTwoDir(board, player, startRow, startCol, drow, dcol):
        (rows, cols) = (len(board), len(board[0]))
        winningRun = 6
        if player == "black":
            accountForMissingAIPiece = 0
        else:
            accountForMissingAIPiece = 1
        for i in range(winningRun):
            row = startRow + i*drow + drow*accountForMissingAIPiece
            col = startCol + i*dcol + dcol*accountForMissingAIPiece
            if ((row < 0) or (row >= rows) or
                (col < 0) or (col >= cols) or
                (board[row][col] != player)):
                return i + accountForMissingAIPiece
        return winningRun

    #Modified from: https://www.cs.cmu.edu/~112/notes/2d-list-case-studies.html
    ##Does not account for oo_oo rows -> will report as 2
    @staticmethod
    def countPiecesFromCellInOneDir(board, player1, player2, startRow, startCol):
        #player1
        countP1 = 0
        longestRunP1 = 0
        #player2
        countP2 = 0
        longestRunP2 = 0
        possibleDirections = 8 # 3^2 - 1
        for dir in range(possibleDirections):
            longestRunP1, countP1 = CheckForWin.countPiecesFromCellHelper(board,
                        player1, longestRunP1,countP1, startRow, startCol, dir)
            longestRunP2, countP2 = CheckForWin.countPiecesFromCellHelper(board,
                        player2, longestRunP2,countP2, startRow, startCol, dir)
        return longestRunP1, countP1, longestRunP2, countP2

    #Helper function that takes calculates the longest run, with the abilty
    #of the current cell being sandwiched, and the connecting pieces of that cell
    #Ex: oo_oo is counted as 5 in a row
    @staticmethod
    def countPiecesFromCellHelper(board, player, playerRun, playerCount, 
                                    startRow, startCol, dir):
        result = CheckForWin.countPiecesInDir(board, player,
                                                startRow, startCol, dir)
        playerRun = max(playerRun, result)
        playerCount += result
        return playerRun, playerCount

    #Modified from: https://www.cs.cmu.edu/~112/notes/2d-list-case-studies.html
    @staticmethod
    def countPiecesInDir(board, player, startRow, startCol, dir):
        (rows, cols) = (len(board), len(board[0]))
        dirs = [ (-1, -1), (-1, 0), (-1, +1),
                ( 0, -1),          ( 0, +1),
                (+1, -1), (+1, 0), (+1, +1) ]
        (drow,dcol) = dirs[dir]    
        winStreak = 6
        if player == "black":
            accountForMissingAIPiece = 0
        else:
            accountForMissingAIPiece = 1
        for i in range(winStreak):
            row = startRow + i*drow + drow*accountForMissingAIPiece
            col = startCol + i*dcol + dcol*accountForMissingAIPiece
            if ((row < 0) or (row >= rows) or
                (col < 0) or (col >= cols) or
                (board[row][col] != player)):
                return i + accountForMissingAIPiece
            winStreak += 1
        return winStreak