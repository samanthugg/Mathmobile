"""This module contains the leaderboard class"""
import json
from enums import DifficultyLevel, Operation


class Leaderboard:
    """Holds data structure, read, write, and insert capabilities for Leaderboard"""

    def __init__(self, file_path: str = "leaderboard.json"):
        self._file_path = file_path
        self._scores_list = []
        self.load_file()

    @property
    def scores_list(self) -> list:
        """Returns the entire leaderboard scores list"""
        return self._scores_list.copy()

    def load_file(self):
        """Loads the saves leaderboard to the in class data structure scores"""
        try:
            with open(self._file_path, 'r', encoding='utf-8') as f:
                self._scores_list = json.load(f)
            print("Load complete.")

        except FileNotFoundError:
            print("File not found. First player yay!.")

        except json.JSONDecodeError:
            print("Error decoding JSON. The file might be corrupted.")

    def _get_scores(self, level: DifficultyLevel, operation: Operation) -> list:
        """Protected - Returns the list of scores on leaderboard
            matching the skill and operation.
            If the list does not exist, returns None"""
        for scores in self._scores_list:
            # find the dictionary that matches the skill and operation
            if scores.get('skill') == level.value and scores.get('operation') == operation.value:
                return scores.get('scores')
        return None

    def get_scores(self, level: DifficultyLevel, operation: Operation) -> list:
        """Public - Returns a copy of the list of scores on leaderboard
            matching the skill and operation.
            If the list does not exist, returns None"""
        scores = self._get_scores(level, operation)
        if scores:
            return scores.copy()
        return None

    def insert_score(self, level: DifficultyLevel,
                     operation: Operation, name: str, score: int) -> bool:
        """Adds a score to the leaderboard. Only maintains the top 10.  Returns True
            if the score was added.  Else returns False"""
        score_list = [dict]
        score_list = self._get_scores(level, operation)
        new_score_dict = {"name": name, "score": score}

        # If false, there are no records for the level and operation.
        # create the dict, append to the master list, write file, return True
        if not score_list:
            score_dict = {
                "operation": operation.value,
                "skill": level.value,
                "scores": [
                    new_score_dict
                ]
            }
            self._scores_list.append(score_dict)
            self._write_file()
            return True

        # If it exists, add it, sort it so lowest score is at end
        score_list.append(new_score_dict)
        score_list.sort(key=lambda score: score['score'], reverse=True)

        # If there are more than 10 entries on list, lowest is popped.
        # if the popped one was the new one no need to write to file
        # return False

        if len(score_list) > 10:
            low_dict = score_list.pop()

            if low_dict == new_score_dict:
                return False

        # Write changes to file and return True
        self._write_file()
        return True

    def _write_file(self):
        """Protected method to write the leaderboard data to file"""
        try:
            with open(self._file_path, 'w', encoding='utf-8') as file:
                json.dump(self._scores_list, file, indent=4)

        except OSError:
            print("Something went wrong. File not written")


def main():
    """Testing the leaderboard class"""
    lb = Leaderboard()
    hard = DifficultyLevel.HARD
    med = DifficultyLevel.MEDIUM
    easy = DifficultyLevel.EASY

    add = Operation.ADD
    sub = Operation.SUBTRACT
    div = Operation.DIVIDE
    mul = Operation.MULTIPLY

    base = 10
    loop = 0

    while loop < 15:
        loop += 1
        lb.insert_score(hard, add, f"Jun {loop}", (loop * base))
        lb.insert_score(easy, mul, f"Dennis {loop}", (loop * base))
        lb.insert_score(med, div, f"Jonathan {loop}", (loop * base))
        lb.insert_score(easy, sub, f"Samantha {loop}", (loop * base))

    list1 = lb.get_scores(hard, add)
    list2 = lb.get_scores(easy, mul)
    list3 = lb.get_scores(med, div)
    list4 = lb.get_scores(easy, sub)

    if list1:
        for item in list1:
            print(item)
    print()

    if list2:
        for item in list2:
            print(item)
    print()

    if list3:
        for item in list3:
            print(item)

    if list4:
        for item in list4:
            print(item)
    print()
    print("All done!")


if __name__ == "__main__":
    main()
