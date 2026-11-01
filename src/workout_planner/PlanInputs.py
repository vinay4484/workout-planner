import typing


class PlanInputs:

    def __init__(self, fitness_goal: str,
                 experience_level: str, days_available_per_week: str,
                 equipment_access: str, injuries_or_limittions: typing.Optional[str]) -> None:
        self.fitness_goal = fitness_goal
        self.experience_level = experience_level
        self.days_available_per_week = days_available_per_week
        self.equipment_access = equipment_access
        self.injuries_or_limittions = injuries_or_limittions





