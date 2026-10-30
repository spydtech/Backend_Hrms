from datetime import datetime

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class BankAccountUpsert(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    account_holder_name: str | None = Field(
        default=None, validation_alias=AliasChoices("accountHolderName", "account_holder_name")
    )
    bank_name: str = Field(
        validation_alias=AliasChoices("bankName", "bank_name")
    )
    account_number: str = Field(
        validation_alias=AliasChoices("accountNumber", "account_number")
    )
    branch_name: str = Field(
        validation_alias=AliasChoices("branchName", "branch_name")
    )
    city: str
    ifsc_code: str = Field(
        validation_alias=AliasChoices("ifscCode", "ifsc_code")
    )


class BankAccountRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int | None = None
    employeeId: str | None = Field(default=None, validation_alias="employee_id")
    employeeName: str | None = Field(default=None, validation_alias="employee_name")
    accountHolderName: str | None = Field(default=None, validation_alias="account_holder_name")
    bankName: str | None = Field(default=None, validation_alias="bank_name")
    accountNumber: str | None = Field(default=None, validation_alias="account_number")
    branchName: str | None = Field(default=None, validation_alias="branch_name")
    city: str | None = None
    ifscCode: str | None = Field(default=None, validation_alias="ifsc_code")
    isConfigured: bool = False
    updatedAt: datetime | None = Field(default=None, validation_alias="updated_at")