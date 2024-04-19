import multiprocessing
import os
import neat
from snake_game import SnakeGame


def eval_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    game = SnakeGame()

    score, length, distance_moved_towards_food, initial_angle, final_angle = game.play_game(net)
    final_distance_to_food = abs(game.food_pos[0] - game.snake_pos[0]) + abs(game.food_pos[1] - game.snake_pos[1])
    moves_made = game.move_limit - game.moves_without_food

    fitness = score * 100
    fitness += length * 5
    fitness += moves_made * 2
    fitness += (moves_made // 5) * 10

    if game.is_collision():
        fitness -= 250

    previous_distance_to_food = abs(game.food_pos[0] - game.snake_pos[0]) + abs(game.food_pos[1] - game.snake_pos[1])
    if final_distance_to_food < previous_distance_to_food:
        fitness += 10

    if abs(final_angle) < abs(initial_angle):
        fitness += 10

    return fitness


def run():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    try:
        pop = neat.Checkpointer.restore_checkpoint('neat-checkpoint-58')
    except FileNotFoundError:
        print("Checkpoint not found. Starting a new population.")
        pop = neat.Population(config)

    stats = neat.StatisticsReporter()
    pop.add_reporter(neat.StdOutReporter(True))
    pop.add_reporter(stats)
    pop.add_reporter(neat.Checkpointer(10))

    pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome)
    winner = pop.run(pe.evaluate, 50)
    print('\nBest genome:\n{!s}'.format(winner))

    print("\n*** End of evolution statistics ***")
    print("\nAverage Fitness per generation:")
    for gen, avg in enumerate(stats.get_fitness_mean()):
        print(f"Generation {gen}: Average Fitness = {avg}")

    print("\nBest Fitness per generation:")
    for gen, best in enumerate(stats.get_fitness_stat(max)):
        print(f"Generation {gen}: Best Fitness = {best}")


if __name__ == '__main__':
    run()
