import concurrent.futures
import time


def get_lines(input_file):
    '''
    Get the lines from the text file
    '''

    with open(input_file, 'r') as f:
        lines = f.readlines()

    return lines


def get_line_number(line):
    '''
    Get the resulting number from a line
    '''

    # Get the first digit
    first_digit = None
    for i in range(len(line)):
        if line[i].isdigit():
            first_digit = line[i]
            break

    # Get the last digit
    last_digit = None
    line = line[::-1]
    for i in range(len(line)):
        if line[i].isdigit():
            last_digit = line[i]
            break

    num = int(first_digit + last_digit)
    return num


def str_digit_check(substring, reverse=False):
    '''
    Check if a substring contains a digit
    '''

    if reverse:
        nums = ['eno', 'owt', 'eerht', 'ruof', 'evif', 'xis',
                'neves', 'thgie', 'enin', 'net']
    else:
        nums = ['one', 'two', 'three', 'four', 'five', 'six',
                'seven', 'eight', 'nine', 'ten']

    found_num = None
    for num in nums:
        if num in substring:
            found_num = num
            break

    dict_mapper = {'eno': '1',
                   'owt': '2',
                   'eerht': '3',
                   'ruof': '4',
                   'evif': '5',
                   'xis': '6',
                   'neves': '7',
                   'thgie': '8',
                   'enin': '9',
                   'net': '10',
                   'one': '1',
                   'two': '2',
                   'three': '3',
                   'four': '4',
                   'five': '5',
                   'six': '6',
                   'seven': '7',
                   'eight': '8',
                   'nine': '9',
                   'ten': '10'
                   }

    if found_num is not None:
        digit = dict_mapper[found_num]
        return digit
    else:
        return False


def get_real_line_number(line):
    '''
    Get the resulting number from a line
    '''

    # Get the first digit
    first_digit = None
    curr_str = ''
    for i in range(len(line)):
        curr_str += line[i]
        if line[i].isdigit():
            first_digit = line[i]
            break

        str_digit = str_digit_check(curr_str)
        if str_digit is not False:
            first_digit = str_digit
            break

    # Get the last digit
    last_digit = None
    line = line[::-1]
    for i in range(len(line)):
        curr_str += line[i]
        if line[i].isdigit():
            last_digit = line[i]
            break

        str_digit = str_digit_check(curr_str, reverse=True)
        if str_digit is not False:
            last_digit = str_digit
            break

    num = int(first_digit + last_digit)
    return num


def get_sum(input_file):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        lines = get_lines(input_file)
        fs = [executor.submit(get_line_number, line) for line in lines]
        results = [f.result() for f in concurrent.futures.as_completed(fs)]

    return sum(results)


def get_real_sum(input_file):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        lines = get_lines(input_file)
        fs = [executor.submit(get_real_line_number, line) for line in lines]
        results = [f.result() for f in concurrent.futures.as_completed(fs)]

    return sum(results)


def main():
    start_time = time.time()
    input_file = 'day1/puzzle_input.txt'
    sum = get_real_sum(input_file)
    end_time = time.time()

    print('Puzzle Answer :', sum)
    print('Time Taken    :', round(end_time - start_time, 3), ' seconds')


if __name__ == '__main__':
    main()
