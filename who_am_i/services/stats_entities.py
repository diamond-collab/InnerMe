from dataclasses import dataclass


@dataclass
class CommonStats:
    users: int
    finished_quizzes: int
    attempts: int


@dataclass
class QuizStats:
    total_attempts: int
    unique_users: int
    avg_result: int


@dataclass
class PopularQuizStats:
    quiz_id: int
    title: str
    attempts_count: int
