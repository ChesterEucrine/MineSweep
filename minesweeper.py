import random


def main():
    play_user = input("Play Game(p), Quit(q): ")
    if play_user == "p":
        user_input = input("Enter the number of bombs and grid size seperated by a comma: ")
    if play_user == "q":
        exit()
    input_arr = user_input.split(",")
    x = int(input_arr[0])
    y = int(input_arr[1])
    if x >= y or x < 1 or x == y*y:
        print("Invalid Input")
        return

    play(y, x)


def set_up_board(dim_size, num_bombs):
    arr = [[0 for row in range(dim_size)] for column in range(dim_size)]
    yaxiz=(dim_size-1) # added yaxiz(for label)
    xaxiz = yaxiz

    toprow = "   "
    for column in arr:
            toprow = toprow + f'{(str(dim_size-xaxiz)).zfill(2)} ' + ' '
            xaxiz-= 1  # this part is for top row, method derived from yaxiz below
    #print(toprow)  # this part is for top row, method derived from yaxiz below
    # added bomb array
    bomb_arr = []
    for _ in range(num_bombs):
        row_bomb = random.randint(0, dim_size - 1)
        column_bomb = random.randint(0, dim_size - 1)
        bomb_placed = False
        while bomb_placed == False:
            if arr[row_bomb][column_bomb] != "#":
                arr[row_bomb][column_bomb] = "#"
                bomb_placed = True
                # Add Random bomb into bomb array
                bomb_arr.append([row_bomb, column_bomb])

            row_bomb = random.randint(0, dim_size - 1)
            column_bomb = random.randint(0, dim_size - 1)
    # Return board and bomb array
    return arr, bomb_arr

# Function to get all the blocks surround a bomb
def get_square_radius(bomb, height, length): # col is x and row is y
    square_radius = [ [bomb[0] - 1, bomb[1] - 1], [bomb[0], bomb[1] - 1], [bomb[0] + 1, bomb[1] -1],
            [bomb[0] - 1, bomb[1]], [bomb[0], bomb[1]], [bomb[0] + 1, bomb[1]],
            [bomb[0] - 1, bomb[1]+1], [bomb[0], bomb[1]+1], [bomb[0] + 1, bomb[1]+1]]
    i = 0
    # create an array to store all elements in the list that are outside of the world bounds
    delete_arr = []
    while i < len(square_radius):
        if square_radius[i][0] < 0 or square_radius[i][1] < 0:
            delete_arr.append(i)
        elif square_radius[i][0] >= length or square_radius[i][1] >= height:
            delete_arr.append(i)
        i += 1

    # delete all items that are out of bounds
    i = len(delete_arr) - 1
    while i >= 0:
        del square_radius[delete_arr[i]]
        i -= 1
    return square_radius

# Function to mark the number of bombs surround a block within the world
# returns marked world
def mark(world, bomb_arr, dim_size):
    length = dim_size
    height = dim_size
    # Mark each bomb
    for bomb in bomb_arr:
        square_radius = get_square_radius(bomb, height, length)
        # Mark blocks in the world
        for block in square_radius:
            if block not in bomb_arr:
                world[block[0]][block[1]] += 1
    return world

def convert_(board, touched, dim_size):
    game_board = board
    i = 0
    while i < dim_size:
        j = 0
        while j < dim_size:
            if touched[i][j] != True:
                game_board[i][j] = ' ';
                pass
            j += 1
            pass
        i += 1
        pass
    return game_board

# Function to show all the adjucent zero blocks if the current block is zero
def show_(board, touched, x, y):
    condition1 = (x >= 0 and x < len(board))
    condition2 = (y >= 0 and y < len(board))
    #print(condition1, " ", condition2)
    if condition1 and condition2:
        #print("done on ", x, " ", y, " ", len(board))
        if touched[x][y]:
            return 0
        touched[x][y] = True
        if board[x][y] == 0:
            # Top Row
            a = show_(board, touched, x - 1, y - 1)
            a += show_(board, touched, x, y - 1)
            a += show_(board, touched, x + 1, y - 1)
            # Middle Row
            a += show_(board, touched, x - 1, y)
            a += show_(board, touched, x + 1, y)
            # Below Row
            a += show_(board, touched, x - 1, y + 1)
            a += show_(board, touched, x, y + 1)
            a += show_(board, touched, x + 1, y + 1)
            return a
        else:
            return 1
    else:
        return 0

def output_board(arr):

    dim_size = 0
    for row in arr:
        dim_size +=1
    
    yaxiz=(dim_size-1) # added yaxiz(for label)
    xaxiz = yaxiz
    toprow = "   "
    for column in arr:
            toprow = toprow + f'{(str(dim_size-xaxiz)).zfill(2)} ' + ' '
            xaxiz-= 1  # this part is for top row, method derived from yaxiz below
    print(toprow)  # this part is for top row, method derived from yaxiz below
    
    yaxiz=(dim_size-1)
    for row in arr:
        yshow = str(dim_size-yaxiz)
        print(yshow.zfill(2)+" " +" | ".join(str(cell) for cell in row))
        print(""+"----"*dim_size)# adjusted the dash to multiply by the dim_size 
        yaxiz-= 1 # yaxiz must decrease since the number minus dim_size must reverse

def step(world, board, touched, x, y):
    #print(world[x][y])
    board[x][y] = world[x][y]
    if world[x][y] == '#':
        print('Lost')
        return False, world
    else:
        return True, board

import subprocess

def play(dim_size, num_bombs):

    board, bomb_arr = set_up_board(dim_size, num_bombs)

    board = mark(board, bomb_arr, dim_size) 

    game_board = [[0 for row in range(dim_size)] for column in range(dim_size)]
    touched = [[False for row in range(dim_size)] for column in range(dim_size)]
    output_board(board)
    
    print("")
    user_input2 = (input("input row,column to search block: "))#Tshpoe Part where 
    input_arr = user_input2.split(",")                         # we ask user to enter 
    x = int(input_arr[0])-1     # x , y co-ord to search 
    y = int(input_arr[1])-1     #board, bomb_arr = set_up_board(dim_size, num_bombs)
    running = True
    won = False
    
    max_moves = dim_size ** 2 - num_bombs
    while running:
        subprocess.call('clear')
        if [x, y] in bomb_arr:
		print('You Lost\n', board[x][y])
	sugar = list(x,y)
	
	print(sugar)
	print([bomb_arr])
        
	running, board_ = step(board, game_board, touched, x, y)
        print(show_(board, touched, x, y))
        if not running:
		print("You Lost!")
	
        output_board(convert_(board, touched, dim_size))
        print(running)
        print("")
        #output_board(touched)
        #print("")

        if max_moves == 0:
		running = False
		print("You Won!")
        else:
		user_input2 = (input("input row,column to search block: "))#Tshpoe Part where 
		input_arr = user_input2.split(",")                         # we ask user to enter 
		x = int(input_arr[0])-1  # x , y co-ord to search 
		y = int(input_arr[1])-1

if __name__ == "__main__":
    main()
