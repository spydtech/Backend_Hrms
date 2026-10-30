from fastapi import APIRouter

from app.api.deps import CurrentUser, DbSession
from app.exceptions import ForbiddenError
from app.models.bank_account import BankAccount
from app.models.user import User, UserRole
from app.schemas.bank_account import BankAccountRead, BankAccountUpsert
from sqlalchemy import select

router = APIRouter(prefix="/bank-account", tags=["bank-account"])

HR_ROLES = (UserRole.super_admin, UserRole.hr_admin, UserRole.admin)


def _is_hr(user) -> bool:
    return user.role in HR_ROLES


def _to_read(record: BankAccount | None, user: User) -> dict:
    if not record:
        return {
            "id": None,
            "employeeId": user.employee_id,
            "employeeName": user.name,
            "accountHolderName": user.name,
            "bankName": None,
            "accountNumber": None,
            "branchName": None,
            "city": None,
            "ifscCode": None,
            "isConfigured": False,
            "updatedAt": None,
        }
    return {
        "id": record.id,
        "employeeId": user.employee_id,
        "employeeName": user.name,
        "accountHolderName": record.account_holder_name,
        "bankName": record.bank_name,
        "accountNumber": record.account_number,
        "branchName": record.branch_name,
        "city": record.city,
        "ifscCode": record.ifsc_code,
        "isConfigured": True,
        "updatedAt": record.updated_at,
    }


@router.get("", response_model=BankAccountRead)
async def get_my_bank_account(session: DbSession, current_user: CurrentUser):
    result = await session.execute(
        select(BankAccount).where(BankAccount.user_id == current_user.id)
    )
    record = result.scalar_one_or_none()
    return _to_read(record, current_user)


@router.put("", response_model=BankAccountRead)
async def upsert_my_bank_account(
    payload: BankAccountUpsert,
    session: DbSession,
    current_user: CurrentUser,
):
    result = await session.execute(
        select(BankAccount).where(BankAccount.user_id == current_user.id)
    )
    record = result.scalar_one_or_none()

    account_holder = (
        (payload.account_holder_name or "").strip() or current_user.name
    )

    if not record:
        record = BankAccount(
            user_id=current_user.id,
            account_holder_name=account_holder,
            bank_name=payload.bank_name.strip(),
            account_number=payload.account_number.strip(),
            branch_name=payload.branch_name.strip(),
            city=payload.city.strip(),
            ifsc_code=payload.ifsc_code.strip().upper(),
        )
        session.add(record)
    else:
        record.account_holder_name = account_holder
        record.bank_name = payload.bank_name.strip()
        record.account_number = payload.account_number.strip()
        record.branch_name = payload.branch_name.strip()
        record.city = payload.city.strip()
        record.ifsc_code = payload.ifsc_code.strip().upper()

    await session.commit()
    await session.refresh(record)
    return _to_read(record, current_user)


@router.get("/all", response_model=list[BankAccountRead])
async def list_all_bank_accounts(session: DbSession, current_user: CurrentUser):
    """HR only — returns every employee's configured bank account."""
    if not _is_hr(current_user):
        raise ForbiddenError("Only HR can view all bank accounts")

    result = await session.execute(
        select(BankAccount, User)
        .join(User, User.id == BankAccount.user_id)
        .order_by(User.name)
    )
    out = []
    for record, user in result.all():
        out.append(_to_read(record, user))
    return out