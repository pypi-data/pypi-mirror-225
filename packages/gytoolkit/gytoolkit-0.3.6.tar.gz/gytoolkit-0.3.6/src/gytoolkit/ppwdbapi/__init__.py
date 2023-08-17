from .api import *
from sqlalchemy import create_engine
from .tables import Reflected, create_table


def login(
    username: str,
    password: str,
    addr: str = "127.0.0.1",
    port: str = "1521",
    dbname: str = "orclpdb",
) -> None:
    """
    使用给定的用户名和密码登录到指定的数据库。

    参数:
        username (str): 用户名。
        password (str): 密码。
        addr (str, optional): 数据库服务器的 IP 地址，默认为 "127.0.0.1"。
        port (str, optional): 数据库服务器的端口号，默认为 "1521"。
        dbname (str, optional): 数据库名称，默认为 "orclpdb"。

    返回:
        None

    异常:
        None
    """
    if not DbClient._instance:
        try:
            engine = create_engine(
                f"oracle+cx_oracle://{username}:{password}@{addr}:{port}/?service_name={dbname}"
            )
            DbClient(engine)
            Reflected.prepare(bind=engine)
            print("Logged in successfully.")
        except Exception as e:
            print(f"Login failed. Error: {e}")
    else:
        print("Already logged in.")
    return DbClient.instance.conn


class TableWrapper:
    subclasses = Reflected.__subclasses__()
    # 创建一个字典，将类名与类本身进行关联
    tables = {subclass.__name__: subclass for subclass in subclasses}

    def __init__(self):
        for subclass in self.subclasses:
            setattr(self, subclass.__name__, subclass)

    def set_schema(self, tablename, schema):
        if hasattr(self, tablename):
            getattr(self, tablename).__table_args__ = {"schema": schema}
            if DbClient._instance:
                getattr(self, tablename).prepare(bind=DbClient.instance.engine)
        else:
            raise AttributeError(f"No table named '{tablename}'")

    def register_table(self, clsname, tablename, schema=None):
        table = create_table(clsname, tablename, schema)
        if DbClient._instance:
            Reflected.prepare(bind=DbClient.instance.engine)
        setattr(self, clsname, table)
        self.tables[clsname] = table  # 更新已注册的表类列表
        return table

    def list_tables(self):
        return list(self.tables.keys())


# 创建一个TableWrapper实例
table = TableWrapper()
