class ComputationOldCurriculum:
    @staticmethod
    def calculation(raw_score, hps):
        # Check if raw score is exactly 50% of HPS
        if raw_score == 0.5 * hps:
            return 75.0  # Automatically set grade to 75%
        return (raw_score / hps) * 100  # Normal calculation

    @staticmethod
    def average(total, qty):
        return total / qty if qty > 0 else 0

    @staticmethod
    def calculate_semestral_grade(midtermgrade, finalsgrade):
        return round((midtermgrade + finalsgrade) / 2, 2)

    @staticmethod
    def get_numerical_equivalent(semestralgrade):
        thresholds = [97, 94, 91, 88, 85, 82, 79, 76, 75]
        grades = [1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0]
        for threshold, grade in zip(thresholds, grades):
            if semestralgrade >= threshold:
                return grade
        return 5.0

    @staticmethod
    def get_remarks(grade):
        return "PASSED" if 1.0 <= grade <= 3.0 else "FAILED"

    @staticmethod
    def get_component_score(name, raw_score, hps):
        if raw_score > hps:
            return "Error: Score cannot be higher than the highest possible score."
        return ComputationOldCurriculum.calculation(raw_score, hps)


    @staticmethod
    def calculate_other_components(phase, scores):
        lab_reports_hps, lab_reports_scores, homework_hps, homework_scores, attendance_days, days_attended, recitations, recitations_participations, portfolio_score = scores

        # Lab Reports/Exercises (10%)
        if lab_reports_scores:
            total_lab_percentage = sum(
                ComputationOldCurriculum.get_component_score(f"{phase} Lab Report/Exercise {i}", score, lab_reports_hps)
                for i, score in enumerate(lab_reports_scores, 1))
            avg_lab_percentage = ComputationOldCurriculum.average(total_lab_percentage, len(lab_reports_scores))
            lab_weighted = avg_lab_percentage * 0.10
        else:
            lab_weighted = 0

        # Homework Assignments (10%)
        if homework_scores:
            total_homework_percentage = sum(
                ComputationOldCurriculum.get_component_score(f"{phase} Homework {i}", score, homework_hps)
                for i, score in enumerate(homework_scores, 1))
            avg_homework_percentage = ComputationOldCurriculum.average(total_homework_percentage, len(homework_scores))
            homework_weighted = avg_homework_percentage * 0.10
        else:
            homework_weighted = 0

        # Attendance (5%)
        if attendance_days > 0:
            attendance_percentage = (days_attended / attendance_days) * 100
            attendance_weighted = attendance_percentage * 0.05
        else:
            attendance_weighted = 0

        # Recitations (5% - Midterm Only)
        recitation_weighted = 0
        if phase.lower() == "midterm":
            if recitations > 0:
                recitation_percentage = (recitations_participations / recitations) * 100
                recitation_weighted = recitation_percentage * 0.05

        # Portfolio (5% - Finals Only)
        portfolio_weighted = 0
        if phase.lower() == "finals":
            if portfolio_score:
                portfolio_weighted = ComputationOldCurriculum.get_component_score(f"{phase} Student Portfolio", portfolio_score, 100) * 0.05

        total_other_components_weight = (10 if lab_weighted > 0 else 0) + \
                                        (10 if homework_weighted > 0 else 0) + \
                                        (5 if attendance_weighted > 0 else 0) + \
                                        (5 if recitation_weighted > 0 else 0) + \
                                        (5 if portfolio_weighted > 0 else 0)

        total_other_components_score = lab_weighted + homework_weighted + attendance_weighted + recitation_weighted + portfolio_weighted

        if total_other_components_weight > 0:
            redistributed_score = total_other_components_score * (30 / total_other_components_weight)
        else:
            redistributed_score = 0

        return redistributed_score

    @staticmethod
    def calculate_midterm_finals(phase, scores):
        quizzes_hps, quizzes_scores, exam_hps, exam_score = scores

        # Quizzes (30%)
        if quizzes_scores:
            total_quiz_percentage = sum(
                ComputationOldCurriculum.get_component_score(f"{phase} Quiz {i}", score, quizzes_hps)
                for i, score in enumerate(quizzes_scores, 1))
            avg_quiz_percentage = ComputationOldCurriculum.average(total_quiz_percentage, len(quizzes_scores))
            quiz_weighted = avg_quiz_percentage * 0.30
        else:
            quiz_weighted = 0

        # Exam (40%)
        exam_weighted = ComputationOldCurriculum.get_component_score(f"{phase} Exam", exam_score, exam_hps) * 0.40

        # Other Components (30%)
        other_components_weighted = ComputationOldCurriculum.calculate_other_components(phase, scores[2:])

        total_grade = quiz_weighted + exam_weighted + other_components_weighted
        return round(total_grade, 2)
