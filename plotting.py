import matplotlib.pyplot as plt
from IPython.display import clear_output, display

plt.ion()

def plot(scores, mean_scores):
    clear_output(wait=True)
    display(plt.gcf())
    plt.clf()
    plt.title('Training')
    plt.xlabel('Episodes (games)')
    plt.ylabel('Score')
    plt.ylim(ymin=0)
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))