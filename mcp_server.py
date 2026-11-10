import os
import sys
import json
from pathlib import Path
from asgiref.sync import sync_to_async

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hms.settings")

import django

django.setup()

from mcp.server.fastmcp import FastMCP
from home.models import booking, dbt, doctor

mcp = FastMCP("Hospital Management Server")


@sync_to_async
def get_departments():
    return list(
        dbt.objects.order_by("department_name").values(
            "id",
            "department_name",
            "dbt_dsc",
        )
    )


@sync_to_async
def get_doctors():
    return [
        {
            "id": item.pk,
            "doctor_name": item.doctor_name,
            "specialization": item.specialization,
            "description": item.doctor_dsc,
            "department": item.department_name.department_name,
        }
        for item in doctor.objects.select_related("department_name")
        .order_by("doctor_name")[:50]
    ]


@sync_to_async
def get_appointment_count():
    return booking.objects.count()


@mcp.tool()
async def list_departments() -> str:
    """List hospital departments and their descriptions."""
    departments = await get_departments()
    return json.dumps(departments)


@mcp.tool()
async def list_doctors() -> str:
    """List up to 50 doctors with their specialty and department."""
    doctors = await get_doctors()
    return json.dumps(doctors)


@mcp.tool()
async def count_appointments() -> str:
    """Count appointment records without exposing patient details."""
    total = await get_appointment_count()
    return json.dumps({"total_appointments": total})


if __name__ == "__main__":
    mcp.run(transport="stdio")