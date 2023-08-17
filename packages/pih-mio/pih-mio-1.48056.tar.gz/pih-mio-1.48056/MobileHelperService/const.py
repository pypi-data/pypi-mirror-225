import importlib.util
import sys

pih_is_exists = importlib.util.find_spec("pih") is not None
if not pih_is_exists:
    sys.path.append("//pih/facade")
from pih.rpc_collection import ServiceDescription
from shared.host_collection import HOSTS

NAME: str = "MobileHelper"

HOST = HOSTS.WS255

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="Mobile helper service",
    host=HOST.NAME,
    commands=["send_mobile_helper_message"]
)