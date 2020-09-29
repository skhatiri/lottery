import unittest
from typing import List
import models
import random
import helpers

#Maximum Kullback–Leibler divergence value to suppose expected and real distributions are similar 
KL_MAX = 0.05

# no. test participants
PARTICIPANTS_NO = 20

# no. test tickets to assign to participants
TICKETS_NO = 1000

# no. draws to find out real distribution
DRAWS_NO = 2000


class Tests(unittest.TestCase):
    

    def test_db(self):
        """tests weather data can be stored in an empty database"""
        print("testing database operations")
        models.drop_tables()
        models.create_tables()
        lottery = models.Lottery.create(name = "test")
        self.assertIsNotNone(lottery)
        owner = models.Participant.create(name="test")
        self.assertIsNotNone(owner)
        ticket = models.Ticket.create(lottery=lottery,owner=owner)
        self.assertIsNotNone(ticket)

    def setup_uniform(self, participants_no:int,tickets_no:int):
        """sets up environment with uniform distribution of tickets between participants"""
        self.lottery = models.Lottery.create(name="uniform lottery")
        self.participants = [ models.Participant.create(name = "p"+str(i)) for i in range(0,participants_no)] 
        self.tickets = [models.Ticket.create(owner=self.participants[random.randrange(0,participants_no)],lottery=self.lottery) for i in range(0,tickets_no)]

    def setup_normal(self, participants_no:int,tickets_no:int):
        """sets up environment with normal distribution of tickets between participants"""
        self.lottery = models.Lottery.create(name="normal lottery")
        self.participants = [ models.Participant.create(name = "p"+str(i)) for i in range(0,participants_no)] 
        owner_inds = helpers.select_owners_with_normal_distribution(participants_no,tickets_no) 
        self.tickets = [models.Ticket.create(owner=self.participants[ind],lottery=self.lottery) for ind in owner_inds]

    def test_draw(self):
        """tests whether a single ticket can be drawn out of the lottery"""
        print("testing single draw")
        self.setup_normal(PARTICIPANTS_NO,TICKETS_NO)
        winner_ticket = self.lottery.draw()
        self.assertIsNotNone(winner_ticket)


    def test_fairness(self):
        """tests whether the draws for multiple are similar enough to the expected distribution, based on Kullback–Leibler divergence"""
        print("testing lottery fairness")
        self.setup_normal(PARTICIPANTS_NO,TICKETS_NO)
        winner_tickets=self.lottery.multiple_draw(DRAWS_NO)
        winners_distribution = helpers.create_distribution(winner_tickets,self.participants)
        expected_distribution = helpers.create_distribution(self.tickets,self.participants)
        kl=helpers.KL_divergence(expected_distribution,winners_distribution)
        print ("KL distance:{}".format(kl))
        helpers.create_plot(expected_distribution,winners_distribution)
        self.assertLessEqual(kl,KL_MAX,"the lottery draw is not fair enough, (KL ={})".format(kl))


if __name__ == '__main__':
    unittest.main(exit=False)
