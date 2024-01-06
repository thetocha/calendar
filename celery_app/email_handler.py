import pandas as pd
import mimetypes
import os

from uuid import UUID
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

from app.attendance.crud import AttendanceCrud
from app.event.crud import EventCrud
from app.group.crud import GroupCrud
from app.users.crud import UserCrud
from config import email_settings


def get_user_events_info(user_id: UUID):
    attendance_crud = AttendanceCrud(None)
    event_crud = EventCrud(None)
    group_crud = GroupCrud(None)
    group = group_crud.get_user_group_by_id(user_id)
    all_attendance = attendance_crud.get_user_attendance(user_id=user_id)
    month, year = datetime.now().month - 1, datetime.now().year
    if month == 0:
        month = 12
        year -= 1

    last_month_group_events = event_crud.get_all_group_events_for_month(group_id=group, month=month, year=year)
    if not last_month_group_events:
        return None
    last_month_events = [last_month_event.id for last_month_event in last_month_group_events]

    all_attendance = [attendance for attendance in all_attendance if attendance.event in last_month_events]

    if not all_attendance:
        return None

    all_events = []
    skipped_events = []
    promised_events = []
    important_skips = []

    for attendance in all_attendance:
        event = event_crud.get_event_by_id(attendance.event)
        all_events.append([event.name, event.professor, event.time])
        if attendance.promised:
            promised_events.append([event.name, event.professor, event.time])
        if not attendance.attended:
            skipped_events.append([event.name, event.professor, event.time])
        if attendance.important_skip:
            important_skips.append([event.name, event.professor, event.time])

    return all_events, skipped_events, promised_events, important_skips


def create_personal_report(user_id: UUID):
    events = get_user_events_info(user_id)
    if not events:
        with open("report.txt", "a") as f:
            f.write("No data for that period")
        return False

    all_events, skipped_events, promised_events, important_skips = events

    data = [
        {"type": "All", "number": len(all_events), "events": all_events},
        {"type": "Skipped", "number": len(skipped_events), "events": skipped_events},
        {"type": "Promised", "number": len(promised_events), "events": promised_events},
        {"type": "Important", "number": len(important_skips), "events": important_skips}
    ]

    df = pd.DataFrame(data)
    df.to_csv("report.csv", index=False)
    return True


def create_group_report(group_id: UUID, group_course: str, group_number: int):
    group_crud = GroupCrud(None)
    user_crud = UserCrud(None)
    students = group_crud.get_all_group_user(group_id)
    data = []
    for student in students:
        events = get_user_events_info(student.user_id)
        user = user_crud.get_user(student.user_id)
        if not events:
            data.append(
                {"first_name": user.first_name, "last_name": user.last_name,
                 "All": pd.NA, "Skipped": pd.NA, "Promised": pd.NA}
            )
            continue
        all_events, skipped_events, promised_events, important_skips = events
        data.append(
            {"first_name": user.first_name, "last_name": user.last_name,
             "All": len(all_events), "Skipped": len(skipped_events), "Promised": len(promised_events),
             "Important": len(important_skips)}
        )
    df = pd.DataFrame(data)
    df.to_csv(f"report {group_course} course, {group_number} number.csv", index=False)


def create_truants_list():
    user_crud = UserCrud(None)
    users = user_crud.get_users()
    group_crud = GroupCrud(None)
    filename = "truants.txt"
    for user in users:
        user_events = get_user_events_info(user.id)
        group_id = group_crud.get_user_group_by_id(user.id)
        group = group_crud.get_group_by_id(group_id)
        if not group:
            continue
        if not user_events:
            with open(filename, "a") as writer:
                writer.write(
                    f"""Student: {user.first_name} {user.last_name},
                        course: {group.course.value}, number: {group.number} - no data for last month \n""")
        else:
            all_events, skipped_events, promised_events, important_skips = user_events
            if (len(skipped_events) - len(important_skips)) > 5:
                with open(filename, "a") as writer:
                    writer.write(
                        f"""Student: {user.first_name} {user.last_name}, 
                            course: {group.course.value}, number:{group.number} \n""")


class MessageHandler:
    def __init__(self, report_type: str, groups: list):
        self.report_type = report_type
        self.groups = groups

    def get_text(self, username: str):
        personal_text = f"""\
                        Hi,{username},
                        Check your attendance report"""
        common_text = f"""\
                        Hello,{username},
                        Check attendance report"""
        truant_text = f"""\
                        Hello,{username},
                        There's list of truants for last month"""
        if self.report_type == "personal":
            return personal_text
        elif self.report_type == "common":
            return common_text
        else:
            return truant_text

    def get_html(self, username: str):
        personal_html = f"""\
                        <html>
                          <body>
                            <p>Hi,{username}<br>
                               Check your report<br>
                               <image src="https://zviazda.by/sites/default/files/field/image/653943.jpg">
                            </p>
                          </body>
                        </html>
                        """
        common_html = f"""\
                        <html>
                          <body>
                            <p>Hello,{username}<br>
                               Here is monthly report<br>
                               <image src="https://zviazda.by/sites/default/files/field/image/653943.jpg">
                            </p>
                          </body>
                        </html>
                        """
        truant_html = f"""\
                        <html>
                          <body>
                            <p>Hello,{username}<br>
                               There's list of truants for last month<br>
                               <image src="https://zviazda.by/sites/default/files/field/image/653943.jpg">
                            </p>
                          </body>
                        </html>
                        """
        if self.report_type == "personal":
            return personal_html
        elif self.report_type == "common":
            return common_html
        else:
            return truant_html

    def get_subject(self):
        personal_subject = "Personal attendance report"
        common_subject = "Monthly attendance report"
        truant_subject = "Truant list last month"
        if self.report_type == "personal":
            return personal_subject
        elif self.report_type == "common":
            return common_subject
        else:
            return truant_subject

    def get_files(self, user_id: UUID, groups: list):
        files = []
        if self.report_type == "personal":
            if create_personal_report(user_id):
                filename = "report.csv"
            else:
                filename = "report.txt"
            files.append(filename)
        elif self.report_type == "common":
            for group_id in groups:
                group_crud = GroupCrud(None)
                group = group_crud.get_group_by_id(group_id)
                create_group_report(group_id, group.course.value, group.number)
                files.append(f"report {group.course.value} course, {group.number} number.csv")
        else:
            create_truants_list()
            files.append("truants.txt")
        return files

    def get_email_template(self, username: str, user_id: UUID, user_email: str):
        if not username:
            username = email_settings.admin_name
        if not user_email:
            user_email = email_settings.admin_address
        message = MIMEMultipart("alternative")
        message['Subject'] = self.get_subject()
        message['From'] = email_settings.email_address
        message['To'] = user_email

        text = self.get_text(username)
        html = self.get_html(username)

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        message.attach(part1)
        message.attach(part2)

        for filename in self.get_files(user_id, self.groups):
            ctype, encoding = mimetypes.guess_type(filename)
            if ctype is None or encoding is not None:
                ctype = "application/octet-stream"

            maintype, subtype = ctype.split("/", 1)

            if maintype == "text":
                fp = open(filename)
                attachment = MIMEText(fp.read(), _subtype=subtype)
                fp.close()
            else:
                fp = open(filename, "rb")
                attachment = MIMEBase(maintype, subtype)
                attachment.set_payload(fp.read())
                fp.close()
                encoders.encode_base64(attachment)
            attachment.add_header("Content-Disposition", "attachment", filename=filename)
            message.attach(attachment)
            os.remove(filename)

        return message
