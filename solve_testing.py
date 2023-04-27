from random import choice
from solving import SolveCube
from other_functions import create_solved_cube, display_cube
import time


def generate_scrambling_algorithm(algorithm_length):
    """Generates and returns a random scramble that doesn't move the centres."""
    moves = "ULFRBD"
    variations = ["", "'", "2"]
    scrambling_algorithm = ""

    for n_move in range(algorithm_length):
        scrambling_algorithm += f"{choice(moves)}{choice(variations)} "

    return scrambling_algorithm


def set_random_selection(solving_cube):
    """
    This procedure is used to simulate a tile selection, eliminating the need
    for human input.
    """
    if solving_cube.is_selection_needed():
        enable_list = solving_cube.get_enable_list()
        solving_cube.set_selected_tile(*choice(enable_list))


def solve_testing(number_of_tests, algorithm_length, display_state_and_algorithm=False):
    """
    Takes a set of parameters and runs a number of tests, to test the solving
    ability of the system.

    :param number_of_tests: A integer for the number of solves wanted to be
    performed.
    :param algorithm_length: The length of the scrambling algorithm.
    :param display_state_and_algorithm: Can be True or False and displays the
    state and algorithm used to solve that state if True.

    :return: Returns the number of tests, number of states solved, number of
    states that couldn't be solved, the time taken to solve all states and the
    total amount of moves made.
    """
    solved = 0
    unsolved = 0
    total_number_of_moves = 0
    total_time_taken = 0

    for solve_test in range(number_of_tests):
        solving_cube = SolveCube(create_solved_cube())

        solving_cube.perform_algorithm([generate_scrambling_algorithm(algorithm_length)])
        if display_state_and_algorithm:
            display_cube(solving_cube.state)

        algorithm = ""

        start_time = time.time()
        while not solving_cube.is_cube_solved():
            try:
                set_random_selection(solving_cube)
                solving_cube.rotate_cube_due_to_selection()
                positioning_algorithm, algorithms = solving_cube.solve_section()
                algorithm += f"{positioning_algorithm} {algorithms[0]}\n".lstrip()

                if solving_cube.is_cube_solved():
                    solved += 1
            except:
                unsolved += 1
                break
        end_time = time.time()

        total_time_taken += (end_time - start_time)

        if display_state_and_algorithm:
            print(algorithm)

        number_of_moves = len(algorithm.split())
        total_number_of_moves += number_of_moves

    return number_of_tests, solved, unsolved, total_time_taken, total_number_of_moves


def display_stats(number_of_tests, solved, unsolved, time_taken, total_number_of_moves):
    """Calculates and displays useful statistics for the testing results."""
    solved_percentage = solved/number_of_tests * 100
    total_time_taken = round(time_taken, 2)

    avg_moves_per_solve = round(total_number_of_moves/number_of_tests)

    avg_time_per_solve = round(time_taken/number_of_tests, 2)

    solves_per_second = round(1/(time_taken/number_of_tests))
    moves_per_second = round(1/(time_taken/total_number_of_moves))

    avg_time_per_move = round(time_taken/total_number_of_moves, 6)

    print(f"Number of test: {number_of_tests}\n"
          f"Solved states: {solved}\n"
          f"Unsolved states: {unsolved}\n")

    print(f"Solved percentage: {solved_percentage}%\n")

    print(f"The total time taken to solve {number_of_tests} states was {total_time_taken}s.\n")

    print(f"{'-'*6} {'Averages ':-<16}")
    print(f"Moves per solve: {avg_moves_per_solve}\n"
          f"Time per solve: {avg_time_per_solve}s\n"
          f"Solves per second: {solves_per_second}\n"
          f"Moves per second: {moves_per_second}\n"
          f"Time per move: {avg_time_per_move}s")


display_stats(*solve_testing(100, 25))
