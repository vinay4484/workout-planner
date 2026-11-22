from dataclasses import dataclass


@dataclass
class WorkoutInput:
    fitness_goal: str
    experience_level: str
    days_per_week: int
    equipment_access: str
    injuries: str