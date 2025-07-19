class Cell:
    def __init__(self, given=False, value=0):
        self.given = given  # If the value is given this is True (default False)
        self.value = value  # If the value is given then updated (default 0)
        self.counter = 0  # For non-given values
        self.acceptable = []  # List of acceptable numbers for a given cell

    def update_value(self) -> bool:
        """Returns True if there is a valid value to be assigned, else counter sets to 0 and returns False."""

        if self.counter < len(self.acceptable):
            self.value = self.acceptable[self.counter]
            self.counter += 1
            return True

        else:
            self.counter = 0
            self.value = 0
            return False


class Sudoku:
    def __init__(self):
        self.board = [[Cell() for i in range(9)] for j in range(9)]
        self.input = [
            [8, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 3, 6, 0, 0, 0, 0, 0],
            [0, 7, 0, 0, 9, 0, 2, 0, 0],
            [0, 5, 0, 0, 0, 7, 0, 0, 0],
            [0, 0, 0, 0, 4, 5, 7, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 3, 0],
            [0, 0, 1, 0, 0, 0, 0, 6, 8],
            [0, 0, 8, 5, 0, 0, 0, 1, 0],
            [0, 9, 0, 0, 0, 0, 4, 0, 0],
        ]

        self.indices = []

    def update_input_values(self):
        """Updates the input values to the Sudoku board"""
        for i in range(9):
            for j in range(9):
                val = self.input[i][j]
                if val != 0:
                    self.board[i][j].given = True
                    self.board[i][j].value = val

    def update_non_given_indices(self):
        """Appends the indices of non-given positions to the indices list."""
        for i in range(9):
            for j in range(9):
                if self.board[i][j].given is False:
                    self.indices.append((i, j))

    def print_board(self):
        """Print the Sudoku board"""
        for j in range(9):
            string = "----" * 9 + "-"
            print(string)
            values = [str(self.board[j][i].value) for i in range(9)]
            string = "| " + " | ".join(values) + " | "
            print(string)

        string = "----" * 9 + "-"
        print(string)

    def update_acceptables_cell(self, i: int, j: int):
        """Update the acceptable values of a cell."""
        num_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        reject_set = set()

        ### Row ###

        for p in range(9):
            val = self.board[i][p].value
            if val != 0 and self.board[i][p].given is True:
                reject_set.add(val)

        ### Column ###

        for q in range(9):
            val = self.board[q][j].value
            if val != 0 and self.board[q][j].given is True:
                reject_set.add(val)

        ### Sub-Square ###

        row_start, col_start = (i // 3) * 3, (j // 3) * 3
        for p in range(row_start, row_start + 3):
            for q in range(col_start, col_start + 3):
                val = self.board[p][q].value
                if val != 0 and self.board[p][q].given is True:
                    reject_set.add(val)

        num_set -= reject_set

        for val in num_set:
            self.board[i][j].acceptable.append(val)

    def update_acceptables(self):
        """Update Acceptable values for non-given cells."""

        for i in range(9):
            for j in range(9):
                if self.board[i][j].given is False:
                    self.update_acceptables_cell(i=i, j=j)

    def prepare_board(self):
        """Prepare the Sudoku board for solving."""

        self.update_input_values()
        self.update_acceptables()
        self.update_non_given_indices()

    def check_value(self, i: int, j: int) -> bool:
        """Check for conflicts within row, column and subsquare.
        i -> Row num
        j -> Column num
        True if no conflict else False"""

        value = self.board[i][j].value

        ### Check Row ###

        for p in range(9):
            row_val = self.board[i][p].value
            if row_val == value and p != j:
                return False

        ### Check Column ###

        for q in range(9):
            column_val = self.board[q][j].value
            if column_val == value and q != i:
                return False

        ### Check Sub-Square ###

        row_start, col_start = (i // 3) * 3, (j // 3) * 3

        for p in range(row_start, row_start + 3):
            for q in range(col_start, col_start + 3):
                sub_sq_val = self.board[p][q].value
                if sub_sq_val == value and p != i and q != j:
                    return False

        return True

    def solve(self):
        """Solve the Sudoku board with DFS backtracking."""

        index = 0
        solved = False
        count = 0

        while not solved and index >= 0:
            count += 1
            row_index, col_index = self.indices[index]
            possible = self.board[row_index][col_index].update_value()

            if not possible:  # Already at the end, backtrack
                index -= 1
                continue

            else:
                try_val = self.check_value(i=row_index, j=col_index)

                if try_val is False:  # Move to the next value
                    continue

                else:
                    if index == len(self.indices) - 1:
                        solved = True  # Solved!
                        self.print_board()
                        print("\n")
                        print(f"Total number of guesses = {count}\n")
                        return

                    else:
                        index += 1  # Move on to the next one

    def start(self):
        """Utility program to solve Sudoku"""
        self.prepare_board()
        self.solve()


sud = Sudoku()
sud.start()
