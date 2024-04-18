import os
import neat

from snake_game import SnakeGame


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        game = SnakeGame()

        try:
            score, length, distance_moved_towards_food = game.play_game(net)

            print(f"Genome {genome_id}: Score={score}, Length={length}, Distance={distance_moved_towards_food}")

            fitness = max(0, score * 100)  # Nagroda za zdobycie punktu
            fitness += max(0, (length - 1) * 100)  # Nagroda za długość węża
            fitness -= max(0, distance_moved_towards_food * 0.1)  # Kara za oddalanie się od jedzenia

            last_moves = game.get_last_moves()
            if len(set(last_moves)) < len(last_moves) / 2:
                fitness -= 100  # Kara za powtarzające się ruchy

            if len(last_moves) > 10 and len(set(last_moves[-10:])) == 1:
                fitness -= 500  # Kara za długo powtarzające się ruchy

            if length - 1 < score:
                fitness -= 100  # Kara za przeżycie bez zdobycia punktu

            genome.fitness = fitness
        except Exception as e:
            print(f"An error occurred while evaluating genome {genome_id}: {e}")
            genome.fitness = 0


def run():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    pop = neat.Population(config)
    stats = neat.StatisticsReporter()
    pop.add_reporter(neat.StdOutReporter(True))
    pop.add_reporter(stats)
    pop.add_reporter(neat.Checkpointer(10))

    winner = pop.run(eval_genomes, 50)
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
