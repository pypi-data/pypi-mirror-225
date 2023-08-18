import json
import os
from dotenv import load_dotenv

load_dotenv()

def connection_parameters():
    connection_parameters = {
        "account"   : "qh77171.east-us-2.azure",
        "user"      : "DIEGONERI",
        "password"  : "Omega@2022",
        "role"      : "SYSADMIN",
        "warehouse" : "COMPUTE_WH",
        "database"  : "DASH_DB",
        "schema"    : "DASH_SCHEMA"
    }

    return connection_parameters