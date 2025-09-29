from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.api_response import api_response, ApiResponse
from app.db.session import get_async_session
from app.application.use_cases.request_report import RequestReportUseCase, RequestReportCommand
from app.infrastructure.uow.sqlalchemy_uow import SqlAlchemyUnitOfWork
from app.schemas.report import ReportRequestIn, ReportStatusOut, ReportRequestOut
from app.application.use_cases.get_report_status import GetReportStatusUseCase, GetReportStatusQuery

router = APIRouter()

@router.post("/requests", response_model=ApiResponse[ReportRequestOut], status_code=201)
async def request_report(payload: ReportRequestIn, session: AsyncSession = Depends(get_async_session)):
    use_case = RequestReportUseCase(lambda: SqlAlchemyUnitOfWork(session))
    report = await use_case.execute(RequestReportCommand(requester_email=payload.requester_email, params=payload.params))
    return api_response(data=report)


@router.get("/requests/{report_id}", response_model=ApiResponse[ReportStatusOut])
async def get_report_status(report_id: int, session: AsyncSession = Depends(get_async_session)):
    use_case = GetReportStatusUseCase(lambda: SqlAlchemyUnitOfWork(session))
    dto = await use_case.execute(GetReportStatusQuery(report_id=report_id))
    out = ReportStatusOut(
        id=dto.id,
        job_id=dto.job_id,
        celery_status=dto.celery_status,
        result_path=dto.result_path,
        error_message=dto.error_message,
    )
    return api_response(data=out)


