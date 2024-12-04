class ComputationNewCurriculum:
    @staticmethod
    def calculation(raw_score, hps):
        if raw_score > hps:
            return "Error: Score cannot be higher than the highest possible score."
        return (raw_score / hps) * 100

    @staticmethod
    def average(total, qty):
        return total / qty if qty > 0 else 0

    @staticmethod
    def calculate_semestral_grade(midtermgrade, finalsgrade):
        return round((midtermgrade * 1 / 3) + (finalsgrade * 2 / 3), 2)

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
        score_percentage = ComputationNewCurriculum.calculation(raw_score, hps)

        if raw_score < 0.60 * hps:
            return score_percentage  # Return the calculated percentage
        elif raw_score == 0.60 * hps:
            return 75  # Set to 75% for meeting the exact threshold
        else:
            return score_percentage  # Return the calculated percentage

    @staticmethod
    def calculate_other_components(phase, scores):
        lab_exam_hps, lab_exam_score, lab_reports_hps, lab_reports_scores, class_activities_hps, class_activities_scores, class_participation_hps, class_participation_scores, practicum_hps, practicum_scores = scores

        lab_exam_weighted = ComputationNewCurriculum.get_component_score(f"{phase} Laboratory Exam", lab_exam_score, lab_exam_hps) * 0.40

        component_weights = {"lab_reports": 0.15, "class_activities": 0.15, "class_participation": 0.15, "practicum": 0.15}

        if lab_reports_scores:
            total_lab_reports_percentage = sum(
                ComputationNewCurriculum.get_component_score(f"{phase} Lab Report {i}", score, lab_reports_hps)
                for i, score in enumerate(lab_reports_scores, 1))
            avg_lab_reports_percentage = ComputationNewCurriculum.average(total_lab_reports_percentage, len(lab_reports_scores))
            lab_reports_weighted = avg_lab_reports_percentage * component_weights["lab_reports"]
        else:
            lab_reports_weighted = 0
            component_weights["lab_reports"] = 0

        if class_activities_scores:
            total_class_activities_percentage = sum(
                ComputationNewCurriculum.get_component_score(f"{phase} Class Activity {i}", score, class_activities_hps)
                for i, score in enumerate(class_activities_scores, 1))
            avg_class_activities_percentage = ComputationNewCurriculum.average(total_class_activities_percentage, len(class_activities_scores))
            class_activities_weighted = avg_class_activities_percentage * component_weights["class_activities"]
        else:
            class_activities_weighted = 0
            component_weights["class_activities"] = 0

        if class_participation_scores:
            total_class_participation_percentage = sum(
                ComputationNewCurriculum.get_component_score(f"{phase} Class Participation {i}", score, class_participation_hps)
                for i, score in enumerate(class_participation_scores, 1))
            avg_class_participation_percentage = ComputationNewCurriculum.average(total_class_participation_percentage,
                                                                 len(class_participation_scores))
            class_participation_weighted = avg_class_participation_percentage * component_weights["class_participation"]
        else:
            class_participation_weighted = 0
            component_weights["class_participation"] = 0

        if practicum_scores:
            total_practicum_percentage = sum(
                ComputationNewCurriculum.get_component_score(f"{phase} Practicum {i}", score, practicum_hps)
                for i, score in enumerate(practicum_scores, 1))
            avg_practicum_percentage = ComputationNewCurriculum.average(total_practicum_percentage, len(practicum_scores))
            practicum_weighted = avg_practicum_percentage * component_weights["practicum"]
        else:
            practicum_weighted = 0
            component_weights["practicum"] = 0

        active_weights = [component_weights[key] for key in component_weights if component_weights[key] > 0]
        total_active_weight = sum(active_weights)

        if total_active_weight > 0:
            scale_factor = 0.60 / total_active_weight
        else:
            scale_factor = 0

        lab_reports_weighted *= scale_factor
        class_activities_weighted *= scale_factor
        class_participation_weighted *= scale_factor
        practicum_weighted *= scale_factor

        total_grade = lab_exam_weighted + lab_reports_weighted + class_activities_weighted + class_participation_weighted + practicum_weighted
        return round(total_grade, 2)
