from django.core.paginator import Paginator
from ninja import File, Query, Router
from ninja.errors import HttpError
from ninja.files import UploadedFile
from openpyxl import load_workbook

from infra.schemas import Page, Pagination
from recycle.models import Company, Region, RegionGrade, StationNature, TransferStation
from recycle.schemas.transfer_station import TransferStationOut

router = Router(tags=["可回收物中转站"])


@router.get("", response=Pagination[TransferStationOut])
def list_stations(
    request,
    name: str = Query(None, title="中转站名称"),
    street_code: str = Query(None, title="街道编号"),
    comm_code: str = Query(None, title="社区编号"),
    nature: StationNature = Query(None, title="场所性质"),
    page: Page = Query(...),
):
    """可回收物中转站台账列表"""

    stations = TransferStation.objects.all()
    if name:
        stations = stations.filter(name__contains=name)
    if street_code:
        stations = stations.filter(street_code=street_code)
    if comm_code:
        stations = stations.filter(comm_code=comm_code)
    if nature:
        stations = stations.filter(nature=nature)
    paginator = Paginator(stations, page.page_size)
    p = paginator.page(page.page)
    return {"count": paginator.count, "results": list(p.object_list)}


@router.post("/upload", response={201: dict})
def upload_stations(request, file: UploadedFile = File(...)):
    """上传中转站台账"""

    wb = load_workbook(filename=file)
    sh = wb.worksheets[0]
    stations = list()

    streets = Region.objects.filter(grade=RegionGrade.STREET)
    streets_dict = dict(streets.values_list("name", "code"))
    communities = Region.objects.filter(parent__in=streets.values_list("id"))
    communities_dict = dict(communities.values_list("name", "code"))
    companies = Company.objects.all()
    companies_dict = {}

    for company in companies:
        company_name = company.name
        companies_dict[company_name] = company

    sh_rows = list(sh.rows)
    for row in sh_rows[2:]:
        name = row[1].value
        street_name = row[2].value
        comm_name = row[3].value
        address = row[4].value
        longitude = row[5].value
        latitude = row[6].value
        company_name = row[7].value
        manager_name = row[8].value
        manager_phone = row[9].value
        nature = row[10].value
        varieties = row[11].value

        if street_name in streets_dict.keys():
            street_code = streets_dict[street_name]
        else:
            raise HttpError(408, f"录入错误，请检查街道名称：{street_name}。")

        if comm_name in communities_dict.keys():
            comm_code = communities_dict[comm_name]
        else:
            raise HttpError(408, f"录入错误，请检查社区名称：{comm_name}。")

        if company_name in companies_dict.keys():
            company = companies_dict[company_name]
        else:
            raise HttpError(408, f"录入错误，请检查公司名称：{company_name}。")

        if nature not in ["自有", "租赁", "委托"]:
            raise HttpError(408, f"录入错误，请检查场所性质(仅包括自有、租赁、委托)：{nature}。")

        station = TransferStation(
            name=name,
            street_code=street_code,
            comm_code=comm_code,
            address=address,
            longitude=longitude,
            latitude=latitude,
            company=company,
            manager_name=manager_name,
            manager_phone=manager_phone,
            nature=nature,
            varieties=varieties,
        )
        stations.append(station)
    TransferStation.objects.bulk_create(stations)
    return {"upload_count": len(stations)}
