# 加载.env的环境变量，连接sqlAlchemy和session

from sqlmodel import create_engine, Session, SQLModel
from config import get_settings
from sqlalchemy import text

# 加载数据库参数
try:
    settings = get_settings()
    DB_SERVER   = settings.db_server
    DB_HOSTNAME = settings.db_hostname
    DB_DATABASE = settings.db_database
    DB_USERNAME = settings.db_username
    DB_PASSWORD = settings.db_password
    DB_PORT     = settings.db_port
    DB_SSLMODE  = settings.db_sslmode
except:
    raise SystemError("Invalid Database Configuration")

# 生成用于连接数据库的 URL 字符串
# 注意：如果使用 pymysql 作为 MySQL 驱动，可将 DB_SERVER 定义为 "mysql+pymysql"
DATABASE_URL = f"{DB_SERVER}+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_DATABASE}"

# 如果启用 SSL，则构造 ssl 参数
ssl_args = {}
if DB_SSLMODE is True:
    ssl_args = {'ssl': {}}

# 输出调试信息，确认配置信息
print(f"ssl_args: {ssl_args}")
print(f"DATABASE_URL: {DATABASE_URL}")

# 创建数据库连接引擎
engine = create_engine(
    DATABASE_URL,
    connect_args=ssl_args,
    pool_recycle=3600,    # 指定连接在 3600 秒后回收
    pool_pre_ping=True    # 每次从连接池获取连接时进行健康检查
)


# 测试连接
try:
    with Session(engine) as session:
        result = session.execute(text("SELECT 1"))
        print("Connection successful, result:", result.scalar())  # 预期结果为 "1"
except Exception as e:
    print("Connection failed:", str(e))

def create_db_and_tables():
    # pass
    """根据所有 SQLModel 模型创建数据库表"""
    try:
        SQLModel.metadata.create_all(engine)
    except:
        pass
    
def get_session():
    """数据库会话生成器，用于依赖注入或按需使用会话"""
    with Session(engine) as session:
        yield session
