from generate_objects import *
np.set_printoptions(precision=3, suppress=True)


number_of_coins = 6
number_of_values = 3
play_transition_matrix = generate_play_transition_matrix(number_of_coins=number_of_coins, number_of_values=number_of_values)

print(f"play shape: {play_transition_matrix.shape}")

print(f"play probabilities for value 0:\n{play_transition_matrix[:number_of_coins+1, :number_of_coins+1]}")

print(f"play probabilities for value 0.5:\n{play_transition_matrix[number_of_coins + 1:2*(number_of_coins + 1), number_of_coins + 1:2*(number_of_coins + 1)]}")

print(f"play probabilities for value 1:\n{play_transition_matrix[2*(number_of_coins + 1):3*(number_of_coins + 1), 2*(number_of_coins + 1):3*(number_of_coins + 1)]}")

pass_transition_matrix = generate_pass_transition_matrix(number_of_coins=number_of_coins, number_of_values=number_of_values)

print(f"pass shape: {pass_transition_matrix.shape}")

print(f"pass probabilities:\n{pass_transition_matrix[:number_of_coins+1, :number_of_coins+1]}")