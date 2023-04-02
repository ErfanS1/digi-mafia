import enum


class Team(enum.Enum):
    Citizen = 'Citizen'
    Mafia = 'Mafia'
    Independent = 'Independent'


class GameStatus(enum.Enum):
    New = 'New'
    Started = 'Started'
    Finished = 'Finished'
