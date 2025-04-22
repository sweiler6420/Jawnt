import sqlalchemy as sa
from .database import Base  # or just use Base if same file

class Organization(Base):
    __tablename__ = "organization"

    id = sa.Column(sa.Integer, primary_key=True)
    uid = sa.Column(sa.String(255), unique=True, nullable=False)
    name = sa.Column(sa.String(255), nullable=False)


class OrganizationAdministrator(Base):
    __tablename__ = "organization_administrator"

    id = sa.Column(sa.Integer, primary_key=True)
    organization_id = sa.Column(sa.Integer, sa.ForeignKey("organization.id"), nullable=False)
    employee_id = sa.Column(sa.Integer, sa.ForeignKey("organization_employee.id"), nullable=False)


class OrganizationEmployee(Base):
    __tablename__ = "organization_employee"

    id = sa.Column(sa.Integer, primary_key=True)
    organization_id = sa.Column(sa.Integer, sa.ForeignKey("organization.id"), nullable=False)
    first_name = sa.Column(sa.String(255), nullable=False)
    last_name = sa.Column(sa.String(255), nullable=False)
    email = sa.Column(sa.String(255), nullable=False)


class OrganizationEmployeeAccount(Base):
    __tablename__ = "organization_employee_account"

    id = sa.Column(sa.Integer, primary_key=True)
    organization_id = sa.Column(sa.Integer, sa.ForeignKey("organization.id"), nullable=False)
    account_id = sa.Column(sa.Integer, nullable=False)
    balance_cents = sa.Column(sa.Integer, nullable=False)


class OrganizationEmployeeAccountDebitCard(Base):
    __tablename__ = "organization_employee_account_debit_card"

    id = sa.Column(sa.Integer, primary_key=True)
    organization_id = sa.Column(sa.Integer, sa.ForeignKey("organization.id"), nullable=False)
    debit_card_id = sa.Column(sa.Integer, nullable=False)


class OrganizationEmployeeAccountPayment(Base):
    __tablename__ = "organization_employee_account_payment"

    id = sa.Column(sa.Integer, primary_key=True)
    type = sa.Column(sa.String(255), nullable=False)
    external_account_id = sa.Column(sa.Integer, nullable=False)
    internal_account_id = sa.Column(sa.Integer, sa.ForeignKey("organization_employee_account.id"), nullable=False)
    external_payment_id = sa.Column(sa.Integer, nullable=False)
    amount_cents = sa.Column(sa.Integer, nullable=False)


class OrganizationEmployeeAccountDebitCardTransaction(Base):
    __tablename__ = "organization_employee_account_debit_card_transaction"

    id = sa.Column(sa.Integer, primary_key=True)
    debit_card_id = sa.Column(sa.Integer, sa.ForeignKey("organization_employee_account_debit_card.id"), nullable=False)
    external_payment_id = sa.Column(sa.Integer, nullable=False)
    merchant_name = sa.Column(sa.String(255), nullable=False)
    amount_cents = sa.Column(sa.Integer, nullable=False)