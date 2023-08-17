from typing import List, Optional, Union
from sqlalchemy import select, join, or_, func
import pandas as pd
from datetime import datetime
from .tables import (
    FundInfo,
    FundStatus,
    FundStrategy,
    CompanyInfo,
    NetValue,
    PersonnelInfo,
    FundPersonnelMapping,
    QRReport,
    QRSummary,
)
from .utils import format_in_clause

class DbClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, engine):
        self.engine = engine

        self.conn = engine.connect().execution_options(stream_results=True)

    @classmethod
    @property
    def instance(cls):
        if cls._instance is not None:
            return cls._instance
        else:
            raise ValueError("Please login first.")

    def get_netvalue(
        self,
        fund_id: Optional[List[str]] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> pd.DataFrame:
        """
        Retrieve net values from the database.

        Args:
            fund_id: The ID(s) of the fund(s) to filter the net values.
                It can be a single string or a list of strings.
            start_date: The start date to filter the net values.
            end_date: The end date to filter the net values.

        Returns:
            A DataFrame containing the net values.
        """
        join_condition = join(NetValue, FundInfo, NetValue.fund_id == FundInfo.fund_id)
        query = select(
            FundInfo.fund_id,
            FundInfo.fund_short_name.label("产品简称"),
            NetValue.price_date.label("净值日期"),
            NetValue.nav.label("单位净值"),
            NetValue.cumulative_nav_withdrawal.label("累计净值"),
            NetValue.cumulative_nav.label("分红复权累计净值"),
        ).select_from(join_condition)

        if fund_id is not None:
            query = format_in_clause(query, NetValue.fund_id, fund_id)
        if start_date is not None:
            query = query.where(NetValue.price_date >= start_date)
        if end_date is not None:
            query = query.where(NetValue.price_date <= end_date)

        return pd.read_sql(query, self.conn, index_col="fund_id")

    def get_fund(
        self,
        names: List[str] = None,
        types: List[int] = None,
        reg_ids: List[str] = None,
        est_start: datetime = None,
        est_end: datetime = None,
        strategies: List[int] = None,
        second_strategies: List[int] = None,
        third_strategies: List[int] = None,
        company_names: List[str] = None,
        company_reg_ids: List[str] = None,
        status: List[int] = None,
        managers: List[str] = None,
    ) -> pd.DataFrame:
        """
        Retrieves fund information based on the specified criteria.

        Args:
            names (List[str], optional): The names of the funds to retrieve. Defaults to None.
            types (List[int], optional): The types of funds to retrieve. Defaults to None.
            reg_ids (List[str], optional): The registration IDs of the funds to retrieve. Defaults to None.
            est_start (datetime, optional): The estimated start date of the funds to retrieve. Defaults to None.
            est_end (datetime, optional): The estimated end date of the funds to retrieve. Defaults to None.
            strategies (List[int], optional): The first strategies of the funds to retrieve. Defaults to None.
            second_strategies (List[int], optional): The second strategies of the funds to retrieve. Defaults to None.
            third_strategies (List[int], optional): The third strategies of the funds to retrieve. Defaults to None.
            company_names (List[str], optional): The names of the companies associated with the funds to retrieve. Defaults to None.
            company_reg_ids (List[str], optional): The registration IDs of the companies associated with the funds to retrieve. Defaults to None.
            status (List[int], optional): The status of the funds to retrieve. Defaults to None.
            managers (List[str], optional): The names of the managers associated with the funds to retrieve. Defaults to None.

        Returns:
            pd.DataFrame: A DataFrame containing the fund information.
        """
        # Create subquery for FundPersonnelMapping and PersonnelInfo tables
        subquery = (
            select(
                FundPersonnelMapping.fund_id,
                func.listagg(PersonnelInfo.personnel_name, ", ").label(
                    "personnel_names"
                ),
            )
            .join(
                PersonnelInfo,
                FundPersonnelMapping.fund_manager_id == PersonnelInfo.personnel_id,
            )
            .group_by(FundPersonnelMapping.fund_id)
        ).subquery()

        # Define the join condition
        join_condition = (
            join(
                FundInfo,
                CompanyInfo,
                FundInfo.trust_id == CompanyInfo.company_id,
                isouter=True,
            )
            .join(FundStatus, FundInfo.fund_id == FundStatus.fund_id, isouter=True)
            .join(FundStrategy, FundInfo.fund_id == FundStrategy.fund_id, isouter=True)
            .join(subquery, FundInfo.fund_id == subquery.c.fund_id, isouter=True)
        )

        # Perform the join table query
        query = select(
            FundInfo.fund_id,
            FundInfo.fund_short_name.label("产品简称"),
            FundInfo.fund_type.label("产品类型"),
            FundInfo.register_number.label("备案编码"),
            FundInfo.inception_date.label("成立日期"),
            FundInfo.trust_id.label("管理人ID"),
            CompanyInfo.company_short_name.label("管理人"),
            FundStatus.fund_status.label("运作状态"),
            FundStrategy.first_strategy.label("一级策略"),
            FundStrategy.second_strategy.label("二级策略"),
            FundStrategy.third_strategy.label("三级策略"),
            subquery.c.personnel_names.label("基金经理"),
        ).select_from(join_condition)

        # Apply filters based on the input arguments
        if names is not None:
            name_conditions = [
                FundInfo.fund_short_name.like(f"%{name}%") for name in names
            ]
            query = query.where(or_(*name_conditions))
        if types is not None:
            query = query.where(FundInfo.fund_type.in_(types))
        if reg_ids is not None:
            query = query.where(FundInfo.register_number.in_(reg_ids))
        if est_start is not None:
            query = query.where(FundInfo.inception_date >= est_start)
        if est_end is not None:
            query = query.where(FundInfo.inception_date <= est_end)
        if strategies is not None:
            query = query.where(FundStrategy.first_strategy.in_(strategies))
        if second_strategies is not None:
            query = query.where(FundStrategy.second_strategy.in_(second_strategies))
        if third_strategies is not None:
            query = query.where(FundStrategy.third_strategy.in_(third_strategies))
        if company_names is not None:
            company_name_conditions = [
                CompanyInfo.company_name.like(f"%{name}%") for name in company_names
            ]
            query = query.where(or_(*company_name_conditions))
        if company_reg_ids is not None:
            query = query.where(CompanyInfo.register_number.in_(company_reg_ids))
        if status is not None:
            query = query.where(FundStatus.fund_status.in_(status))
        if managers is not None:
            query = query.where(PersonnelInfo.manager_name.in_(managers))

        return pd.read_sql(query, self.conn, index_col="fund_id")

    def get_company(
        self,
        company_type: List[int] = None,  # 管理人类型
        company_name: List[str] = None,  # 管理人名称,模糊查询
        company_id: List[str] = None,  # 排排网管理人id批量查询
        register_number: List[str] = None,  # 协会备案id批量查询
        est_start: datetime = None,  # 成立起始时间
        est_end: datetime = None,  # 成立终止时间
        province: str = None,
        city: str = None,
        aum: List[int] = None,
    ):
        query = select(
            CompanyInfo.company_id,
            CompanyInfo.company_short_name.label("公司简称"),
            CompanyInfo.company_type.label("公司类型"),
            CompanyInfo.establish_date.label("成立日期"),
            CompanyInfo.company_asset_size.label("管理规模"),
            CompanyInfo.register_number.label("备案编码"),
            CompanyInfo.province.label("办公省"),
            CompanyInfo.city.label("办公市"),
        )

        # Apply filters based on the input arguments
        if company_type is not None:
            query = query.where(CompanyInfo.company_type.in_(company_type))

        if company_name is not None:
            name_conditions = [
                CompanyInfo.company_short_name.like(f"%{name}%")
                for name in company_name
            ]
            query = query.where(or_(*name_conditions))

        if company_id is not None:
            query = query.where(CompanyInfo.company_id.in_(company_id))

        if register_number is not None:
            query = query.where(CompanyInfo.register_number.in_(register_number))

        if province is not None:
            query = query.where(CompanyInfo.province.like(f"%{province}%"))

        if city is not None:
            query = query.where(CompanyInfo.city.like(f"%{city}%"))

        if est_start is not None:
            query = query.where(CompanyInfo.establish_date > est_start)

        if est_end is not None:
            query = query.where(CompanyInfo.establish_date < est_end)

        if aum is not None:
            query = query.where(CompanyInfo.company_asset_size.in_(aum))

        return pd.read_sql(query, self.conn, index_col="company_id")

    def get_qr_report(
        self,
        company_id: List[str] = None,
    ) -> pd.DataFrame:
        """
        Retrieve QR report from the database.

        Args:
            company_id (List[str], optional): List of company IDs. Defaults to None.

        Returns:
            pd.DataFrame: DataFrame containing the QR report.
        """
        # Join QRReport and QRSummary tables
        join_condition = join(QRReport, QRSummary, QRReport.id == QRSummary.qr_id)

        # Construct the initial query
        query = select(
            QRReport.organization_name.label("公司名称"),
            QRReport.report_date.label("报告日期"),
            QRSummary,
        ).select_from(join_condition)

        # Add where condition if company_id is provided
        if company_id is not None:
            query = format_in_clause(query, QRReport.company_id, company_id)

        # Execute the query and fetch the result
        result = pd.read_sql(query, self.conn)

        def desc_metrics(subdf):
            """
            Process the sub-dataframe to extract metrics.

            Args:
                subdf (pd.DataFrame): Sub-dataframe containing a subset of the result data.

            Returns:
                pd.Series: Series containing the extracted metrics.
            """

            def process_query(subdf, query_arg, level_name):
                """
                Process a query argument to extract the corresponding metric.

                Args:
                    subdf (pd.DataFrame): Sub-dataframe containing a subset of the result data.
                    query_arg (str): Query argument to be processed.
                    level_name (str): Name of the level to filter the data on.

                Returns:
                    Union[str, None]: Extracted metric or None if no data is found.
                """
                rlt = subdf.query(f"{level_name}=='{query_arg}'")

                if rlt.empty:
                    return None
                else:
                    rlt = rlt.node_name_content.squeeze()

                    if isinstance(rlt, pd.Series):
                        rlt = "\n".join(
                            [f"策略{idx+1}:{val}" for idx, val in enumerate(rlt)]
                        )

                    return rlt

            metrics = {}

            querys = {
                "公司概况": "second_root_name",
                "股东情况": "second_root_name",
                "组织架构": "second_root_name",
                "核心人员背景": "second_root_name",
                "其他人员背景": "second_root_name",
                "策略类型": "node_name",
                "大类资产配置": "node_name",
                "配置逻辑": "node_name",
                "持仓特征": "node_name",
                "交易风格": "node_name",
                "容量": "node_name",
                "风控手段": "second_root_name",
                "风控效果": "second_root_name",
                "管理规模": "second_root_name",
                "产品概述": "second_root_name",
                "代表产品": "second_root_name",
                "其他产品": "second_root_name",
                "结论": "root_name",
            }

            for query_arg, level_name in querys.items():
                rlt = process_query(subdf, query_arg, level_name)
                metrics[query_arg] = rlt

            return pd.Series(metrics)

        # Group the result by 公司名称 and 报告日期, and apply desc_metrics function
        return result.groupby(["公司名称", "报告日期"]).apply(desc_metrics)
