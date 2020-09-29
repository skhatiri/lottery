from peewee import *
import uuid
from typing import List
import random

database = SqliteDatabase("sqlite.db")
database.connect()

def create_tables():
    with database:
        database.create_tables([Lottery,Ticket,Participant])

def drop_tables():
    with database:
        database.drop_tables([Lottery,Ticket,Participant])


class BaseModel(Model):
    class Meta:
        database = database

class Participant(BaseModel):
    """lottery participant"""

    name = CharField() 

    def __str__(self):
        return "participant:{}".format(self.name)


class Lottery(BaseModel):
    name = CharField()

    def draw (self):
        """returns a winner ticket at random"""
        tickets_count = self.tickets.count()
        winner_index = random.randrange (0,tickets_count)
        winner = self.tickets[winner_index]
        return winner

    def multiple_draw (self,count:int):
        """returns winner tickets at random"""
        tickets_count = self.tickets.count()
        winners = []
        for i in range (0,count):
            winner_index = random.randrange (0,tickets_count/10)
            winner = self.tickets[winner_index]
            winners.append(winner)
        return winners

    def __str__(self):
        return "lottery:{}".format(self.name)

class Ticket(BaseModel):
    """lottry ticket implementation"""
    owner = ForeignKeyField(Participant, backref='tickets')
    id = UUIDField(default=uuid.uuid4())
    lottery = ForeignKeyField(Lottery, backref='tickets')

    def __str__(self):
        return "ticket_no:{}\t owner:{}\t lottery:{}".format(self.id,self.owner.name,self.lottery.name)


if __name__ == '__main__':
    create_tables()
