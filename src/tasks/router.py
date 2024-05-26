from fastapi import APIRouter, Depends, BackgroundTasks
from auth.base_config import current_user

from tasks.tasks import send_email_report_dashboard


router = APIRouter(prefix="/report")


@router.get("/dashboard")
def get_dashboard_report():
    send_email_report_dashboard.delay('pavelkovvv')
    return {
        "status": 200,
        "data": "Письмо отправлено",
        "details": None
    }
