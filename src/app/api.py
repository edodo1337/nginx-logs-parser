from django.http import HttpRequest
from ninja import Query, Router
from ninja.pagination import paginate

from app.models import NginxLog
from app.schemas import NginxLogFilters, NginxLogResponseItem

logs_router = Router()


@logs_router.get("/", response=list[NginxLogResponseItem])
@paginate
def list_logs(request: HttpRequest, filters: NginxLogFilters = Query(...)):
    all_objs = NginxLog.objects.all()
    return filters.filter(all_objs)
