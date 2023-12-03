import numpy as np
import time 


def txt_to_numpy(input_path):

    # Collect all lines
    line_list = []

    # Open file and read in lines
    with open(input_path, 'r') as f:
        lines = f.readlines()
        # Unpack each line into a list of characters
        for line in lines:
            line_chars = [char for char in line.strip()]
            line_list.append(line_chars)

    # Convert the list into a NumPy array
    data_array = np.array(line_list)

    return data_array


def generate_symbol_mask(data_arr):

    # Mask numpy array to get symbols 
    # Anything not a digit or "." is a symbol
    symbol_mask = ~(np.char.isdigit(data_arr) | (data_arr == '.'))

    # Use symbol mask to get adjacency mask
    # I.e. if a digit is adjacent to a symbol
    adj_mask = (
        np.char.isdigit(data_arr) & # check if it's a digit
        (
        np.roll(symbol_mask, shift=(1, 0), axis=(0, 1)) |  # N
        np.roll(symbol_mask, shift=(-1, 0), axis=(0, 1)) |  # S
        np.roll(symbol_mask, shift=(0, 1), axis=(0, 1)) |  # E
        np.roll(symbol_mask, shift=(0, -1), axis=(0, 1)) |  # W
        np.roll(symbol_mask, shift=(1, 1), axis=(0, 1)) |  # NE
        np.roll(symbol_mask, shift=(-1, -1), axis=(0, 1)) |  # SW
        np.roll(symbol_mask, shift=(-1, 1), axis=(0, 1)) |  # NW
        np.roll(symbol_mask, shift=(1, -1), axis=(0, 1))  # SE
        )
    )

    return adj_mask


def get_engine_sum(data_arr):
    '''
    Part One Solution 
    '''

    # Get adjacency mask 
    adj_mask = generate_symbol_mask(data_arr)

    # Collector objects
    engine_parts = []
    curr_dig = ''
    skip = 0
    engine_indices = []

    # Loop through each cell by row and column
    for row in range(data_arr.shape[0]):
        for col in range(data_arr.shape[1]):

            # If we need to skip digit
            if skip > 0:
                skip -= 1
                continue

            # Check if current value is a digit
            if np.char.isdigit(data_arr[row, col]):
                curr_dig += data_arr[row, col]

            # If current value meets condition
            if adj_mask[row, col]:

                # Add index to engine indices list
                engine_indices.append((row, col))

                # Check to see if future values are digits
                next_col = col + 1
                while True:
                    try:
                        # Check if the next value is a digit
                        if np.char.isdigit(data_arr[row, next_col]):
                            curr_dig += data_arr[row, next_col]
                            engine_indices.append((row, next_col))
                            next_col += 1
                            skip += 1
                        else:
                            break
                    except IndexError:
                        break
                
                # Add current digit to list 
                engine_parts.append(int(curr_dig))

            if np.char.isdigit(data_arr[row, col]) == False:
                curr_dig = ''

    # Sum the engine parts
    engine_sum = sum(engine_parts)
    return engine_sum


def get_full_number(row, col, data_arr):
    '''
    Helper function for part two 
    Would have helped for part one but did not back-implement
    '''

    # Get any preceding digits
    prev_digits = ''
    next_col = col
    while True:
        try:
            if np.char.isdigit(data_arr[row, next_col - 1]):
                prev_digits = data_arr[row, next_col - 1] + prev_digits
                next_col -= 1
            else:
                break
        except IndexError:
            break

    # Get any following digits
    next_digits = ''
    next_col = col
    while True:
        try:
            if np.char.isdigit(data_arr[row, next_col + 1]):
                next_digits += data_arr[row, next_col + 1]
                next_col += 1
            else:
                break
        except IndexError:
            break

    # Concat digits 
    full_num = prev_digits + data_arr[row, col] + next_digits
    return int(full_num)


def get_engine_ratios(data_arr):
    '''
    Part two solution
    '''

    # Store star indices 
    star_indices = {}

    # Loop through all data arr indices
    for row in range(data_arr.shape[0]):
        for col in range(data_arr.shape[1]):

            # Check if current value is *
            if data_arr[row, col] != '*':
                continue
            else:

                total_engines = 0
                eng_indices = []

                # Check to see if adjacent to two numbers
                if np.char.isdigit(data_arr[row - 1, col]):
                    eng_indices.append((row - 1, col)) # N
                    total_engines += 1
                else:
                    if np.char.isdigit(data_arr[row - 1, col-1]):
                        eng_indices.append((row - 1, col-1)) #NW
                        total_engines += 1
                    if np.char.isdigit(data_arr[row - 1, col+1]):
                        eng_indices.append((row - 1, col+1)) #NE
                        total_engines += 1
                
                if np.char.isdigit(data_arr[row + 1, col]):
                    eng_indices.append((row + 1, col)) # S
                    total_engines += 1
                else:
                    if np.char.isdigit(data_arr[row + 1, col-1]):
                        eng_indices.append((row + 1, col-1)) # SW
                        total_engines += 1
                    if np.char.isdigit(data_arr[row + 1, col+1]):
                        eng_indices.append((row + 1, col+1)) # SE
                        total_engines += 1
                
                if np.char.isdigit(data_arr[row, col - 1]):
                    eng_indices.append((row, col - 1)) # W
                    total_engines += 1
                
                if np.char.isdigit(data_arr[row, col + 1]):
                    eng_indices.append((row, col + 1)) # E
                    total_engines += 1

                if total_engines >= 2:
                    gear_ratio = 1
                    for eng_idx in eng_indices:
                        full_eng_num = get_full_number(eng_idx[0], eng_idx[1], data_arr)
                        gear_ratio *= full_eng_num
                    
                    star_indices[(row, col)] = gear_ratio


    gear_ratio_sum = sum(star_indices.values())
    return gear_ratio_sum


def main():

    start_time = time.time()

    # Get data array
    data_arr = txt_to_numpy('day3/puzzle_input.txt')

    # Part One Solution
    engine_sum = get_engine_sum(data_arr)
    print('Part One Solution :', engine_sum)

    # Part Two Solution
    gear_ratio_sum = get_engine_ratios(data_arr)
    print('Part Two Solution :', gear_ratio_sum)

    print('Total Time :', round(time.time() - start_time, 3), ' seconds')


if __name__ == '__main__':
    main()