from dotenv import load_dotenv
from environs import Env

env = Env()
load_dotenv()


class Config:
    CISCO_XLS_URL = env.str(
        "WLCL_CISCO_XLS_URL",
        "https://www.cisco.com/c/dam/assets/prod/wireless/wireless-compliance-tool/ComplianceStatus.xls"
    )
    SQLITE_URI = env.str("WLCL_SQLITE_URI", "wlcl.db")
    REFRESH_DAYS = env.int("WLCL_REFRESH_DAYS", 5)


__all__ = ["Config"]
