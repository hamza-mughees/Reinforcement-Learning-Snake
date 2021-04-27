import torch
from torch import nn, optim
from torch.nn import functional as F
import os
import numpy as np

class LinearQNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear0 = nn.Linear(input_size, hidden_size)
        self.linear1 = nn.Linear(hidden_size, output_size)
    
    def forward(self, X):
        linear0_out = F.relu(self.linear0(X))
        linear1_out = self.linear1(linear0_out)
        return linear1_out
    
    def save(self, file_name='model.pth'):
        model_dir_path = './model'
        if not os.path.exists(model_dir_path):
            os.mkdir(model_dir_path)
        file_path = os.path.join(model_dir_path, file_name)
        torch.save(self.state_dict(), file_path)

class QTrainer:
    def __init__(self, model, lr, gamma):
        self.model = model
        self.lr = lr
        self.gamma = gamma
        self.optimizer = optim.Adam(model.parameters(), lr=lr)
        self.loss_function = nn.MSELoss()
    
    def train_step(self, state, action, reward, next_state, is_game_over):
        state_tensor = torch.tensor(state, dtype=torch.float)
        next_state_tensor = torch.tensor(next_state, dtype=torch.float)
        action_tensor = torch.tensor(action, dtype=torch.long)
        reward_tensor = torch.tensor(reward, dtype=torch.float)

        if len(np.shape(state)) == 1:
            # x -> (1, x)
            state_tensor = torch.unsqueeze(state_tensor, 0)
            next_state_tensor = torch.unsqueeze(next_state_tensor, 0)
            action_tensor = torch.unsqueeze(action_tensor, 0)
            reward_tensor = torch.unsqueeze(reward_tensor, 0)
            is_game_over = (is_game_over, )
        
        # predicted Q values with current state
        pred = self.model(state_tensor)
        target = pred.clone()

        for i in range(len(is_game_over)):
            new_Q = reward_tensor[i]
            if not is_game_over[i]:
                new_Q = reward_tensor[i] + self.gamma * torch.max(self.model(next_state_tensor[i]))
            
            target[i][torch.argmax(action_tensor).item()] = new_Q
        
        self.optimizer.zero_grad()
        loss = self.loss_function(target, pred)
        loss.backward()

        self.optimizer.step()