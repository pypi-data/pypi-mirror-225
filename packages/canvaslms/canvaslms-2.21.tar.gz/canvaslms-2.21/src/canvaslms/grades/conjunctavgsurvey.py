"""
This module is the same as `canvaslms.grades.conjunctavg` except that any 
submissions with grades other than A--F and P/F are treated as P. For instance, 
numeric grades (like points). Also, all submissions must have a date. This 
makes this module useful for including mandatory, ungraded surveys.
"""

import datetime as dt
from canvaslms.grades.conjunctavg import a2e_average
from canvaslms.cli import results
from canvasapi.exceptions import ResourceDoesNotExist

def summarize(user, assignments_list):
  """
  Extracts user's submissions for assignments in assingments_list to summarize 
  results into one grade and a grade date. Summarize by conjunctive average.

  If some submission lacks date, return ("F", None).
  """

  pf_grades = []
  a2e_grades = []
  dates = []
  graders = []

  for assignment in assignments_list:
    try:
      submission = assignment.get_submission(user,
                                            include=["submission_history"])
    except ResourceDoesNotExist:
      pf_grades.append("F")
      continue

    grade = submission.grade
    graders += results.all_graders(submission)

    if grade is None:
      grade = "F"

    if grade in "ABCDE":
      a2e_grades.append(grade)
    elif grade in "PF":
      pf_grades.append(grade)
    elif grade == "Fx":
      pf_grades.append("F")
    else:
      pf_grades.append("P")

    grade_date = submission.submitted_at or submission.graded_at

    if grade_date:
      grade_date = dt.date.fromisoformat(grade_date.split("T")[0])
      dates.append(grade_date)

  if all(map(lambda x: x == "P", pf_grades)):
    final_grade = "P"
    if a2e_grades:
      final_grade = a2e_average(a2e_grades)

  if dates:
    final_date = max(dates)
  else:
    final_date = None
    final_grade = None

  if len(dates) < len(pf_grades) + len(a2e_grades):
    final_grade = "F"

  return (final_grade, final_date, graders)

def summarize_group(assignments_list, users_list):
  """Summarizes a particular set of assignments (assignments_list) for all
  users in users_list"""

  for user in users_list:
    grade, grade_date, graders = summarize(user, assignments_list)
    yield [user, grade, grade_date, *graders]
