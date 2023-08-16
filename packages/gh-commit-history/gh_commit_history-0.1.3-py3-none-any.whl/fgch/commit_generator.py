import sys
import os
import subprocess
import random
from datetime import datetime, timedelta
from dateutil.parser import parse
from pathlib import Path


def validate_boolean(value, name):
    if not isinstance(value, bool):
        raise ValueError(f"{name} must be a boolean value.")


def validate_percentage(value, name):
    if not (0 <= value <= 1):
        raise ValueError(
            f"{name} must be a floating-point number between 0 and 1 (inclusive).")


def validate_working_hours(value, name):
    if not isinstance(value, list) or len(value) != 2 or not all(isinstance(item, int) or (0 <= item <= 23) for item in value):
        raise ValueError(
            f"{name} must be in the format 'int-int' of values between 0-23 in military hours.")
    elif value[0] > value[1]:
        raise ValueError(f"{name} must have a valid ascending range")


def validate_commit_ranges(value, name):
    if not isinstance(value, list) or len(value) != 2 or not all(isinstance(item, int) or (item >= 0) for item in value):
        raise ValueError(
            f"{name} must be in the format 'int-int' of values 0 and above.")
    elif value[0] > value[1]:
        raise ValueError(f"{name} must have a valid ascending range")


def validate_gradient(value):
    if value not in ['linear', 'exponential', 'bursts']:
        raise TypeError(
            "gradient must be either 'linear', 'exponential', or 'bursts'.")


def generate_commits(workdays_only=False, weekend_behavior=False, commits_per_day="0-3", start_date=None, end_date=None, gradient=None, no_commit_percentage=0, working_hours="9-17"):
    try:
        try:
            commits_per_day = list(map(int, commits_per_day.split("-")))
            validate_commit_ranges(commits_per_day, "commits_per_day")
        except:
            print(
                "Error: commits_per_day must be in the format 'int-int' of values 0 and above of valid ascending ranges.")
            return
        try:
            working_hours_range = list(map(int, working_hours.split("-")))
            validate_working_hours(working_hours_range, "working_hours")
        except:
            print(
                "Error: working_hours must be in the format 'int-int' of values between 0-23 in military hours of valid ascending ranges.")
            return
        try:
            start_date = parse(
                start_date) if start_date else datetime.now() - timedelta(days=365)
        except:
            print("Error: must be in a valid date in the format MM/DD/YYYY.")
            return
        try:
            end_date = parse(end_date) if end_date else datetime.now()
        except:
            print("Error: end_date must be in a valid date in the format MM/DD/YYYY.")
            return
        if(start_date >= end_date):
            raise ValueError("start_date cannot be later than the end_date")
        validate_boolean(weekend_behavior, "weekend_behavior")
        validate_gradient(gradient)
        validate_boolean(workdays_only, "workdays_only")
        validate_percentage(no_commit_percentage, "no_commit_percentage")

        commit_date_list = create_commit_date_list(
            commits_per_day=commits_per_day, gradient=gradient, workdays_only=workdays_only, no_commit_percentage=no_commit_percentage, working_hours_range=working_hours_range, start_date=start_date, end_date=end_date, weekend_behavior=weekend_behavior
        )
        print("Generating your GitHub commit history")

        history_folder = "github-history"

        # Remove git history folder if it already exists.
        if os.path.exists(history_folder):
            subprocess.run(
                [sys.executable, "-c",
                    f"import shutil; shutil.rmtree('{history_folder}')"],
                shell=True,
            )

        os.makedirs(history_folder, exist_ok=True)
        os.chdir(history_folder)
        subprocess.run(["git", "init"])

        for commit_date in commit_date_list:
            print(
                f"Generating GitHub commit history... ({commit_date.strftime('%Y-%m-%d %H:%M:%S')})")
            with open("fake-history.txt", "w") as file:
                file.write(commit_date.strftime('%Y-%m-%d %H:%M:%S'))
            subprocess.run(["git", "add", "."])
            subprocess.run(
                ["git", "commit", "--quiet", "--date",
                    commit_date.strftime('%Y-%m-%d %H:%M:%S'), "-m", "fake commit"]
            )
        print(f"{len(commit_date_list)} commits have been created.")
    except Exception as e:
        print(f"Error: {str(e)}")


def create_commit_date_list(commits_per_day, gradient, workdays_only, no_commit_percentage, working_hours_range, start_date, end_date, weekend_behavior):
    commit_date_list = []
    current_date = start_date
    date_difference = (end_date - start_date).days
    day_count = 0

    while current_date <= end_date:
        day_count += 1
        if workdays_only and current_date.weekday() >= 5:
            current_date += timedelta(days=1)
        else:
            if random.random() <= no_commit_percentage:
                current_date += timedelta(days=1)
            else:
                lower_bound = 0
                commits_range = random.randint(commits_per_day[0], commits_per_day[1])
                if weekend_behavior and current_date.weekday() >= 5:
                    commits_range = random.randint(0,1)
                else:
                    if (gradient == 'linear'):
                        lower_bound = round(commits_per_day[0] + (round(sum(commits_per_day) / len(commits_per_day)) - commits_per_day[0]) * (day_count/date_difference))
                        commits_range = random.randint(lower_bound, commits_per_day[1])
                    elif(gradient == 'exponential'):
                        lower_bound = round(commits_per_day[0] + (sum(commits_per_day) // len(commits_per_day)) * (1 - (2 ** (-day_count / date_difference))))
                        commits_range = random.randint(lower_bound, commits_per_day[1])
                    elif(gradient=='bursts'):
                        period = 21 #Every 3 weeks
                        lower_bound = round(commits_per_day[0] + (commits_per_day[1] - commits_per_day[0]) * (abs(day_count % period - period // 2) / (period // 2)))
                        commits_range = random.randint(lower_bound, commits_per_day[1])
                for commit in range(commits_range):
                    date_with_hours = current_date.replace(
                        hour=random.randint(working_hours_range[0], working_hours_range[1])
                    )
                    date_with_hours_and_minutes = date_with_hours.replace(
                        minute=random.randint(0, 59)
                    )
                    commit_date = date_with_hours_and_minutes.replace(
                        second=random.randint(0, 59)
                    )

                    commit_date_list.append(commit_date)
            current_date += timedelta(days=1)

    return commit_date_list
