from typing import List, Optional, Union
import pandas as pd
from datetime import datetime
from .client import DbClient
from .constants import (
    AUM_MAPPER,
    COMPANYTYPE_PPW_MAP,
    PPW_AUM_MAP,
    PPW_COMPANYTYPE_MAP,
    PPW_FUNDTYPE_MAP,
    PPW_SECOND_STRATEGY_MAP,
    PPW_STATUS_MAP,
    PPW_STRATEGY_MAP,
    PPW_THIRD_STRATEGY_MAP,
    STRATEGY_PPW_MAP,
    SECOND_STRATEGY_PPW_MAP,
    THIRD_STRATEGY_PPW_MAP,
    STATUS_PPW_MAP,
    FUNDTYPE_PPW_MAP,
)


def get_netvalue(
    fund_id: Optional[Union[str, List[str]]] = None,
    start_date: Optional[Union[datetime, str]] = None,
    end_date: Optional[Union[datetime, str]] = None,
) -> pd.DataFrame:
    """
    获取给定日期范围内基金的净值。

    参数:
        fund_id (Optional[Union[str, List[str]]]): 基金的ID（可选）。默认为None。
        start_date (Optional[Union[datetime, str]]): 日期范围的开始日期（可选）。默认为None。
        end_date (Optional[Union[datetime, str]]): 日期范围的结束日期（可选）。默认为None。

    返回:
        pd.DataFrame: 给定日期范围内基金的净值。
    """
    # convert types of input arguments
    if isinstance(fund_id, str):
        fund_id = [fund_id]
    if isinstance(start_date, str):
        start_date = pd.to_datetime(start_date)
    if isinstance(end_date, str):
        end_date = pd.to_datetime(end_date)

    # get net value from the database
    net_value = DbClient.instance.get_netvalue(fund_id, start_date, end_date)
    return net_value


def get_fund(
    names: Union[str, List[str]] = None,
    types: Union[str, List[str]] = "私募证券",
    reg_ids: Union[str, List[str]] = None,
    est_start: Union[str, pd.Timestamp] = None,
    est_end: Union[str, pd.Timestamp] = None,
    strategies: Union[str, List[str]] = None,
    second_strategies: Union[str, List[str]] = None,
    third_strategies: Union[str, List[str]] = None,
    company_names: Union[str, List[str]] = None,
    company_reg_ids: Union[str, List[str]] = None,
    status: Union[str, List[str]] = None,
    managers: Union[str, List[str]] = None,
) -> pd.DataFrame:
    """
    根据提供的参数从数据库中检索基金数据。

    参数:
        names (Union[str, List[str]], 可选): 要模糊检索的基金名称。默认为None。
        types (Union[str, List[str]], 可选): 要检索的基金类型。默认为"私募证券"。
        reg_ids (Union[str, List[str]], 可选): 要检索的基金协会备案ID。默认为None。
        est_start (Union[str, pd.Timestamp], 可选): 要检索的基金最早成立日期。默认为None。
        est_end (Union[str, pd.Timestamp], 可选): 要检索的基金最迟成立日期。默认为None。
        strategies (Union[str, List[str]], 可选): 要检索的基金投资策略。默认为None。
        second_strategies (Union[str, List[str]], 可选): 要检索的基金次级投资策略。默认为None。
        third_strategies (Union[str, List[str]], 可选): 要检索的基金三级投资策略。默认为None。
        company_names (Union[str, List[str]], 可选): 要模糊检索的与基金关联的管理人名称。默认为None。
        company_reg_ids (Union[str, List[str]], 可选): 要检索的与基金关联的公司登记ID。默认为None。
        status (Union[str, List[str]], 可选): 要检索的基金运作状态。默认为None。
        managers (Union[str, List[str]], 可选): 要检索的基金经理。默认为None。

    返回:
        pd.DataFrame: 包含检索到的基金数据的DataFrame。

    """
    # Convert names parameter to list
    if isinstance(names, str):
        names = [names]

    # Convert types parameter using TYPES_PPW_MAP
    if types:
        if isinstance(types, str):
            types = [types]
        types = [FUNDTYPE_PPW_MAP.get(t) for t in types]

    # convert reg_ids parameter to list
    if isinstance(reg_ids, str):
        reg_ids = [reg_ids]

    # Convert est_start parameter to datetime
    if isinstance(est_start, str):
        est_start = pd.to_datetime(est_start)

    # convert est_end parameter to datetime
    if isinstance(est_end, str):
        est_end = pd.to_datetime(est_end)

    # Convert strategies parameter using STRATEGY_PPW_MAP
    if strategies:
        if isinstance(strategies, str):
            strategies = [strategies]
        strategies = [STRATEGY_PPW_MAP.get(s) for s in strategies]

    # Convert second_strategies parameter using SECOND_STRATEGY_PPW_MAP
    if second_strategies:
        if isinstance(second_strategies, str):
            second_strategies = [second_strategies]
        second_strategies = [SECOND_STRATEGY_PPW_MAP.get(s) for s in second_strategies]

    # Convert third_strategies parameter using THIRD_STRATEGY_PPW_MAP
    if third_strategies:
        if isinstance(third_strategies, str):
            third_strategies = [third_strategies]
        third_strategies = [THIRD_STRATEGY_PPW_MAP.get(s) for s in third_strategies]

    # convert company_names parameter to list
    if isinstance(company_names, str):
        company_names = [company_names]

    # convert company_reg_ids parameter to list
    if isinstance(company_reg_ids, str):
        company_reg_ids = [company_reg_ids]

    # Convert status parameter using STATUS_PPW_MAP
    if status:
        if isinstance(status, str):
            status = [status]
        status = [STATUS_PPW_MAP.get(s) for s in status]

    # convert managers parameter to list
    if isinstance(managers, str):
        managers = [managers]

    # Call DbClient's get_fund method with the converted parameters
    result = DbClient.instance.get_fund(
        names=names,
        types=types,
        reg_ids=reg_ids,
        est_start=est_start,
        est_end=est_end,
        strategies=strategies,
        second_strategies=second_strategies,
        third_strategies=third_strategies,
        company_names=company_names,
        company_reg_ids=company_reg_ids,
        status=status,
        managers=managers,
    )
    # replace values in result with dictionary
    replacement_dict = {
        "运作状态": PPW_STATUS_MAP,
        "一级策略": PPW_STRATEGY_MAP,
        "二级策略": PPW_SECOND_STRATEGY_MAP,
        "三级策略": PPW_THIRD_STRATEGY_MAP,
        "产品类型": PPW_FUNDTYPE_MAP,
    }

    result.replace(replacement_dict, inplace=True)

    return result


def get_company(
    company_type: Union[str, List[str]] = "私募证券投资",  # 管理人类型
    company_name: Union[str, List[str]] = None,  # 管理人名称,模糊查询
    company_id: Union[str, List[str]] = None,  # 排排网管理人id批量查询
    register_number: Union[str, List[str]] = None,  # 协会备案id批量查询
    est_start: Union[str, pd.Timestamp] = None,  # 成立起始时间
    est_end: Union[str, pd.Timestamp] = None,  # 成立终止时间
    province: str = None,
    city: str = None,
    aum_min: [int] = None,
    aum_max: [int] = None,
):
    """
    根据各种过滤条件检索公司信息。

    参数:
        company_type (Union[str, List[str]], 可选): 要检索的公司类型。默认为'私募证券投资'。
        company_name (Union[str, List[str]], 可选): 要模糊检索的公司名称。默认为None。
        company_id (Union[str, List[str]], 可选): 要检索的公司ID。默认为None。
        register_number (Union[str, List[str]], 可选): 要检索的公司登记ID。默认为None。
        est_start (Union[str, pd.Timestamp], 可选): 公司最早成立日期。默认为None。
        est_end (Union[str, pd.Timestamp], 可选): 公司最迟成立日期。默认为None。
        province (str, 可选): 公司办公地所在的省份。默认为None。
        city (str, 可选): 公司办公地所在的城市。默认为None。
        aum_min ([int], 可选): 公司的最小管理资产规模。默认为None。
        aum_max ([int], 可选): 公司的最大管理资产规模。默认为None。

    返回:
        检索到的公司信息。
    """
    # convert types of input arguments
    if company_type:
        if isinstance(company_type, str):
            company_type = [company_type]
        company_type = [COMPANYTYPE_PPW_MAP.get(t) for t in company_type]

    if isinstance(company_name, str):
        company_name = [company_name]

    if isinstance(company_id, str):
        company_id = [company_id]

    if isinstance(register_number, str):
        register_number = [register_number]

    if isinstance(est_start, str):
        est_start = pd.to_datetime(est_start)

    if isinstance(est_end, str):
        est_end = pd.to_datetime(est_end)

    if aum_min is not None:
        if aum_min not in [0, 5, 10, 20, 50, 100]:
            raise ValueError("资管规模下限必须为0,5,10,20,50,100中的一个")
    if aum_max is not None:
        if aum_max not in [5, 10, 20, 50, 100]:
            raise ValueError("资管规模上限必须为5,10,20,50,100中的一个")
    aum_min = AUM_MAPPER.get(aum_min, 1)
    aum_max = AUM_MAPPER.get(aum_max, 7)

    if aum_max <= aum_min:
        raise ValueError("资管规模上限必须大于下限")

    if aum_max == 7 and aum_min == 1:
        aum = None
    else:
        aum = tuple(range(aum_min, aum_max))
    # Call DbClient's get_company method with the converted parameters
    result = DbClient.instance.get_company(
        company_type=company_type,
        company_name=company_name,
        company_id=company_id,
        register_number=register_number,
        est_start=est_start,
        est_end=est_end,
        province=province,
        city=city,
        aum=aum,
    )

    # replace values in result with dictionary
    replacement_dict = {
        "公司类型":PPW_COMPANYTYPE_MAP,
        "管理规模":PPW_AUM_MAP
    }

    result.replace(replacement_dict, inplace=True)

    return result

def get_qr_report(
    company_id: Union[str,List[str]] = None,
) -> pd.DataFrame:
    """
    根据给定的公司ID或公司ID列表检索私募排排网尽调报告。

    参数:
        company_id (Union[str, List[str]], 可选): 要检索尽调报告的公司ID或公司ID列表。默认为None。

    返回:
        pd.DataFrame: 以pandas DataFrame形式返回的尽调报告。

    """
    # convert types of input arguments
    if isinstance(company_id, str):
        company_id = [company_id]
    
    return DbClient.instance.get_qr_report(company_id)
