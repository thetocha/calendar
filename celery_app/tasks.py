from fastapi import APIRouter, Depends, HTTPException, Query
from celery_app.celery_worker import send_email_report
from uuid import UUID
from app.users.schemas import GetUser
from app.auth.token_handler import get_current_user_details, verify_is_not_default_user
from app.group.crud import GroupCrud


tasks_router = APIRouter(tags=["Celery tasks"])


def verify_groups(groups: list[UUID]):
    group_crud = GroupCrud(None)
    for group_id in groups:
        if not group_crud.get_group_by_id(group_id):
            raise HTTPException(status_code=404, detail=f"No such group {group_id}")


@tasks_router.get("/get_personal_report")
def get_personal_report(user: GetUser = Depends(get_current_user_details)):
    send_email_report.delay("personal", user.username, user.id, user.email)
    return {
        "data": "Message sent",
        "to": user.email,
    }


@tasks_router.get("/get_common_report", dependencies=[Depends(verify_is_not_default_user)])
def get_common_report(groups: list[UUID] = Query(None), user: GetUser = Depends(get_current_user_details)):
    verify_groups(groups)
    send_email_report.delay("common", user.username, user.id, user.email, groups)
    if not groups:
        raise HTTPException(status_code=403, detail="No groups selected")
    return {
        "data": "Message sent",
        "to": user.email,
    }
