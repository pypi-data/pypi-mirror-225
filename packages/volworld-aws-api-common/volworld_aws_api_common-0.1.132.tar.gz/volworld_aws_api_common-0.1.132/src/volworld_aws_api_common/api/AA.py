from typing import Final
from volworld_common.api.CA import CA


# ====== A: Attribute ======
class AA(CA):

    CheckBox: Final[str] = "chkbx"

    Token: Final[str] = "tk"


AAList = [AA, CA]
