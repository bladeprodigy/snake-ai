import multiprocessing
import os
import neat
from visualize import plot_stats

from snake_game import SnakeGame


def eval_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    game = SnakeGame(manual_mode=False)

    score, length, distance_moved_towards_food, initial_angle, final_angle = game.play_game(net)
    moves = game.move_limit - game.moves_without_food

    fitness = score * 100

    fitness += moves
    fitness -= game.moves_without_food * 0.5

    if game.is_collision():
        fitness -= 25 * (1 + score / 100)
    if game.move_limit == 0:
        fitness -= 25 * (1 + score / 100)

    return fitness


def run():
    checkpoint_dir = 'checkpoints'

    if not os.path.exists(checkpoint_dir):
        os.makedirs(checkpoint_dir)

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    try:
        pop = neat.Checkpointer.restore_checkpoint('checkpoints/neat-checkpoint-399')
    except FileNotFoundError:
        print("Checkpoint not found. Starting a new population.")
        pop = neat.Population(config)

    stats = neat.StatisticsReporter()
    pop.add_reporter(neat.StdOutReporter(True))
    pop.add_reporter(stats)
    pop.add_reporter(neat.Checkpointer(5, filename_prefix=checkpoint_dir + '/neat-checkpoint-'))

    pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome)
    pop.run(pe.evaluate, 50)

    plot_stats(stats)


if __name__ == '__main__':
    run()
