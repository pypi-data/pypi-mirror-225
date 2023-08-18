import random

positive_comments = [
    "🥳",
    "Awesome work.",
    "Boom! You got it.",
    "Correct.",
    "Excellent work.",
    "Excellent! Keep going.",
    "Good work!",
    "Party time! 🎉🎉🎉",
    "Python master 😁",
    "Spot on! 🎯",
    "That's right.",
    "That's the right answer. Keep it up!",
    "Time to put on your cool kid glasses. 😎",
    "Very impressive.",
    "Way to go!",
    "Wow, you're making great progress.",
    "Yes! Great problem solving.",
    "Yes! Keep on rockin'. 🎸",
    "Yes! Your hard work is paying off.",
    "You = coding 🥷",
    "You got it. Dance party time! 🕺💃🕺💃",
    "You're making this look easy. 😉",
    "Yup. You got it.",
]


error_codes = {
    "A01": "type",
    "A02": "title",
    "A03": "x-axis label",
    "A04": "y-axis label",
    "A05": "data",
    "E01": "is missing",
    "E02": "must be a(n) {object_name}",
    "E03": "should be `'{expected_object_val}'`, not `'{actual_object_val}'`",
    "E04": "doesn't match the expected result",
    "MP": "plot",
}


class Feedback:
    """Data class for feedback passed to student machine."""

    def __init__(self, evaluation) -> None:
        """Initialization method.

        Args:
            evaluation (Evaluation): Evaluation passed from ``graders`` module.
        """
        self.passed = evaluation.eval_code == "0"
        self.score = evaluation.points_awarded
        self.comment = self.convert_eval_to_comment(evaluation)

    def convert_eval_to_comment(self, evaluation) -> str:
        """Method converts eight-character error code into student-readable string.

        Args:
            evaluation (Evaluation): Evaluation passed from ``graders`` module.

        Returns:
            str: student-readable comment
        """
        if self.passed:
            return random.choice(positive_comments)

        object = error_codes.get(evaluation.eval_code[:2], "")
        attribute = error_codes.get(evaluation.eval_code[2:5], "")
        error = error_codes.get(evaluation.eval_code[-3:], "")
        if not evaluation.eval_context:
            comment = f"The {attribute} of your {object} " + error + "."
            return comment
        elif attribute == "type":
            comment = f"Your {object} " + error + "."
            return comment.format(
                object_name=evaluation.eval_context.object_name
            )
        else:
            comment = f"The {attribute} of your {object} " + error + "."
            return comment.format(
                actual_object_val=evaluation.eval_context.actual_object_val,
                expected_object_val=evaluation.eval_context.expected_object_val,
            )
