##############################################################
# Student Name: Moulik Jain
# PS Number: 94
# Project Title: Examination Timetable Generator
# Email: moulik.jain@rungta.org
# Section: B.Tech A2
##############################################################

from datetime import datetime, timedelta


DATE_FORMAT = "%d-%m-%Y"


# Function to validate the entered date
def validate_date(date_text):
    """Validate and convert a date in DD-MM-YYYY format."""
    try:
        parsed_date = datetime.strptime(date_text.strip(), DATE_FORMAT)

        if parsed_date.strftime(DATE_FORMAT) != date_text.strip():
            raise ValueError

        return parsed_date.date()

    except ValueError:
        raise ValueError(
            f"Invalid date: {date_text}. "
            "Please enter the date as DD-MM-YYYY."
        )


# Function to validate subjects and reject duplicates
def validate_subjects(subject_text):
    """Validate subjects and reject empty or duplicate entries."""

    if subject_text.strip().casefold() in ("", "none", "na", "n/a"):
        raise ValueError("At least one subject is required.")

    subjects = [subject.strip() for subject in subject_text.split(",")]

    if any(
        not subject or subject.casefold() in ("none", "na", "n/a")
        for subject in subjects
    ):
        raise ValueError("At least one subject is required.")

    # Check for duplicate subjects
    seen = set()

    for subject in subjects:
        if subject.casefold() in seen:
            raise ValueError(f"Duplicate subject: {subject}.")
        seen.add(subject.casefold())

    return subjects


# Function to validate and store holiday dates
def validate_holidays(holiday_text):
    """Convert optional holiday dates into a set."""
    holidays = set()

    # If the user enters none, there are no holidays
    if holiday_text.strip().casefold() == "none":
        return holidays

    # Validate each holiday date
    for holiday in holiday_text.split(","):
        if not holiday.strip():
            raise ValueError(
                "Invalid holiday date. "
                "Enter holidays as DD-MM-YYYY, separated by commas, "
                "or enter none."
            )

        holidays.add(validate_date(holiday))

    return holidays


# Function to generate the examination timetable
def generate_timetable(subjects, start_date, holidays):
    """Generate a timetable while skipping Sundays and holidays."""
    timetable = []
    exam_date = start_date

    for subject in subjects:

        # Skip Sundays and holidays
        while exam_date.weekday() == 6 or exam_date in holidays:
            exam_date += timedelta(days=1)

        timetable.append((subject, exam_date))

        # Move to the next calendar day
        exam_date += timedelta(days=1)

    return timetable


# Function to display the examination timetable
def display_timetable(timetable):
    """Display the examination timetable."""
    print("\n========== EXAMINATION TIMETABLE ==========")
    print("--------------------------------------------")

    for subject, exam_date in timetable:
        formatted_date = exam_date.strftime("%d-%m-%Y (%A)")
        print(f"{subject} : {formatted_date}")

    print("--------------------------------------------")


# Main function to execute the program
def main():
    print("============================================")
    print("     EXAMINATION TIMETABLE GENERATOR")
    print("============================================")

    try:
        # Accept and validate subjects
        subject_text = input(
            "Enter subjects separated by commas: "
        )
        subjects = validate_subjects(subject_text)

        # Accept and validate the starting date
        start_text = input(
            "Enter start date (DD-MM-YYYY): "
        )
        start_date = validate_date(start_text)

        # Accept holidays or none if there are no holidays
        holiday_text = input(
            "Enter holidays separated by commas (or enter none): "
        )
        holidays = validate_holidays(holiday_text)

        # Generate and display the timetable
        timetable = generate_timetable(
            subjects, start_date, holidays
        )

        display_timetable(timetable)

    except ValueError as error:
        print(f"\nError: {error}")


# Start the program
if __name__ == "__main__":
    main()
