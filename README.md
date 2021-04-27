# Q-Learning-Snake

Click [here](https://www.youtube.com/watch?v=PJl4iabBEz0&t=67s) to navigate to the video tutorial

## Notes:

### Rewards
- eat foot: +10
- game over: -10
- else: 0

### Actions
One-hot encoding
- straight: [1,0,0]
- right turn: [0,1,0]
- left turn: [0,0,1]

### States
- danger straight
- danger right
- danger left
- direction left
- direction right
- direction up 
- direction down
- food left
- food right
- food up 
- food down