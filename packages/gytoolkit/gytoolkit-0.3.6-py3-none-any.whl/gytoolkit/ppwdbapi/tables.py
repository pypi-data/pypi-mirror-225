from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.declarative import DeferredReflection

class Base(DeclarativeBase):
    pass

class Reflected(DeferredReflection,Base):
    __abstract__ = True
    __table_args__ = {'schema': "smppw"}

class FundInfo(Reflected):
    __tablename__ = "pvn_fund_info"

class FundStatus(Reflected):
    __tablename__ = "pvn_fund_status"

class FundStrategy(Reflected):
    __tablename__ = "pvn_fund_strategy"

class CompanyInfo(Reflected):
    __tablename__ = "pvn_company_info"

class NetValue(Reflected):
    __tablename__ = "pvn_nav"

class PersonnelInfo(Reflected):
    __tablename__ = "pvn_personnel_info"

class FundPersonnelMapping(Reflected):
    __tablename__ = "pvn_fund_manager_mapping"

class QRReport(Reflected):
    __tablename__ = "pvn_qr_qualitative_report"

class QRSummary(Reflected):
    __tablename__ = "pvn_qr_summary_desc"

def create_table(clsname,tablename,schema=None):
    kwargs = {'__tablename__': tablename}
    if schema:
       kwargs['__table_args__']: {'schema': schema} 
    table = type(clsname, (Reflected,), kwargs)
    return table