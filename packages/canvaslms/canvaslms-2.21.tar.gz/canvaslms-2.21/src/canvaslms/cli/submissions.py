import canvasapi.submission

import canvaslms.cli.assignments as assignments
import canvaslms.cli.users as users
import canvaslms.hacks.canvasapi

import argparse
import csv
import json
import os
import pypandoc
import re
import rich.console
import rich.markdown
import sys
import urllib.request

def submissions_command(config, canvas, args):
  assignment_list = assignments.process_assignment_option(canvas, args)
  if args.ungraded:
    submissions = list_ungraded_submissions(assignment_list)
  else:
    submissions = list_submissions(assignment_list)

  if args.user or args.category or args.group:
    user_list = users.process_user_or_group_option(canvas, args)
    submissions = filter_submissions(submissions, user_list)

  output = csv.writer(sys.stdout, delimiter=args.delimiter)

  for submission in submissions:
    if args.login_id:
      output.writerow(format_submission_short_unique(submission))
    else:
      output.writerow(format_submission_short(submission))
def speedgrader(submission):
  """Returns the SpeedGrader URL of the submission"""
  speedgrader_url = submission.preview_url

  speedgrader_url = re.sub("assignments/",
    "gradebook/speed_grader?assignment_id=",
    speedgrader_url)

  speedgrader_url = re.sub("/submissions/",
    "&student_id=",
    speedgrader_url)

  speedgrader_url = re.sub(r"\?preview.*$", "", speedgrader_url)

  return speedgrader_url
def submission_command(config, canvas, args):
  submission_list = process_submission_options(canvas, args)
  console = rich.console.Console()
  for submission in submission_list:
    output = format_submission(submission)

    if sys.stdout.isatty():
      pager = ""
      if "MANPAGER" in os.environ:
        pager = os.environ["MANPAGER"]
      elif "PAGER" in os.environ:
        pager = os.environ["PAGER"]

      styles = False
      if "less" in pager and ("-R" in pager or "-r" in pager):
        styles = True
      with console.pager(styles=styles):
        console.print(rich.markdown.Markdown(output,
                                             code_theme="manni"))
    else:
      print(output)
def add_submission_options(parser, required=False):
  try:
    assignments.add_assignment_option(parser, required=required)
  except argparse.ArgumentError:
    pass

  try:
    users.add_user_or_group_option(parser, required=required)
  except argparse.ArgumentError:
    pass

  submissions_parser = parser.add_argument_group("filter submissions")
  try: # to protect from this option already existing in add_assignment_option
    submissions_parser.add_argument("-U", "--ungraded", action="store_true",
      help="Only ungraded submissions.")
  except argparse.ArgumentError:
    pass

def process_submission_options(canvas, args):
  assignment_list = assignments.process_assignment_option(canvas, args)
  user_list = users.process_user_or_group_option(canvas, args)

  if args.ungraded:
    submissions = list_ungraded_submissions(assignment_list,
      include=["submission_history", "submission_comments", 
      "rubric_assessment"])
  else:
    submissions = list_submissions(assignment_list,
      include=["submission_history", "submission_comments", 
      "rubric_assessment"])

  return list(filter_submissions(submissions, user_list))
def list_submissions(assignments, include=["submission_comments"]):
  for assignment in assignments:
    submissions = assignment.get_submissions(include=include)
    for submission in submissions:
      submission.assignment = assignment
      yield submission

def list_ungraded_submissions(assignments, include=["submisson_comments"]):
  for assignment in assignments:
    submissions = assignment.get_submissions(bucket="ungraded",
      include=include)
    for submission in submissions:
      if submission.submitted_at and (submission.graded_at is None or
          not submission.grade_matches_current_submission):
        submission.assignment = assignment
        yield submission
def filter_submissions(submission_list, user_list):
  user_list = set(user_list)

  for submission in submission_list:
    for user in user_list:
      if submission.user_id == user.id:
        submission.user = user
        yield submission
        break
def format_submission_short(submission):
  return [
    submission.assignment.course.course_code,
    submission.assignment.name,
    submission.user.name,
    submission.grade, submission.submitted_at, submission.graded_at
  ]
def format_submission_short_unique(submission):
  uid = users.get_uid(submission.user)

  return [
    submission.assignment.course.course_code,
    submission.assignment.name,
    uid,
    submission.grade, submission.submitted_at, submission.graded_at
  ]
def format_submission(submission):
  """Formats submission for printing to stdout"""
  student = submission.assignment.course.get_user(submission.user_id)

  formatted_submission = ""

  formatted_submission += format_section(
    "Metadata",
    f"{submission.assignment.course.course_code} > {submission.assignment.name}"
    f"\n\n"
    f" - Student: {student.name} "
      f"({student.login_id or None}, {submission.user_id})\n"
    f" - Submission ID: {submission.id}\n"
    f" - Submitted (graded): {submission.submitted_at} "
      f"({submission.graded_at})\n"
    f" - Grade: {submission.grade} ({submission.score})\n"
    f" - Graded by: {resolve_grader(submission)}\n"
    f" - SpeedGrader: {speedgrader(submission)}")
  try:
    if submission.rubric_assessment:
      formatted_submission += format_section(
        "Rubric assessment",
        format_rubric(submission))
  except AttributeError:
    pass
  try:
    if submission.submission_comments:
      body = ""
      for comment in submission.submission_comments:
        body += f"{comment['author_name']} ({comment['created_at']}):\n\n"
        body += comment["comment"] + "\n\n"
      formatted_submission += format_section("Comments", body)
  except AttributeError:
    pass
  try:
    if submission.body:
      formatted_submission += format_section("Body", submission.body)
  except AttributeError:
    pass
  try:
    if submission.submission_data:
      formatted_submission += format_section(
        "Quiz answers",
        json.dumps(submission.submission_data, indent=2))
  except AttributeError:
    pass
  try:
    for attachment in submission.attachments:
      content_type = ct_to_md(attachment["content-type"])
      if not content_type:
        continue

      contents = urllib.request.urlopen(attachment["url"]).read().decode("utf8")

      formatted_submission += format_section(
        attachment["filename"],
        f"```{content_type}\n{contents}\n```"
      )
  except AttributeError:
    pass
  try:
    if submission.submission_history:
      for prev_submission in submission.submission_history:
        prev_submission = canvasapi.submission.Submission(
          submission._requester, prev_submission)
        prev_submission.assignment = submission.assignment

        formatted_submission += "\n\n" + format_submission(prev_submission)
  except AttributeError:
    pass

  return formatted_submission
def format_section(title, body):
  return f"\n# {title}\n\n{body}\n\n"
def resolve_grader(submission):
  """
  Returns a user object if the submission was graded by a human.
  Otherwise returns None if ungraded or a descriptive string.
  """
  try:
    if submission.grader_id is None:
      return None
  except AttributeError:
    return None
    
  if submission.grader_id < 0:
    return "autograded"
  return submission.assignment.course.get_user(submission.grader_id)
def ct_to_md(content_type):
  """
  Takes a content type, returns Markdown code block type.
  Returns None if not possible.
  """
  if content_type.startswith("text/"):
    content_type = content_type[len("text/"):]
  else:
    return None

  if content_type.startswith("x-"):
    content_type = content_type[2:]
  if content_type == "python-script":
    content_type = "python"

  return content_type
def format_rubric(submission):
  """Format the rubric assessment of the `submission` in readable form."""

  result = ""

  for crit_id, rating_data in submission.rubric_assessment.items():
    criterion = get_criterion(crit_id, submission.assignment.rubric)
    rating = get_rating(rating_data["rating_id"], criterion)

    result += f"{criterion['description']}: {rating['description']} " \
      f"({rating['points']})\n"

    if rating_data["comments"]:
      result += f"Comments: {rating_data['comments']}\n"

    result += "\n"

  return result.strip()
def get_criterion(criterion_id, rubric):
  """Returns criterion with ID `criterion_id` from rubric `rubric`"""
  for criterion in rubric:
    if criterion["id"] == criterion_id:
      return criterion

  return None
def get_rating(rating_id, criterion):
  """Returns rating with ID `rating_id` from rubric criterion `criterion`"""
  for rating in criterion["ratings"]:
    if rating["id"] == rating_id:
      return rating

  return None

def add_command(subp):
  """Adds the submissions and submission commands to argparse parser subp"""
  add_submissions_command(subp)
  add_submission_command(subp)

def add_submissions_command(subp):
  """Adds submissions command to argparse parser subp"""
  submissions_parser = subp.add_parser("submissions",
      help="Lists submissions of an assignment",
      description="Lists submissions of assignment(s). Output format: "
        "<course code> <assignment name> <user> <grade> "
        "<submission date> <grade date>")
  submissions_parser.set_defaults(func=submissions_command)
  assignments.add_assignment_option(submissions_parser)
  add_submission_options(submissions_parser)
  submissions_parser.add_argument("-l", "--login-id",
    help="Print login ID instead of name.",
    default=False, action="store_true")

def add_submission_command(subp):
  """Adds submission command to argparse parser subp"""
  submission_parser = subp.add_parser("submission",
    help="Prints information about a submission",
    description="Prints data about matching submissions, "
      "including submission and grading time, any text-based attachments.")
  submission_parser.set_defaults(func=submission_command)
  add_submission_options(submission_parser)
