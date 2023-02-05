import numpy as np


def generate_play_transition_matrix(number_of_coins=20, number_of_values=101, save=False):
    # preparing needed value list, draw probability and setting up final matrix
    values = [i / (number_of_values - 1) for i in range(number_of_values)]
    draw_probability = 1 / number_of_values
    final_matrix = np.zeros((0, (number_of_coins + 1) * number_of_values))
    # iterating over every value in possible values to get
    for value in values:
        row_matrix = np.zeros((number_of_coins + 1, 0))
        # setting win and loss probabilities
        if value == 1:
            win_probability = 1 - draw_probability
            loss_probability = 0
        elif value == 0:
            win_probability = 0
            loss_probability = 1 - draw_probability
        else:
            win_probability = value - draw_probability / 2
            loss_probability = 1 - win_probability - draw_probability
        # calculating probability matrix for one selected value from all available values
        single_probability_matrix = np.zeros((number_of_coins + 1, number_of_coins + 1))
        # iterating over every current coins number
        for current_coins in range(number_of_coins + 1):
            if current_coins < 2:
                single_probability_matrix[current_coins, 0] = 1
            elif current_coins > number_of_coins - 2:
                single_probability_matrix[current_coins, number_of_coins] = 1
            else:
                # iterating over every future coins number and setting appropriate probability values
                for future_coins in range(number_of_coins + 1):
                    if current_coins == future_coins:
                        single_probability_matrix[current_coins, future_coins] = draw_probability / number_of_values
                    elif future_coins == current_coins + 2:
                        single_probability_matrix[current_coins, future_coins] = win_probability / number_of_values
                    elif future_coins == current_coins - 2:
                        single_probability_matrix[current_coins, future_coins] = loss_probability / number_of_values
        # stacking matrices horizontally, to take into account all possible values in next game turn
        for columns in range(number_of_values):
            row_matrix = np.hstack((row_matrix, single_probability_matrix))
        # inserting matrix for one value into the final "play" action probability matrix
        final_matrix = np.vstack((final_matrix, row_matrix))
    if save:
        np.save("objects/play_matrix.npy", final_matrix)
    return final_matrix


def generate_pass_transition_matrix(number_of_coins=20, number_of_values=101, save=False):
    # setting up matrices
    final_matrix = np.zeros((0, (number_of_coins + 1) * number_of_values))
    row_matrix = np.zeros((number_of_coins + 1, 0))
    single_probability_matrix = np.zeros((number_of_coins + 1, number_of_coins + 1))
    # iterating over every current coins number
    for current_coins in range(number_of_coins + 1):
        if current_coins in [0, 1, 2]:
            single_probability_matrix[current_coins, 0] = 1
        else:
            single_probability_matrix[current_coins, current_coins - 1] = 1
    # stacking matrix to fit the desired shape
    for value in range(number_of_values):
        row_matrix = np.hstack((row_matrix, single_probability_matrix))
    for value in range(number_of_values):
        final_matrix = np.vstack((final_matrix, row_matrix))
    if save:
        np.save("objects/pass_matrix.npy", final_matrix)
    return final_matrix


def generate_reward_list(number_of_coins=20, modifier=1, alternative=False, save=False):
    if alternative:
        rewards = np.zeros(number_of_coins + 1)
        rewards[0] = -10
        rewards[-1] = 10
    else:
        rewards = [modifier * i for i in range(number_of_coins + 1)]
    if save:
        np.save("objects/reward_list.npy", rewards)
    return rewards
