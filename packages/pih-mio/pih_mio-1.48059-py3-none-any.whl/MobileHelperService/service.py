import sys
import importlib.util

pih_is_exists = importlib.util.find_spec("pih") is not None
if not pih_is_exists:
    sys.path.append("//pih/facade")
from pih import A

from MobileHelperService.service_api import MobileHelperService 

def checker(telephone_number: str) -> bool:
    if not A.D_C.empty(A.SRV.get_support_host_list(A.CT_SR.MOBILE_HELPER)):
        am_i_tester: bool = A.D.is_not_none(A.CT.TEST.USER) and telephone_number in [
            A.D_TN.by_login(A.CT.TEST.USER), A.D.get(A.CT_ME_WH.GROUP.IT)]
        if MobileHelperService.is_developer():
            return am_i_tester
        return not am_i_tester
    return True

MobileHelperService(None, checker).start()