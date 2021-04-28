# Reinforcement Learning Snake

In this project, I built a simple snake game which the user can play. I then used Q-Learning to train an AI to play the game.

## Prerequisites

### Python

### NumPy
```
pip install numpy
```

### PyTorch

Please navigate to [pytorch.org](https://pytorch.org/) to install the correct version of PyTorch for your machine. Below are the preferences that I selected:

- PyTorch Build: Stable (1.8.1)
- Your OS: Windows
- Package: Pip
- Language: Python
- Computer Platform: CPU

If the above match your preferences, you can use the following command to install PyTorch:
```
pip3 install torch==1.8.1+cpu torchvision==0.9.1+cpu torchaudio===0.8.1 -f https://download.pytorch.org/whl/torch_stable.html
```

**NOTE**: I would still recomend checking out [pytorch.org](https://pytorch.org/) in case of any version updates.

## Installing and running

1. Clone the repository:
```
git clone https://github.com/hamza-mughees/Reinforcement-Learning-Snake.git
```
2. `cd` into the working directory:
```
cd Reinforcement-Learning-Snake
```
3. To play the snake game yourself, run `snake_game.py`:
```
python snake_game.py
```
4. To train the AI to play the snake game, run `agent.py`:
```
python agent.py
```