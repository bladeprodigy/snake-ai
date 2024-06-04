## 1. About the Project

This project is a Python implementation of the classic Snake game, with an added twist: an AI that learns to play the game using a genetic algorithm. The AI uses a neural network to make decisions based on the current game state, and evolves over time to get better at the game.

The game is built using Python and Pygame, a set of Python modules designed for writing video games. The AI is implemented using a genetic algorithm, a search heuristic that is inspired by Charles Darwin’s theory of natural evolution. This algorithm reflects the process of natural selection where the fittest individuals are selected for reproduction in order to produce the offspring of the next generation.

The game includes a manual play mode where you can control the snake using the arrow keys, and an AI mode where the snake is controlled by the AI. The AI learns to play the game by playing it over and over again, and improving its performance over time.

The game also includes a difficulty selection feature, where you can choose the difficulty level of the game. The difficulty level affects the speed of the snake, with higher difficulty levels resulting in a faster snake.

The goal of the project is to create an AI that can play the Snake game as well as, or better than, a human player. This is a challenging task, as the AI needs to learn to navigate the game area, avoid its own tail, and eat the food that appears in the game area.

The project is open-source, and contributions are welcome. If you have any suggestions or improvements, feel free to open an issue or submit a pull request.

## 2. Project Setup

This project is built using Python and Pygame. To get started, you'll need to have Python installed on your machine. If you don't have Python installed, you can download it from the official website: https://www.python.org/downloads/

Once you have Python installed, you'll need to install the required dependencies for this project. The dependencies are listed in the `requirements.txt` file. You can install these dependencies using pip, which is a package manager for Python.

Here are the steps to set up the project:

1. Clone the repository to your local machine using git. If you don't have git installed, you can download it from the official website: https://git-scm.com/downloads

```bash
git clone https://github.com/bladeprodigy/snake-ai.git
```

2. Navigate to the project directory:

```bash
cd snake-ai
```

3. Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## 3. Manual Play Mode

To play the game in manual play mode, run the following command:

```bash
python play_snake.py
```

This will start the game in manual play mode, where you can control the snake using the arrow keys. The goal of the game is to eat the food that appears in the game area, without running into the walls or the snake's own tail.

## 4. AI Learning Mode

To play the game in AI learning mode, run the following command:

```bash
python train_snake.py
```

This will start the game in AI learning mode, where the snake is controlled by the AI. The AI learns to play the game by playing it over and over again, and improving its performance over time.

Every 5 generations there is a checkpoint saved in the `checkpoints` folder. You can load a checkpoint by changing the name of the checkpoint in method run() in the `train_snake.py` file (line 45).

## 5. Fitness Function

The fitness function is used to evaluate the performance of each individual in the population. In this project, the fitness function is based on the following criteria:

1. The score of the snake: The score is calculated based on the number of food items eaten by the snake. The higher the score, the better the performance of the snake.
2. The length of the snake: The length of the snake is also taken into account, as a longer snake is generally better at avoiding obstacles and eating food.
3. The number of moves made by the snake: It is a measurement used to reward the snake for surviving longer.
4. Collision with the wall: If the snake collides with the wall, it is penalized.
5. Collision with itself: If the snake collides with its own tail, it is penalized.
6. Repetition of moves: If the snake repeats the same move multiple times, it is penalized.

You can modify the fitness function eval_genomes() in the `train_snake.py` to experiment with different criteria and improve the performance of the AI.

## 6. Configuration

You can adjust setting in config-feedforward.txt file to suit your needs and ideas. It contains a lot of variables. You can find documentation explaining each variable in the `config-feedforward.txt` file here: https://neat-python.readthedocs.io/en/latest/index.html

## 7. Running your trained AI

After training your AI, you can run it to see how well it performs in the game. To select which checkpoint you want to run change it in `run_best_genome.py` file (line 12).

To run your trained AI, you can use the following command:

```bash
python run_best_genome.py
```

This will let your best genome play the game in a loop.

## 8. Conclusion

This project is a fun and challenging way to learn about genetic algorithms and neural networks. By implementing an AI that learns to play the Snake game, you can gain a better understanding of how these algorithms work and how they can be applied to real-world problems.

If you have any questions or feedback about this project, feel free to reach out to us. I'm always happy to help and learn from others.