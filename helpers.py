import matplotlib.pyplot as plt
import scipy.stats as stats
import models
from typing import List
import math



def select_owners_with_normal_distribution(participants_no,randoms_count):
    normal_rand = stats.truncnorm(-participants_no/10, participants_no /10, loc=participants_no/2, scale=5)
    owner_ids = normal_rand.rvs(randoms_count)
    owner_ids = [math.floor(id) for id in owner_ids]
    return owner_ids

def KL_divergence(expected:List[int],real:List[int]):
    kl = stats.entropy(real,expected)
    return kl


def create_distribution(tickets:List[models.Ticket],owners:List[models.Participant]) -> List[float]:
    participant_wins=[0.0]*len(owners)
    for t in tickets:
        participant_wins[owners.index(t.owner)] += float(1)/len(tickets)
    return participant_wins

def create_plot(expected_distribution:List[float],real_distribution:List[float]):
    plt.plot(expected_distribution,label="expected")
    plt.plot(real_distribution,label="real")
    plt.legend()
    print("saving distribution plot...")
    plt.savefig("test_distributions.png")

