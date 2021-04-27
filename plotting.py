import matplotlib.pyplot as plt
from IPython.display import clear_output, display

plt.ion()
plt.show()

def plot(scores, mean_scores):
    clear_output(wait=True)
    display(plt.gcf())
    plt.clf()
    plt.title('Training')
    plt.xlabel('Episodes (games)')
    plt.ylabel('Score')
    plt.ylim(ymin=0)
    plt.plot(scores, color='orange', label='Score')
    plt.plot(mean_scores, color='green', label='Mean score')
    plt.legend()
    plt.pause(0.001)