import os

import neat

from snake_game import SnakeGame


def run_game_with_best_genome():
    import pygame

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    def find_best_genome(population):
        checkpoint_best_genome = None
        best_fitness = -float('inf')
        for genome_id, genome in population.items():
            if genome.fitness is not None and genome.fitness > best_fitness:
                checkpoint_best_genome = genome
                best_fitness = genome.fitness
        return checkpoint_best_genome

    p = neat.Checkpointer.restore_checkpoint('try2/neat-checkpoint-293')
    best_genome = find_best_genome(p.population)

    if not best_genome:
        print("Failed to retrieve best genome from checkpoint.")
        return

    print(f"Best Genome ID: {best_genome.key}, Fitness: {best_genome.fitness}")

    net = neat.nn.FeedForwardNetwork.create(best_genome, config)

    while True:
        game = SnakeGame()
        game.play_game(net)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        print("Game over! Starting new game session...")


if __name__ == "__main__":
    run_game_with_best_genome()
