from pydantic import BaseModel

from .id_ID import id_ID
from .pt_br import pt_br
from .vi_VN import vi_VN
from .zh_CN import zh_CN
from .cs import cs
from .en import en
from .zh_TW import zh_TW
from .ja import ja
from .de import de
from .fr import fr
from .it import it
from .ko import ko
from .es_ES import es_ES
from .sv import sv
from .ru import ru
from .nl import nl
from .pl import pl
from .tr import tr
from .th import th


class Language(BaseModel):
    localLanguage: str
    commitFix: str
    commitFeat: str
    commitDescription: str

cs = Language(**cs)
en = Language(**en)
zh_CN = Language(**zh_CN)
zh_TW = Language(**zh_TW)
ja = Language(**ja)
de = Language(**de)
fr = Language(**fr)
it = Language(**it)
ko = Language(**ko)
pt_br = Language(**pt_br)
vi_VN = Language(**vi_VN)
es_ES = Language(**es_ES)
sv = Language(**sv)
ru = Language(**ru)
id_ID = Language(**id_ID)
nl = Language(**nl)
pl = Language(**pl)
tr = Language(**tr)
th = Language(**th)

class I18nLocals:
    EN = 'en'
    ZH_CN = 'zh_CN'
    ZH_TW = 'zh_TW'
    JA = 'ja'
    CS = 'cs'
    DE = 'de'
    FR = 'fr'
    IT = 'it'
    KO = 'ko'
    PT_BR = 'pt_br'
    VI_VN = 'vi_VN'
    ES_ES = 'es_ES'
    SV = 'sv'
    RU = 'ru'
    ID_ID = 'id_ID'
    PL = 'pl'
    TR = 'tr'
    TH = 'th'

i18n = {
    'en': en,
    'zh_CN': zh_CN,
    'zh_TW': zh_TW,
    'ja': ja,
    'cs': cs,
    'de': de,
    'fr': fr,
    'it': it,
    'ko': ko,
    'pt_br': pt_br,
    'vi_VN': vi_VN,
    'es_ES': es_ES,
    'sv': sv,
    'ru': ru,
    'id_ID': id_ID,
    'nl': nl,
    'pl': pl,
    'tr': tr,
    'th': th
}

I18N_CONFIG_ALIAS = {
    'zh_CN': ['zh_CN', '简体中文', '中文', '简体'],
    'zh_TW': ['zh_TW', '繁體中文', '繁體'],
    'ja': ['ja', 'Japanese', 'にほんご'],
    'ko': ['ko', 'Korean', '한국어'],
    'cs': ['cs', 'Czech', 'česky'],
    'de': ['de', 'German', 'Deutsch'],
    'fr': ['fr', 'French', 'française'],
    'it': ['it', 'Italian', 'italiano'],
    'nl': ['nl', 'Dutch', 'Nederlands'],
    'pt_br': ['pt_br', 'Portuguese', 'português'],
    'vi_VN': ['vi_VN', 'Vietnamese', 'tiếng Việt'],
    'en': ['en', 'English', 'english'],
    'es_ES': ['es_ES', 'Spanish', 'español'],
    'sv': ['sv', 'Swedish', 'Svenska'],
    'ru': ['ru', 'Russian', 'русский'],
    'id_ID': ['id_ID', 'Bahasa', 'bahasa'],
    'pl': ['pl', 'Polish', 'Polski'],
    'tr': ['tr', 'Turkish', 'Turkish'],
    'th': ['th', 'Thai', 'ไทย']
}

def get_i18n_local(value: str) -> str | bool:
    for key, aliases in I18N_CONFIG_ALIAS.items():
        if value in aliases:
            return key
    return False
