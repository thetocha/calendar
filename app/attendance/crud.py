from app.attendance.schemas import CreateAttendance, GetAttendance
from app.users.models import Attendance
from uuid import UUID


class AttendanceCrud:
    def __init__(self, session):
        self.session = session

    def create_attendance(self, attendance: CreateAttendance):
        db_attendance = Attendance(**attendance.dict())
        self.session.add(db_attendance)
        self.session.commit()
        return attendance

    def get_attendance(self, attendance: CreateAttendance):
        return self.session.query(Attendance).filter(Attendance.user == attendance.user,
                                                     Attendance.event == attendance.event).first()

    def get_attendance_by_id(self, attendance_id: UUID):
        return self.session.query(Attendance).filter(Attendance.id == attendance_id).first()

    def update_attendance(self, attendance: CreateAttendance, attendance_id: UUID):
        update_query = self.session.query(Attendance).filter(Attendance.id == attendance_id)
        db_attendance = update_query.first()
        if not db_attendance:
            return None
        new_data = {
            "id": attendance_id,
            "event": attendance.event,
            "user": attendance.user,
            "promised": attendance.promised,
            "attended": attendance.attended
        }
        update_query.update(new_data)
        self.session.commit()
        return new_data

    def delete_attendance(self, attendance: GetAttendance):
        attendance_to_delete = self.get_attendance_by_id(attendance.id)
        self.session.delete(attendance_to_delete)
        self.session.commit()
        return attendance_to_delete

    def get_user_attendance(self, user_id: UUID):
        return self.session.query(Attendance).filter(Attendance.user == user_id).all()

    def get_event_attendance(self, event_id: UUID):
        return self.session.query(Attendance).filter(Attendance.event == event_id).all()

    def update_promised(self, attendance_id: UUID, new_promised: bool):
        update_query = self.session.query(Attendance).filter(Attendance.id == attendance_id)
        attendance = update_query.first()
        if not attendance:
            return None
        new_data = {
            "id": attendance_id,
            "event": attendance.event,
            "user": attendance.user,
            "promised": new_promised,
            "attended": attendance.attended
        }
        update_query.update(new_data)
        self.session.commit()
        return new_data
