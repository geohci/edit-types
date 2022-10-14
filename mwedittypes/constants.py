import re
# https://en.wikipedia.org/wiki/Help:Wikitext
# bold, italic, strikethrough, underline
# horizontal rule and line break (hr is not really text formatting but close enough)
# pre and nowiki are for mono-spaced text (I leave out `code` because it generally contains code not text)
# small / big / sub / sup all affect text size
TEXT_FORMATTING_TAGS = ('b', 'i', 's', 'u', 'del', 'ins','hr', 'br','pre', 'nowiki','small',
                         'big', 'sub', 'sup', 'font', 'blockquote', 'span', 'center')
TABLE_ELEMENTS_TAGS = ('th', 'tr', 'td')
LIST_TAGS = ('li', 'dt', 'dd', 'ul', 'ol', 'dl')

# See: https://www.mediawiki.org/wiki/User:TJones_(WMF)/Notes/Spaceless_Writing_Systems_and_Wiki-Projects
NON_WHITESPACE_LANGUAGES = ('bo', 'dz', 'gan', 'ja', 'km', 'lo', 'my', 'th', 'wuu', 'zh', 'zh-classical', 'zh-yue',  # space-less
                            'bug', 'cdo', 'cr', 'hak',  # mixed space/spaceless. could also add: 'jv', 'zh-min-nan'
                            'vi')  # spaces but between syllables and not words

# CJK period/question/exclamation; Bengali full-stops
NON_ENGLISH_FULL_STOPS = '。？！।॥'
# This regex identifies end-of-sentence punctuation and new-lines as sentence breaks
# It avoids matching dots between two digits but takes into account ellipses and fullstops.
# fuller explanation:
# [!?...] - 1 or more !, ?, new-line, or non-english stops
# | - or
# (?<!\.) - next character must not precede a fullstop
# \. - next character
# (?<=\d.) - must be preceded by a digit containing a fullstop
# (?!(?<=\d.)\d) -  next character must not be followed by matching dots between two digits
# (?!\.) - next character must not be followed by fullstop
SENTENCE_BREAKS_REGEX = r'[!?\n{0}]+|(?<!\.)\.(?!(?<=\d.)\d)(?!\.)'.format(NON_ENGLISH_FULL_STOPS)

# TODO non-English quotation marks -- e.g., German
NON_ENGLISH_UNICODE = '''[\u0609\u060a\u060c\u060d\u061b\u061e\u061f\u066a\u066b\u066c
\u070a\u070b\u070c\u070d\u07f7\u07f8\u07f9\u0830\u0831\u0832\u0833\u0834\u0835
\u0836\u0837\u0838\u0839\u083a\u083b\u083c\u083d\u083e\u085e\u0964
\u0965\u0970\u09fd\u0a76\u0af0\u0c77\u0c84\u0df4
\u0e4f\u0e5a\u0e5b\u0f04\u0f05\u0f06\u0f07\u0f08\u0f09\u0f0a\u0f0b
\u0f0c\u0f0d\u0f0e\u0f0f\u0f10\u0f11\u0f12\u0f14\u0f85\u0fd0\u0fd1
\u0fd2\u0fd3\u0fd4\u0fd9\u0fda\u104a\u104b\u104c\u104d\u104e\u104f
\u10fb\u1360\u1361\u1362\u1363\u1364\u1365\u1366\u1367\u1368\u166e
\u16eb\u16ec\u16ed\u1735\u1736\u17d4\u17d5\u17d6\u17d8\u17d9\u17da
\u1800\u1801\u1802\u1803\u1804\u1805\u1807\u1808\u1809\u180a\u1944
\u1945\u1a1e\u1a1f\u1aa0\u1aa1\u1aa2\u1aa3\u1aa4\u1aa5\u1aa6\u1aa8
\u1aa9\u1aaa\u1aab\u1aac\u1aad\u1b5a\u1b5b\u1b5c\u1b5d\u1b5e\u1b5f
\u1b60\u1bfc\u1bfd\u1bfe\u1bff\u1c3b\u1c3c\u1c3d\u1c3e\u1c3f\u1c7e
\u1c7f\u1cc0\u1cc1\u1cc2\u1cc3\u1cc4\u1cc5\u1cc6\u1cc7\u1cd3\u2016
\u2017\u2020\u2021\u2022\u2023\u2025\u2026\u2027\u2030\u2031
\u2032\u2033\u2034\u2035\u2036\u2037\u2038\u203b\u203c\u203d\u203e
\u2041\u2042\u2043\u2047\u2048\u2049\u204a\u204b\u204c\u204d\u204e
\u204f\u2050\u2051\u2053\u2055\u2056\u2057\u2058\u2059\u205a\u205b
\u205c\u205d\u205e\u2cf9\u2cfa\u2cfb\u2cfc\u2cfe\u2cff
\u3000-\u303f\uff0c\uff01\uff1f\uff1b\uff1a\uff08\uff3b\u3010\u09E4\u09E5]'''.replace('\n','')

ENGLISH_UNICODE = '[\u00b7\u00bf]'

# https://commons.wikimedia.org/wiki/Commons:File_types
IMAGE_EXTENSIONS = ['.jpg', '.png', '.svg', '.gif', '.jpeg', '.tif', '.bmp', '.webp', '.xcf']
VIDEO_EXTENSIONS = ['.ogv', '.webm', '.mpg', '.mpeg']
AUDIO_EXTENSIONS = ['.ogg', '.mp3', '.mid', '.webm', '.flac', '.wav', '.oga']
MEDIA_EXTENSIONS = list(set(IMAGE_EXTENSIONS + VIDEO_EXTENSIONS + AUDIO_EXTENSIONS))

# build regex that checks for all media extensions
EXTEN_REGEX = ('(' + '|'.join([e + r'\b' for e in MEDIA_EXTENSIONS]) + ')').replace('.', r'\.')
# join in the extension regex with one that requiries at least one alphanumeric and/or a few special characters before it
EXTEN_PATTERN = re.compile(fr'([\w ,().-]+){EXTEN_REGEX}', flags=re.UNICODE)

MEDIA_PREFIXES = ['File', 'Image', 'Media']
CAT_PREFIXES = ['Category']

# Source: for each Wikipedia language code (example shown for "ab"), aliases for namespaces -2 and 6 accessed via this API call:
# https://ab.wikipedia.org/w/api.php?action=query&meta=siteinfo&siprop=namespacealiases|namespaces&format=json&formatversion=2
# Last accessed: 21 December 2021
MEDIA_ALIASES = {
    "ab": ["Медиа", "Файл", "Афаил", "Амедиа", "Изображение"],
    "ace": ["Beureukaih", "Gambar", "Alat", "Berkas"],
    "ady": ["Медиа"],
    "af": ["Lêer", "Beeld"],
    "als": ["Medium", "Datei", "Bild"],
    "am": ["ፋይል", "ስዕል"],
    "an": ["Imachen", "Imagen"],
    "ang": ["Ymele", "Biliþ"],
    "ar": ["ميديا", "صورة", "وسائط", "ملف"],
    "arc": ["ܠܦܦܐ", "ܡܝܕܝܐ"],
    "arz": ["ميديا", "صورة", "وسائط", "ملف"],
    "as": ["চিত্ৰ", "चित्र", "চিত্র", "মাধ্যম"],
    "ast": ["Imaxen", "Ficheru", "Imaxe", "Archivu", "Imagen", "Medios"],
    "atj": ["Tipatcimoctakewin", "Natisinahikaniwoc"],
    "av": ["Медиа", "Файл", "Изображение"],
    "ay": ["Medio", "Archivo", "Imagen"],
    "az": ["Mediya", "Şəkil", "Fayl"],
    "azb": ["رسانه", "تصویر", "مدیا", "فایل", "رسانه‌ای"],
    "ba": ["Медиа", "Рәсем", "Файл", "Изображение"],
    "bar": ["Medium", "Datei", "Bild"],
    "bat-smg": ["Vaizdas", "Medėjė", "Abruozdielis"],
    "bcl": ["Medio", "Ladawan"],
    "be": ["Мультымедыя", "Файл", "Выява"],
    "be-x-old": ["Мэдыя", "Файл", "Выява"],
    "bg": ["Медия", "Файл", "Картинка"],
    "bh": ["मीडिया", "चित्र"],
    "bjn": ["Barakas", "Gambar", "Berkas"],
    "bm": ["Média", "Fichier"],
    "bn": ["চিত্র", "মিডিয়া"],
    "bpy": ["ছবি", "মিডিয়া"],
    "br": ["Skeudenn", "Restr"],
    "bs": ["Mediji", "Slika", "Datoteka", "Medija"],
    "bug": ["Gambar", "Berkas"],
    "bxr": ["Файл", "Меди", "Изображение"],
    "ca": ["Fitxer", "Imatge"],
    "cbk-zam": ["Medio", "Archivo", "Imagen"],
    "cdo": ["文件", "媒體", "圖像", "檔案"],
    "ce": ["Хlум", "Медиа", "Сурт", "Файл", "Медйа", "Изображение"],
    "ceb": ["Payl", "Medya", "Imahen"],
    "ch": ["Litratu"],
    "ckb": ["میدیا", "پەڕگە"],
    "co": ["Immagine"],
    "crh": ["Медиа", "Resim", "Файл", "Fayl", "Ресим"],
    "cs": ["Soubor", "Média", "Obrázok"],
    "csb": ["Òbrôzk", "Grafika"],
    "cu": ["Видъ", "Ви́дъ", "Дѣло", "Срѣдьства"],
    "cv": ["Медиа", "Ӳкерчĕк", "Изображение"],
    "cy": ["Delwedd"],
    "da": ["Billede", "Fil"],
    "de": ["Medium", "Datei", "Bild"],
    "din": ["Ciɛl", "Apamduööt"],
    "diq": ["Medya", "Dosya"],
    "dsb": ["Wobraz", "Dataja", "Bild", "Medija"],
    "dty": ["चित्र", "मिडिया"],
    "dv": ["ފައިލު", "މީޑިއާ", "ފައިލް"],
    "el": ["Εικόνα", "Αρχείο", "Μέσο", "Μέσον"],
    "eml": ["Immagine"],
    "eo": ["Dosiero", "Aŭdvidaĵo"],
    "es": ["Medio", "Archivo", "Imagen"],
    "et": ["Pilt", "Fail", "Meedia"],
    "eu": ["Irudi", "Fitxategi"],
    "ext": ["Archivu", "Imagen", "Mediu"],
    "fa": ["رسانه", "تصویر", "مدیا", "پرونده", "رسانه‌ای"],
    "ff": ["Média", "Fichier"],
    "fi": ["Kuva", "Tiedosto"],
    "fiu-vro": ["Pilt", "Meediä"],
    "fo": ["Miðil", "Mynd"],
    "fr": ["Média", "Fichier"],
    "frp": ["Émâge", "Fichiér", "Mèdia"],
    "frr": ["Medium", "Datei", "Bild"],
    "fur": ["Immagine", "Figure"],
    "fy": ["Ofbyld"],
    "ga": ["Íomhá", "Meán"],
    "gag": ["Mediya", "Medya", "Resim", "Dosya", "Dosye"],
    "gan": ["媒体文件", "文件", "文檔", "档案", "媒體", "图像", "圖像", "媒体", "檔案"],
    "gd": ["Faidhle", "Meadhan"],
    "gl": ["Imaxe", "Ficheiro", "Arquivo", "Imagem"],
    "glk": ["رسانه", "تصویر", "پرونده", "فاىل", "رسانه‌ای", "مديا"],
    "gn": ["Medio", "Imagen", "Ta'ãnga"],
    "gom": ["माध्यम", "मिडिया", "फायल"],
    "gor": ["Gambar", "Berkas"],
    "got": ["𐍆𐌴𐌹𐌻𐌰"],
    "gu": ["દ્રશ્ય-શ્રાવ્ય (મિડિયા)", "દ્રશ્ય-શ્રાવ્ય_(મિડિયા)", "ચિત્ર"],
    "gv": ["Coadan", "Meanyn"],
    "hak": ["文件", "媒體", "圖像", "檔案"],
    "haw": ["Kiʻi", "Waihona", "Pāpaho"],
    "he": ["תמונה", "קו", "מדיה", "קובץ"],
    "hi": ["मीडिया", "चित्र"],
    "hif": ["file", "saadhan"],
    "hr": ["Mediji", "DT", "Slika", "F", "Datoteka"],
    "hsb": ["Wobraz", "Dataja", "Bild"],
    "ht": ["Imaj", "Fichye", "Medya"],
    "hu": ["Kép", "Fájl", "Média"],
    "hy": ["Պատկեր", "Մեդիա"],
    "ia": ["Imagine", "Multimedia"],
    "id": ["Gambar", "Berkas"],
    "ig": ["Nká", "Midia", "Usòrò", "Ákwúkwó orünotu", "Ákwúkwó_orünotu"],
    "ii": ["媒体文件", "文件", "档案", "图像", "媒体"],
    "ilo": ["Midia", "Papeles"],
    "inh": ["Медиа", "Файл", "Изображение"],
    "io": ["Imajo", "Arkivo"],
    "is": ["Miðill", "Mynd"],
    "it": ["Immagine"],
    "ja": ["メディア", "ファイル", "画像"],
    "jbo": ["velsku", "datnyvei"],
    "jv": ["Barkas", "Medhia", "Gambar", "Médhia"],
    "ka": ["მედია", "სურათი", "ფაილი"],
    "kaa": ["Swret", "Таспа", "سۋرەت", "Taspa", "Su'wret", "Сурет", "تاسپا"],
    "kab": ["Tugna"],
    "kbd": ["Медиа", "Файл"],
    "kbp": ["Média", "Fichier"],
    "kg": ["Fisye"],
    "kk": ["Swret", "سۋرەت", "Таспа", "Taspa", "Сурет", "تاسپا"],
    "kl": ["Billede", "Fiileq", "Fil"],
    "km": ["ឯកសារ", "រូបភាព", "មេឌា", "មីឌា"],
    "kn": ["ಚಿತ್ರ", "ಮೀಡಿಯ"],
    "ko": ["미디어", "파일", "그림"],
    "koi": ["Медиа", "Файл", "Изображение"],
    "krc": ["Медиа", "Файл", "Изображение"],
    "ks": ["میڈیا", "فَیِل"],
    "ksh": ["Beld", "Meedije", "Medie", "Belld", "Medium", "Datei", "Meedijum", "Bild"],
    "ku": ["میدیا", "پەڕگە", "Medya", "Wêne"],
    "kv": ["Медиа", "Файл", "Изображение"],
    "kw": ["Restren"],
    "ky": ["Медиа", "Файл"],
    "la": ["Imago", "Fasciculus"],
    "lad": ["Dossia", "Medya", "Archivo", "Dosya", "Imagen", "Meddia"],
    "lb": ["Fichier", "Bild"],
    "lbe": ["Медиа", "Сурат", "Изображение"],
    "lez": ["Медиа", "Mediya", "Файл", "Şəkil", "Изображение"],
    "lfn": ["Fix"],
    "li": ["Afbeelding", "Plaetje", "Aafbeilding"],
    "lij": ["Immaggine", "Immagine"],
    "lmo": ["Immagine", "Imàjine", "Archivi"],
    "ln": ["Média", "Fichier"],
    "lo": ["ສື່ອ", "ສື່", "ຮູບ"],
    "lrc": ["رسانه", "تصویر", "رسانه‌ای", "جانیا", "أسگ", "ڤارئسگأر"],
    "lt": ["Vaizdas", "Medija"],
    "ltg": ["Medeja", "Fails"],
    "lv": ["Attēls"],
    "mai": ["मेडिया", "फाइल"],
    "map-bms": ["Barkas", "Medhia", "Gambar", "Médhia"],
    "mdf": ["Медиа", "Няйф", "Изображение"],
    "mg": ["Rakitra", "Sary", "Média"],
    "mhr": ["Медиа", "Файл", "Изображение"],
    "min": ["Gambar", "Berkas"],
    "mk": ["Податотека", "Медија", "Медиум", "Слика"],
    "ml": ["പ്രമാണം", "ചി", "മീഡിയ", "പ്ര", "ചിത്രം"],
    "mn": ["Медиа", "Файл", "Зураг"],
    "mr": ["चित्र", "मिडिया"],
    "mrj": ["Медиа", "Файл", "Изображение"],
    "ms": ["Fail", "Imej"],
    "mt": ["Midja", "Medja", "Stampa"],
    "mwl": ["Multimédia", "Fexeiro", "Ficheiro", "Arquivo", "Imagem"],
    "my": ["ဖိုင်", "မီဒီယာ"],
    "myv": ["Медия", "Артовкс", "Изображение"],
    "mzn": ["رسانه", "تصویر", "مه‌دیا", "مدیا", "پرونده", "رسانه‌ای"],
    "nah": ["Mēdiatl", "Īxiptli", "Imagen"],
    "nap": ["Fiùra", "Immagine"],
    "nds": ["Datei", "Bild"],
    "nds-nl": ["Ofbeelding", "Afbeelding", "Bestaand"],
    "ne": ["मीडिया", "चित्र"],
    "new": ["किपा", "माध्यम"],
    "nl": ["Bestand", "Afbeelding"],
    "nn": ["Fil", "Bilde", "Filpeikar"],
    "no": ["Fil", "Medium", "Bilde"],
    "nov": [],
    "nrm": ["Média", "Fichier"],
    "nso": ["Seswantšho"],
    "nv": ["Eʼelyaaígíí"],
    "oc": ["Imatge", "Fichièr", "Mèdia"],
    "olo": ["Kuva", "Medii", "Failu"],
    "or": ["ମାଧ୍ୟମ", "ଫାଇଲ"],
    "os": ["Ныв", "Медиа", "Файл", "Изображение"],
    "pa": ["ਤਸਵੀਰ", "ਮੀਡੀਆ"],
    "pcd": ["Média", "Fichier"],
    "pdc": ["Medium", "Datei", "Bild", "Feil"],
    "pfl": ["Dadai", "Medium", "Datei", "Bild"],
    "pi": ["मीडिया", "पटिमा"],
    "pl": ["Plik", "Grafika"],
    "pms": ["Figura", "Immagine"],
    "pnb": ["میڈیا", "تصویر", "فائل"],
    "pnt": ["Εικόνα", "Αρχείον", "Εικόναν", "Μέσον"],
    "ps": ["انځور", "رسنۍ", "دوتنه"],
    "pt": ["Multimédia", "Ficheiro", "Arquivo", "Imagem"],
    "qu": ["Midya", "Imagen", "Rikcha"],
    "rm": ["Multimedia", "Datoteca"],
    "rmy": ["Fişier", "Mediya", "Chitro", "Imagine"],
    "ro": ["Fişier", "Imagine", "Fișier"],
    "roa-rup": ["Fişier", "Imagine", "Fișier"],
    "roa-tara": ["Immagine"],
    "ru": ["Медиа", "Файл", "Изображение"],
    "rue": ["Медіа", "Медиа", "Файл", "Изображение", "Зображення"],
    "rw": ["Dosiye", "Itangazamakuru"],
    "sa": ["चित्रम्", "माध्यमम्", "सञ्चिका", "माध्यम", "चित्रं"],
    "sah": ["Миэдьийэ", "Ойуу", "Билэ", "Изображение"],
    "sat": ["ᱨᱮᱫ", "ᱢᱤᱰᱤᱭᱟ"],
    "sc": ["Immàgini"],
    "scn": ["Immagine", "Mmàggini", "Mèdia"],
    "sd": ["عڪس", "ذريعات", "فائل"],
    "se": ["Fiila"],
    "sg": ["Média", "Fichier"],
    "sh": ["Mediji", "Slika", "Медија", "Datoteka", "Medija", "Слика"],
    "si": ["රූපය", "මාධ්‍යය", "ගොනුව"],
    "sk": ["Súbor", "Obrázok", "Médiá"],
    "sl": ["Slika", "Datoteka"],
    "sq": ["Figura", "Skeda"],
    "sr": ["Датотека", "Medij", "Slika", "Медија", "Datoteka", "Медиј", "Medija", "Слика"],
    "srn": ["Afbeelding", "Gefre"],
    "stq": ["Bielde", "Bild"],
    "su": ["Média", "Gambar"],
    "sv": ["Fil", "Bild"],
    "sw": ["Faili", "Picha"],
    "szl": ["Plik", "Grafika"],
    "ta": ["படிமம்", "ஊடகம்"],
    "tcy": ["ಮಾದ್ಯಮೊ", "ಫೈಲ್"],
    "te": ["ఫైలు", "దస్త్రం", "బొమ్మ", "మీడియా"],
    "tet": ["Imajen", "Arquivo", "Imagem"],
    "tg": ["Акс", "Медиа"],
    "th": ["ไฟล์", "สื่อ", "ภาพ"],
    "ti": ["ፋይል", "ሜድያ"],
    "tk": ["Faýl"],
    "tl": ["Midya", "Talaksan"],
    "tpi": ["Fail"],
    "tr": ["Medya", "Resim", "Dosya", "Ortam"],
    "tt": ["Медиа", "Рәсем", "Файл", "Räsem", "Изображение"],
    "ty": ["Média", "Fichier"],
    "tyv": ["Медиа", "Файл", "Изображение"],
    "udm": ["Медиа", "Файл", "Суред", "Изображение"],
    "ug": ["ۋاسىتە", "ھۆججەت"],
    "uk": ["Медіа", "Медиа", "Файл", "Изображение", "Зображення"],
    "ur": ["میڈیا", "تصویر", "وسیط", "زریعہ", "فائل", "ملف"],
    "uz": ["Mediya", "Tasvir", "Fayl"],
    "vec": ["Immagine", "Imàjine", "Mèdia"],
    "vep": ["Pilt", "Fail"],
    "vi": ["Phương_tiện", "Tập_tin", "Hình", "Tập tin", "Phương tiện"],
    "vls": ["Afbeelding", "Ofbeeldienge"],
    "vo": ["Ragiv", "Magod", "Nünamakanäd"],
    "wa": ["Imådje"],
    "war": ["Medya", "Fayl", "Paypay"],
    "wo": ["Xibaarukaay", "Dencukaay"],
    "wuu": ["文件", "档案", "图像", "媒体"],
    "xal": ["Аһар", "Боомг", "Изображение", "Зург"],
    "xmf": ["მედია", "სურათი", "ფაილი"],
    "yi": ["מעדיע", "תמונה", "טעקע", "בילד"],
    "yo": ["Fáìlì", "Amóhùnmáwòrán", "Àwòrán"],
    "za": ["媒体文件", "文件", "档案", "图像", "媒体"],
    "zea": ["Afbeelding", "Plaetje"],
    "zh": ["媒体文件", "F", "文件", "媒體", "档案", "图像", "圖像", "媒体", "檔案"],
    "zh-classical": ["文件", "媒體", "圖像", "檔案"],
    "zh-min-nan": ["tóng-àn", "文件", "媒體", "Mûi-thé", "圖像", "檔案"],
    "zh-yue": ["檔", "档", "文件", "图", "媒體", "圖", "档案", "图像", "圖像", "媒体", "檔案"],
}

# Source: for each Wikipedia language code (example shown for "ab"), aliases for namespace 14 accessed via this API call:
# https://ab.wikipedia.org/w/api.php?action=query&meta=siteinfo&siprop=namespacealiases|namespaces&format=json&formatversion=2
# Last accessed: 21 December 2021
CAT_ALIASES = {
    "ab": ["Категория", "Акатегориа"],
    "ace": ["Kawan", "Kategori"],
    "af": ["Kategorie"],
    "ak": ["Nkyekyem"],
    "als": ["Kategorie"],
    "am": ["መደብ"],
    "an": ["Categoría"],
    "ang": ["Flocc"],
    "ar": ["تصنيف"],
    "arc": ["ܣܕܪܐ"],
    "arz": ["تصنيف"],
    "as": ["CAT", "শ্ৰেণী", "श्रेणी", "শ্রেণী"],
    "ast": ["Categoría"],
    "atj": ["Tipanictawin"],
    "av": ["Категория"],
    "ay": ["Categoría"],
    "az": ["Kateqoriya"],
    "azb": ["بؤلمه"],
    "ba": ["Төркөм", "Категория"],
    "bar": ["Kategorie"],
    "bat-smg": ["Kategorija", "Kateguorėjė"],
    "bcl": ["Kategorya"],
    "be": ["Катэгорыя"],
    "be-x-old": ["Катэгорыя"],
    "bg": ["Категория"],
    "bh": ["श्रेणी"],
    "bjn": ["Tumbung", "Kategori"],
    "bm": ["Catégorie"],
    "bn": ["বিষয়শ্রেণী", "വിഭാഗം"],
    "bpy": ["থাক"],
    "br": ["Rummad"],
    "bs": ["Kategorija"],
    "bug": ["Kategori"],
    "bxr": ["Категори", "Категория"],
    "ca": ["Categoria"],
    "cbk-zam": ["Categoría"],
    "cdo": ["分類"],
    "ce": ["Категори", "Тоба", "Кадегар"],
    "ceb": ["Kategoriya"],
    "ch": ["Katigoria"],
    "ckb": ["پ", "پۆل"],
    "co": ["Categoria"],
    "crh": ["Категория", "Kategoriya"],
    "cs": ["Kategorie"],
    "csb": ["Kategòrëjô"],
    "cu": ["Катигорї", "Категория", "Катигорїꙗ"],
    "cv": ["Категори"],
    "cy": ["Categori"],
    "da": ["Kategori"],
    "de": ["Kategorie"],
    "din": ["Bekätakthook"],
    "diq": ["Kategoriye", "Kategori"],
    "dsb": ["Kategorija"],
    "dty": ["श्रेणी"],
    "dv": ["ޤިސްމު"],
    "el": ["Κατηγορία"],
    "eml": ["Categoria"],
    "eo": ["Kategorio"],
    "es": ["CAT", "Categoría"],
    "et": ["Kategooria"],
    "eu": ["Kategoria"],
    "ext": ["Categoría", "Categoria"],
    "fa": ["رده"],
    "ff": ["Catégorie"],
    "fi": ["Luokka"],
    "fiu-vro": ["Katõgooria"],
    "fo": ["Bólkur"],
    "fr": ["Catégorie"],
    "frp": ["Catègorie"],
    "frr": ["Kategorie"],
    "fur": ["Categorie"],
    "fy": ["Kategory"],
    "ga": ["Rang", "Catagóir"],
    "gag": ["Kategori", "Kategoriya"],
    "gan": ["分類", "分类"],
    "gd": ["Roinn-seòrsa"],
    "gl": ["Categoría"],
    "glk": ["جرگه", "رده"],
    "gn": ["Ñemohenda"],
    "gom": ["वर्ग", "श्रेणी"],
    "gor": ["Dalala"],
    "got": ["𐌷𐌰𐌽𐍃𐌰"],
    "gu": ["શ્રેણી", "CAT", "શ્રે"],
    "gv": ["Ronney"],
    "hak": ["分類"],
    "haw": ["Māhele"],
    "he": ["קטגוריה", "קט"],
    "hi": ["श्र", "श्रेणी"],
    "hif": ["vibhag"],
    "hr": ["CT", "KT", "Kategorija"],
    "hsb": ["Kategorija"],
    "ht": ["Kategori"],
    "hu": ["Kategória"],
    "hy": ["Կատեգորիա"],
    "ia": ["Categoria"],
    "id": ["Kategori"],
    "ie": ["Categorie"],
    "ig": ["Ébéonọr", "Òtù"],
    "ii": ["分类"],
    "ilo": ["Kategoria"],
    "inh": ["ОагӀат"],
    "io": ["Kategorio"],
    "is": ["Flokkur"],
    "it": ["CAT", "Categoria"],
    "ja": ["カテゴリ"],
    "jbo": ["klesi"],
    "jv": ["Kategori"],
    "ka": ["კატეგორია"],
    "kaa": ["Sanat", "Kategoriya", "Санат", "سانات"],
    "kab": ["Taggayt"],
    "kbd": ["Категория", "Категориэ"],
    "kbp": ["Catégorie"],
    "kg": ["Kalasi"],
    "kk": ["Sanat", "Санат", "سانات"],
    "kl": ["Sumut_atassuseq", "Kategori", "Sumut atassuseq"],
    "km": ["ចំនាត់ថ្នាក់ក្រុម", "ចំណាត់ក្រុម", "ចំណាត់ថ្នាក់ក្រុម"],
    "kn": ["ವರ್ಗ"],
    "ko": ["분류"],
    "koi": ["Категория"],
    "krc": ["Категория"],
    "ks": ["زٲژ"],
    "ksh": ["Saachjropp", "Saachjrop", "Katejori", "Kategorie", "Saachjrupp", "Kattejori", "Sachjrop"],
    "ku": ["Kategorî", "پۆل"],
    "kv": ["Категория"],
    "kw": ["Class", "Klass"],
    "ky": ["Категория"],
    "la": ["Categoria"],
    "lad": ["Kateggoría", "Katēggoría", "Categoría"],
    "lb": ["Kategorie"],
    "lbe": ["Категория"],
    "lez": ["Категория"],
    "lfn": ["Categoria"],
    "li": ["Categorie", "Kategorie"],
    "lij": ["Categorîa", "Categoria"],
    "lmo": ["Categuria", "Categoria"],
    "ln": ["Catégorie"],
    "lo": ["ໝວດ"],
    "lrc": ["دأسە"],
    "lt": ["Kategorija"],
    "ltg": ["Kategoreja"],
    "lv": ["Kategorija"],
    "mai": ["CA", "श्रेणी"],
    "map-bms": ["Kategori"],
    "mdf": ["Категорие", "Категория"],
    "mg": ["Sokajy", "Catégorie"],
    "mhr": ["Категория", "Категорий"],
    "min": ["Kategori"],
    "mk": ["Категорија"],
    "ml": ["വിഭാഗം", "വി", "വർഗ്ഗം", "വ"],
    "mn": ["Ангилал"],
    "mr": ["वर्ग"],
    "mrj": ["Категори", "Категория"],
    "ms": ["Kategori"],
    "mt": ["Kategorija"],
    "mwl": ["Catadorie", "Categoria"],
    "my": ["ကဏ္ဍ"],
    "myv": ["Категория"],
    "mzn": ["رج", "رده"],
    "nah": ["Neneuhcāyōtl", "Categoría"],
    "nap": ["Categurìa", "Categoria"],
    "nds": ["Kategorie"],
    "nds-nl": ["Categorie", "Kattegerie", "Kategorie"],
    "ne": ["श्रेणी"],
    "new": ["पुचः"],
    "nl": ["Categorie"],
    "nn": ["Kategori"],
    "no": ["Kategori"],
    "nrm": ["Catégorie"],
    "nso": ["Setensele"],
    "nv": ["Tʼááłáhági_átʼéego", "Tʼááłáhági átʼéego"],
    "oc": ["Categoria"],
    "olo": ["Kategourii"],
    "or": ["ବିଭାଗ", "ଶ୍ରେଣୀ"],
    "os": ["Категори"],
    "pa": ["ਸ਼੍ਰੇਣੀ"],
    "pcd": ["Catégorie"],
    "pdc": ["Abdeeling", "Kategorie"],
    "pfl": ["Kadegorie", "Sachgrubb", "Kategorie"],
    "pi": ["विभाग"],
    "pl": ["Kategoria"],
    "pms": ["Categorìa"],
    "pnb": ["گٹھ"],
    "pnt": ["Κατηγορίαν"],
    "ps": ["وېشنيزه"],
    "pt": ["Categoria"],
    "qu": ["Katiguriya"],
    "rm": ["Categoria"],
    "rmy": ["Shopni"],
    "ro": ["Categorie"],
    "roa-rup": ["Categorie"],
    "roa-tara": ["Categoria"],
    "ru": ["Категория", "К"],
    "rue": ["Категория", "Катеґорія"],
    "rw": ["Ikiciro"],
    "sa": ["वर्गः"],
    "sah": ["Категория"],
    "sat": ["ᱛᱷᱚᱠ"],
    "sc": ["Categoria"],
    "scn": ["Catigurìa"],
    "sd": ["زمرو"],
    "se": ["Kategoriija"],
    "sg": ["Catégorie"],
    "sh": ["Kategorija", "Категорија"],
    "si": ["ප්‍රවර්ගය"],
    "sk": ["Kategória"],
    "sl": ["Kategorija"],
    "sq": ["Kategoria", "Kategori"],
    "sr": ["Kategorija", "Категорија"],
    "srn": ["Categorie", "Guru"],
    "stq": ["Kategorie"],
    "su": ["Kategori"],
    "sv": ["Kategori"],
    "sw": ["Jamii"],
    "szl": ["Kategoryjo", "Kategoria"],
    "ta": ["பகுப்பு"],
    "tcy": ["ವರ್ಗೊ"],
    "te": ["వర్గం"],
    "tet": ["Kategoría", "Kategoria"],
    "tg": ["Гурӯҳ"],
    "th": ["หมวดหมู่"],
    "ti": ["መደብ"],
    "tk": ["Kategoriýa"],
    "tl": ["Kategorya", "Kaurian"],
    "tpi": ["Grup"],
    "tr": ["Kategori", "KAT"],
    "tt": ["Төркем", "Törkem", "Категория"],
    "ty": ["Catégorie"],
    "tyv": ["Аңгылал", "Категория"],
    "udm": ["Категория"],
    "ug": ["تۈر"],
    "uk": ["Категория", "Категорія"],
    "ur": ["زمرہ"],
    "uz": ["Turkum", "Kategoriya"],
    "vec": ["Categoria"],
    "vep": ["Kategorii"],
    "vi": ["Thể_loại", "Thể loại"],
    "vls": ["Categorie"],
    "vo": ["Klad"],
    "wa": ["Categoreye"],
    "war": ["Kaarangay"],
    "wo": ["Wàll", "Catégorie"],
    "wuu": ["分类"],
    "xal": ["Янз", "Әәшл"],
    "xmf": ["კატეგორია"],
    "yi": ["קאטעגאריע", "קאַטעגאָריע"],
    "yo": ["Ẹ̀ka"],
    "za": ["分类"],
    "zea": ["Categorie"],
    "zh": ["分类", "分類", "CAT"],
    "zh-classical": ["分類", "CAT"],
    "zh-min-nan": ["分類", "Lūi-pia̍t"],
    "zh-yue": ["分类", "分類", "类", "類"],
}

# See: https://www.mediawiki.org/wiki/Help:Images#Syntax
# Gathered via: https://public.paws.wmcloud.org/User:Isaac_(WMF)/Edit%20Diffs/generate_img_option_params.ipynb
DEF_OPTION_TAGS = {
    "keywords": [
        "baseline",
        "border",
        "bottom",
        "center",
        "centre",
        "enframed",
        "frame",
        "framed",
        "frameless",
        "left",
        "middle",
        "none",
        "right",
        "sub",
        "sup",
        "super",
        "text-bottom",
        "text-top",
        "thumb",
        "thumbnail",
        "top",
        "upright"
    ],
    "params": [
        "alt",
        "class",
        "lang",
        "link",
        "lossy",
        "page",
        "thumb",
        "thumbnail",
        "upright"
    ],
    "startswith": [
        "page ",
        "upright "
    ],
    "endswith": [
        "px"
    ]
}

IMG_OPTION_ALIASES = {
    "ab": {
        "keywords": [
            "\u0431\u0435\u0437",
            "\u0431\u0435\u0437\u0440\u0430\u043c\u043a\u0438",
            "\u0433\u0440\u0430\u043d\u0438\u0446\u0430",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u043d\u0430\u0434",
            "\u043e\u0431\u0440\u0430\u043c\u0438\u0442\u044c",
            "\u043e\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u0435",
            "\u043f\u043e\u0434",
            "\u043f\u043e\u0441\u0435\u0440\u0435\u0434\u0438\u043d\u0435",
            "\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u043b\u0435\u0432\u0430",
            "\u0441\u043d\u0438\u0437\u0443",
            "\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u043d\u0438\u0437\u0443",
            "\u0446\u0435\u043d\u0442\u0440"
        ],
        "params": [
            "\u0430\u043b\u044c\u0442",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u0441\u044b\u043b\u043a\u0430",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430"
        ],
        "startswith": [
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430 ",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430 "
        ],
        "endswith": [
            "\u043f\u043a\u0441"
        ]
    },
    "ace": {
        "keywords": [
            "atas",
            "atas-teks",
            "atek",
            "batas",
            "batek",
            "bawah",
            "bawah-teks",
            "bing",
            "bingkai",
            "gada",
            "garis_dasar",
            "jempol",
            "jmpl",
            "ka",
            "kanan",
            "ki",
            "kiri",
            "lurus",
            "mini",
            "miniatur",
            "nir",
            "nirbing",
            "pus",
            "pusat",
            "tanpa",
            "tanpabingkai",
            "tegak",
            "tengah",
            "tepi",
            "upa"
        ],
        "params": [
            "al",
            "alternatif",
            "bhs",
            "hal",
            "halaman",
            "jempol",
            "jmpl",
            "lurus",
            "mini",
            "miniatur",
            "pra",
            "pranala",
            "tegak"
        ],
        "startswith": [
            "hal_",
            "halaman_",
            "lurus_",
            "tegak_"
        ]
    },
    "af": {
        "keywords": [
            "bo",
            "duimnael",
            "geen",
            "links",
            "middel",
            "omraam",
            "onder",
            "raam",
            "raamloos",
            "regs",
            "senter",
            "teks-bo",
            "teks-onder"
        ],
        "params": [
            "skakel"
        ]
    },
    "als": {
        "keywords": [
            "gerahmt",
            "grundlinie",
            "hoch",
            "hochgestellt",
            "hochkant",
            "links",
            "mini",
            "miniatur",
            "mitte",
            "oben",
            "ohne",
            "rahmenlos",
            "rand",
            "rechts",
            "text-oben",
            "text-unten",
            "tief",
            "tiefgestellt",
            "unten",
            "zentriert"
        ],
        "params": [
            "alternativtext",
            "hochkant",
            "klasse",
            "mini",
            "miniatur",
            "seite",
            "sprache",
            "verweis"
        ],
        "startswith": [
            "hochkant ",
            "hochkant_",
            "seite ",
            "seite_"
        ]
    },
    "alt": {
        "keywords": [
            "\u0431\u0435\u0437",
            "\u0431\u0435\u0437\u0440\u0430\u043c\u043a\u0438",
            "\u0433\u0440\u0430\u043d\u0438\u0446\u0430",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u043d\u0430\u0434",
            "\u043e\u0431\u0440\u0430\u043c\u0438\u0442\u044c",
            "\u043e\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u0435",
            "\u043f\u043e\u0434",
            "\u043f\u043e\u0441\u0435\u0440\u0435\u0434\u0438\u043d\u0435",
            "\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u043b\u0435\u0432\u0430",
            "\u0441\u043d\u0438\u0437\u0443",
            "\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u043d\u0438\u0437\u0443",
            "\u0446\u0435\u043d\u0442\u0440"
        ],
        "params": [
            "\u0430\u043b\u044c\u0442",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u0441\u044b\u043b\u043a\u0430",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430"
        ],
        "startswith": [
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430 ",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430 "
        ],
        "endswith": [
            "\u043f\u043a\u0441"
        ]
    },
    "ami": {
        "keywords": [
            "\u4e0a\u6a19",
            "\u4e0b\u6a19",
            "\u4e2d\u95f4",
            "\u53f3",
            "\u53f3\u4e0a",
            "\u5782\u76f4\u7f6e\u4e2d",
            "\u5782\u76f4\u7f6e\u5e95",
            "\u5782\u76f4\u7f6e\u9802",
            "\u57fa\u7ebf",
            "\u5b50",
            "\u5c45\u4e2d",
            "\u5de6",
            "\u5e95\u90e8",
            "\u6587\u5b57\u5e95\u90e8",
            "\u6587\u5b57\u7f6e\u5e95",
            "\u6587\u5b57\u7f6e\u9802",
            "\u6587\u5b57\u9876\u90e8",
            "\u65e0",
            "\u65e0\u6846",
            "\u66ff\u4ee3\u6587\u5b57",
            "\u6709\u6846",
            "\u7121",
            "\u7121\u6846",
            "\u7e2e\u5716",
            "\u7f29\u7565\u56fe",
            "\u7f6e\u4e2d",
            "\u8d85",
            "\u8fb9\u6846",
            "\u908a\u6846",
            "\u9876\u90e8"
        ],
        "params": [
            "\u53f3\u4e0a",
            "\u66ff\u4ee3",
            "\u66ff\u4ee3\u6587\u672c",
            "\u7c7b",
            "\u7e2e\u5716",
            "\u7f29\u7565\u56fe",
            "\u8a9e\u8a00",
            "\u8bed\u8a00",
            "\u9023\u7d50",
            "\u94fe\u63a5",
            "\u9801",
            "\u985e\u5225",
            "\u9875\u6570"
        ],
        "startswith": [
            "\u53f3\u4e0a"
        ],
        "endswith": [
            "\u50cf\u7d20",
            "\u9801",
            "\u9875"
        ]
    },
    "an": {
        "keywords": [
            "abajo",
            "arriba",
            "borde",
            "centrada",
            "centrado",
            "centrar",
            "centro",
            "cucha",
            "dcha",
            "der",
            "derecha",
            "dreita",
            "enmarcada",
            "enmarcado",
            "izda",
            "izq",
            "izquierda",
            "marco",
            "medio",
            "mini",
            "miniatura",
            "miniaturadeimagen",
            "nada",
            "ninguna",
            "ninguno",
            "no",
            "sin_enmarcar",
            "sinenmarcar",
            "sinmarco",
            "zurda"
        ],
        "params": [
            "enlace",
            "idioma",
            "miniatura",
            "miniaturadeimagen",
            "pagina",
            "p\u00e1gina",
            "vinculo",
            "v\u00ednculo"
        ],
        "startswith": [
            "pagina_",
            "p\u00e1gina_"
        ]
    },
    "ar": {
        "keywords": [
            "\u0623\u0633\u0641\u0644",
            "\u0623\u0639\u0644\u0649",
            "\u0625\u0637\u0627\u0631",
            "\u0628\u0625\u0637\u0627\u0631",
            "\u0628\u062f\u0648\u0646",
            "\u0628\u0644\u0627",
            "\u062a\u0635\u063a\u064a\u0631",
            "\u062d\u062f\u0648\u062f",
            "\u062e\u0637_\u0623\u0633\u0627\u0633\u064a",
            "\u0633\u0628",
            "\u0633\u0648\u0628\u0631",
            "\u0641\u0631\u0639\u064a",
            "\u0644\u0627\u0625\u0637\u0627\u0631",
            "\u0645\u0631\u0643\u0632",
            "\u0645\u0639\u062f\u0648\u0644",
            "\u0646\u0635_\u0623\u0633\u0641\u0644",
            "\u0646\u0635_\u0623\u0639\u0644\u0649",
            "\u0648\u0633\u0637",
            "\u064a\u0633\u0627\u0631",
            "\u064a\u0645\u064a\u0646"
        ],
        "params": [
            "\u0628\u062f\u064a\u0644",
            "\u062a\u0635\u063a\u064a\u0631",
            "\u0631\u0627\u0628\u0637",
            "\u0631\u062a\u0628\u0629",
            "\u0635\u0641\u062d\u0629",
            "\u0644\u063a\u0629",
            "\u0645\u0635\u063a\u0631",
            "\u0645\u0639\u062f\u0648\u0644",
            "\u0648\u0635\u0644\u0629"
        ],
        "startswith": [
            "\u0635\u0641\u062d\u0629_",
            "\u0645\u0639\u062f\u0648\u0644_"
        ],
        "endswith": [
            "\u0628\u0643",
            "\u0639\u0646"
        ]
    },
    "arc": {
        "keywords": [
            "\u0719\u0725\u0718\u072a\u072c\u0710",
            "\u071d\u0721\u071d\u0722\u0710",
            "\u0720\u0710_\u0721\u0715\u0721",
            "\u0721\u0728\u0725\u0710",
            "\u0723\u0721\u0720\u0710",
            "\u0723\u072a\u071b\u0710_\u072b\u072a\u072b\u071d\u0710",
            "\u0726\u072a\u0725\u071d\u0710",
            "\u072c\u071a\u0718\u0721\u0710"
        ],
        "params": [
            "\u0719\u0725\u0718\u072a\u072c\u0710",
            "\u0726\u0710\u072c\u0710"
        ],
        "startswith": [
            "\u0726\u0710\u072c\u0710 "
        ]
    },
    "ary": {
        "keywords": [
            "\u0623\u0633\u0641\u0644",
            "\u0623\u0639\u0644\u0649",
            "\u0625\u0637\u0627\u0631",
            "\u0628\u0625\u0637\u0627\u0631",
            "\u0628\u062f\u0648\u0646",
            "\u0628\u0644\u0627",
            "\u062a\u0635\u063a\u064a\u0631",
            "\u062d\u062f\u0648\u062f",
            "\u062e\u0637_\u0623\u0633\u0627\u0633\u064a",
            "\u0633\u0628",
            "\u0633\u0648\u0628\u0631",
            "\u0641\u0631\u0639\u064a",
            "\u0644\u0627\u0625\u0637\u0627\u0631",
            "\u0645\u0631\u0643\u0632",
            "\u0645\u0639\u062f\u0648\u0644",
            "\u0646\u0635_\u0623\u0633\u0641\u0644",
            "\u0646\u0635_\u0623\u0639\u0644\u0649",
            "\u0648\u0633\u0637",
            "\u064a\u0633\u0627\u0631",
            "\u064a\u0645\u064a\u0646"
        ],
        "params": [
            "\u0628\u062f\u064a\u0644",
            "\u062a\u0635\u063a\u064a\u0631",
            "\u0631\u0627\u0628\u0637",
            "\u0631\u062a\u0628\u0629",
            "\u0635\u0641\u062d\u0629",
            "\u0644\u063a\u0629",
            "\u0645\u0635\u063a\u0631",
            "\u0645\u0639\u062f\u0648\u0644",
            "\u0648\u0635\u0644\u0629"
        ],
        "startswith": [
            "\u0635\u0641\u062d\u0629_",
            "\u0645\u0639\u062f\u0648\u0644_"
        ],
        "endswith": [
            "\u0628\u0643",
            "\u0639\u0646"
        ]
    },
    "arz": {
        "keywords": [
            "\u0623\u0633\u0641\u0644",
            "\u0623\u0639\u0644\u0649",
            "\u0625\u0637\u0627\u0631",
            "\u0628\u0625\u0637\u0627\u0631",
            "\u0628\u062f\u0648\u0646",
            "\u0628\u0644\u0627",
            "\u062a\u0635\u063a\u064a\u0631",
            "\u062d\u062f",
            "\u062d\u062f\u0648\u062f",
            "\u062e\u0637_\u0623\u0633\u0627\u0633\u064a",
            "\u062e\u0637_\u0627\u0633\u0627\u0633\u0649",
            "\u0633\u0628",
            "\u0633\u0648\u0628\u0631",
            "\u0641\u0631\u0639\u0649",
            "\u0641\u0631\u0639\u064a",
            "\u0644\u0627\u0625\u0637\u0627\u0631",
            "\u0645\u0631\u0643\u0632",
            "\u0645\u0635\u063a\u0631",
            "\u0645\u0639\u062f\u0648\u0644",
            "\u0645\u0646_\u063a\u064a\u0631_\u0627\u0637\u0627\u0631",
            "\u0646\u0635_\u0623\u0633\u0641\u0644",
            "\u0646\u0635_\u0623\u0639\u0644\u0649",
            "\u0648\u0633\u0637",
            "\u064a\u0633\u0627\u0631",
            "\u064a\u0645\u064a\u0646"
        ],
        "params": [
            "\u0628\u062f\u064a\u0644",
            "\u062a\u0635\u063a\u064a\u0631",
            "\u0631\u0627\u0628\u0637",
            "\u0631\u062a\u0628\u0629",
            "\u0631\u062a\u0628\u0647",
            "\u0635\u0641\u062d",
            "\u0635\u0641\u062d\u0629",
            "\u0644\u063a\u0629",
            "\u0644\u063a\u0647",
            "\u0645\u0635\u063a\u0631",
            "\u0645\u0639\u062f\u0648\u0644",
            "\u0648\u0635\u0644\u0629"
        ],
        "startswith": [
            "\u0635\u0641\u062d\u0629_",
            "\u0635\u0641\u062d\u0647_",
            "\u0645\u0639\u062f\u0648\u0644_"
        ],
        "endswith": [
            "\u0628\u0643",
            "\u0639\u0646"
        ]
    },
    "ast": {
        "keywords": [
            "abajo",
            "arriba",
            "borde",
            "centrada",
            "centrado",
            "centrar",
            "centro",
            "dcha",
            "der",
            "derecha",
            "enmarcada",
            "enmarcado",
            "izda",
            "izq",
            "izquierda",
            "marco",
            "medio",
            "mini",
            "miniatura",
            "miniaturadeimagen",
            "nada",
            "ninguna",
            "ninguno",
            "no",
            "sin_enmarcar",
            "sinenmarcar",
            "sinmarco"
        ],
        "params": [
            "enlace",
            "idioma",
            "miniatura",
            "miniaturadeimagen",
            "pagina",
            "p\u00e1gina",
            "vinculo",
            "v\u00ednculo"
        ],
        "startswith": [
            "pagina_",
            "p\u00e1gina_"
        ]
    },
    "atj": {
        "keywords": [
            "bas",
            "bas-texte",
            "bas-txt",
            "base",
            "bordure",
            "cadre",
            "centr\u00e9",
            "droite",
            "encadre",
            "encadr\u00e9",
            "exp",
            "exposant",
            "gauche",
            "haut",
            "haut-texte",
            "haut-txt",
            "ind",
            "indice",
            "ligne-de-base",
            "milieu",
            "neant",
            "non_encadre",
            "non_encadr\u00e9",
            "n\u00e9ant",
            "redresse",
            "sans_cadre",
            "vignette"
        ],
        "params": [
            "classe",
            "langue",
            "lien",
            "redresse",
            "vignette"
        ],
        "startswith": [
            "redresse_"
        ]
    },
    "av": {
        "keywords": [
            "\u0431\u0435\u0437",
            "\u0431\u0435\u0437\u0440\u0430\u043c\u043a\u0438",
            "\u0433\u0440\u0430\u043d\u0438\u0446\u0430",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u043d\u0430\u0434",
            "\u043e\u0431\u0440\u0430\u043c\u0438\u0442\u044c",
            "\u043e\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u0435",
            "\u043f\u043e\u0434",
            "\u043f\u043e\u0441\u0435\u0440\u0435\u0434\u0438\u043d\u0435",
            "\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u043b\u0435\u0432\u0430",
            "\u0441\u043d\u0438\u0437\u0443",
            "\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u043d\u0438\u0437\u0443",
            "\u0446\u0435\u043d\u0442\u0440"
        ],
        "params": [
            "\u0430\u043b\u044c\u0442",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u0441\u044b\u043b\u043a\u0430",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430"
        ],
        "startswith": [
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430 ",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430 "
        ],
        "endswith": [
            "\u043f\u043a\u0441"
        ]
    },
    "avk": {
        "keywords": [
            "abajo",
            "arriba",
            "bas",
            "bas-texte",
            "bas-txt",
            "base",
            "borde",
            "bordure",
            "cadre",
            "centrada",
            "centrado",
            "centrar",
            "centro",
            "centr\u00e9",
            "dcha",
            "der",
            "derecha",
            "droite",
            "encadre",
            "encadr\u00e9",
            "enmarcada",
            "enmarcado",
            "exp",
            "exposant",
            "gauche",
            "haut",
            "haut-texte",
            "haut-txt",
            "ind",
            "indice",
            "izda",
            "izq",
            "izquierda",
            "ligne-de-base",
            "marco",
            "medio",
            "milieu",
            "mini",
            "miniatura",
            "miniaturadeimagen",
            "nada",
            "neant",
            "ninguna",
            "ninguno",
            "no",
            "non_encadre",
            "non_encadr\u00e9",
            "n\u00e9ant",
            "redresse",
            "sans_cadre",
            "sin_enmarcar",
            "sinenmarcar",
            "sinmarco",
            "vignette",
            "\u0431\u0435\u0437",
            "\u0431\u0435\u0437\u0440\u0430\u043c\u043a\u0438",
            "\u0433\u0440\u0430\u043d\u0438\u0446\u0430",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u043d\u0430\u0434",
            "\u043e\u0431\u0440\u0430\u043c\u0438\u0442\u044c",
            "\u043e\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u0435",
            "\u043f\u043e\u0434",
            "\u043f\u043e\u0441\u0435\u0440\u0435\u0434\u0438\u043d\u0435",
            "\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u043b\u0435\u0432\u0430",
            "\u0441\u043d\u0438\u0437\u0443",
            "\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u043d\u0438\u0437\u0443",
            "\u0446\u0435\u043d\u0442\u0440"
        ],
        "params": [
            "classe",
            "enlace",
            "idioma",
            "langue",
            "lien",
            "miniatura",
            "miniaturadeimagen",
            "pagina",
            "p\u00e1gina",
            "redresse",
            "vignette",
            "vinculo",
            "v\u00ednculo",
            "\u0430\u043b\u044c\u0442",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u0441\u044b\u043b\u043a\u0430",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430"
        ],
        "startswith": [
            "pagina_",
            "p\u00e1gina_",
            "redresse_",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430 ",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430 "
        ],
        "endswith": [
            "\u043f\u043a\u0441"
        ]
    },
    "awa": {
        "keywords": [
            "\u0905\u0902\u0917\u0942\u0920\u093e",
            "\u0905\u0902\u0917\u0942\u0920\u093e\u0915\u093e\u0930",
            "\u0906\u0927\u093e\u0930_\u0930\u0947\u0916\u093e",
            "\u0915\u093f\u0928\u093e\u0930\u093e",
            "\u0915\u0947\u0902\u0926\u094d\u0930",
            "\u0915\u0947\u0902\u0926\u094d\u0930\u093f\u0924",
            "\u0915\u0947\u0928\u094d\u0926\u094d\u0930",
            "\u0915\u0947\u0928\u094d\u0926\u094d\u0930\u093f\u0924",
            "\u0915\u094b\u0908_\u0928\u0939\u0940\u0902",
            "\u0916\u0921\u093c\u0940",
            "\u0924\u0932",
            "\u0926\u093e\u090f\u0901",
            "\u0926\u093e\u090f\u0902",
            "\u0926\u093e\u092f\u0947\u0902",
            "\u092a\u0926",
            "\u092a\u093e\u0920-\u0924\u0932",
            "\u092a\u093e\u0920-\u0936\u0940\u0930\u094d\u0937",
            "\u092b\u093c\u094d\u0930\u0947\u092e",
            "\u092b\u093c\u094d\u0930\u0947\u092e\u0939\u0940\u0928",
            "\u092b\u094d\u0930\u0947\u092e",
            "\u092b\u094d\u0930\u0947\u092e\u0939\u0940\u0928",
            "\u092c\u093e\u090f\u0901",
            "\u092c\u093e\u090f\u0902",
            "\u092c\u093e\u092f\u0947\u0902",
            "\u092c\u0949\u0930\u094d\u0921\u0930",
            "\u092e\u0927\u094d\u092f",
            "\u092e\u0942\u0930\u094d\u0927",
            "\u0936\u0940\u0930\u094d\u0937"
        ],
        "params": [
            "\u0905\u0902\u0917\u0942\u0920\u093e",
            "\u0905\u0902\u0917\u0942\u0920\u093e\u0915\u093e\u0930",
            "\u0915\u0921\u093c\u0940",
            "\u0916\u0921\u093c\u0940",
            "\u092a\u093e\u0920",
            "\u092a\u0943\u0937\u094d\u0920",
            "\u092d\u093e\u0937\u093e",
            "\u0935\u0930\u094d\u0917"
        ],
        "startswith": [
            "\u0916\u0921\u093c\u0940_",
            "\u092a\u0943\u0937\u094d\u0920_"
        ],
        "endswith": [
            "\u092a\u093f\u0915\u094d\u0938\u0947\u0932"
        ]
    },
    "ay": {
        "keywords": [
            "abajo",
            "arriba",
            "borde",
            "centrada",
            "centrado",
            "centrar",
            "centro",
            "dcha",
            "der",
            "derecha",
            "enmarcada",
            "enmarcado",
            "izda",
            "izq",
            "izquierda",
            "marco",
            "medio",
            "mini",
            "miniatura",
            "miniaturadeimagen",
            "nada",
            "ninguna",
            "ninguno",
            "no",
            "sin_enmarcar",
            "sinenmarcar",
            "sinmarco"
        ],
        "params": [
            "enlace",
            "idioma",
            "miniatura",
            "miniaturadeimagen",
            "pagina",
            "p\u00e1gina",
            "vinculo",
            "v\u00ednculo"
        ],
        "startswith": [
            "pagina_",
            "p\u00e1gina_"
        ]
    },
    "azb": {
        "keywords": [
            "\u0627\u0646\u06af\u0634\u062a\u062f\u0627\u0646",
            "\u0627\u0646\u06af\u0634\u062a\u06cc",
            "\u0627\u06cc\u0633\u062a\u0627\u062f\u0647",
            "\u0628\u0627\u0644\u0627",
            "\u0628\u0646\u062f\u0627\u0646\u06af\u0634\u062a\u06cc",
            "\u0628\u06cc_\u0642\u0627\u0628",
            "\u0628\u06cc\u0642\u0627\u0628",
            "\u0628\u06cc\u200c\u0642\u0627\u0628",
            "\u062d\u0627\u0634\u06cc\u0647",
            "\u0631\u0627\u0633\u062a",
            "\u0632\u0628\u0631",
            "\u0632\u06cc\u0631",
            "\u0633\u0627\u063a",
            "\u0633\u0648\u0644",
            "\u0642\u0627\u0628",
            "\u0642\u0627\u0628\u06cc\u0642",
            "\u0645\u062a\u0646-\u0628\u0627\u0644\u0627",
            "\u0645\u062a\u0646-\u067e\u0627\u06cc\u06cc\u0646",
            "\u0645\u06cc\u0627\u0646\u0647",
            "\u0647\u0626\u0686",
            "\u0647\u0645\u06a9\u0641",
            "\u0647\u06cc\u0686",
            "\u0648\u0633\u0637",
            "\u067e\u0627\u06cc\u06cc\u0646",
            "\u0686\u067e"
        ],
        "params": [
            "\u0627\u0646\u06af\u0634\u062a\u062f\u0627\u0646",
            "\u0627\u0646\u06af\u0634\u062a\u06cc",
            "\u0627\u06cc\u0633\u062a\u0627\u062f\u0647",
            "\u0628\u0646\u062f\u0627\u0646\u06af\u0634\u062a\u06cc",
            "\u062c\u0627\u06cc\u06af\u0632\u06cc\u0646",
            "\u0632\u0628\u0627\u0646",
            "\u0635\u0641\u062d\u0647",
            "\u067e\u06cc\u0648\u0646\u062f",
            "\u06a9\u0644\u0627\u0633"
        ],
        "startswith": [
            "\u0627\u06cc\u0633\u062a\u0627\u062f\u0647_",
            "\u0635\u0641\u062d\u0647_"
        ],
        "endswith": [
            "\u067e\u06cc\u06a9\u0633\u0644"
        ]
    },
    "ba": {
        "keywords": [
            "\u0431\u0435\u0437",
            "\u0431\u0435\u0437\u0440\u0430\u043c\u043a\u0438",
            "\u0433\u0440\u0430\u043d\u0438\u0446\u0430",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u043d\u0430\u0434",
            "\u043e\u0431\u0440\u0430\u043c\u0438\u0442\u044c",
            "\u043e\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u0435",
            "\u043f\u043e\u0434",
            "\u043f\u043e\u0441\u0435\u0440\u0435\u0434\u0438\u043d\u0435",
            "\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u043b\u0435\u0432\u0430",
            "\u0441\u043d\u0438\u0437\u0443",
            "\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u043d\u0438\u0437\u0443",
            "\u0446\u0435\u043d\u0442\u0440"
        ],
        "params": [
            "\u0430\u043b\u044c\u0442",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u0441\u044b\u043b\u043a\u0430",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430"
        ],
        "startswith": [
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430 ",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430 "
        ],
        "endswith": [
            "\u043f\u043a\u0441"
        ]
    },
    "ban": {
        "keywords": [
            "atas",
            "atas-teks",
            "atek",
            "batas",
            "batek",
            "bawah",
            "bawah-teks",
            "bing",
            "bingkai",
            "gada",
            "garis_dasar",
            "jempol",
            "jmpl",
            "ka",
            "kanan",
            "ki",
            "kiri",
            "lurus",
            "mini",
            "miniatur",
            "nir",
            "nirbing",
            "pus",
            "pusat",
            "tanpa",
            "tanpabingkai",
            "tegak",
            "tengah",
            "tepi",
            "upa"
        ],
        "params": [
            "al",
            "alternatif",
            "bhs",
            "hal",
            "halaman",
            "jempol",
            "jmpl",
            "lurus",
            "mini",
            "miniatur",
            "pra",
            "pranala",
            "tegak"
        ],
        "startswith": [
            "hal_",
            "halaman_",
            "lurus_",
            "tegak_"
        ]
    },
    "bar": {
        "keywords": [
            "gerahmt",
            "grundlinie",
            "hoch",
            "hochgestellt",
            "hochkant",
            "links",
            "mini",
            "miniatur",
            "mitte",
            "oben",
            "ohne",
            "rahmenlos",
            "rand",
            "rechts",
            "text-oben",
            "text-unten",
            "tief",
            "tiefgestellt",
            "unten",
            "zentriert"
        ],
        "params": [
            "alternativtext",
            "hochkant",
            "klasse",
            "mini",
            "miniatur",
            "seite",
            "sprache",
            "verweis"
        ],
        "startswith": [
            "hochkant ",
            "hochkant_",
            "seite ",
            "seite_"
        ]
    },
    "bat-smg": {
        "keywords": [
            "de\u0161in\u0117je",
            "kair\u0117je",
            "mini",
            "miniati\u016bra"
        ],
        "params": [
            "mini",
            "miniati\u016bra"
        ]
    },
    "bcl": {
        "keywords": [
            "daing kwadro",
            "kwadro",
            "may\u00f2",
            "nakakawadro",
            "sentro",
            "tang\u00e2",
            "too",
            "wala"
        ],
        "params": [
            "pahina"
        ],
        "startswith": [
            "pahina "
        ]
    },
    "be": {
        "keywords": [
            "\u0431\u0435\u0437\u0440\u0430\u043c\u043a\u0456",
            "\u0437\u043b\u0435\u0432\u0430",
            "\u043c\u0456\u043d\u0456",
            "\u043c\u0456\u043d\u0456\u044f\u0446\u044e\u0440\u0430",
            "\u043d\u044f\u043c\u0430",
            "\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0446\u044d\u043d\u0442\u0440"
        ],
        "params": [
            "\u043c\u0456\u043d\u0456",
            "\u043c\u0456\u043d\u0456\u044f\u0446\u044e\u0440\u0430"
        ],
        "endswith": [
            "\u043f\u043a\u0441"
        ]
    },
    "be-tarask": {
        "keywords": [
            "\u0431\u0435\u0437\u0440\u0430\u043c\u043a\u0456",
            "\u0437\u043b\u0435\u0432\u0430",
            "\u0437\u043d\u0430\u0447\u0430\u043a",
            "\u0437\u044c\u0432\u0435\u0440\u0445\u0443",
            "\u0437\u044c\u043b\u0435\u0432\u0430",
            "\u0437\u044c\u043d\u0456\u0437\u0443",
            "\u043c\u0456\u043d\u0456",
            "\u043c\u0456\u043d\u0456\u044f\u0446\u044e\u0440\u0430",
            "\u043d\u044f\u043c\u0430",
            "\u043f\u0430\u0441\u044f\u0440\u044d\u0434\u0437\u0456\u043d\u0435",
            "\u0440\u0430\u043c\u043a\u0430",
            "\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0446\u044d\u043d\u0442\u0430\u0440",
            "\u0446\u044d\u043d\u0442\u0440"
        ],
        "params": [
            "\u0437\u043d\u0430\u0447\u0430\u043a",
            "\u043c\u0456\u043d\u0456",
            "\u043c\u0456\u043d\u0456\u044f\u0446\u044e\u0440\u0430",
            "\u0441\u043f\u0430\u0441\u044b\u043b\u043a\u0430",
            "\u0441\u0442\u0430\u0440\u043e\u043d\u043a\u0430"
        ],
        "startswith": [
            "\u0441\u0442\u0430\u0440\u043e\u043d\u043a\u0430 "
        ],
        "endswith": [
            "\u043f\u043a\u0441"
        ]
    },
    "bg": {
        "keywords": [
            "\u0431\u0435\u0437\u0440\u0430\u043c\u043a\u0430",
            "\u0432\u0434\u044f\u0441\u043d\u043e",
            "\u0432\u043b\u044f\u0432\u043e",
            "\u0432\u0440\u0430\u043c\u043a\u0430",
            "\u0434",
            "\u0434\u044f\u0441\u043d\u043e",
            "\u043a\u043e\u043d\u0442\u0443\u0440",
            "\u043b",
            "\u043b\u044f\u0432\u043e",
            "\u043c\u0438\u043d\u0438",
            "\u043d",
            "\u0440\u0430\u043c\u043a\u0430",
            "\u0440\u044a\u0431",
            "\u0446",
            "\u0446\u0435\u043d\u0442\u0440",
            "\u0446\u0435\u043d\u0442\u044a\u0440"
        ],
        "params": [
            "\u043c\u0438\u043d\u0438"
        ],
        "endswith": [
            "\u043f",
            "\u043f\u043a\u0441"
        ]
    },
    "bjn": {
        "keywords": [
            "atas",
            "atas-teks",
            "atek",
            "batas",
            "batek",
            "bawah",
            "bawah-teks",
            "bing",
            "bingkai",
            "gada",
            "garis_dasar",
            "jempol",
            "jmpl",
            "ka",
            "kanan",
            "ki",
            "kiri",
            "lurus",
            "mini",
            "miniatur",
            "nir",
            "nirbing",
            "pus",
            "pusat",
            "tanpa",
            "tanpabingkai",
            "tegak",
            "tengah",
            "tepi",
            "upa"
        ],
        "params": [
            "al",
            "alternatif",
            "bhs",
            "hal",
            "halaman",
            "jempol",
            "jmpl",
            "lurus",
            "mini",
            "miniatur",
            "pra",
            "pranala",
            "tegak"
        ],
        "startswith": [
            "hal_",
            "halaman_",
            "lurus_",
            "tegak_"
        ]
    },
    "bm": {
        "keywords": [
            "bas",
            "bas-texte",
            "bas-txt",
            "base",
            "bordure",
            "cadre",
            "centr\u00e9",
            "droite",
            "encadre",
            "encadr\u00e9",
            "exp",
            "exposant",
            "gauche",
            "haut",
            "haut-texte",
            "haut-txt",
            "ind",
            "indice",
            "ligne-de-base",
            "milieu",
            "neant",
            "non_encadre",
            "non_encadr\u00e9",
            "n\u00e9ant",
            "redresse",
            "sans_cadre",
            "vignette"
        ],
        "params": [
            "classe",
            "langue",
            "lien",
            "redresse",
            "vignette"
        ],
        "startswith": [
            "redresse_"
        ]
    },
    "bn": {
        "keywords": [
            "\u0989\u09aa\u09b0",
            "\u0989\u09aa\u09b0\u09c7",
            "\u0995\u09bf\u099b\u09c1\u0987_\u09a8\u09be",
            "\u0995\u09bf\u099b\u09c1\u0987\u09a8\u09be",
            "\u0995\u09c7\u09a8\u09cd\u09a6\u09cd\u09b0",
            "\u0995\u09c7\u09a8\u09cd\u09a6\u09cd\u09b0\u09c7",
            "\u0995\u09cb\u09a8\u099f\u09bf_\u09a8\u09be",
            "\u0995\u09cb\u09a8\u099f\u09bf\u09a8\u09be",
            "\u09a1\u09be\u09a8",
            "\u09a1\u09be\u09a8\u09a6\u09bf\u0995\u09c7_\u0989\u09aa\u09b0\u09c7",
            "\u09a1\u09be\u09a8\u09c7",
            "\u09a1\u09be\u09a8\u09c7_\u0989\u09aa\u09b0\u09c7",
            "\u09a4\u09b2\u09a6\u09c7\u09b6",
            "\u09a5\u09be\u09ae\u09cd\u09ac",
            "\u09a5\u09be\u09ae\u09cd\u09ac\u09a8\u09c7\u0987\u09b2",
            "\u09a8\u09bf\u099a",
            "\u09a8\u09bf\u099a\u09c7",
            "\u09a8\u09bf\u09ae\u09cd\u09a8\u09c7",
            "\u09a8\u09c0\u099a",
            "\u09a8\u09c0\u099a\u09c7",
            "\u09aa\u09be\u09a0\u09cd\u09af-\u0989\u09aa\u09b0",
            "\u09aa\u09be\u09a0\u09cd\u09af-\u0989\u09aa\u09b0\u09c7",
            "\u09aa\u09be\u09a0\u09cd\u09af-\u09a8\u09c0\u099a\u09c7",
            "\u09ab\u09cd\u09b0\u09c7\u09ae",
            "\u09ab\u09cd\u09b0\u09c7\u09ae\u09ac\u09bf\u09b9\u09c0\u09a8",
            "\u09ab\u09cd\u09b0\u09c7\u09ae\u09b8\u09b9",
            "\u09ab\u09cd\u09b0\u09c7\u09ae\u09b9\u09c0\u09a8",
            "\u09ac\u09be\u09ae",
            "\u09ac\u09be\u09ae\u09c7",
            "\u09ae\u09a7\u09cd\u09af",
            "\u09ae\u09a7\u09cd\u09af\u09c7",
            "\u09b2\u09c7\u0996\u09be-\u0989\u09aa\u09b0",
            "\u09b2\u09c7\u0996\u09be-\u0989\u09aa\u09b0\u09c7",
            "\u09b2\u09c7\u0996\u09be-\u09a8\u09c0\u099a",
            "\u09b6\u09c0\u09b0\u09cd\u09b7",
            "\u09b6\u09c0\u09b0\u09cd\u09b7\u09c7",
            "\u09b8\u09c0\u09ae\u09be\u09a8\u09be",
            "\u09b8\u09c0\u09ae\u09be\u09a8\u09cd\u09a4"
        ],
        "params": [
            "\u0995\u09cd\u09b2\u09be\u09b8",
            "\u09a1\u09be\u09a8\u09a6\u09bf\u0995\u09c7_\u0989\u09aa\u09b0\u09c7",
            "\u09a1\u09be\u09a8\u09c7\u0989\u09aa\u09b0\u09c7",
            "\u09a5\u09be\u09ae\u09cd\u09ac",
            "\u09a5\u09be\u09ae\u09cd\u09ac\u09a8\u09c7\u0987\u09b2",
            "\u09aa\u09be\u09a4\u09be",
            "\u09aa\u09c3\u09b7\u09cd\u09a0\u09be",
            "\u09ad\u09be\u09b7\u09be",
            "\u09b2\u09bf\u0999\u09cd\u0995",
            "\u09b8\u0982\u09af\u09cb\u0997"
        ],
        "startswith": [
            "\u09a1\u09be\u09a8\u09a6\u09bf\u0995\u09c7_\u0989\u09aa\u09b0\u09c7 ",
            "\u09a1\u09be\u09a8\u09c7\u0989\u09aa\u09b0\u09c7 ",
            "\u09aa\u09be\u09a4\u09be ",
            "\u09aa\u09c3\u09b7\u09cd\u09a0\u09be "
        ],
        "endswith": [
            "\u09aa\u09bf\u0995\u09cd\u09b8",
            "\u09aa\u09bf\u0995\u09cd\u09b8\u09c7\u09b2"
        ]
    },
    "bpy": {
        "keywords": [
            "\u0989\u09aa\u09b0",
            "\u0989\u09aa\u09b0\u09c7",
            "\u0995\u09bf\u099b\u09c1\u0987_\u09a8\u09be",
            "\u0995\u09bf\u099b\u09c1\u0987\u09a8\u09be",
            "\u0995\u09c7\u09a8\u09cd\u09a6\u09cd\u09b0",
            "\u0995\u09c7\u09a8\u09cd\u09a6\u09cd\u09b0\u09c7",
            "\u0995\u09cb\u09a8\u099f\u09bf_\u09a8\u09be",
            "\u0995\u09cb\u09a8\u099f\u09bf\u09a8\u09be",
            "\u09a1\u09be\u09a8",
            "\u09a1\u09be\u09a8\u09a6\u09bf\u0995\u09c7_\u0989\u09aa\u09b0\u09c7",
            "\u09a1\u09be\u09a8\u09c7",
            "\u09a1\u09be\u09a8\u09c7_\u0989\u09aa\u09b0\u09c7",
            "\u09a4\u09b2\u09a6\u09c7\u09b6",
            "\u09a5\u09be\u09ae\u09cd\u09ac",
            "\u09a5\u09be\u09ae\u09cd\u09ac\u09a8\u09c7\u0987\u09b2",
            "\u09a8\u09bf\u099a",
            "\u09a8\u09bf\u099a\u09c7",
            "\u09a8\u09bf\u09ae\u09cd\u09a8\u09c7",
            "\u09a8\u09c0\u099a",
            "\u09a8\u09c0\u099a\u09c7",
            "\u09aa\u09be\u09a0\u09cd\u09af-\u0989\u09aa\u09b0",
            "\u09aa\u09be\u09a0\u09cd\u09af-\u0989\u09aa\u09b0\u09c7",
            "\u09aa\u09be\u09a0\u09cd\u09af-\u09a8\u09c0\u099a\u09c7",
            "\u09ab\u09cd\u09b0\u09c7\u09ae",
            "\u09ab\u09cd\u09b0\u09c7\u09ae\u09ac\u09bf\u09b9\u09c0\u09a8",
            "\u09ab\u09cd\u09b0\u09c7\u09ae\u09b8\u09b9",
            "\u09ab\u09cd\u09b0\u09c7\u09ae\u09b9\u09c0\u09a8",
            "\u09ac\u09be\u09ae",
            "\u09ac\u09be\u09ae\u09c7",
            "\u09ae\u09a7\u09cd\u09af",
            "\u09ae\u09a7\u09cd\u09af\u09c7",
            "\u09b2\u09c7\u0996\u09be-\u0989\u09aa\u09b0",
            "\u09b2\u09c7\u0996\u09be-\u0989\u09aa\u09b0\u09c7",
            "\u09b2\u09c7\u0996\u09be-\u09a8\u09c0\u099a",
            "\u09b6\u09c0\u09b0\u09cd\u09b7",
            "\u09b6\u09c0\u09b0\u09cd\u09b7\u09c7",
            "\u09b8\u09c0\u09ae\u09be\u09a8\u09be",
            "\u09b8\u09c0\u09ae\u09be\u09a8\u09cd\u09a4"
        ],
        "params": [
            "\u0995\u09cd\u09b2\u09be\u09b8",
            "\u09a1\u09be\u09a8\u09a6\u09bf\u0995\u09c7_\u0989\u09aa\u09b0\u09c7",
            "\u09a1\u09be\u09a8\u09c7\u0989\u09aa\u09b0\u09c7",
            "\u09a5\u09be\u09ae\u09cd\u09ac",
            "\u09a5\u09be\u09ae\u09cd\u09ac\u09a8\u09c7\u0987\u09b2",
            "\u09aa\u09be\u09a4\u09be",
            "\u09aa\u09c3\u09b7\u09cd\u09a0\u09be",
            "\u09ad\u09be\u09b7\u09be",
            "\u09b2\u09bf\u0999\u09cd\u0995",
            "\u09b8\u0982\u09af\u09cb\u0997"
        ],
        "startswith": [
            "\u09a1\u09be\u09a8\u09a6\u09bf\u0995\u09c7_\u0989\u09aa\u09b0\u09c7 ",
            "\u09a1\u09be\u09a8\u09c7\u0989\u09aa\u09b0\u09c7 ",
            "\u09aa\u09be\u09a4\u09be ",
            "\u09aa\u09c3\u09b7\u09cd\u09a0\u09be "
        ],
        "endswith": [
            "\u09aa\u09bf\u0995\u09cd\u09b8",
            "\u09aa\u09bf\u0995\u09cd\u09b8\u09c7\u09b2"
        ]
    },
    "br": {
        "keywords": [
            "dehou",
            "is",
            "kleiz",
            "krec'h",
            "kreiz",
            "kreizenn",
            "netra",
            "trao\u00f1"
        ],
        "params": [
            "liamm",
            "pajenn"
        ],
        "startswith": [
            "pajenn "
        ]
    },
    "bs": {
        "keywords": [
            "bez",
            "bez_okvira",
            "c",
            "centar",
            "d",
            "desno",
            "dugme",
            "granica",
            "ivica",
            "l",
            "lijevo",
            "mini",
            "n",
            "na_gore",
            "odjeljak",
            "okvir",
            "pocetna_linija",
            "po\u010detna_linija",
            "ram",
            "sredina",
            "tekst-dugme",
            "vrh",
            "vrh_teksta"
        ],
        "params": [
            "mini",
            "na_gore",
            "stranica"
        ],
        "startswith": [
            "na_gore_",
            "stranica "
        ],
        "endswith": [
            "p",
            "piksel"
        ]
    },
    "bug": {
        "keywords": [
            "atas",
            "atas-teks",
            "atek",
            "batas",
            "batek",
            "bawah",
            "bawah-teks",
            "bing",
            "bingkai",
            "gada",
            "garis_dasar",
            "jempol",
            "jmpl",
            "ka",
            "kanan",
            "ki",
            "kiri",
            "lurus",
            "mini",
            "miniatur",
            "nir",
            "nirbing",
            "pus",
            "pusat",
            "tanpa",
            "tanpabingkai",
            "tegak",
            "tengah",
            "tepi",
            "upa"
        ],
        "params": [
            "al",
            "alternatif",
            "bhs",
            "hal",
            "halaman",
            "jempol",
            "jmpl",
            "lurus",
            "mini",
            "miniatur",
            "pra",
            "pranala",
            "tegak"
        ],
        "startswith": [
            "hal_",
            "halaman_",
            "lurus_",
            "tegak_"
        ]
    },
    "bxr": {
        "keywords": [
            "\u0431\u0435\u0437",
            "\u0431\u0435\u0437\u0440\u0430\u043c\u043a\u0438",
            "\u0433\u0440\u0430\u043d\u0438\u0446\u0430",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u043d\u0430\u0434",
            "\u043e\u0431\u0440\u0430\u043c\u0438\u0442\u044c",
            "\u043e\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u0435",
            "\u043f\u043e\u0434",
            "\u043f\u043e\u0441\u0435\u0440\u0435\u0434\u0438\u043d\u0435",
            "\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u043b\u0435\u0432\u0430",
            "\u0441\u043d\u0438\u0437\u0443",
            "\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u043d\u0438\u0437\u0443",
            "\u0446\u0435\u043d\u0442\u0440"
        ],
        "params": [
            "\u0430\u043b\u044c\u0442",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u0441\u044b\u043b\u043a\u0430",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430"
        ],
        "startswith": [
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430 ",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430 "
        ],
        "endswith": [
            "\u043f\u043a\u0441"
        ]
    },
    "ca": {
        "keywords": [
            "baix",
            "baix-text",
            "bas",
            "bas-txt",
            "bas-t\u00e8xte",
            "bordadura",
            "cap",
            "centrat",
            "dalt",
            "dalt-text",
            "drecha",
            "dreta",
            "enquagrat",
            "esquerra",
            "esqu\u00e8rra",
            "exp",
            "gaucha",
            "ind",
            "indici",
            "linha_de_basa",
            "l\u00ednia de base",
            "marc",
            "miniatura",
            "mitan",
            "mitj\u00e0",
            "naut",
            "naut-txt",
            "naut-t\u00e8xte",
            "neant",
            "nonr\u00e9s",
            "quadre",
            "redre\u00e7a",
            "redre\u00e7at",
            "sens_quadre",
            "sense marc",
            "sen\u00e8stra",
            "vinheta",
            "vora"
        ],
        "params": [
            "enlla\u00e7",
            "idioma",
            "ligam",
            "llengua",
            "miniatura",
            "p\u00e0gina",
            "redre\u00e7at",
            "vinheta"
        ],
        "startswith": [
            "p\u00e0gina ",
            "redre\u00e7a",
            "redre\u00e7a ",
            "redre\u00e7at "
        ]
    },
    "cbk-zam": {
        "keywords": [
            "abajo",
            "arriba",
            "borde",
            "centrada",
            "centrado",
            "centrar",
            "centro",
            "dcha",
            "der",
            "derecha",
            "enmarcada",
            "enmarcado",
            "izda",
            "izq",
            "izquierda",
            "marco",
            "medio",
            "mini",
            "miniatura",
            "miniaturadeimagen",
            "nada",
            "ninguna",
            "ninguno",
            "no",
            "sin_enmarcar",
            "sinenmarcar",
            "sinmarco"
        ],
        "params": [
            "enlace",
            "idioma",
            "miniatura",
            "miniaturadeimagen",
            "pagina",
            "p\u00e1gina",
            "vinculo",
            "v\u00ednculo"
        ],
        "startswith": [
            "pagina_",
            "p\u00e1gina_"
        ]
    },
    "cdo": {
        "keywords": [
            "\u4e0a\u6a19",
            "\u4e0b\u6a19",
            "\u4e2d\u95f4",
            "\u53f3",
            "\u53f3\u4e0a",
            "\u5782\u76f4\u7f6e\u4e2d",
            "\u5782\u76f4\u7f6e\u5e95",
            "\u5782\u76f4\u7f6e\u9802",
            "\u57fa\u7ebf",
            "\u5b50",
            "\u5c45\u4e2d",
            "\u5de6",
            "\u5e95\u90e8",
            "\u6587\u5b57\u5e95\u90e8",
            "\u6587\u5b57\u7f6e\u5e95",
            "\u6587\u5b57\u7f6e\u9802",
            "\u6587\u5b57\u9876\u90e8",
            "\u65e0",
            "\u65e0\u6846",
            "\u66ff\u4ee3\u6587\u5b57",
            "\u6709\u6846",
            "\u7121",
            "\u7121\u6846",
            "\u7e2e\u5716",
            "\u7f29\u7565\u56fe",
            "\u7f6e\u4e2d",
            "\u8d85",
            "\u8fb9\u6846",
            "\u908a\u6846",
            "\u9876\u90e8"
        ],
        "params": [
            "\u53f3\u4e0a",
            "\u66ff\u4ee3",
            "\u66ff\u4ee3\u6587\u672c",
            "\u7c7b",
            "\u7e2e\u5716",
            "\u7f29\u7565\u56fe",
            "\u8a9e\u8a00",
            "\u8bed\u8a00",
            "\u9023\u7d50",
            "\u94fe\u63a5",
            "\u9801",
            "\u985e\u5225",
            "\u9875\u6570"
        ],
        "startswith": [
            "\u53f3\u4e0a"
        ],
        "endswith": [
            "\u50cf\u7d20",
            "\u9801",
            "\u9875"
        ]
    },
    "ce": {
        "keywords": [
            "\u0431\u0430\u043a\u044a\u0445\u044c\u0430",
            "\u0431\u0430\u043a\u044a\u0445\u044c\u0430\u043b\u0430\u043a\u0445\u043e",
            "\u0431\u0435\u0437",
            "\u0431\u0435\u0437\u0440\u0430\u043c\u043a\u0438",
            "\u0431\u0443\u0445",
            "\u0431\u0443\u0445\u0430",
            "\u0431\u0443\u0445\u0430\u0440",
            "\u0431\u0443\u0445\u0430\u0440\u0430-\u0439\u043e\u0437\u0430",
            "\u0433\u0440\u0430\u043d\u0438\u0446\u0430",
            "\u0433\u0443\u0440\u0430\u0431\u0435",
            "\u0433\u0443\u0440\u0430\u0431\u043e\u0446\u0430\u0448",
            "\u0434\u043e\u0437\u0430",
            "\u0436\u0438\u043c\u0430",
            "\u0436\u0438\u043c\u043e",
            "\u0439\u043e\u0446\u0443\u0448",
            "\u043b\u0430\u043a\u0445\u0430\u0445\u044c",
            "\u043b\u0430\u043a\u0445\u0445\u044c\u0430\u0440\u0430-\u0439\u043e\u0437\u0430",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u043d\u0430\u0434",
            "\u043e\u0431\u0440\u0430\u043c\u0438\u0442\u044c",
            "\u043e\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u0435",
            "\u043f\u043e\u0434",
            "\u043f\u043e\u0441\u0435\u0440\u0435\u0434\u0438\u043d\u0435",
            "\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u043b\u0435\u0432\u0430",
            "\u0441\u043d\u0438\u0437\u0443",
            "\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u043d\u0438\u0437\u0443",
            "\u0442\u04c0\u0435",
            "\u0445\u0430\u0440\u0446\u0445\u044c\u0430",
            "\u0446\u0435\u043d\u0442\u0440",
            "\u044e\u043a\u043a\u044a",
            "\u044e\u043a\u043a\u044a\u0435"
        ],
        "params": [
            "\u0430\u0433l\u043e",
            "\u0430\u043b\u044c\u0442",
            "\u0431\u0430\u043a\u044a\u0445\u044c\u0430\u043b\u0430\u043a\u0445\u043e",
            "\u0436\u0438\u043c\u0430",
            "\u0436\u0438\u043c\u043e",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u0441\u044b\u043b\u043a\u0430",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430",
            "\u0445\u044c\u0430\u0436\u043e\u0440\u0433"
        ],
        "startswith": [
            "page_",
            "upright_",
            "\u0430\u0433l\u043e_",
            "\u0431\u0430\u043a\u044a\u0445\u044c\u0430\u043b\u0430\u043a\u0445\u043e_",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430 ",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430_",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430 ",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430_"
        ],
        "endswith": [
            "\u043f\u043a\u0441"
        ]
    },
    "ckb": {
        "keywords": [
            "\u0628\u06ce\u0686\u0648\u0627\u0631\u0686\u06ce\u0648\u06d5",
            "\u0633\u0646\u0648\u0648\u0631",
            "\u0646\u0627\u0648\u06d5\u0695\u0627\u0633\u062a",
            "\u0648\u06ce\u0646\u06c6\u06a9",
            "\u0686\u0648\u0627\u0631\u0686\u06ce\u0648\u06d5",
            "\u0686\u06d5\u067e",
            "\u0695\u0627\u0633\u062a"
        ],
        "endswith": [
            "\u067e\u06cc\u06a9\u0633\u06b5"
        ]
    },
    "co": {
        "keywords": [
            "bordo",
            "centro",
            "destra",
            "incorniciato",
            "met\u00e0",
            "min",
            "miniatura",
            "nessuno",
            "originale",
            "pedice",
            "riquadrato",
            "senza_cornice",
            "sinistra",
            "sopra",
            "sotto",
            "testo-sopra",
            "testo-sotto",
            "verticale"
        ],
        "params": [
            "min",
            "miniatura",
            "pagina",
            "verticale"
        ],
        "startswith": [
            "pagina_",
            "verticale_"
        ]
    },
    "cs": {
        "keywords": [
            "bezr\u00e1mu",
            "n\u00e1hled",
            "n\u00e1h\u013ead",
            "n\u00e1h\u013eadobr\u00e1zka",
            "okraj",
            "r\u00e1m",
            "stred",
            "st\u0159ed",
            "vlevo",
            "vpravo",
            "v\u013eavo",
            "\u017eiadny",
            "\u017e\u00e1dn\u00e9"
        ],
        "params": [
            "jazyk",
            "n\u00e1hled",
            "odkaz",
            "strana",
            "t\u0159\u00edda"
        ],
        "startswith": [
            "strana_"
        ],
        "endswith": [
            "bod",
            "pixel\u016f"
        ]
    },
    "csb": {
        "keywords": [
            "bez_ramki",
            "bezramki",
            "brak",
            "centruj",
            "d\u00f3\u0142",
            "g\u00f3ra",
            "lewo",
            "ma\u0142y",
            "prawo",
            "ramka",
            "t\u0142o",
            "\u015brodek"
        ],
        "params": [
            "ma\u0142y",
            "strona"
        ]
    },
    "cv": {
        "keywords": [
            "\u0431\u0435\u0437",
            "\u0431\u0435\u0437\u0440\u0430\u043c\u043a\u0438",
            "\u0433\u0440\u0430\u043d\u0438\u0446\u0430",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u043d\u0430\u0434",
            "\u043e\u0431\u0440\u0430\u043c\u0438\u0442\u044c",
            "\u043e\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u0435",
            "\u043f\u043e\u0434",
            "\u043f\u043e\u0441\u0435\u0440\u0435\u0434\u0438\u043d\u0435",
            "\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u043b\u0435\u0432\u0430",
            "\u0441\u043d\u0438\u0437\u0443",
            "\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u043d\u0438\u0437\u0443",
            "\u0446\u0435\u043d\u0442\u0440"
        ],
        "params": [
            "\u0430\u043b\u044c\u0442",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u0441\u044b\u043b\u043a\u0430",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430"
        ],
        "startswith": [
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430 ",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430 "
        ],
        "endswith": [
            "\u043f\u043a\u0441"
        ]
    },
    "cy": {
        "keywords": [
            "bawd",
            "brig",
            "canol",
            "chwith",
            "de",
            "dim",
            "ewin_bawd",
            "godre",
            "gwaelod",
            "is",
            "m\u00e2n-lun",
            "unionsyth",
            "uwch"
        ],
        "params": [
            "bawd",
            "m\u00e2n-lun",
            "tudalen",
            "unionsyth"
        ],
        "startswith": [
            "tudalen_",
            "unionsyth_"
        ]
    },
    "de": {
        "keywords": [
            "gerahmt",
            "grundlinie",
            "hoch",
            "hochgestellt",
            "hochkant",
            "links",
            "mini",
            "miniatur",
            "mitte",
            "oben",
            "ohne",
            "rahmenlos",
            "rand",
            "rechts",
            "text-oben",
            "text-unten",
            "tief",
            "tiefgestellt",
            "unten",
            "zentriert"
        ],
        "params": [
            "alternativtext",
            "hochkant",
            "klasse",
            "mini",
            "miniatur",
            "seite",
            "sprache",
            "verweis"
        ],
        "startswith": [
            "hochkant ",
            "hochkant_",
            "seite ",
            "seite_"
        ]
    },
    "diq": {
        "keywords": [
            "Sinor\u00e9erdi",
            "anvar",
            "b\u00e9\u00e7er\u00e7ewe",
            "cor",
            "cor\u00e9n",
            "disleg",
            "erd",
            "erd-metin",
            "gedug",
            "gedug-metin",
            "merkez",
            "miyan",
            "q\u0131ckek",
            "ra\u015ft",
            "resmoq\u0131ckek",
            "sinor",
            "werte",
            "\u00e7ep",
            "\u00e7er\u00e7ewe",
            "\u00e7er\u00e7ewekerden",
            "\u00e7er\u00e7ewey\u0131n",
            "\u00e7\u0131niyo"
        ],
        "params": [
            "disleg",
            "gre",
            "klik",
            "pera",
            "q\u0131ckek",
            "resmoq\u0131ckek",
            "s\u0131n\u0131f",
            "zuwan"
        ],
        "startswith": [
            "disleg_",
            "pera_"
        ],
        "endswith": [
            "pik",
            "piksel"
        ]
    },
    "dsb": {
        "keywords": [
            "gerahmt",
            "grundlinie",
            "hoch",
            "hochgestellt",
            "hochkant",
            "links",
            "mini",
            "miniatur",
            "mitte",
            "oben",
            "ohne",
            "rahmenlos",
            "rand",
            "rechts",
            "text-oben",
            "text-unten",
            "tief",
            "tiefgestellt",
            "unten",
            "zentriert"
        ],
        "params": [
            "alternativtext",
            "hochkant",
            "klasse",
            "mini",
            "miniatur",
            "seite",
            "sprache",
            "verweis"
        ],
        "startswith": [
            "hochkant ",
            "hochkant_",
            "seite ",
            "seite_"
        ]
    },
    "el": {
        "keywords": [
            "\u03ac\u03bd\u03c9",
            "\u03b1\u03c1\u03b9\u03c3\u03c4\u03b5\u03c1\u03ac",
            "\u03b3\u03c1\u03b1\u03bc\u03bc\u03ae\u03b2\u03ac\u03c3\u03b7\u03c2",
            "\u03b4\u03b5\u03af\u03ba\u03c4\u03b7\u03c2",
            "\u03b4\u03b5\u03be\u03b9\u03ac",
            "\u03b5\u03ba\u03b8\u03ad\u03c4\u03b7\u03c2",
            "\u03ba\u03ac\u03c4\u03c9",
            "\u03ba\u03ac\u03c4\u03c9-\u03b1\u03c0\u03cc-\u03c4\u03bf-\u03ba\u03b5\u03af\u03bc\u03b5\u03bd\u03bf",
            "\u03ba\u03ad\u03bd\u03c4\u03c1\u03bf",
            "\u03ba\u03b1\u03b8\u03cc\u03bb\u03bf\u03c5",
            "\u03ba\u03b1\u03c4\u03b1\u03ba\u03cc\u03c1\u03c5\u03c6\u03b1",
            "\u03bc\u03ad\u03c3\u03bf",
            "\u03bc\u03b5-\u03c0\u03bb\u03b1\u03af\u03c3\u03b9\u03bf",
            "\u03bc\u03b9\u03ba\u03c1\u03bf\u03b3\u03c1\u03b1\u03c6\u03af\u03b1",
            "\u03bc\u03b9\u03bd\u03b9\u03b1\u03c4\u03bf\u03cd\u03c1\u03b1",
            "\u03c0\u03ac\u03bd\u03c9-\u03b1\u03c0\u03cc-\u03c4\u03bf-\u03ba\u03b5\u03af\u03bc\u03b5\u03bd\u03bf",
            "\u03c0\u03bb\u03b1\u03af\u03c3\u03b9\u03bf",
            "\u03c7\u03c9\u03c1\u03af\u03c2-\u03c0\u03bb\u03b1\u03af\u03c3\u03b9\u03bf"
        ],
        "params": [
            "\u03b5\u03bd\u03b1\u03bb\u03bb.",
            "\u03ba\u03b1\u03c4\u03b1\u03ba\u03cc\u03c1\u03c5\u03c6\u03b1",
            "\u03bc\u03b9\u03ba\u03c1\u03bf\u03b3\u03c1\u03b1\u03c6\u03af\u03b1",
            "\u03bc\u03b9\u03bd\u03b9\u03b1\u03c4\u03bf\u03cd\u03c1\u03b1",
            "\u03c3\u03b5\u03bb\u03af\u03b4\u03b1",
            "\u03c3\u03cd\u03bd\u03b4\u03b5\u03c3\u03bc\u03bf\u03c2"
        ],
        "startswith": [
            "\u03ba\u03b1\u03c4\u03b1\u03ba\u03cc\u03c1\u03c5\u03c6\u03b1_",
            "\u03c3\u03b5\u03bb\u03af\u03b4\u03b1_"
        ],
        "endswith": [
            "\u03b5\u03c3"
        ]
    },
    "eml": {
        "keywords": [
            "bordo",
            "centro",
            "destra",
            "incorniciato",
            "met\u00e0",
            "min",
            "miniatura",
            "nessuno",
            "originale",
            "pedice",
            "riquadrato",
            "senza_cornice",
            "sinistra",
            "sopra",
            "sotto",
            "testo-sopra",
            "testo-sotto",
            "verticale"
        ],
        "params": [
            "min",
            "miniatura",
            "pagina",
            "verticale"
        ],
        "startswith": [
            "pagina_",
            "verticale_"
        ]
    },
    "eo": {
        "keywords": [
            "altdekstre",
            "alte",
            "centra",
            "dekstra",
            "dekstre",
            "enkadrita",
            "enkadrite",
            "eta",
            "kadra",
            "kadrigita",
            "kadrigite",
            "kadrita",
            "kadrite",
            "kadro",
            "malalte",
            "maldekstra",
            "maldekstre",
            "malsube",
            "malsupre",
            "meza",
            "meze",
            "nenio",
            "neniu",
            "senkadra",
            "suba-teksto",
            "sube",
            "supre",
            "tekst-alte"
        ],
        "params": [
            "altdekstre",
            "alternative",
            "eta",
            "klaso",
            "ligilo",
            "pagxo",
            "pa\u011do"
        ],
        "startswith": [
            "altdekstre_",
            "pagxo_",
            "pa\u011do "
        ],
        "endswith": [
            "ra"
        ]
    },
    "es": {
        "keywords": [
            "abajo",
            "arriba",
            "borde",
            "centrada",
            "centrado",
            "centrar",
            "centro",
            "dcha",
            "der",
            "derecha",
            "enmarcada",
            "enmarcado",
            "izda",
            "izq",
            "izquierda",
            "marco",
            "medio",
            "mini",
            "miniatura",
            "miniaturadeimagen",
            "nada",
            "ninguna",
            "ninguno",
            "no",
            "sin_enmarcar",
            "sinenmarcar",
            "sinmarco"
        ],
        "params": [
            "enlace",
            "idioma",
            "miniatura",
            "miniaturadeimagen",
            "pagina",
            "p\u00e1gina",
            "vinculo",
            "v\u00ednculo"
        ],
        "startswith": [
            "pagina_",
            "p\u00e1gina_"
        ]
    },
    "et": {
        "keywords": [
            "keskel",
            "paremal",
            "pisi",
            "pisipilt",
            "p\u00fcsti",
            "raam",
            "raamita",
            "t\u00fchi",
            "vasakul",
            "\u00e4\u00e4ris"
        ],
        "params": [
            "keel",
            "lehek\u00fclg",
            "pisi",
            "pisipilt",
            "p\u00fcsti"
        ],
        "startswith": [
            "lehek\u00fclg_"
        ]
    },
    "eu": {
        "keywords": [
            "erdian",
            "eskuinera",
            "ezkerrera"
        ]
    },
    "ext": {
        "keywords": [
            "abajo",
            "arriba",
            "borde",
            "centrada",
            "centrado",
            "centrar",
            "centro",
            "dcha",
            "der",
            "derecha",
            "enmarcada",
            "enmarcado",
            "izda",
            "izq",
            "izquierda",
            "marco",
            "medio",
            "mini",
            "miniatura",
            "miniaturadeimagen",
            "nada",
            "ninguna",
            "ninguno",
            "no",
            "sin_enmarcar",
            "sinenmarcar",
            "sinmarco"
        ],
        "params": [
            "enlace",
            "idioma",
            "miniatura",
            "miniaturadeimagen",
            "pagina",
            "p\u00e1gina",
            "vinculo",
            "v\u00ednculo"
        ],
        "startswith": [
            "pagina_",
            "p\u00e1gina_"
        ]
    },
    "fa": {
        "keywords": [
            "\u0627\u0646\u06af\u0634\u062a\u062f\u0627\u0646",
            "\u0627\u0646\u06af\u0634\u062a\u06cc",
            "\u0627\u06cc\u0633\u062a\u0627\u062f\u0647",
            "\u0628\u0627\u0644\u0627",
            "\u0628\u0646\u062f\u0627\u0646\u06af\u0634\u062a\u06cc",
            "\u0628\u06cc_\u0642\u0627\u0628",
            "\u0628\u06cc\u0642\u0627\u0628",
            "\u0628\u06cc\u200c\u0642\u0627\u0628",
            "\u062d\u0627\u0634\u06cc\u0647",
            "\u0631\u0627\u0633\u062a",
            "\u0632\u0628\u0631",
            "\u0632\u06cc\u0631",
            "\u0642\u0627\u0628",
            "\u0645\u062a\u0646-\u0628\u0627\u0644\u0627",
            "\u0645\u062a\u0646-\u067e\u0627\u06cc\u06cc\u0646",
            "\u0645\u06cc\u0627\u0646\u0647",
            "\u0647\u0645\u06a9\u0641",
            "\u0647\u06cc\u0686",
            "\u0648\u0633\u0637",
            "\u067e\u0627\u06cc\u06cc\u0646",
            "\u0686\u067e"
        ],
        "params": [
            "\u0627\u0646\u06af\u0634\u062a\u062f\u0627\u0646",
            "\u0627\u0646\u06af\u0634\u062a\u06cc",
            "\u0627\u06cc\u0633\u062a\u0627\u062f\u0647",
            "\u0628\u0646\u062f\u0627\u0646\u06af\u0634\u062a\u06cc",
            "\u062c\u0627\u06cc\u06af\u0632\u06cc\u0646",
            "\u0632\u0628\u0627\u0646",
            "\u0635\u0641\u062d\u0647",
            "\u067e\u06cc\u0648\u0646\u062f",
            "\u06a9\u0644\u0627\u0633"
        ],
        "startswith": [
            "\u0627\u06cc\u0633\u062a\u0627\u062f\u0647_",
            "\u0635\u0641\u062d\u0647_"
        ],
        "endswith": [
            "\u067e\u06cc\u06a9\u0633\u0644"
        ]
    },
    "fi": {
        "keywords": [
            "alaindeksi",
            "alas",
            "alhaalla",
            "kehykset\u00f6n",
            "kehys",
            "kehystetty",
            "keskell\u00e4",
            "keski",
            "keskitetty",
            "oikea",
            "perustaso",
            "pienois",
            "pienoiskuva",
            "pysty",
            "reunus",
            "tyhj\u00e4",
            "vasen",
            "ylh\u00e4\u00e4ll\u00e4",
            "yl\u00e4indeksi",
            "yl\u00e4oikea",
            "yl\u00f6s"
        ],
        "params": [
            "linkki",
            "pienois",
            "pienoiskuva",
            "pysty",
            "sivu",
            "yl\u00e4oikea"
        ],
        "startswith": [
            "pysty_",
            "sivu_",
            "yl\u00e4oikea_"
        ]
    },
    "fiu-vro": {
        "keywords": [
            "keskel",
            "paremal",
            "pisi",
            "pisipilt",
            "p\u00fcsti",
            "raam",
            "raamita",
            "t\u00fchi",
            "vasakul",
            "\u00e4\u00e4ris"
        ],
        "params": [
            "keel",
            "lehek\u00fclg",
            "pisi",
            "pisipilt",
            "p\u00fcsti"
        ],
        "startswith": [
            "lehek\u00fclg_"
        ]
    },
    "fr": {
        "keywords": [
            "bas",
            "bas-texte",
            "bas-txt",
            "base",
            "bordure",
            "cadre",
            "centr\u00e9",
            "droite",
            "encadre",
            "encadr\u00e9",
            "exp",
            "exposant",
            "gauche",
            "haut",
            "haut-texte",
            "haut-txt",
            "ind",
            "indice",
            "ligne-de-base",
            "milieu",
            "neant",
            "non_encadre",
            "non_encadr\u00e9",
            "n\u00e9ant",
            "redresse",
            "sans_cadre",
            "vignette"
        ],
        "params": [
            "classe",
            "langue",
            "lien",
            "redresse",
            "vignette"
        ],
        "startswith": [
            "redresse_"
        ]
    },
    "frp": {
        "keywords": [
            "bas",
            "bas-texte",
            "bas-txt",
            "base",
            "bordura",
            "bordure",
            "cadre",
            "centr\u00e2",
            "centr\u00e9",
            "c\u00e2dro",
            "d'amont",
            "d'av\u00e2l",
            "droite",
            "dr\u00eat",
            "dr\u00eata",
            "encadre",
            "encadr\u00e9",
            "enc\u00e2dr\u00e2",
            "entre-mi\u00e9",
            "exp",
            "exposant",
            "figura",
            "gauche",
            "g\u00f4che",
            "haut",
            "haut-texte",
            "haut-txt",
            "ind",
            "indice",
            "legne_de_b\u00e2sa",
            "ligne-de-base",
            "ligne_de_base",
            "milieu",
            "neant",
            "non_encadre",
            "non_encadr\u00e9",
            "n\u00e9ant",
            "pas_enc\u00e2dr\u00e2",
            "redresse",
            "sans_cadre",
            "segno",
            "sen_c\u00e2dro",
            "t\u00e8xto-d'amont",
            "t\u00e8xto-d'av\u00e2l",
            "vignette",
            "vouedo",
            "\u00e8xp",
            "\u00e8xposent"
        ],
        "params": [
            "classe",
            "dr\u00eat",
            "figura",
            "langue",
            "lien",
            "lim",
            "p\u00e2ge",
            "redresse",
            "vignette"
        ],
        "startswith": [
            "dr\u00eat ",
            "p\u00e2ge ",
            "redresse ",
            "redresse_"
        ]
    },
    "frr": {
        "keywords": [
            "gerahmt",
            "grundlinie",
            "hoch",
            "hochgestellt",
            "hochkant",
            "links",
            "mini",
            "miniatur",
            "mitte",
            "oben",
            "ohne",
            "rahmenlos",
            "rand",
            "rechts",
            "text-oben",
            "text-unten",
            "tief",
            "tiefgestellt",
            "unten",
            "zentriert"
        ],
        "params": [
            "alternativtext",
            "hochkant",
            "klasse",
            "mini",
            "miniatur",
            "seite",
            "sprache",
            "verweis"
        ],
        "startswith": [
            "hochkant ",
            "hochkant_",
            "seite ",
            "seite_"
        ]
    },
    "fur": {
        "keywords": [
            "bordo",
            "centro",
            "destra",
            "incorniciato",
            "met\u00e0",
            "min",
            "miniatura",
            "nessuno",
            "originale",
            "pedice",
            "riquadrato",
            "senza_cornice",
            "sinistra",
            "sopra",
            "sotto",
            "testo-sopra",
            "testo-sotto",
            "verticale"
        ],
        "params": [
            "min",
            "miniatura",
            "pagina",
            "verticale"
        ],
        "startswith": [
            "pagina_",
            "verticale_"
        ]
    },
    "ga": {
        "keywords": [
            "cl\u00e9",
            "deas",
            "faic",
            "fr\u00e1ma",
            "fr\u00e1maithe",
            "l\u00e1r",
            "mion",
            "mionsamhail"
        ]
    },
    "gag": {
        "keywords": [
            "alt",
            "alt\u00e7izgi",
            "dikey",
            "k\u00fc\u00e7\u00fck",
            "k\u00fc\u00e7\u00fckresim",
            "merkez",
            "metin-taban",
            "metin-tavan",
            "metin-tepe",
            "orta",
            "sa\u011f",
            "sol",
            "s\u0131n\u0131r",
            "taban",
            "taban\u00e7izgisi",
            "tavan",
            "tepe",
            "yok",
            "\u00e7er\u00e7eve",
            "\u00e7er\u00e7eveli",
            "\u00e7er\u00e7evesiz",
            "\u00fcs",
            "\u00fcst"
        ],
        "params": [
            "ba\u011flant\u0131",
            "dikey",
            "k\u00fc\u00e7\u00fck",
            "k\u00fc\u00e7\u00fckresim",
            "sayfa",
            "s\u0131n\u0131f"
        ],
        "startswith": [
            "dikey ",
            "sayfa "
        ],
        "endswith": [
            "pik",
            "piksel"
        ]
    },
    "gan": {
        "keywords": [
            "\u4e0a\u6a19",
            "\u4e0b\u6a19",
            "\u4e2d\u95f4",
            "\u53f3",
            "\u53f3\u4e0a",
            "\u5782\u76f4\u7f6e\u4e2d",
            "\u5782\u76f4\u7f6e\u5e95",
            "\u5782\u76f4\u7f6e\u9802",
            "\u57fa\u7ebf",
            "\u5b50",
            "\u5c45\u4e2d",
            "\u5de6",
            "\u5e95\u90e8",
            "\u6587\u5b57\u5e95\u90e8",
            "\u6587\u5b57\u7f6e\u5e95",
            "\u6587\u5b57\u7f6e\u9802",
            "\u6587\u5b57\u9876\u90e8",
            "\u65e0",
            "\u65e0\u6846",
            "\u66ff\u4ee3\u6587\u5b57",
            "\u6709\u6846",
            "\u7121",
            "\u7121\u6846",
            "\u7e2e\u5716",
            "\u7f29\u7565\u56fe",
            "\u7f6e\u4e2d",
            "\u8d85",
            "\u8fb9\u6846",
            "\u908a\u6846",
            "\u9876\u90e8"
        ],
        "params": [
            "\u53f3\u4e0a",
            "\u66ff\u4ee3",
            "\u66ff\u4ee3\u6587\u672c",
            "\u7c7b",
            "\u7e2e\u5716",
            "\u7f29\u7565\u56fe",
            "\u8a9e\u8a00",
            "\u8bed\u8a00",
            "\u9023\u7d50",
            "\u94fe\u63a5",
            "\u9801",
            "\u985e\u5225",
            "\u9875\u6570"
        ],
        "startswith": [
            "\u53f3\u4e0a"
        ],
        "endswith": [
            "\u50cf\u7d20",
            "\u9801",
            "\u9875"
        ]
    },
    "gcr": {
        "keywords": [
            "bas",
            "bas-texte",
            "bas-txt",
            "base",
            "bordure",
            "cadre",
            "centr\u00e9",
            "droite",
            "encadre",
            "encadr\u00e9",
            "exp",
            "exposant",
            "gauche",
            "haut",
            "haut-texte",
            "haut-txt",
            "ind",
            "indice",
            "ligne-de-base",
            "milieu",
            "neant",
            "non_encadre",
            "non_encadr\u00e9",
            "n\u00e9ant",
            "redresse",
            "sans_cadre",
            "vignette"
        ],
        "params": [
            "classe",
            "langue",
            "lien",
            "redresse",
            "vignette"
        ],
        "startswith": [
            "redresse_"
        ]
    },
    "gl": {
        "keywords": [
            "abaixo",
            "acima",
            "arriba",
            "arriba\u00e1dereita",
            "borda",
            "bordo",
            "centro",
            "comborda",
            "commoldura",
            "conbordo",
            "conmarco",
            "dereita",
            "direita",
            "esquerda",
            "linhadebase",
            "li\u00f1adebase",
            "marco",
            "medio",
            "meio",
            "miniatura",
            "miniaturadaimagem",
            "miniaturadaimaxe",
            "nenhum",
            "ning\u00fan",
            "semborda",
            "semmoldura",
            "senbordo",
            "senmarco",
            "superiordireito",
            "texto-abaixo",
            "texto-arriba"
        ],
        "params": [
            "arriba\u00e1dereita",
            "clase",
            "ligaz\u00f3n",
            "liga\u00e7\u00e3o",
            "miniatura",
            "miniaturadaimagem",
            "miniaturadaimaxe",
            "p\u00e1gina",
            "p\u00e1xina",
            "superiordireito"
        ],
        "startswith": [
            "arriba\u00e1dereita_",
            "p\u00e1gina ",
            "p\u00e1gina_",
            "p\u00e1xina_",
            "superiordireito ",
            "superiordireito_"
        ]
    },
    "glk": {
        "keywords": [
            "\u0627\u0646\u06af\u0634\u062a\u062f\u0627\u0646",
            "\u0627\u0646\u06af\u0634\u062a\u06cc",
            "\u0627\u06cc\u0633\u062a\u0627\u062f\u0647",
            "\u0628\u0627\u0644\u0627",
            "\u0628\u0646\u062f\u0627\u0646\u06af\u0634\u062a\u06cc",
            "\u0628\u06cc_\u0642\u0627\u0628",
            "\u0628\u06cc\u0642\u0627\u0628",
            "\u0628\u06cc\u200c\u0642\u0627\u0628",
            "\u062d\u0627\u0634\u06cc\u0647",
            "\u0631\u0627\u0633\u062a",
            "\u0632\u0628\u0631",
            "\u0632\u06cc\u0631",
            "\u0642\u0627\u0628",
            "\u0645\u062a\u0646-\u0628\u0627\u0644\u0627",
            "\u0645\u062a\u0646-\u067e\u0627\u06cc\u06cc\u0646",
            "\u0645\u06cc\u0627\u0646\u0647",
            "\u0647\u0645\u06a9\u0641",
            "\u0647\u06cc\u0686",
            "\u0648\u0633\u0637",
            "\u067e\u0627\u06cc\u06cc\u0646",
            "\u0686\u067e"
        ],
        "params": [
            "\u0627\u0646\u06af\u0634\u062a\u062f\u0627\u0646",
            "\u0627\u0646\u06af\u0634\u062a\u06cc",
            "\u0627\u06cc\u0633\u062a\u0627\u062f\u0647",
            "\u0628\u0646\u062f\u0627\u0646\u06af\u0634\u062a\u06cc",
            "\u062c\u0627\u06cc\u06af\u0632\u06cc\u0646",
            "\u0632\u0628\u0627\u0646",
            "\u0635\u0641\u062d\u0647",
            "\u067e\u06cc\u0648\u0646\u062f",
            "\u06a9\u0644\u0627\u0633"
        ],
        "startswith": [
            "\u0627\u06cc\u0633\u062a\u0627\u062f\u0647_",
            "\u0635\u0641\u062d\u0647_"
        ],
        "endswith": [
            "\u067e\u06cc\u06a9\u0633\u0644"
        ]
    },
    "gn": {
        "keywords": [
            "abajo",
            "arriba",
            "borde",
            "centrada",
            "centrado",
            "centrar",
            "centro",
            "dcha",
            "der",
            "derecha",
            "enmarcada",
            "enmarcado",
            "izda",
            "izq",
            "izquierda",
            "marco",
            "medio",
            "mini",
            "miniatura",
            "miniaturadeimagen",
            "nada",
            "ninguna",
            "ninguno",
            "no",
            "sin_enmarcar",
            "sinenmarcar",
            "sinmarco"
        ],
        "params": [
            "enlace",
            "idioma",
            "miniatura",
            "miniaturadeimagen",
            "pagina",
            "p\u00e1gina",
            "vinculo",
            "v\u00ednculo"
        ],
        "startswith": [
            "pagina_",
            "p\u00e1gina_"
        ]
    },
    "gor": {
        "keywords": [
            "atas",
            "atas-teks",
            "atek",
            "batas",
            "batek",
            "bawah",
            "bawah-teks",
            "bing",
            "bingkai",
            "gada",
            "garis_dasar",
            "jempol",
            "jmpl",
            "ka",
            "kanan",
            "ki",
            "kiri",
            "lurus",
            "mini",
            "miniatur",
            "nir",
            "nirbing",
            "pus",
            "pusat",
            "tanpa",
            "tanpabingkai",
            "tegak",
            "tengah",
            "tepi",
            "upa"
        ],
        "params": [
            "al",
            "alternatif",
            "bhs",
            "hal",
            "halaman",
            "jempol",
            "jmpl",
            "lurus",
            "mini",
            "miniatur",
            "pra",
            "pranala",
            "tegak"
        ],
        "startswith": [
            "hal_",
            "halaman_",
            "lurus_",
            "tegak_"
        ]
    },
    "hak": {
        "keywords": [
            "\u4e0a\u6a19",
            "\u4e0b\u6a19",
            "\u4e2d\u95f4",
            "\u53f3",
            "\u53f3\u4e0a",
            "\u5782\u76f4\u7f6e\u4e2d",
            "\u5782\u76f4\u7f6e\u5e95",
            "\u5782\u76f4\u7f6e\u9802",
            "\u57fa\u7ebf",
            "\u5b50",
            "\u5c45\u4e2d",
            "\u5de6",
            "\u5e95\u90e8",
            "\u6587\u5b57\u5e95\u90e8",
            "\u6587\u5b57\u7f6e\u5e95",
            "\u6587\u5b57\u7f6e\u9802",
            "\u6587\u5b57\u9876\u90e8",
            "\u65e0",
            "\u65e0\u6846",
            "\u66ff\u4ee3\u6587\u5b57",
            "\u6709\u6846",
            "\u7121",
            "\u7121\u6846",
            "\u7e2e\u5716",
            "\u7f29\u7565\u56fe",
            "\u7f6e\u4e2d",
            "\u8d85",
            "\u8fb9\u6846",
            "\u908a\u6846",
            "\u9876\u90e8"
        ],
        "params": [
            "\u53f3\u4e0a",
            "\u66ff\u4ee3",
            "\u66ff\u4ee3\u6587\u672c",
            "\u7c7b",
            "\u7e2e\u5716",
            "\u7f29\u7565\u56fe",
            "\u8a9e\u8a00",
            "\u8bed\u8a00",
            "\u9023\u7d50",
            "\u94fe\u63a5",
            "\u9801",
            "\u985e\u5225",
            "\u9875\u6570"
        ],
        "startswith": [
            "\u53f3\u4e0a"
        ],
        "endswith": [
            "\u50cf\u7d20",
            "\u9801",
            "\u9875"
        ]
    },
    "haw": {
        "keywords": [
            "akau",
            "aohe",
            "hema",
            "waena",
            "\u0101kau",
            "\u02bba\u02bbohe",
            "\u02bb\u0101kau"
        ],
        "params": [
            "loulou"
        ]
    },
    "he": {
        "keywords": [
            "\u05d1\u05d0\u05de\u05e6\u05e2",
            "\u05d1\u05e8\u05d0\u05e9 \u05d4\u05d8\u05e7\u05e1\u05d8",
            "\u05d1\u05ea\u05d7\u05ea\u05d9\u05ea \u05d4\u05d8\u05e7\u05e1\u05d8",
            "\u05d2\u05d1\u05d5\u05dc",
            "\u05d2\u05d1\u05d5\u05dc\u05d5\u05ea",
            "\u05d9\u05de\u05d9\u05df",
            "\u05d9\u05de\u05d9\u05df \u05dc\u05de\u05e2\u05dc\u05d4",
            "\u05dc\u05d0 \u05de\u05de\u05d5\u05e1\u05d2\u05e8",
            "\u05dc\u05dc\u05d0",
            "\u05dc\u05dc\u05d0 \u05de\u05e1\u05d2\u05e8\u05ea",
            "\u05dc\u05de\u05d8\u05d4",
            "\u05dc\u05de\u05e2\u05dc\u05d4",
            "\u05de\u05de\u05d5\u05d6\u05e2\u05e8",
            "\u05de\u05de\u05d5\u05e1\u05d2\u05e8",
            "\u05de\u05e1\u05d2\u05e8\u05ea",
            "\u05de\u05e8\u05db\u05d6",
            "\u05e2\u05d9\u05dc\u05d9",
            "\u05e9\u05d5\u05e8\u05ea \u05d4\u05d1\u05e1\u05d9\u05e1",
            "\u05e9\u05de\u05d0\u05dc",
            "\u05ea\u05d7\u05ea\u05d9"
        ],
        "params": [
            "\u05d3\u05e3",
            "\u05d8\u05e7\u05e1\u05d8",
            "\u05d9\u05de\u05d9\u05df \u05dc\u05de\u05e2\u05dc\u05d4",
            "\u05de\u05de\u05d5\u05d6\u05e2\u05e8",
            "\u05e7\u05d9\u05e9\u05d5\u05e8"
        ],
        "startswith": [
            "\u05d3\u05e3 ",
            "\u05d9\u05de\u05d9\u05df \u05dc\u05de\u05e2\u05dc\u05d4 "
        ],
        "endswith": [
            " \u05e4\u05d9\u05e7\u05e1\u05dc\u05d9\u05dd"
        ]
    },
    "hi": {
        "keywords": [
            "\u0905\u0902\u0917\u0942\u0920\u093e",
            "\u0905\u0902\u0917\u0942\u0920\u093e\u0915\u093e\u0930",
            "\u0906\u0927\u093e\u0930_\u0930\u0947\u0916\u093e",
            "\u0915\u093f\u0928\u093e\u0930\u093e",
            "\u0915\u0947\u0902\u0926\u094d\u0930",
            "\u0915\u0947\u0902\u0926\u094d\u0930\u093f\u0924",
            "\u0915\u0947\u0928\u094d\u0926\u094d\u0930",
            "\u0915\u0947\u0928\u094d\u0926\u094d\u0930\u093f\u0924",
            "\u0915\u094b\u0908_\u0928\u0939\u0940\u0902",
            "\u0916\u0921\u093c\u0940",
            "\u0924\u0932",
            "\u0926\u093e\u090f\u0901",
            "\u0926\u093e\u090f\u0902",
            "\u0926\u093e\u092f\u0947\u0902",
            "\u092a\u0926",
            "\u092a\u093e\u0920-\u0924\u0932",
            "\u092a\u093e\u0920-\u0936\u0940\u0930\u094d\u0937",
            "\u092b\u093c\u094d\u0930\u0947\u092e",
            "\u092b\u093c\u094d\u0930\u0947\u092e\u0939\u0940\u0928",
            "\u092b\u094d\u0930\u0947\u092e",
            "\u092b\u094d\u0930\u0947\u092e\u0939\u0940\u0928",
            "\u092c\u093e\u090f\u0901",
            "\u092c\u093e\u090f\u0902",
            "\u092c\u093e\u092f\u0947\u0902",
            "\u092c\u0949\u0930\u094d\u0921\u0930",
            "\u092e\u0927\u094d\u092f",
            "\u092e\u0942\u0930\u094d\u0927",
            "\u0936\u0940\u0930\u094d\u0937"
        ],
        "params": [
            "\u0905\u0902\u0917\u0942\u0920\u093e",
            "\u0905\u0902\u0917\u0942\u0920\u093e\u0915\u093e\u0930",
            "\u0915\u0921\u093c\u0940",
            "\u0916\u0921\u093c\u0940",
            "\u092a\u093e\u0920",
            "\u092a\u0943\u0937\u094d\u0920",
            "\u092d\u093e\u0937\u093e",
            "\u0935\u0930\u094d\u0917"
        ],
        "startswith": [
            "\u0916\u0921\u093c\u0940_",
            "\u092a\u0943\u0937\u094d\u0920_"
        ],
        "endswith": [
            "\u092a\u093f\u0915\u094d\u0938\u0947\u0932"
        ]
    },
    "hr": {
        "keywords": [
            "bezokvira",
            "desno",
            "dno",
            "eks",
            "ind",
            "lijevo",
            "mini",
            "minijatura",
            "natpis",
            "ni\u0161ta",
            "obrub",
            "okvir",
            "osnovnacrta",
            "pola",
            "potpis",
            "sredi\u0161te",
            "tekst-dno",
            "tekst-vrh",
            "vrh"
        ],
        "params": [
            "jezik",
            "minijatura",
            "poveznica",
            "stranica",
            "uspravno"
        ],
        "startswith": [
            "stranica ",
            "uspravno "
        ]
    },
    "hsb": {
        "keywords": [
            "gerahmt",
            "grundlinie",
            "hoch",
            "hochgestellt",
            "hochkant",
            "links",
            "mini",
            "miniatur",
            "mitte",
            "oben",
            "ohne",
            "rahmenlos",
            "rand",
            "rechts",
            "text-oben",
            "text-unten",
            "tief",
            "tiefgestellt",
            "unten",
            "zentriert"
        ],
        "params": [
            "alternativtext",
            "hochkant",
            "klasse",
            "mini",
            "miniatur",
            "seite",
            "sprache",
            "verweis"
        ],
        "startswith": [
            "hochkant ",
            "hochkant_",
            "seite ",
            "seite_"
        ]
    },
    "ht": {
        "keywords": [
            "bas",
            "bas-texte",
            "bas-txt",
            "base",
            "bordure",
            "cadre",
            "centr\u00e9",
            "droite",
            "encadre",
            "encadr\u00e9",
            "exp",
            "exposant",
            "gauche",
            "haut",
            "haut-texte",
            "haut-txt",
            "ind",
            "indice",
            "ligne-de-base",
            "milieu",
            "neant",
            "non_encadre",
            "non_encadr\u00e9",
            "n\u00e9ant",
            "redresse",
            "sans_cadre",
            "vignette"
        ],
        "params": [
            "classe",
            "langue",
            "lien",
            "redresse",
            "vignette"
        ],
        "startswith": [
            "redresse_"
        ]
    },
    "hu": {
        "keywords": [
            "ai",
            "alapvonal",
            "als\u00f3index",
            "bal",
            "balra",
            "b\u00e9lyeg",
            "b\u00e9lyegk\u00e9p",
            "fels\u0151index",
            "fenn",
            "fennjobbra",
            "fent",
            "fi",
            "jobb",
            "jobbra",
            "keret",
            "keretben",
            "keretes",
            "keretezett",
            "keretn\u00e9lk\u00fcli",
            "kerettel",
            "k\u00f6z\u00e9p",
            "k\u00f6z\u00e9pre",
            "lenn",
            "lent",
            "miniat\u0171r",
            "semmi",
            "sz\u00f6veg-fenn",
            "sz\u00f6veg-fent",
            "sz\u00f6veg-lenn",
            "sz\u00f6veg-lent",
            "vk\u00f6z\u00e9pen",
            "vk\u00f6z\u00e9pre"
        ],
        "params": [
            "b\u00e9lyeg",
            "b\u00e9lyegk\u00e9p",
            "fennjobbra",
            "miniat\u0171r",
            "oldal"
        ],
        "startswith": [
            "fennjobbra ",
            "oldal "
        ]
    },
    "hy": {
        "keywords": [
            "\u0561\u057b\u056b\u0581",
            "\u0561\u057c\u0561\u0576\u0581",
            "\u056f\u0565\u0576\u057f\u0580\u0578\u0576",
            "\u0571\u0561\u056d\u056b\u0581",
            "\u0574\u056b\u0576\u056b",
            "\u0577\u0580\u057b\u0561\u0583\u0561\u056f\u0565\u056c"
        ],
        "params": [
            "\u0567\u057b\u0568",
            "\u0574\u056b\u0576\u056b"
        ],
        "startswith": [
            "\u0567\u057b "
        ],
        "endswith": [
            "\u0583\u0584\u057d"
        ]
    },
    "hyw": {
        "keywords": [
            "\u0561\u057b\u056b\u0581",
            "\u0561\u057c\u0561\u0576\u0581",
            "\u056f\u0565\u0576\u057f\u0580\u0578\u0576",
            "\u0571\u0561\u056d\u056b\u0581",
            "\u0574\u056b\u0576\u056b",
            "\u0577\u0580\u057b\u0561\u0583\u0561\u056f\u0565\u056c"
        ],
        "params": [
            "\u0567\u057b\u0568",
            "\u0574\u056b\u0576\u056b"
        ],
        "startswith": [
            "\u0567\u057b "
        ],
        "endswith": [
            "\u0583\u0584\u057d"
        ]
    },
    "id": {
        "keywords": [
            "atas",
            "atas-teks",
            "atek",
            "batas",
            "batek",
            "bawah",
            "bawah-teks",
            "bing",
            "bingkai",
            "gada",
            "garis_dasar",
            "jempol",
            "jmpl",
            "ka",
            "kanan",
            "ki",
            "kiri",
            "lurus",
            "mini",
            "miniatur",
            "nir",
            "nirbing",
            "pus",
            "pusat",
            "tanpa",
            "tanpabingkai",
            "tegak",
            "tengah",
            "tepi",
            "upa"
        ],
        "params": [
            "al",
            "alternatif",
            "bhs",
            "hal",
            "halaman",
            "jempol",
            "jmpl",
            "lurus",
            "mini",
            "miniatur",
            "pra",
            "pranala",
            "tegak"
        ],
        "startswith": [
            "hal_",
            "halaman_",
            "lurus_",
            "tegak_"
        ]
    },
    "ig": {
        "keywords": [
            "okp\u00far\u00f9-ede",
            "\u00e1k\u00e1_\u00e8kp\u00e8",
            "\u00e1k\u00e1_\u1ecbk\u1eb9ng\u1ea1",
            "\u00e9l\u00fa",
            "\u1eb9t\u00edt\u00ec"
        ]
    },
    "inh": {
        "keywords": [
            "\u0431\u0435\u0437",
            "\u0431\u0435\u0437\u0440\u0430\u043c\u043a\u0438",
            "\u0433\u0440\u0430\u043d\u0438\u0446\u0430",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u043d\u0430\u0434",
            "\u043e\u0431\u0440\u0430\u043c\u0438\u0442\u044c",
            "\u043e\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u0435",
            "\u043f\u043e\u0434",
            "\u043f\u043e\u0441\u0435\u0440\u0435\u0434\u0438\u043d\u0435",
            "\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u043b\u0435\u0432\u0430",
            "\u0441\u043d\u0438\u0437\u0443",
            "\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u043d\u0438\u0437\u0443",
            "\u0446\u0435\u043d\u0442\u0440"
        ],
        "params": [
            "\u0430\u043b\u044c\u0442",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u0441\u044b\u043b\u043a\u0430",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430"
        ],
        "startswith": [
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430 ",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430 "
        ],
        "endswith": [
            "\u043f\u043a\u0441"
        ]
    },
    "io": {
        "keywords": [
            "altdekstre",
            "alte",
            "centra",
            "dekstra",
            "dekstre",
            "enkadrita",
            "enkadrite",
            "eta",
            "kadra",
            "kadrigita",
            "kadrigite",
            "kadrita",
            "kadrite",
            "kadro",
            "malalte",
            "maldekstra",
            "maldekstre",
            "malsube",
            "malsupre",
            "meza",
            "meze",
            "nenio",
            "neniu",
            "senkadra",
            "suba-teksto",
            "sube",
            "supre",
            "tekst-alte"
        ],
        "params": [
            "altdekstre",
            "alternative",
            "eta",
            "klaso",
            "ligilo",
            "pagxo",
            "pa\u011do"
        ],
        "startswith": [
            "altdekstre_",
            "pagxo_",
            "pa\u011do "
        ],
        "endswith": [
            "ra"
        ]
    },
    "is": {
        "keywords": [
            "efst",
            "engin",
            "h\u00e6gri",
            "mi\u00f0ja",
            "ne\u00f0st",
            "texti-ne\u00f0st",
            "undir",
            "vinstri",
            "yfir",
            "\u00feumall"
        ],
        "endswith": [
            "dp"
        ]
    },
    "it": {
        "keywords": [
            "bordo",
            "centro",
            "destra",
            "incorniciato",
            "met\u00e0",
            "min",
            "miniatura",
            "nessuno",
            "originale",
            "pedice",
            "riquadrato",
            "senza_cornice",
            "sinistra",
            "sopra",
            "sotto",
            "testo-sopra",
            "testo-sotto",
            "verticale"
        ],
        "params": [
            "min",
            "miniatura",
            "pagina",
            "verticale"
        ],
        "startswith": [
            "pagina_",
            "verticale_"
        ]
    },
    "ja": {
        "keywords": [
            "\u306a\u3057",
            "\u30b5\u30e0\u30cd\u30a4\u30eb",
            "\u30d5\u30ec\u30fc\u30e0",
            "\u30d5\u30ec\u30fc\u30e0\u306a\u3057",
            "\u30d9\u30fc\u30b9\u30e9\u30a4\u30f3",
            "\u30dc\u30fc\u30c0\u30fc",
            "\u4e0a\u4ed8\u304d",
            "\u4e0a\u7aef",
            "\u4e0b\u4ed8\u304d",
            "\u4e0b\u7aef",
            "\u4e0b\u7dda",
            "\u4e2d\u592e",
            "\u4e2d\u5fc3",
            "\u53f3",
            "\u53f3\u4e0a",
            "\u5883\u754c",
            "\u5de6",
            "\u6587\u4e0a\u7aef",
            "\u6587\u4e0b\u7aef",
            "\u7121\u3057"
        ],
        "params": [
            "\u30b5\u30e0\u30cd\u30a4\u30eb",
            "\u30da\u30fc\u30b8",
            "\u30ea\u30f3\u30af",
            "\u4ee3\u66ff\u6587",
            "\u4ee3\u66ff\u753b\u50cf"
        ],
        "startswith": [
            "\u30da\u30fc\u30b8 "
        ],
        "endswith": [
            "\u30d4\u30af\u30bb\u30eb"
        ]
    },
    "jv": {
        "keywords": [
            "atas",
            "atas-teks",
            "atek",
            "batas",
            "batek",
            "bawah",
            "bawah-teks",
            "bing",
            "bingkai",
            "gada",
            "garis_dasar",
            "jempol",
            "jmpl",
            "ka",
            "kanan",
            "ki",
            "kiri",
            "lurus",
            "mini",
            "miniatur",
            "nir",
            "nirbing",
            "pus",
            "pusat",
            "tanpa",
            "tanpabingkai",
            "tegak",
            "tengah",
            "tepi",
            "upa"
        ],
        "params": [
            "al",
            "alternatif",
            "bhs",
            "hal",
            "halaman",
            "jempol",
            "jmpl",
            "lurus",
            "mini",
            "miniatur",
            "pra",
            "pranala",
            "tegak"
        ],
        "startswith": [
            "hal_",
            "halaman_",
            "lurus_",
            "tegak_"
        ]
    },
    "ka": {
        "keywords": [
            "\u10d0\u10e0\u10d0",
            "\u10d6\u10d4\u10d3\u10d0",
            "\u10db\u10d0\u10e0\u10ea\u10ee\u10dc\u10d8\u10d5",
            "\u10db\u10d0\u10e0\u10ef\u10d5\u10dc\u10d8\u10d5",
            "\u10db\u10d8\u10dc\u10d8",
            "\u10db\u10d8\u10dc\u10d8\u10d0\u10e1\u10da\u10d8",
            "\u10db\u10d8\u10dc\u10d8\u10d0\u10e2\u10d8\u10e3\u10e0\u10d0",
            "\u10e1\u10d0\u10d6\u10e6\u10d5\u10d0\u10e0\u10d8",
            "\u10e5\u10d5\u10d4\u10d3\u10d0",
            "\u10e8\u10e3\u10d0",
            "\u10ea\u10d4\u10dc\u10e2\u10e0\u10d8",
            "\u10ea\u10d4\u10dc\u10e2\u10e0\u10e8\u10d8",
            "\u10ea\u10d4\u10e0\u10dd\u10d3\u10d4\u10dc\u10d0"
        ],
        "params": [
            "\u10d0\u10da\u10e2",
            "\u10d1\u10db\u10e3\u10da\u10d8",
            "\u10d2\u10d5\u10d4\u10e0\u10d3\u10d8",
            "\u10db\u10d8\u10dc\u10d8",
            "\u10db\u10d8\u10dc\u10d8\u10d0\u10e2\u10d8\u10e3\u10e0\u10d0"
        ],
        "startswith": [
            "\u10d2\u10d5\u10d4\u10e0\u10d3\u10d8_"
        ],
        "endswith": [
            "\u10de\u10e5"
        ]
    },
    "kaa": {
        "keywords": [
            "aral\u0131\u011f\u0131na",
            "ast",
            "ast\u0131l\u0131\u011f\u0131",
            "ast\u0131na",
            "e\u015fqanda\u00fd",
            "joq",
            "j\u00efekti",
            "m\u00e4tin-ast\u0131nda",
            "m\u00e4tin-\u00fcstinde",
            "noba\u00fd",
            "orta",
            "orta\u011fa",
            "o\u00f1",
            "o\u00f1\u011fa",
            "sol",
            "sol\u011fa",
            "s\u00fcrmeli",
            "s\u00fcrmesiz",
            "tikti",
            "tirekjol",
            "\u00fcst",
            "\u00fcstiligi",
            "\u00fcstine",
            "\u0430\u0440\u0430\u043b\u044b\u0493\u044b\u043d\u0430",
            "\u0430\u0441\u0442",
            "\u0430\u0441\u0442\u044b\u043b\u044b\u0493\u044b",
            "\u0430\u0441\u0442\u044b\u043d\u0430",
            "\u0435\u0448\u049b\u0430\u043d\u0434\u0430\u0439",
            "\u0436\u0438\u0435\u043a\u0442\u0456",
            "\u0436\u043e\u049b",
            "\u043c\u04d9\u0442\u0456\u043d-\u0430\u0441\u0442\u044b\u043d\u0434\u0430",
            "\u043c\u04d9\u0442\u0456\u043d-\u04af\u0441\u0442\u0456\u043d\u0434\u0435",
            "\u043d\u043e\u0431\u0430\u0439",
            "\u043e\u0440\u0442\u0430",
            "\u043e\u0440\u0442\u0430\u0493\u0430",
            "\u043e\u04a3",
            "\u043e\u04a3\u0493\u0430",
            "\u0441\u043e\u043b",
            "\u0441\u043e\u043b\u0493\u0430",
            "\u0441\u04af\u0440\u043c\u0435\u043b\u0456",
            "\u0441\u04af\u0440\u043c\u0435\u0441\u0456\u0437",
            "\u0442\u0456\u043a\u0442\u0456",
            "\u0442\u0456\u0440\u0435\u043a\u0436\u043e\u043b",
            "\u04af\u0441\u0442",
            "\u04af\u0441\u0442\u0456\u043b\u0456\u0433\u0456",
            "\u04af\u0441\u0442\u0456\u043d\u0435"
        ],
        "params": [
            "bet",
            "noba\u00fd",
            "tiktik",
            "\u0431\u0435\u0442",
            "\u043d\u043e\u0431\u0430\u0439",
            "\u0442\u0456\u043a\u0442\u0456\u043a"
        ],
        "startswith": [
            "bet ",
            "tiktik ",
            "\u0431\u0435\u0442 ",
            "\u0442\u0456\u043a\u0442\u0456\u043a "
        ],
        "endswith": [
            " n\u00fckte",
            " \u043d\u04af\u043a\u0442\u0435"
        ]
    },
    "kab": {
        "keywords": [
            "bas",
            "bas-texte",
            "bas-txt",
            "base",
            "bordure",
            "cadre",
            "centr\u00e9",
            "droite",
            "encadre",
            "encadr\u00e9",
            "exp",
            "exposant",
            "gauche",
            "haut",
            "haut-texte",
            "haut-txt",
            "ind",
            "indice",
            "ligne-de-base",
            "milieu",
            "neant",
            "non_encadre",
            "non_encadr\u00e9",
            "n\u00e9ant",
            "redresse",
            "sans_cadre",
            "vignette"
        ],
        "params": [
            "classe",
            "langue",
            "lien",
            "redresse",
            "vignette"
        ],
        "startswith": [
            "redresse_"
        ]
    },
    "kbp": {
        "keywords": [
            "bas",
            "bas-texte",
            "bas-txt",
            "base",
            "bordure",
            "cadre",
            "centr\u00e9",
            "droite",
            "encadre",
            "encadr\u00e9",
            "exp",
            "exposant",
            "gauche",
            "haut",
            "haut-texte",
            "haut-txt",
            "ind",
            "indice",
            "ligne-de-base",
            "milieu",
            "neant",
            "non_encadre",
            "non_encadr\u00e9",
            "n\u00e9ant",
            "redresse",
            "sans_cadre",
            "vignette"
        ],
        "params": [
            "classe",
            "langue",
            "lien",
            "redresse",
            "vignette"
        ],
        "startswith": [
            "redresse_"
        ]
    },
    "kk": {
        "keywords": [
            "\u0430\u0440\u0430\u043b\u044b\u0493\u044b\u043d\u0430",
            "\u0430\u0441\u0442",
            "\u0430\u0441\u0442\u044b\u043b\u044b\u0493\u044b",
            "\u0430\u0441\u0442\u044b\u043d\u0430",
            "\u0435\u0448\u049b\u0430\u043d\u0434\u0430\u0439",
            "\u0436\u0438\u0435\u043a\u0442\u0456",
            "\u0436\u043e\u049b",
            "\u043c\u04d9\u0442\u0456\u043d-\u0430\u0441\u0442\u044b\u043d\u0434\u0430",
            "\u043c\u04d9\u0442\u0456\u043d-\u04af\u0441\u0442\u0456\u043d\u0434\u0435",
            "\u043d\u043e\u0431\u0430\u0439",
            "\u043e\u0440\u0442\u0430",
            "\u043e\u0440\u0442\u0430\u0493\u0430",
            "\u043e\u04a3",
            "\u043e\u04a3\u0493\u0430",
            "\u0441\u043e\u043b",
            "\u0441\u043e\u043b\u0493\u0430",
            "\u0441\u04af\u0440\u043c\u0435\u043b\u0456",
            "\u0441\u04af\u0440\u043c\u0435\u0441\u0456\u0437",
            "\u0442\u0456\u043a\u0442\u0456",
            "\u0442\u0456\u0440\u0435\u043a\u0436\u043e\u043b",
            "\u04af\u0441\u0442",
            "\u04af\u0441\u0442\u0456\u043b\u0456\u0433\u0456",
            "\u04af\u0441\u0442\u0456\u043d\u0435"
        ],
        "params": [
            "\u0431\u0435\u0442",
            "\u043d\u043e\u0431\u0430\u0439",
            "\u0442\u0456\u043a\u0442\u0456\u043a"
        ],
        "startswith": [
            "\u0431\u0435\u0442 ",
            "\u0442\u0456\u043a\u0442\u0456\u043a "
        ],
        "endswith": [
            " \u043d\u04af\u043a\u0442\u0435"
        ]
    },
    "km": {
        "keywords": [
            "\u1780\u178e\u17d2\u178f\u17b6\u179b",
            "\u1781\u17b6\u1784\u1792\u17d2\u179c\u17c1\u1784",
            "\u1781\u17b6\u1784\u179f\u17d2\u178f\u17b6\u17c6",
            "\u1782\u17d2\u1798\u17b6\u1793",
            "\u1782\u17d2\u1798\u17b6\u1793\u179f\u17ca\u17bb\u1798",
            "\u1783\u17d2\u179b\u17b6\u1793\u17c5\u1795\u17d2\u1793\u17c2\u1780\u1781\u17b6\u1784\u179b\u17be",
            "\u1783\u17d2\u179b\u17b6\u1793\u17c5\u1795\u17d2\u1793\u17c2\u1780\u1794\u17b6\u178f",
            "\u1783\u17d2\u179b\u17b6\u1795\u17d2\u1793\u17c2\u1780\u1781\u17b6\u1784\u179b\u17be",
            "\u1783\u17d2\u179b\u17b6\u1795\u17d2\u1793\u17c2\u1780\u1794\u17b6\u178f",
            "\u1791\u1791\u17c1",
            "\u1792\u17d2\u179c\u17c1\u1784",
            "\u1794\u17b6\u178f",
            "\u1795\u17d2\u1793\u17c2\u1780\u1780\u178e\u17d2\u178f\u17b6\u179b",
            "\u1795\u17d2\u1793\u17c2\u1780\u1781\u17b6\u1784\u179b\u17be",
            "\u1795\u17d2\u1793\u17c2\u1780\u1794\u17b6\u178f",
            "\u1795\u17d2\u1793\u17c2\u1780\u179b\u17be",
            "\u179a\u17bc\u1794\u178f\u17bc\u1785",
            "\u179a\u17bc\u1794\u1797\u17b6\u1796\u178f\u17bc\u1785",
            "\u179f\u17ca\u17bb\u1798",
            "\u179f\u17d2\u178f\u17b6\u17c6"
        ],
        "params": [
            "\u178f\u17c6\u178e\u1797\u17d2\u1787\u17b6\u1794\u17cb",
            "\u178f\u17c6\u1793\u1797\u17d2\u1787\u17b6\u1794\u17cb",
            "\u1791\u17c6\u1796\u17d0\u179a",
            "\u179a\u17bc\u1794\u178f\u17bc\u1785",
            "\u179a\u17bc\u1794\u1797\u17b6\u1796\u178f\u17bc\u1785"
        ],
        "startswith": [
            "\u1791\u17c6\u1796\u17d0\u179a"
        ],
        "endswith": [
            "\u1797\u179f",
            "\u1797\u17b8\u1780\u179f\u17c2\u179b"
        ]
    },
    "ko": {
        "keywords": [
            "\uac00\uc6b4\ub370",
            "\uae00\uc790\uc544\ub798",
            "\uae00\uc790\uc704",
            "\ubc11\uc904",
            "\uc12c\ub124\uc77c",
            "\uc378\ub124\uc77c",
            "\uc544\ub798",
            "\uc544\ub798\ucca8\uc790",
            "\uc5c6\uc74c",
            "\uc624\ub978\ucabd",
            "\uc67c\ucabd",
            "\uc704",
            "\uc704\uc624\ub978\ucabd",
            "\uc704\ucca8\uc790",
            "\uc911\uac04",
            "\ucd95\uc18c\ud310",
            "\ud14c\ub450\ub9ac",
            "\ud14d\uc2a4\ud2b8\uc544\ub798",
            "\ud14d\uc2a4\ud2b8\uc704",
            "\ud504\ub808\uc784",
            "\ud504\ub808\uc784\uc5c6\uc74c"
        ],
        "params": [
            "\ub300\uccb4\uae00",
            "\ub9c1\ud06c",
            "\ubb38\uc11c",
            "\uc12c\ub124\uc77c",
            "\uc378\ub124\uc77c",
            "\uc5b8\uc5b4",
            "\uc704\uc624\ub978\ucabd",
            "\ucd95\uc18c\ud310",
            "\ud074\ub798\uc2a4"
        ],
        "endswith": [
            "\ud53d\uc140"
        ]
    },
    "koi": {
        "keywords": [
            "\u0431\u0435\u0437",
            "\u0431\u0435\u0437\u0440\u0430\u043c\u043a\u0438",
            "\u0433\u0440\u0430\u043d\u0438\u0446\u0430",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u043d\u0430\u0434",
            "\u043e\u0431\u0440\u0430\u043c\u0438\u0442\u044c",
            "\u043e\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u0435",
            "\u043f\u043e\u0434",
            "\u043f\u043e\u0441\u0435\u0440\u0435\u0434\u0438\u043d\u0435",
            "\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u043b\u0435\u0432\u0430",
            "\u0441\u043d\u0438\u0437\u0443",
            "\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u043d\u0438\u0437\u0443",
            "\u0446\u0435\u043d\u0442\u0440"
        ],
        "params": [
            "\u0430\u043b\u044c\u0442",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u0441\u044b\u043b\u043a\u0430",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430"
        ],
        "startswith": [
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430 ",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430 "
        ],
        "endswith": [
            "\u043f\u043a\u0441"
        ]
    },
    "krc": {
        "keywords": [
            "\u0431\u0435\u0437",
            "\u0431\u0435\u0437\u0440\u0430\u043c\u043a\u0438",
            "\u0433\u0440\u0430\u043d\u0438\u0446\u0430",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u043d\u0430\u0434",
            "\u043e\u0431\u0440\u0430\u043c\u0438\u0442\u044c",
            "\u043e\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u0435",
            "\u043f\u043e\u0434",
            "\u043f\u043e\u0441\u0435\u0440\u0435\u0434\u0438\u043d\u0435",
            "\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u043b\u0435\u0432\u0430",
            "\u0441\u043d\u0438\u0437\u0443",
            "\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u043d\u0438\u0437\u0443",
            "\u0446\u0435\u043d\u0442\u0440"
        ],
        "params": [
            "\u0430\u043b\u044c\u0442",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u0441\u044b\u043b\u043a\u0430",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430"
        ],
        "startswith": [
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430 ",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430 "
        ],
        "endswith": [
            "\u043f\u043a\u0441"
        ]
    },
    "ksh": {
        "keywords": [
            "gerahmt",
            "grundlinie",
            "hoch",
            "hochgestellt",
            "hochkant",
            "lengks",
            "lenks",
            "links",
            "mini",
            "miniatur",
            "mitte",
            "oben",
            "ohne",
            "rahmenlos",
            "rand",
            "rechts",
            "r\u00e4h\u00df",
            "r\u00e4ts",
            "text-oben",
            "text-unten",
            "tief",
            "tiefgestellt",
            "unten",
            "zentriert"
        ],
        "params": [
            "alternativtext",
            "hochkant",
            "klasse",
            "mini",
            "miniatur",
            "seite",
            "sprache",
            "verweis"
        ],
        "startswith": [
            "hochkant ",
            "hochkant_",
            "seite ",
            "seite_"
        ]
    },
    "ku": {
        "keywords": [
            "rast",
            "\u00e7ep"
        ],
        "params": [
            "gir\u00eadan"
        ]
    },
    "kv": {
        "keywords": [
            "\u0431\u0435\u0437",
            "\u0431\u0435\u0437\u0440\u0430\u043c\u043a\u0438",
            "\u0433\u0440\u0430\u043d\u0438\u0446\u0430",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u043d\u0430\u0434",
            "\u043e\u0431\u0440\u0430\u043c\u0438\u0442\u044c",
            "\u043e\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u0435",
            "\u043f\u043e\u0434",
            "\u043f\u043e\u0441\u0435\u0440\u0435\u0434\u0438\u043d\u0435",
            "\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u043b\u0435\u0432\u0430",
            "\u0441\u043d\u0438\u0437\u0443",
            "\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u043d\u0438\u0437\u0443",
            "\u0446\u0435\u043d\u0442\u0440"
        ],
        "params": [
            "\u0430\u043b\u044c\u0442",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u0441\u044b\u043b\u043a\u0430",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430"
        ],
        "startswith": [
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430 ",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430 "
        ],
        "endswith": [
            "\u043f\u043a\u0441"
        ]
    },
    "kw": {
        "keywords": [
            "dyhow",
            "fremys",
            "goles",
            "gwartha",
            "hebfram",
            "kledh",
            "kres",
            "kresel",
            "nagonan",
            "skeusennik",
            "tekst-goles",
            "tekst-gwartha"
        ],
        "params": [
            "folen",
            "kevren",
            "skeusennik"
        ],
        "startswith": [
            "folen_"
        ]
    },
    "lad": {
        "keywords": [
            "abajo",
            "arriba",
            "borde",
            "centrada",
            "centrado",
            "centrar",
            "centro",
            "cierda",
            "dcha",
            "der",
            "derecha",
            "dinguna",
            "dinguno",
            "enmarcada",
            "enmarcado",
            "izda",
            "izq",
            "izquierda",
            "marco",
            "medio",
            "mini",
            "miniatura",
            "miniaturadeimagen",
            "nada",
            "ninguna",
            "ninguno",
            "no",
            "sin_enmarcar",
            "sinenmarcar",
            "sinmarco"
        ],
        "params": [
            "enlace",
            "idioma",
            "miniatura",
            "miniaturadeimagen",
            "pagina",
            "p\u00e1gina",
            "vinculo",
            "v\u00ednculo"
        ],
        "startswith": [
            "pagina_",
            "p\u00e1gina_"
        ]
    },
    "lb": {
        "keywords": [
            "Miniatur",
            "bord",
            "gerahmt",
            "gerummt",
            "grundlinie",
            "hoch",
            "hochgestellt",
            "hochkant",
            "links",
            "l\u00e9nks",
            "mini",
            "miniatur",
            "mitte",
            "m\u00ebtt",
            "net_gerummt",
            "oben",
            "ohne",
            "ouni",
            "rahmenlos",
            "rand",
            "rechts",
            "riets",
            "text-oben",
            "text-unten",
            "tief",
            "tiefgestellt",
            "uewen",
            "unten",
            "zentriert",
            "zentr\u00e9iert",
            "\u00ebnnen"
        ],
        "params": [
            "S\u00e4it",
            "alternativtext",
            "hochkant",
            "klasse",
            "mini",
            "miniatur",
            "seite",
            "sprache",
            "verweis"
        ],
        "startswith": [
            "S\u00e4it_",
            "hochkant ",
            "hochkant_",
            "seite ",
            "seite_"
        ]
    },
    "lbe": {
        "keywords": [
            "\u0431\u0435\u0437",
            "\u0431\u0435\u0437\u0440\u0430\u043c\u043a\u0438",
            "\u0433\u0440\u0430\u043d\u0438\u0446\u0430",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u043d\u0430\u0434",
            "\u043e\u0431\u0440\u0430\u043c\u0438\u0442\u044c",
            "\u043e\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u0435",
            "\u043f\u043e\u0434",
            "\u043f\u043e\u0441\u0435\u0440\u0435\u0434\u0438\u043d\u0435",
            "\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u043b\u0435\u0432\u0430",
            "\u0441\u043d\u0438\u0437\u0443",
            "\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u043d\u0438\u0437\u0443",
            "\u0446\u0435\u043d\u0442\u0440"
        ],
        "params": [
            "\u0430\u043b\u044c\u0442",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u0441\u044b\u043b\u043a\u0430",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430"
        ],
        "startswith": [
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430 ",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430 "
        ],
        "endswith": [
            "\u043f\u043a\u0441"
        ]
    },
    "lez": {
        "keywords": [
            "\u0431\u0435\u0437",
            "\u0431\u0435\u0437\u0440\u0430\u043c\u043a\u0438",
            "\u0433\u0440\u0430\u043d\u0438\u0446\u0430",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u043d\u0430\u0434",
            "\u043e\u0431\u0440\u0430\u043c\u0438\u0442\u044c",
            "\u043e\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u0435",
            "\u043f\u043e\u0434",
            "\u043f\u043e\u0441\u0435\u0440\u0435\u0434\u0438\u043d\u0435",
            "\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u043b\u0435\u0432\u0430",
            "\u0441\u043d\u0438\u0437\u0443",
            "\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u043d\u0438\u0437\u0443",
            "\u0446\u0435\u043d\u0442\u0440"
        ],
        "params": [
            "\u0430\u043b\u044c\u0442",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u0441\u044b\u043b\u043a\u0430",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430"
        ],
        "startswith": [
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430 ",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430 "
        ],
        "endswith": [
            "\u043f\u043a\u0441"
        ]
    },
    "li": {
        "keywords": [
            "beneden",
            "boven",
            "gecentreerd",
            "geen",
            "grondlijn",
            "kaderloos",
            "links",
            "midden",
            "miniatuur",
            "omkaderd",
            "rand",
            "rechtop",
            "rechts",
            "tekst-beneden",
            "tekst-boven"
        ],
        "params": [
            "klasse",
            "koppeling",
            "miniatuur",
            "pagina",
            "rechtop",
            "taal",
            "verwijzing"
        ],
        "startswith": [
            "pagina_",
            "rechtop"
        ]
    },
    "lij": {
        "keywords": [
            "bordo",
            "centro",
            "destra",
            "incorniciato",
            "met\u00e0",
            "min",
            "miniatura",
            "nessuno",
            "originale",
            "pedice",
            "riquadrato",
            "senza_cornice",
            "sinistra",
            "sopra",
            "sotto",
            "testo-sopra",
            "testo-sotto",
            "verticale"
        ],
        "params": [
            "min",
            "miniatura",
            "pagina",
            "verticale"
        ],
        "startswith": [
            "pagina_",
            "verticale_"
        ]
    },
    "lld": {
        "keywords": [
            "bordo",
            "centro",
            "destra",
            "incorniciato",
            "met\u00e0",
            "min",
            "miniatura",
            "nessuno",
            "originale",
            "pedice",
            "riquadrato",
            "senza_cornice",
            "sidretg",
            "sinistra",
            "sopra",
            "sotto",
            "testo-sopra",
            "testo-sotto",
            "verticale"
        ],
        "params": [
            "min",
            "miniatura",
            "pagina",
            "sidretg",
            "verticale"
        ],
        "startswith": [
            "pagina_",
            "sidretg_",
            "verticale_"
        ]
    },
    "lmo": {
        "keywords": [
            "bordo",
            "centro",
            "destra",
            "drita",
            "incorniciato",
            "manz\u00edna",
            "met\u00e0",
            "min",
            "miniatura",
            "nessuno",
            "niss\u00f6n",
            "originale",
            "pedice",
            "riquadrato",
            "senza_cornice",
            "sinistra",
            "sopra",
            "sotto",
            "testo-sopra",
            "testo-sotto",
            "verticale"
        ],
        "params": [
            "min",
            "miniatura",
            "pagina",
            "verticale"
        ],
        "startswith": [
            "pagina_",
            "verticale_"
        ]
    },
    "ln": {
        "keywords": [
            "bas",
            "bas-texte",
            "bas-txt",
            "base",
            "bordure",
            "cadre",
            "centr\u00e9",
            "droite",
            "encadre",
            "encadr\u00e9",
            "exp",
            "exposant",
            "gauche",
            "haut",
            "haut-texte",
            "haut-txt",
            "ind",
            "indice",
            "ligne-de-base",
            "milieu",
            "neant",
            "non_encadre",
            "non_encadr\u00e9",
            "n\u00e9ant",
            "redresse",
            "sans_cadre",
            "vignette"
        ],
        "params": [
            "classe",
            "langue",
            "lien",
            "redresse",
            "vignette"
        ],
        "startswith": [
            "redresse_"
        ]
    },
    "lt": {
        "keywords": [
            "de\u0161in\u0117je",
            "kair\u0117je",
            "mini",
            "miniati\u016bra"
        ],
        "params": [
            "mini",
            "miniati\u016bra"
        ]
    },
    "mad": {
        "keywords": [
            "atas",
            "atas-teks",
            "atek",
            "batas",
            "batek",
            "bawah",
            "bawah-teks",
            "bing",
            "bingkai",
            "gada",
            "garis_dasar",
            "jempol",
            "jmpl",
            "ka",
            "kanan",
            "ki",
            "kiri",
            "lurus",
            "mini",
            "miniatur",
            "nir",
            "nirbing",
            "pus",
            "pusat",
            "tanpa",
            "tanpabingkai",
            "tegak",
            "tengah",
            "tepi",
            "upa"
        ],
        "params": [
            "al",
            "alternatif",
            "bhs",
            "hal",
            "halaman",
            "jempol",
            "jmpl",
            "lurus",
            "mini",
            "miniatur",
            "pra",
            "pranala",
            "tegak"
        ],
        "startswith": [
            "hal_",
            "halaman_",
            "lurus_",
            "tegak_"
        ]
    },
    "mai": {
        "keywords": [
            "\u0905\u0902\u0917\u0942\u0920\u093e",
            "\u0905\u0902\u0917\u0942\u0920\u093e\u0915\u093e\u0930",
            "\u0906\u0927\u093e\u0930_\u0930\u0947\u0916\u093e",
            "\u0915\u093f\u0928\u093e\u0930\u093e",
            "\u0915\u0947\u0902\u0926\u094d\u0930",
            "\u0915\u0947\u0902\u0926\u094d\u0930\u093f\u0924",
            "\u0915\u0947\u0928\u094d\u0926\u094d\u0930",
            "\u0915\u0947\u0928\u094d\u0926\u094d\u0930\u093f\u0924",
            "\u0915\u094b\u0908_\u0928\u0939\u0940\u0902",
            "\u0916\u0921\u093c\u0940",
            "\u0924\u0932",
            "\u0926\u093e\u090f\u0901",
            "\u0926\u093e\u090f\u0902",
            "\u0926\u093e\u092f\u0947\u0902",
            "\u092a\u0926",
            "\u092a\u093e\u0920-\u0924\u0932",
            "\u092a\u093e\u0920-\u0936\u0940\u0930\u094d\u0937",
            "\u092b\u093c\u094d\u0930\u0947\u092e",
            "\u092b\u093c\u094d\u0930\u0947\u092e\u0939\u0940\u0928",
            "\u092b\u094d\u0930\u0947\u092e",
            "\u092b\u094d\u0930\u0947\u092e\u0939\u0940\u0928",
            "\u092c\u093e\u090f\u0901",
            "\u092c\u093e\u090f\u0902",
            "\u092c\u093e\u092f\u0947\u0902",
            "\u092c\u0949\u0930\u094d\u0921\u0930",
            "\u092e\u0927\u094d\u092f",
            "\u092e\u0942\u0930\u094d\u0927",
            "\u0936\u0940\u0930\u094d\u0937"
        ],
        "params": [
            "\u0905\u0902\u0917\u0942\u0920\u093e",
            "\u0905\u0902\u0917\u0942\u0920\u093e\u0915\u093e\u0930",
            "\u0915\u0921\u093c\u0940",
            "\u0916\u0921\u093c\u0940",
            "\u092a\u093e\u0920",
            "\u092a\u0943\u0937\u094d\u0920",
            "\u092d\u093e\u0937\u093e",
            "\u0935\u0930\u094d\u0917"
        ],
        "startswith": [
            "\u0916\u0921\u093c\u0940_",
            "\u092a\u0943\u0937\u094d\u0920_"
        ],
        "endswith": [
            "\u092a\u093f\u0915\u094d\u0938\u0947\u0932"
        ]
    },
    "map-bms": {
        "keywords": [
            "atas",
            "atas-teks",
            "atek",
            "batas",
            "batek",
            "bawah",
            "bawah-teks",
            "bing",
            "bingkai",
            "gada",
            "garis_dasar",
            "jempol",
            "jmpl",
            "ka",
            "kanan",
            "ki",
            "kiri",
            "lurus",
            "mini",
            "miniatur",
            "nir",
            "nirbing",
            "pus",
            "pusat",
            "tanpa",
            "tanpabingkai",
            "tegak",
            "tengah",
            "tepi",
            "upa"
        ],
        "params": [
            "al",
            "alternatif",
            "bhs",
            "hal",
            "halaman",
            "jempol",
            "jmpl",
            "lurus",
            "mini",
            "miniatur",
            "pra",
            "pranala",
            "tegak"
        ],
        "startswith": [
            "hal_",
            "halaman_",
            "lurus_",
            "tegak_"
        ]
    },
    "mdf": {
        "keywords": [
            "\u0430\u043b\u043a\u0441",
            "\u0431\u0435\u0437",
            "\u0431\u0435\u0437\u0440\u0430\u043c\u043a\u0438",
            "\u0432\u0435\u0439\u043a\u0435\u044f\u043a_\u0430\u0440\u0430\u0441\u044c",
            "\u0432\u0435\u0440\u044c\u043a\u0441",
            "\u0432\u0438\u0442\u044c_\u043a\u0435\u0434\u044c",
            "\u0433\u0440\u0430\u043d\u0438\u0446\u0430",
            "\u043a\u0435\u043d\u0436\u0435\u0448\u043a\u0430",
            "\u043a\u0435\u0440\u0448_\u043a\u0435\u0434\u044c",
            "\u043a\u0443\u043d\u0434\u043e\u0432\u0442\u043e\u043c\u043e",
            "\u043a\u0443\u043d\u0434\u0441\u043e",
            "\u043a\u0443\u043d\u0448\u043a\u0430",
            "\u043a\u0443\u043d\u0448\u043a\u0430\u0441\u043e",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u043d\u0430\u0434",
            "\u043e\u0431\u0440\u0430\u043c\u0438\u0442\u044c",
            "\u043e\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u0435",
            "\u043f\u043e\u0434",
            "\u043f\u043e\u0441\u0435\u0440\u0435\u0434\u0438\u043d\u0435",
            "\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u043b\u0435\u0432\u0430",
            "\u0441\u043d\u0438\u0437\u0443",
            "\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0442\u0435\u043a\u0441\u0442-\u0430\u043b\u043a\u0441",
            "\u0442\u0435\u043a\u0441\u0442-\u0432\u0435\u0440\u044c\u043a\u0441",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u043d\u0438\u0437\u0443",
            "\u0446\u0435\u043d\u0442\u0440"
        ],
        "params": [
            "\u0430\u043b\u044c\u0442",
            "\u043b\u043e\u043f\u0430",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u0441\u044b\u043b\u043a\u0430",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430"
        ],
        "startswith": [
            "\u043b\u043e\u043f\u0430_",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430 ",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430 ",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430_"
        ],
        "endswith": [
            "\u043f\u043a\u0441"
        ]
    },
    "mg": {
        "keywords": [
            "ambany",
            "ambony",
            "ampivoany",
            "anivo",
            "anivony",
            "ankavanana",
            "ankavia",
            "bas",
            "bas-texte",
            "bas-txt",
            "base",
            "bordure",
            "cadre",
            "centr\u00e9",
            "droite",
            "encadre",
            "encadr\u00e9",
            "exp",
            "exposant",
            "gauche",
            "haut",
            "haut-texte",
            "haut-txt",
            "ind",
            "indice",
            "ligne-de-base",
            "milieu",
            "neant",
            "non_encadre",
            "non_encadr\u00e9",
            "n\u00e9ant",
            "redresse",
            "sans_cadre",
            "sisiny",
            "tsymisy",
            "vignette"
        ],
        "params": [
            "classe",
            "langue",
            "lien",
            "redresse",
            "vignette"
        ],
        "startswith": [
            "pejy ",
            "redresse_"
        ]
    },
    "mhr": {
        "keywords": [
            "\u0431\u0435\u0437",
            "\u0431\u0435\u0437\u0440\u0430\u043c\u043a\u0438",
            "\u0433\u0440\u0430\u043d\u0438\u0446\u0430",
            "\u0439\u044b\u043c\u0430\u043b\u043d\u0435",
            "\u043a\u04f1\u0448\u044b\u0447\u044b\u043d",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u043d\u0430\u0434",
            "\u043e\u0431\u0440\u0430\u043c\u0438\u0442\u044c",
            "\u043e\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u0435",
            "\u043f\u043e\u0434",
            "\u043f\u043e\u043a\u0448\u0435\u043b\u043d\u0435",
            "\u043f\u043e\u0441\u0435\u0440\u0435\u0434\u0438\u043d\u0435",
            "\u043f\u0443\u0440\u043b\u0430",
            "\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u043b\u0435\u0432\u0430",
            "\u0441\u043d\u0438\u0437\u0443",
            "\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u043d\u0438\u0437\u0443",
            "\u0446\u0435\u043d\u0442\u0440",
            "\u0447\u0435\u043a",
            "\u0448\u043e\u043b\u0430",
            "\u04f1\u043b\u044b\u0447\u044b\u043d",
            "\u04f1\u043c\u0431\u0430\u043b\u043d\u0435"
        ],
        "params": [
            "\u0430\u043b\u044c\u0442",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u0441\u044b\u043b\u043a\u0430",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430"
        ],
        "startswith": [
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430 ",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430 "
        ],
        "endswith": [
            "\u043f\u043a\u0441"
        ]
    },
    "min": {
        "keywords": [
            "atas",
            "atas-teks",
            "atek",
            "batas",
            "batek",
            "bawah",
            "bawah-teks",
            "bing",
            "bingkai",
            "gada",
            "garis_dasar",
            "jempol",
            "jmpl",
            "ka",
            "kanan",
            "ki",
            "kiri",
            "lurus",
            "mini",
            "miniatur",
            "nir",
            "nirbing",
            "pus",
            "pusat",
            "tanpa",
            "tanpabingkai",
            "tegak",
            "tengah",
            "tepi",
            "upa"
        ],
        "params": [
            "al",
            "alternatif",
            "bhs",
            "hal",
            "halaman",
            "jempol",
            "jmpl",
            "lurus",
            "mini",
            "miniatur",
            "pra",
            "pranala",
            "tegak"
        ],
        "startswith": [
            "hal_",
            "halaman_",
            "lurus_",
            "tegak_"
        ]
    },
    "mk": {
        "keywords": [
            "\u0431\u0435\u0437\u0440\u0430\u043c\u043a\u0430",
            "\u0432\u043e\u0440\u0430\u043c\u043a\u0430",
            "\u0432\u0440\u0432",
            "\u0433\u043e\u0440",
            "\u0433\u043e\u0440\u0435\u043d\u0438\u043d\u0434\u0435\u043a\u0441",
            "\u0433\u0440\u0430\u043d\u0438\u0446\u0430",
            "\u0433\u0440\u0430\u043d\u0438\u0447\u043d\u0438\u043a",
            "\u0434",
            "\u0434\u0435\u0441\u043d\u043e",
            "\u0434\u043d\u043e",
            "\u0434\u043e\u043b",
            "\u0434\u043e\u043b\u0435\u043d\u0438\u043d\u0434\u0435\u043a\u0441",
            "\u0438\u0441\u043f\u0440\u0430\u0432\u0435\u043d\u043e",
            "\u043b",
            "\u043b\u0435\u0432\u043e",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438-\u0441\u043b\u0438\u043a\u0430",
            "\u043d",
            "\u043d\u0430\u0458\u0433\u043e\u0440\u0435",
            "\u043d\u0430\u0458\u0434\u043e\u043b\u0443",
            "\u043d\u0435\u043c\u0430",
            "\u043e\u0441\u043d\u043e\u0432\u043d\u0430\u043b\u0438\u043d\u0438\u0458\u0430",
            "\u0440\u0430\u043c\u043a\u0430",
            "\u0441\u0440\u0435\u0434\u0438\u043d\u0430",
            "\u0442\u0435\u043a\u0441\u0442-\u0432\u0440\u0432",
            "\u0442\u0435\u043a\u0441\u0442-\u0434\u043d\u043e",
            "\u0442\u0435\u043a\u0441\u0442-\u043d\u0430\u0458\u0433\u043e\u0440\u0435",
            "\u0442\u0435\u043a\u0441\u0442-\u043d\u0430\u0458\u0434\u043e\u043b\u0443",
            "\u0446",
            "\u0446\u0435\u043d\u0442\u0430\u0440"
        ],
        "params": [
            "\u0430\u043b\u0442",
            "\u0432\u0440\u0441\u043a\u0430",
            "\u0438\u0441\u043f\u0440\u0430\u0432\u0435\u043d\u043e",
            "\u043a\u043b\u0430\u0441\u0430",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438-\u0441\u043b\u0438\u043a\u0430",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430",
            "\u0458\u0430\u0437"
        ],
        "startswith": [
            "\u0438\u0441\u043f\u0440\u0430\u0432\u0435\u043d\u043e_",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430_"
        ],
        "endswith": [
            "\u043f",
            "\u043f\u043a\u0441"
        ]
    },
    "ml": {
        "keywords": [
            "\u0d05\u0d24\u0d3f\u0d7c\u0d35\u0d30",
            "\u0d07\u0d1f\u0d24\u0d4d\u0d24\u0d4d\u200c",
            "\u0d07\u0d1f\u0d24\u0d4d\u200c",
            "\u0d0e\u0d34\u0d41\u0d24\u0d4d\u0d24\u0d4d-\u0d24\u0d3e\u0d34\u0d46",
            "\u0d0e\u0d34\u0d41\u0d24\u0d4d\u0d24\u0d4d-\u0d2e\u0d47\u0d32\u0d46",
            "\u0d15\u0d40\u0d34\u0d46\u0d2f\u0d46\u0d34\u0d41\u0d24\u0d4d\u0d24\u0d4d",
            "\u0d1a\u0d1f\u0d4d\u0d1f\u0d02",
            "\u0d1a\u0d1f\u0d4d\u0d1f\u0d24\u0d4d\u0d24\u0d3f\u0d7d",
            "\u0d1a\u0d1f\u0d4d\u0d1f\u0d30\u0d39\u0d3f\u0d24\u0d02",
            "\u0d24\u0d3e\u0d34\u0d46",
            "\u0d24\u0d3e\u0d34\u0d46\u0d2f\u0d41\u0d33\u0d4d\u0d33\u0d35\u0d30",
            "\u0d28\u0d1f\u0d41\u0d15\u0d4d\u0d15\u0d4d\u200c",
            "\u0d28\u0d1f\u0d41\u0d35\u0d3f\u0d7d",
            "\u0d28\u0d47\u0d30\u0d47\u0d15\u0d41\u0d24\u0d4d\u0d24\u0d28\u0d46",
            "\u0d2e\u0d26\u0d4d\u0d27\u0d4d\u0d2f\u0d02",
            "\u0d2e\u0d47\u0d32\u0d46",
            "\u0d2e\u0d47\u0d32\u0d47\u0d2f\u0d46\u0d34\u0d41\u0d24\u0d4d\u0d24\u0d4d",
            "\u0d32\u0d18\u0d41",
            "\u0d32\u0d18\u0d41\u0d1a\u0d3f\u0d24\u0d4d\u0d30\u0d02",
            "\u0d35\u0d32\u0d24\u0d4d\u0d24\u0d4d\u200c",
            "\u0d35\u0d32\u0d24\u0d4d\u200c",
            "\u0d36\u0d42\u0d28\u0d4d\u0d2f\u0d02"
        ],
        "params": [
            "\u0d15\u0d23\u0d4d\u0d23\u0d3f",
            "\u0d24\u0d3e\u0d7e",
            "\u0d28\u0d47\u0d30\u0d47\u0d15\u0d41\u0d24\u0d4d\u0d24\u0d28\u0d46",
            "\u0d2a\u0d15\u0d30\u0d02",
            "\u0d2d\u0d3e\u0d37",
            "\u0d32\u0d18\u0d41",
            "\u0d32\u0d18\u0d41\u0d1a\u0d3f\u0d24\u0d4d\u0d30\u0d02",
            "\u0d36\u0d4d\u0d30\u0d47\u0d23\u0d3f"
        ],
        "startswith": [
            "\u0d24\u0d3e\u0d7e_",
            "\u0d28\u0d47\u0d30\u0d47\u0d15\u0d41\u0d24\u0d4d\u0d24\u0d28\u0d46_"
        ],
        "endswith": [
            "\u0d2c\u0d3f\u0d28\u0d4d\u0d26\u0d41"
        ]
    },
    "mr": {
        "keywords": [
            "\u0905\u0924\u094d\u092f\u0942\u091a\u094d\u091a",
            "\u0905\u0927\u094b",
            "\u0906\u0927\u093e\u0930\u0930\u0947\u0937\u093e",
            "\u0907\u0935\u0932\u0947\u0938\u0947",
            "\u0909\u091c\u0935\u0947",
            "\u0909\u092d\u093e",
            "\u0909\u0930\u094d\u0927\u094d\u0935",
            "\u0915\u094b\u0923\u0924\u0947\u091a\u0928\u093e\u0939\u0940",
            "\u091a\u094c\u0915\u091f",
            "\u0921\u093e\u0935\u0947",
            "\u0924\u0933",
            "\u0924\u0933\u0930\u0947\u0937\u093e",
            "\u0928\u0928\u094d\u0928\u093e",
            "\u092b\u093c\u094d\u0930\u0947\u092e",
            "\u092c\u0942\u0921",
            "\u092e\u091c\u0915\u0941\u0930\u0924\u0933",
            "\u092e\u091c\u0915\u0942\u0930-\u0936\u0940\u0930\u094d\u0937",
            "\u092e\u0927\u094d\u092f",
            "\u092e\u0927\u094d\u092f\u0935\u0930\u094d\u0924\u0940",
            "\u0935\u093f\u0928\u093e\u091a\u094c\u0915\u091f",
            "\u0935\u093f\u0928\u093e\u092b\u093c\u094d\u0930\u0947\u092e",
            "\u0936\u0940\u0930\u094d\u0937-\u092e\u091c\u0915\u0942\u0930",
            "\u0938\u0940\u092e\u093e"
        ],
        "params": [
            "\u0905\u0932\u094d\u091f",
            "\u0907\u0935\u0932\u0947\u0938\u0947",
            "\u0909\u092d\u093e",
            "\u0926\u0941\u0935\u093e",
            "\u092a\u093e\u0928"
        ],
        "startswith": [
            "\u0909\u092d\u093e_",
            "\u092a\u093e\u0928_"
        ],
        "endswith": [
            "\u0905\u0902\u0936",
            "\u0915\u0923\u0940",
            "\u092a\u0915\u094d\u0937"
        ]
    },
    "mrj": {
        "keywords": [
            "\u0431\u0435\u0437",
            "\u0431\u0435\u0437\u0440\u0430\u043c\u043a\u0438",
            "\u0433\u0440\u0430\u043d\u0438\u0446\u0430",
            "\u0439\u044b\u043c\u0430\u043b\u043d\u0435",
            "\u043a\u04f1\u0448\u044b\u0447\u044b\u043d",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u043d\u0430\u0434",
            "\u043e\u0431\u0440\u0430\u043c\u0438\u0442\u044c",
            "\u043e\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u0435",
            "\u043f\u043e\u0434",
            "\u043f\u043e\u043a\u0448\u0435\u043b\u043d\u0435",
            "\u043f\u043e\u0441\u0435\u0440\u0435\u0434\u0438\u043d\u0435",
            "\u043f\u0443\u0440\u043b\u0430",
            "\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u043b\u0435\u0432\u0430",
            "\u0441\u043d\u0438\u0437\u0443",
            "\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u043d\u0438\u0437\u0443",
            "\u0446\u0435\u043d\u0442\u0440",
            "\u0447\u0435\u043a",
            "\u0448\u043e\u043b\u0430",
            "\u04f1\u043b\u044b\u0447\u044b\u043d",
            "\u04f1\u043c\u0431\u0430\u043b\u043d\u0435"
        ],
        "params": [
            "\u0430\u043b\u044c\u0442",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u0441\u044b\u043b\u043a\u0430",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430"
        ],
        "startswith": [
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430 ",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430 "
        ],
        "endswith": [
            "\u043f\u043a\u0441"
        ]
    },
    "ms": {
        "keywords": [
            "bingkai",
            "kanan",
            "kiri",
            "tengah",
            "tiada"
        ]
    },
    "mt": {
        "keywords": [
            "b'tilar",
            "ba\u017ci_tal-linja",
            "bid",
            "bla_tilar",
            "bordura",
            "burdura",
            "daqsminuri",
            "fuq",
            "lemin",
            "minuri",
            "nofs",
            "tajjeb",
            "ta\u0127t",
            "test-fuq",
            "test-ta\u0127t",
            "tilar",
            "tilat",
            "wieqaf",
            "xejn",
            "xellug",
            "\u010bentrali",
            "\u010bentru"
        ],
        "params": [
            "daqsminuri",
            "minuri",
            "pa\u0121na",
            "wieqaf",
            "\u0127olqa"
        ],
        "startswith": [
            "pa\u0121na ",
            "wieqaf "
        ]
    },
    "mwl": {
        "keywords": [
            "abaixo",
            "acima",
            "borda",
            "centro",
            "comborda",
            "commoldura",
            "direita",
            "dreita",
            "esquerda",
            "linhadebase",
            "meio",
            "miniatura",
            "miniaturadaimagem",
            "nanhun",
            "nenhum",
            "semborda",
            "semmoldura",
            "squierda",
            "superiordireito"
        ],
        "params": [
            "liga\u00e7\u00e3o",
            "miniatura",
            "miniaturadaimagem",
            "p\u00e1gina",
            "superiordireito"
        ],
        "startswith": [
            "p\u00e1gina ",
            "p\u00e1gina_",
            "superiordireito ",
            "superiordireito_"
        ]
    },
    "myv": {
        "keywords": [
            "\u0430\u043b\u043a\u0441",
            "\u0431\u0435\u0437",
            "\u0431\u0435\u0437\u0440\u0430\u043c\u043a\u0438",
            "\u0432\u0435\u0439\u043a\u0435\u044f\u043a_\u0430\u0440\u0430\u0441\u044c",
            "\u0432\u0435\u0440\u044c\u043a\u0441",
            "\u0432\u0438\u0442\u044c_\u043a\u0435\u0434\u044c",
            "\u0433\u0440\u0430\u043d\u0438\u0446\u0430",
            "\u043a\u0435\u043d\u0436\u0435\u0448\u043a\u0430",
            "\u043a\u0435\u0440\u0448_\u043a\u0435\u0434\u044c",
            "\u043a\u0443\u043d\u0434\u043e\u0432\u0442\u043e\u043c\u043e",
            "\u043a\u0443\u043d\u0434\u0441\u043e",
            "\u043a\u0443\u043d\u0448\u043a\u0430",
            "\u043a\u0443\u043d\u0448\u043a\u0430\u0441\u043e",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u043d\u0430\u0434",
            "\u043e\u0431\u0440\u0430\u043c\u0438\u0442\u044c",
            "\u043e\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u0435",
            "\u043f\u043e\u0434",
            "\u043f\u043e\u0441\u0435\u0440\u0435\u0434\u0438\u043d\u0435",
            "\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u043b\u0435\u0432\u0430",
            "\u0441\u043d\u0438\u0437\u0443",
            "\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0442\u0435\u043a\u0441\u0442-\u0430\u043b\u043a\u0441",
            "\u0442\u0435\u043a\u0441\u0442-\u0432\u0435\u0440\u044c\u043a\u0441",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u043d\u0438\u0437\u0443",
            "\u0446\u0435\u043d\u0442\u0440"
        ],
        "params": [
            "\u0430\u043b\u044c\u0442",
            "\u043b\u043e\u043f\u0430",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u0441\u044b\u043b\u043a\u0430",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430"
        ],
        "startswith": [
            "\u043b\u043e\u043f\u0430_",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430 ",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430 ",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430_"
        ],
        "endswith": [
            "\u043f\u043a\u0441"
        ]
    },
    "mzn": {
        "keywords": [
            "\u0627\u0646\u06af\u0634\u062a\u062f\u0627\u0646",
            "\u0627\u0646\u06af\u0634\u062a\u06cc",
            "\u0627\u06cc\u0633\u062a\u0627\u062f\u0647",
            "\u0628\u0627\u0644\u0627",
            "\u0628\u0646\u062f\u0627\u0646\u06af\u0634\u062a\u06cc",
            "\u0628\u06cc_\u0642\u0627\u0628",
            "\u0628\u06cc\u0642\u0627\u0628",
            "\u0628\u06cc\u200c\u0642\u0627\u0628",
            "\u062d\u0627\u0634\u06cc\u0647",
            "\u0631\u0627\u0633\u062a",
            "\u0632\u0628\u0631",
            "\u0632\u06cc\u0631",
            "\u0642\u0627\u0628",
            "\u0645\u062a\u0646-\u0628\u0627\u0644\u0627",
            "\u0645\u062a\u0646-\u067e\u0627\u06cc\u06cc\u0646",
            "\u0645\u06cc\u0627\u0646\u0647",
            "\u0647\u0645\u06a9\u0641",
            "\u0647\u06cc\u0686",
            "\u0648\u0633\u0637",
            "\u067e\u0627\u06cc\u06cc\u0646",
            "\u0686\u067e"
        ],
        "params": [
            "\u0627\u0646\u06af\u0634\u062a\u062f\u0627\u0646",
            "\u0627\u0646\u06af\u0634\u062a\u06cc",
            "\u0627\u06cc\u0633\u062a\u0627\u062f\u0647",
            "\u0628\u0646\u062f\u0627\u0646\u06af\u0634\u062a\u06cc",
            "\u062c\u0627\u06cc\u06af\u0632\u06cc\u0646",
            "\u0632\u0628\u0627\u0646",
            "\u0635\u0641\u062d\u0647",
            "\u067e\u06cc\u0648\u0646\u062f",
            "\u06a9\u0644\u0627\u0633"
        ],
        "startswith": [
            "\u0627\u06cc\u0633\u062a\u0627\u062f\u0647_",
            "\u0635\u0641\u062d\u0647_"
        ],
        "endswith": [
            "\u067e\u06cc\u06a9\u0633\u0644"
        ]
    },
    "nah": {
        "keywords": [
            "abajo",
            "arriba",
            "borde",
            "centrada",
            "centrado",
            "centrar",
            "centro",
            "dcha",
            "der",
            "derecha",
            "enmarcada",
            "enmarcado",
            "izda",
            "izq",
            "izquierda",
            "marco",
            "medio",
            "mini",
            "miniatura",
            "miniaturadeimagen",
            "nada",
            "ninguna",
            "ninguno",
            "no",
            "sin_enmarcar",
            "sinenmarcar",
            "sinmarco"
        ],
        "params": [
            "enlace",
            "idioma",
            "miniatura",
            "miniaturadeimagen",
            "pagina",
            "p\u00e1gina",
            "vinculo",
            "v\u00ednculo"
        ],
        "startswith": [
            "pagina_",
            "p\u00e1gina_"
        ]
    },
    "nap": {
        "keywords": [
            "bordo",
            "centro",
            "destra",
            "incorniciato",
            "met\u00e0",
            "min",
            "miniatura",
            "nessuno",
            "originale",
            "pedice",
            "riquadrato",
            "senza_cornice",
            "sinistra",
            "sopra",
            "sotto",
            "testo-sopra",
            "testo-sotto",
            "verticale"
        ],
        "params": [
            "min",
            "miniatura",
            "pagina",
            "verticale"
        ],
        "startswith": [
            "pagina_",
            "verticale_"
        ]
    },
    "nds": {
        "keywords": [
            "duum",
            "gerahmt",
            "grundlinie",
            "hoch",
            "hochgestellt",
            "hochkant",
            "keen",
            "links",
            "merrn",
            "mini",
            "miniatur",
            "mitte",
            "oben",
            "ohne",
            "rahmenlos",
            "rahmt",
            "rand",
            "rechts",
            "text-oben",
            "text-unten",
            "tief",
            "tiefgestellt",
            "unten",
            "zentriert"
        ],
        "params": [
            "alternativtext",
            "hochkant",
            "klasse",
            "mini",
            "miniatur",
            "seite",
            "sprache",
            "verweis"
        ],
        "startswith": [
            "hochkant ",
            "hochkant_",
            "seite ",
            "seite_"
        ]
    },
    "nds-nl": {
        "keywords": [
            "beneden",
            "benejen",
            "boven",
            "doem",
            "duum",
            "esentreerd",
            "gecentreerd",
            "geen",
            "gien",
            "grondliende",
            "grondlijn",
            "kaderloos",
            "kaoderloos",
            "links",
            "midden",
            "mini",
            "miniatuur",
            "omkaderd",
            "raand",
            "rand",
            "rechtop",
            "rechts",
            "tekst-beneden",
            "tekst-boven",
            "tekste-benejen",
            "tekste-boven",
            "umraand"
        ],
        "params": [
            "doemnaegel",
            "duumnegel",
            "klasse",
            "koppeling",
            "miniatuur",
            "pagina",
            "rechtop",
            "taal",
            "verwiezing",
            "verwijzing",
            "zied"
        ],
        "startswith": [
            "pagina ",
            "pagina_",
            "rechtop",
            "zied_"
        ]
    },
    "nia": {
        "keywords": [
            "atas",
            "atas-teks",
            "atek",
            "batas",
            "batek",
            "bawah",
            "bawah-teks",
            "bing",
            "bingkai",
            "gada",
            "garis_dasar",
            "jempol",
            "jmpl",
            "ka",
            "kanan",
            "ki",
            "kiri",
            "lurus",
            "mini",
            "miniatur",
            "nir",
            "nirbing",
            "pus",
            "pusat",
            "tanpa",
            "tanpabingkai",
            "tegak",
            "tengah",
            "tepi",
            "upa"
        ],
        "params": [
            "al",
            "alternatif",
            "bhs",
            "hal",
            "halaman",
            "jempol",
            "jmpl",
            "lurus",
            "mini",
            "miniatur",
            "pra",
            "pranala",
            "tegak"
        ],
        "startswith": [
            "hal_",
            "halaman_",
            "lurus_",
            "tegak_"
        ]
    },
    "nl": {
        "keywords": [
            "beneden",
            "boven",
            "gecentreerd",
            "geen",
            "grondlijn",
            "kaderloos",
            "links",
            "midden",
            "miniatuur",
            "omkaderd",
            "rand",
            "rechtop",
            "rechts",
            "tekst-beneden",
            "tekst-boven"
        ],
        "params": [
            "klasse",
            "koppeling",
            "miniatuur",
            "pagina",
            "rechtop",
            "taal",
            "verwijzing"
        ],
        "startswith": [
            "pagina_",
            "rechtop"
        ]
    },
    "nn": {
        "keywords": [
            "bunn",
            "grunnlinje",
            "h\u00f8gre",
            "h\u00f8yre",
            "ingen",
            "ingenramme",
            "midt",
            "midtstilt",
            "mini",
            "miniatyr",
            "portrett",
            "ramma",
            "ramme",
            "rammelaus",
            "rammel\u00f8s",
            "senter",
            "sentrer",
            "sentrum",
            "tekst-bunn",
            "topp",
            "venstre"
        ],
        "params": [
            "lenke",
            "lenkje",
            "mini",
            "miniatyr",
            "portrett",
            "side",
            "spr\u00e5k"
        ],
        "startswith": [
            "portrett_",
            "side ",
            "side_"
        ],
        "endswith": [
            "pk"
        ]
    },
    "no": {
        "keywords": [
            "bunn",
            "grunnlinje",
            "h\u00f8gre",
            "h\u00f8yre",
            "ingen",
            "ingenramme",
            "midt",
            "midtstilt",
            "mini",
            "miniatyr",
            "portrett",
            "ramma",
            "ramme",
            "rammelaus",
            "rammel\u00f8s",
            "senter",
            "sentrer",
            "sentrum",
            "tekst-bunn",
            "topp",
            "venstre"
        ],
        "params": [
            "lenke",
            "lenkje",
            "mini",
            "miniatyr",
            "portrett",
            "side",
            "spr\u00e5k"
        ],
        "startswith": [
            "portrett_",
            "side ",
            "side_"
        ],
        "endswith": [
            "pk"
        ]
    },
    "nrm": {
        "keywords": [
            "bas",
            "bas-texte",
            "bas-txt",
            "base",
            "bordure",
            "cadre",
            "centr\u00e9",
            "droite",
            "encadre",
            "encadr\u00e9",
            "exp",
            "exposant",
            "gauche",
            "haut",
            "haut-texte",
            "haut-txt",
            "ind",
            "indice",
            "ligne-de-base",
            "milieu",
            "neant",
            "non_encadre",
            "non_encadr\u00e9",
            "n\u00e9ant",
            "redresse",
            "sans_cadre",
            "vignette"
        ],
        "params": [
            "classe",
            "langue",
            "lien",
            "redresse",
            "vignette"
        ],
        "startswith": [
            "redresse_"
        ]
    },
    "oc": {
        "keywords": [
            "baix",
            "baix-text",
            "bas",
            "bas-texte",
            "bas-txt",
            "bas-t\u00e8xte",
            "base",
            "bordadura",
            "bordure",
            "cadre",
            "cap",
            "centrat",
            "centr\u00e9",
            "dalt",
            "dalt-text",
            "drecha",
            "dreta",
            "droite",
            "encadre",
            "encadr\u00e9",
            "enquagrat",
            "esquerra",
            "esqu\u00e8rra",
            "exp",
            "exposant",
            "gaucha",
            "gauche",
            "haut",
            "haut-texte",
            "haut-txt",
            "ind",
            "indice",
            "indici",
            "ligne-de-base",
            "linha_de_basa",
            "l\u00ednia de base",
            "marc",
            "milieu",
            "miniatura",
            "mitan",
            "mitj\u00e0",
            "naut",
            "naut-txt",
            "naut-t\u00e8xte",
            "neant",
            "non_encadre",
            "non_encadr\u00e9",
            "nonr\u00e9s",
            "n\u00e9ant",
            "quadre",
            "redresse",
            "redre\u00e7a",
            "redre\u00e7at",
            "sans_cadre",
            "sens_quadre",
            "sense marc",
            "sen\u00e8stra",
            "vignette",
            "vinheta",
            "vora"
        ],
        "params": [
            "classe",
            "enlla\u00e7",
            "idioma",
            "langue",
            "lien",
            "ligam",
            "llengua",
            "miniatura",
            "p\u00e0gina",
            "redresse",
            "redre\u00e7at",
            "vignette",
            "vinheta"
        ],
        "startswith": [
            "p\u00e0gina ",
            "redresse_",
            "redre\u00e7a",
            "redre\u00e7a ",
            "redre\u00e7at "
        ]
    },
    "olo": {
        "keywords": [
            "alaindeksi",
            "alas",
            "alhaalla",
            "kehykset\u00f6n",
            "kehys",
            "kehystetty",
            "keskell\u00e4",
            "keski",
            "keskitetty",
            "oikea",
            "perustaso",
            "pienois",
            "pienoiskuva",
            "pysty",
            "reunus",
            "tyhj\u00e4",
            "vasen",
            "ylh\u00e4\u00e4ll\u00e4",
            "yl\u00e4indeksi",
            "yl\u00e4oikea",
            "yl\u00f6s"
        ],
        "params": [
            "linkki",
            "pienois",
            "pienoiskuva",
            "pysty",
            "sivu",
            "yl\u00e4oikea"
        ],
        "startswith": [
            "pysty_",
            "sivu_",
            "yl\u00e4oikea_"
        ]
    },
    "or": {
        "keywords": [
            "\u0b09\u0b2a\u0b30",
            "\u0b15\u0b3f\u0b1b\u0b3f_\u0b28\u0b41\u0b39\u0b47\u0b01",
            "\u0b15\u0b47\u0b28\u0b4d\u0b26\u0b4d\u0b30",
            "\u0b21\u0b3e\u0b39\u0b3e\u0b23",
            "\u0b24\u0b33",
            "\u0b2b\u0b4d\u0b30\u0b47\u0b2e\u0b15\u0b30\u0b3e",
            "\u0b2b\u0b4d\u0b30\u0b47\u0b2e\u0b28\u0b25\u0b3f\u0b2c\u0b3e",
            "\u0b2c\u0b30\u0b4d\u0b21\u0b30",
            "\u0b2c\u0b3e\u0b06\u0b01",
            "\u0b2c\u0b47\u0b38\u0b32\u0b3e\u0b07\u0b28",
            "\u0b2e\u0b1d\u0b3f",
            "\u0b32\u0b47\u0b16\u0b3e-\u0b09\u0b2a\u0b30",
            "\u0b32\u0b47\u0b16\u0b3e-\u0b24\u0b33"
        ],
        "params": [
            "\u0b26\u0b47\u0b16\u0b23\u0b3e",
            "\u0b28\u0b16\u0b26\u0b47\u0b16\u0b23\u0b3e",
            "\u0b32\u0b3f\u0b19\u0b4d\u0b15"
        ],
        "endswith": [
            "_\u0b2a\u0b3f\u0b15\u0b38\u0b47\u0b32"
        ]
    },
    "os": {
        "keywords": [
            "\u00e6\u043d\u00e6",
            "\u0430\u0441\u0442\u00e6\u0443",
            "\u0431\u0435\u0437",
            "\u0431\u0435\u0437\u0440\u0430\u043c\u043a\u0438",
            "\u0433\u0430\u043b\u0438\u0443",
            "\u0433\u0440\u0430\u043d\u0438\u0446\u0430",
            "\u043a\u044a\u0430\u0434\u0434\u00e6\u0440",
            "\u043a\u044a\u0430\u0434\u0434\u00e6\u0440\u0433\u043e\u043d\u0434",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u043d\u0430\u0434",
            "\u043e\u0431\u0440\u0430\u043c\u0438\u0442\u044c",
            "\u043e\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u0435",
            "\u043f\u043e\u0434",
            "\u043f\u043e\u0441\u0435\u0440\u0435\u0434\u0438\u043d\u0435",
            "\u0440\u0430\u0445\u0438\u0437",
            "\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u043b\u0435\u0432\u0430",
            "\u0441\u043d\u0438\u0437\u0443",
            "\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u043d\u0438\u0437\u0443",
            "\u0446\u0435\u043d\u0442\u0440"
        ],
        "params": [
            "\u0430\u043b\u044c\u0442",
            "\u043a\u044a\u0430\u0434\u0434\u00e6\u0440",
            "\u043a\u044a\u0430\u0434\u0434\u00e6\u0440\u0433\u043e\u043d\u0434",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u0441\u044b\u043b\u043a\u0430",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430"
        ],
        "startswith": [
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430 ",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430 "
        ],
        "endswith": [
            "\u043f\u043a\u0441"
        ]
    },
    "pcd": {
        "keywords": [
            "bas",
            "bas-texte",
            "bas-txt",
            "base",
            "bordure",
            "cadre",
            "centr\u00e9",
            "droite",
            "encadre",
            "encadr\u00e9",
            "exp",
            "exposant",
            "gauche",
            "haut",
            "haut-texte",
            "haut-txt",
            "ind",
            "indice",
            "ligne-de-base",
            "milieu",
            "neant",
            "non_encadre",
            "non_encadr\u00e9",
            "n\u00e9ant",
            "redresse",
            "sans_cadre",
            "vignette"
        ],
        "params": [
            "classe",
            "langue",
            "lien",
            "redresse",
            "vignette"
        ],
        "startswith": [
            "redresse_"
        ]
    },
    "pdc": {
        "keywords": [
            "gerahmt",
            "grundlinie",
            "hoch",
            "hochgestellt",
            "hochkant",
            "links",
            "mini",
            "miniatur",
            "mitte",
            "oben",
            "ohne",
            "rahmenlos",
            "rand",
            "rechts",
            "text-oben",
            "text-unten",
            "tief",
            "tiefgestellt",
            "unten",
            "zentriert"
        ],
        "params": [
            "alternativtext",
            "hochkant",
            "klasse",
            "mini",
            "miniatur",
            "seite",
            "sprache",
            "verweis"
        ],
        "startswith": [
            "hochkant ",
            "hochkant_",
            "seite ",
            "seite_"
        ]
    },
    "pfl": {
        "keywords": [
            "gerahmt",
            "grundlinie",
            "hoch",
            "hochgestellt",
            "hochkant",
            "links",
            "mini",
            "miniatur",
            "mitte",
            "oben",
            "ohne",
            "rahmenlos",
            "rand",
            "rechts",
            "text-oben",
            "text-unten",
            "tief",
            "tiefgestellt",
            "unten",
            "zentriert"
        ],
        "params": [
            "alternativtext",
            "hochkant",
            "klasse",
            "mini",
            "miniatur",
            "seite",
            "sprache",
            "verweis"
        ],
        "startswith": [
            "hochkant ",
            "hochkant_",
            "seite ",
            "seite_"
        ]
    },
    "pl": {
        "keywords": [
            "bez_ramki",
            "bezramki",
            "brak",
            "centruj",
            "d\u00f3\u0142",
            "g\u00f3ra",
            "lewo",
            "ma\u0142y",
            "prawo",
            "ramka",
            "t\u0142o",
            "\u015brodek"
        ],
        "params": [
            "ma\u0142y",
            "strona"
        ]
    },
    "pms": {
        "keywords": [
            "bordo",
            "centro",
            "destra",
            "incorniciato",
            "met\u00e0",
            "min",
            "miniatura",
            "nessuno",
            "originale",
            "pedice",
            "riquadrato",
            "senza_cornice",
            "sinistra",
            "sopra",
            "sotto",
            "testo-sopra",
            "testo-sotto",
            "verticale"
        ],
        "params": [
            "min",
            "miniatura",
            "pagina",
            "verticale"
        ],
        "startswith": [
            "pagina_",
            "verticale_"
        ]
    },
    "pnt": {
        "keywords": [
            "\u03ac\u03bd\u03c9",
            "\u03b1\u03c1\u03b9\u03c3\u03c4\u03b5\u03c1\u03ac",
            "\u03b3\u03c1\u03b1\u03bc\u03bc\u03ae\u03b2\u03ac\u03c3\u03b7\u03c2",
            "\u03b4\u03b5\u03af\u03ba\u03c4\u03b7\u03c2",
            "\u03b4\u03b5\u03be\u03b9\u03ac",
            "\u03b5\u03ba\u03b8\u03ad\u03c4\u03b7\u03c2",
            "\u03ba\u03ac\u03c4\u03c9",
            "\u03ba\u03ac\u03c4\u03c9-\u03b1\u03c0\u03cc-\u03c4\u03bf-\u03ba\u03b5\u03af\u03bc\u03b5\u03bd\u03bf",
            "\u03ba\u03ad\u03bd\u03c4\u03c1\u03bf",
            "\u03ba\u03b1\u03b8\u03cc\u03bb\u03bf\u03c5",
            "\u03ba\u03b1\u03c4\u03b1\u03ba\u03cc\u03c1\u03c5\u03c6\u03b1",
            "\u03bc\u03ad\u03c3\u03bf",
            "\u03bc\u03b5-\u03c0\u03bb\u03b1\u03af\u03c3\u03b9\u03bf",
            "\u03bc\u03b9\u03ba\u03c1\u03bf\u03b3\u03c1\u03b1\u03c6\u03af\u03b1",
            "\u03bc\u03b9\u03bd\u03b9\u03b1\u03c4\u03bf\u03cd\u03c1\u03b1",
            "\u03c0\u03ac\u03bd\u03c9-\u03b1\u03c0\u03cc-\u03c4\u03bf-\u03ba\u03b5\u03af\u03bc\u03b5\u03bd\u03bf",
            "\u03c0\u03bb\u03b1\u03af\u03c3\u03b9\u03bf",
            "\u03c7\u03c9\u03c1\u03af\u03c2-\u03c0\u03bb\u03b1\u03af\u03c3\u03b9\u03bf"
        ],
        "params": [
            "\u03b5\u03bd\u03b1\u03bb\u03bb.",
            "\u03ba\u03b1\u03c4\u03b1\u03ba\u03cc\u03c1\u03c5\u03c6\u03b1",
            "\u03bc\u03b9\u03ba\u03c1\u03bf\u03b3\u03c1\u03b1\u03c6\u03af\u03b1",
            "\u03bc\u03b9\u03bd\u03b9\u03b1\u03c4\u03bf\u03cd\u03c1\u03b1",
            "\u03c3\u03b5\u03bb\u03af\u03b4\u03b1",
            "\u03c3\u03cd\u03bd\u03b4\u03b5\u03c3\u03bc\u03bf\u03c2"
        ],
        "startswith": [
            "\u03ba\u03b1\u03c4\u03b1\u03ba\u03cc\u03c1\u03c5\u03c6\u03b1_",
            "\u03c3\u03b5\u03bb\u03af\u03b4\u03b1_"
        ],
        "endswith": [
            "\u03b5\u03c3"
        ]
    },
    "ps": {
        "keywords": [
            "\u0628\u067c\u0646\u0648\u06a9",
            "\u0645\u06d0\u0646\u0681\u060c_center",
            "\u0647\u06d0\u0685",
            "\u069a\u064a",
            "\u06a9\u064a\u06bc"
        ]
    },
    "pt": {
        "keywords": [
            "abaixo",
            "acima",
            "borda",
            "centro",
            "comborda",
            "commoldura",
            "direita",
            "esquerda",
            "linhadebase",
            "meio",
            "miniatura",
            "miniaturadaimagem",
            "nenhum",
            "semborda",
            "semmoldura",
            "superiordireito"
        ],
        "params": [
            "liga\u00e7\u00e3o",
            "miniatura",
            "miniaturadaimagem",
            "p\u00e1gina",
            "superiordireito"
        ],
        "startswith": [
            "p\u00e1gina ",
            "p\u00e1gina_",
            "superiordireito ",
            "superiordireito_"
        ]
    },
    "pwn": {
        "keywords": [
            "\u4e0a\u6a19",
            "\u4e0b\u6a19",
            "\u4e2d\u95f4",
            "\u53f3",
            "\u53f3\u4e0a",
            "\u5782\u76f4\u7f6e\u4e2d",
            "\u5782\u76f4\u7f6e\u5e95",
            "\u5782\u76f4\u7f6e\u9802",
            "\u57fa\u7ebf",
            "\u5b50",
            "\u5c45\u4e2d",
            "\u5de6",
            "\u5e95\u90e8",
            "\u6587\u5b57\u5e95\u90e8",
            "\u6587\u5b57\u7f6e\u5e95",
            "\u6587\u5b57\u7f6e\u9802",
            "\u6587\u5b57\u9876\u90e8",
            "\u65e0",
            "\u65e0\u6846",
            "\u66ff\u4ee3\u6587\u5b57",
            "\u6709\u6846",
            "\u7121",
            "\u7121\u6846",
            "\u7e2e\u5716",
            "\u7f29\u7565\u56fe",
            "\u7f6e\u4e2d",
            "\u8d85",
            "\u8fb9\u6846",
            "\u908a\u6846",
            "\u9876\u90e8"
        ],
        "params": [
            "\u53f3\u4e0a",
            "\u66ff\u4ee3",
            "\u66ff\u4ee3\u6587\u672c",
            "\u7c7b",
            "\u7e2e\u5716",
            "\u7f29\u7565\u56fe",
            "\u8a9e\u8a00",
            "\u8bed\u8a00",
            "\u9023\u7d50",
            "\u94fe\u63a5",
            "\u9801",
            "\u985e\u5225",
            "\u9875\u6570"
        ],
        "startswith": [
            "\u53f3\u4e0a"
        ],
        "endswith": [
            "\u50cf\u7d20",
            "\u9801",
            "\u9875"
        ]
    },
    "qu": {
        "keywords": [
            "abajo",
            "alliq",
            "arriba",
            "borde",
            "centrada",
            "centrado",
            "centrar",
            "centro",
            "chawpi",
            "dcha",
            "der",
            "derecha",
            "enmarcada",
            "enmarcado",
            "hanan",
            "hawa",
            "ichuq",
            "inchu",
            "inchunnaq",
            "inchuyuq",
            "izda",
            "izq",
            "izquierda",
            "lluqi",
            "mana",
            "manaima",
            "marco",
            "medio",
            "mini",
            "miniatura",
            "miniaturadeimagen",
            "nada",
            "ninguna",
            "ninguno",
            "no",
            "pa\u00f1a",
            "qillqahawa",
            "qillqasiki",
            "rikchacha",
            "sayaq",
            "saywa",
            "sikipi",
            "sin_embarcar",
            "sin_enmarcar",
            "sinenmarcar",
            "sinmarco",
            "tiksisiqi",
            "ukhupi",
            "uran"
        ],
        "params": [
            "enlace",
            "idioma",
            "miniatura",
            "miniaturadeimagen",
            "pagina",
            "panqa",
            "p\u00e1gina",
            "rikchacha",
            "sayaq",
            "tinki",
            "vinculo",
            "v\u00ednculo",
            "wak"
        ],
        "startswith": [
            "pagina_",
            "p\u00e1gina_"
        ]
    },
    "rm": {
        "keywords": [
            "miniatura",
            "sidretg"
        ],
        "params": [
            "miniatura",
            "sidretg"
        ],
        "startswith": [
            "sidretg_"
        ]
    },
    "rmy": {
        "keywords": [
            "cadru",
            "centru",
            "chenar",
            "dreapta",
            "dreaptasus",
            "exponent",
            "faracadru",
            "indice",
            "jos",
            "linia_de_baz\u0103",
            "mijloc",
            "mini",
            "miniatura",
            "nu",
            "stanga",
            "sus",
            "text-jos",
            "text-sus"
        ],
        "params": [
            "dreaptasus",
            "leg\u0103tur\u0103",
            "mini",
            "miniatura",
            "pagina"
        ],
        "startswith": [
            "dreaptasus ",
            "pagina "
        ]
    },
    "ro": {
        "keywords": [
            "cadru",
            "centru",
            "chenar",
            "dreapta",
            "dreaptasus",
            "exponent",
            "faracadru",
            "indice",
            "jos",
            "linia_de_baz\u0103",
            "mijloc",
            "mini",
            "miniatura",
            "nu",
            "stanga",
            "sus",
            "text-jos",
            "text-sus"
        ],
        "params": [
            "dreaptasus",
            "leg\u0103tur\u0103",
            "mini",
            "miniatura",
            "pagina"
        ],
        "startswith": [
            "dreaptasus ",
            "pagina "
        ]
    },
    "roa-rup": {
        "keywords": [
            "cadru",
            "centru",
            "chenar",
            "dreapta",
            "dreaptasus",
            "exponent",
            "faracadru",
            "indice",
            "jos",
            "linia_de_baz\u0103",
            "mijloc",
            "mini",
            "miniatura",
            "nu",
            "stanga",
            "sus",
            "text-jos",
            "text-sus"
        ],
        "params": [
            "dreaptasus",
            "leg\u0103tur\u0103",
            "mini",
            "miniatura",
            "pagina"
        ],
        "startswith": [
            "dreaptasus ",
            "pagina "
        ]
    },
    "roa-tara": {
        "keywords": [
            "bordo",
            "centro",
            "destra",
            "incorniciato",
            "met\u00e0",
            "min",
            "miniatura",
            "nessuno",
            "originale",
            "pedice",
            "riquadrato",
            "senza_cornice",
            "sinistra",
            "sopra",
            "sotto",
            "testo-sopra",
            "testo-sotto",
            "verticale"
        ],
        "params": [
            "min",
            "miniatura",
            "pagina",
            "verticale"
        ],
        "startswith": [
            "pagina_",
            "verticale_"
        ]
    },
    "ru": {
        "keywords": [
            "\u0431\u0435\u0437",
            "\u0431\u0435\u0437\u0440\u0430\u043c\u043a\u0438",
            "\u0433\u0440\u0430\u043d\u0438\u0446\u0430",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u043d\u0430\u0434",
            "\u043e\u0431\u0440\u0430\u043c\u0438\u0442\u044c",
            "\u043e\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u0435",
            "\u043f\u043e\u0434",
            "\u043f\u043e\u0441\u0435\u0440\u0435\u0434\u0438\u043d\u0435",
            "\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u043b\u0435\u0432\u0430",
            "\u0441\u043d\u0438\u0437\u0443",
            "\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u043d\u0438\u0437\u0443",
            "\u0446\u0435\u043d\u0442\u0440"
        ],
        "params": [
            "\u0430\u043b\u044c\u0442",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u0441\u044b\u043b\u043a\u0430",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430"
        ],
        "startswith": [
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430 ",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430 "
        ],
        "endswith": [
            "\u043f\u043a\u0441"
        ]
    },
    "rue": {
        "keywords": [
            "\u0431\u0435\u0437",
            "\u0431\u0435\u0437\u0440\u0430\u043c\u043a\u0438",
            "\u0433\u0440\u0430\u043d\u0438\u0446\u0430",
            "\u0433\u0440\u0430\u043d\u0438\u0446\u044f",
            "\u0437\u0432\u0435\u0440\u0445\u0443",
            "\u0437\u0432\u0435\u0440\u0445\u0443\u043f\u0440\u0430\u0432\u043e\u0440\u0443\u0447",
            "\u0437\u043d\u0438\u0437\u0443",
            "\u043b\u0456\u0432\u043e\u0440\u0443\u0447",
            "\u043c\u0435\u0436\u0430",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u043c\u0456\u043d\u0456",
            "\u043c\u0456\u043d\u0456\u0430\u0442\u044e\u0440\u0430",
            "\u043d\u0430\u0434",
            "\u043e\u0431\u0440\u0430\u043c\u0438\u0442\u0438",
            "\u043e\u0431\u0440\u0430\u043c\u0438\u0442\u044c",
            "\u043e\u0441\u043d\u043e\u0432\u0430",
            "\u043e\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u0435",
            "\u043f\u043e\u0434",
            "\u043f\u043e\u0441\u0435\u0440\u0435\u0434\u0438\u043d\u0435",
            "\u043f\u043e\u0441\u0435\u0440\u0435\u0434\u0438\u043d\u0456",
            "\u043f\u0440\u0430\u0432\u043e\u0440\u0443\u0447",
            "\u043f\u0456\u0434",
            "\u0440\u0430\u043c\u043a\u0430",
            "\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u043b\u0435\u0432\u0430",
            "\u0441\u043d\u0438\u0437\u0443",
            "\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0442\u0435\u043a\u0441\u0442-\u0437\u0432\u0435\u0440\u0445\u0443",
            "\u0442\u0435\u043a\u0441\u0442-\u0437\u043d\u0438\u0437\u0443",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u043d\u0438\u0437\u0443",
            "\u0446\u0435\u043d\u0442\u0440"
        ],
        "params": [
            "\u0430\u043b\u044c\u0442",
            "\u0437\u0432\u0435\u0440\u0445\u0443\u043f\u0440\u0430\u0432\u043e\u0440\u0443\u0447",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u043c\u0456\u043d\u0456",
            "\u043c\u0456\u043d\u0456\u0430\u0442\u044e\u0440\u0430",
            "\u043f\u043e\u0441\u0438\u043b\u0430\u043d\u043d\u044f",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u0441\u044b\u043b\u043a\u0430",
            "\u0441\u0442\u043e\u0440\u0456\u043d\u043a\u0430",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430"
        ],
        "startswith": [
            "\u0437\u0432\u0435\u0440\u0445\u0443\u043f\u0440\u0430\u0432\u043e\u0440\u0443\u0447_",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430 ",
            "\u0441\u0442\u043e\u0440\u0456\u043d\u043a\u0430_",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430 "
        ],
        "endswith": [
            "\u043f\u043a\u0441"
        ]
    },
    "sa": {
        "keywords": [
            "\u0905\u0902\u0917\u0942\u0920\u093e",
            "\u0905\u0902\u0917\u0942\u0920\u093e\u0915\u093e\u0930",
            "\u0905\u0917\u094d\u0930",
            "\u0905\u0919\u094d\u0917\u0941\u0937\u094d\u0920",
            "\u0905\u0919\u094d\u0917\u0941\u0937\u094d\u0920\u091a\u093f\u0924\u094d\u0930\u092e\u094d",
            "\u0905\u0924\u093f",
            "\u0905\u0927\u0903",
            "\u0905\u0927\u0938",
            "\u0906\u0927\u093e\u0930_\u0930\u0947\u0916\u093e",
            "\u0906\u0927\u093e\u0930\u0930\u0947\u0916\u093e",
            "\u0906\u092c\u0928\u094d\u0927",
            "\u0906\u092c\u0928\u094d\u0927\u0903",
            "\u0909\u0928\u094d\u0928\u0924",
            "\u0915\u093f\u0928\u093e\u0930\u093e",
            "\u0915\u093f\u092e\u092a\u093f_\u0928",
            "\u0915\u0947\u0902\u0926\u094d\u0930",
            "\u0915\u0947\u0902\u0926\u094d\u0930\u093f\u0924",
            "\u0915\u0947\u0928\u094d\u0926\u094d\u0930",
            "\u0915\u0947\u0928\u094d\u0926\u094d\u0930\u092e\u094d",
            "\u0915\u0947\u0928\u094d\u0926\u094d\u0930\u093f\u0924",
            "\u0915\u094b\u0908_\u0928\u0939\u0940\u0902",
            "\u0916\u0921\u093c\u0940",
            "\u091a\u093f\u0924\u094d\u0930\u0917\u092e\u093f\u0915\u093e",
            "\u091a\u093f\u0924\u094d\u0930\u0938\u0942\u091a\u0915\u092e\u094d",
            "\u0924\u0932",
            "\u0924\u0940\u0935\u094d\u0930",
            "\u0926\u0915\u094d\u0937\u093f\u0923\u0924",
            "\u0926\u0915\u094d\u0937\u093f\u0923\u0924\u0903",
            "\u0926\u093e\u090f\u0901",
            "\u0926\u093e\u090f\u0902",
            "\u0926\u093e\u092f\u0947\u0902",
            "\u0928\u093f\u0930\u093e\u092c\u0928\u094d\u0927",
            "\u0928\u093f\u0930\u093e\u092c\u0928\u094d\u0927\u0903",
            "\u0928\u0948\u0935",
            "\u092a\u0926",
            "\u092a\u093e\u0920-\u0924\u0932",
            "\u092a\u093e\u0920-\u0936\u0940\u0930\u094d\u0937",
            "\u092a\u093e\u0920\u094d\u092f-\u0905\u0917\u094d\u0930",
            "\u092a\u093e\u0920\u094d\u092f-\u0905\u0927\u0903",
            "\u092a\u093e\u0920\u094d\u092f-\u0905\u0927\u0938",
            "\u092a\u093e\u0920\u094d\u092f-\u0936\u0940\u0930\u094d\u0937\u092e\u094d",
            "\u092b\u093c\u094d\u0930\u0947\u092e",
            "\u092b\u093c\u094d\u0930\u0947\u092e\u0939\u0940\u0928",
            "\u092b\u094d\u0930\u0947\u092e",
            "\u092b\u094d\u0930\u0947\u092e\u0939\u0940\u0928",
            "\u092c\u093e\u090f\u0901",
            "\u092c\u093e\u090f\u0902",
            "\u092c\u093e\u092f\u0947\u0902",
            "\u092c\u0949\u0930\u094d\u0921\u0930",
            "\u092e\u0927\u094d\u092f",
            "\u092e\u0927\u094d\u092f\u0947",
            "\u092e\u0942\u0930\u094d\u0927",
            "\u0932\u0918\u0941\u091a\u093f\u0924\u094d\u0930\u092e\u094d",
            "\u0932\u0918\u0941\u0924\u094d\u0924\u092e",
            "\u0935\u093e\u092e\u0924\u0903",
            "\u0935\u093f\u0937\u092f\u0947",
            "\u0936\u0940\u0930\u094d\u0937",
            "\u0936\u0940\u0930\u094d\u0937\u0926\u0915\u094d\u0937\u093f\u0923\u0924\u0903",
            "\u0936\u0940\u0930\u094d\u0937\u092e\u094d",
            "\u0936\u0940\u0930\u094d\u0937\u0938\u0919\u094d\u0916\u094d\u092f\u093e",
            "\u0938\u0919\u094d\u0915\u0941\u091a\u093f\u0924\u091a\u093f\u0924\u094d\u0930",
            "\u0938\u0919\u094d\u0915\u0941\u091a\u093f\u0924\u091a\u093f\u0924\u094d\u0930\u092e\u094d",
            "\u0938\u0940\u092e\u093e"
        ],
        "params": [
            "\u0905\u0902\u0917\u0942\u0920\u093e",
            "\u0905\u0902\u0917\u0942\u0920\u093e\u0915\u093e\u0930",
            "\u0905\u0919\u094d\u0917\u0941\u0937\u094d\u0920",
            "\u0905\u0919\u094d\u0917\u0941\u0937\u094d\u0920\u091a\u093f\u0924\u094d\u0930\u092e\u094d",
            "\u0909\u0928\u094d\u0928\u0924",
            "\u0915\u0921\u093c\u0940",
            "\u0916\u0921\u093c\u0940",
            "\u091a\u093f\u0924\u094d\u0930\u092a\u0930\u093f\u0938\u0928\u094d\u0927\u093f\u0903",
            "\u091a\u093f\u0924\u094d\u0930\u092a\u093e\u0920\u094d\u092f\u092e\u094d",
            "\u091a\u093f\u0924\u094d\u0930\u092a\u0943\u0937\u094d\u0920\u092e\u094d",
            "\u092a\u093e\u0920",
            "\u092a\u0943\u0937\u094d\u0920",
            "\u092d\u093e\u0937\u093e",
            "\u0932\u0918\u0941\u091a\u093f\u0924\u094d\u0930\u092e\u094d",
            "\u0932\u0918\u0941\u0924\u094d\u0924\u092e\u091a\u093f\u0924\u094d\u0930",
            "\u0935\u0930\u094d\u0917",
            "\u0935\u093f\u0915\u0932\u094d\u092a",
            "\u0936\u0940\u0930\u094d\u0937\u0926\u0915\u094d\u0937\u093f\u0923\u0924\u0903",
            "\u0938\u0919\u094d\u0915\u0941\u091a\u093f\u0924\u091a\u093f\u0924\u094d\u0930",
            "\u0938\u0919\u094d\u0915\u0941\u091a\u093f\u0924\u091a\u093f\u0924\u094d\u0930\u092e\u094d",
            "\u0938\u092e\u094d\u092c\u0926\u094d\u0927\u0902"
        ],
        "startswith": [
            "\u0909\u0928\u094d\u0928\u0924 ",
            "\u0916\u0921\u093c\u0940_",
            "\u091a\u093f\u0924\u094d\u0930\u092a\u0943\u0937\u094d\u0920\u092e\u094d_",
            "\u092a\u0943\u0937\u094d\u0920 ",
            "\u092a\u0943\u0937\u094d\u0920_",
            "\u0936\u0940\u0930\u094d\u0937\u0926\u0915\u094d\u0937\u093f\u0923\u0924\u0903_"
        ],
        "endswith": [
            "\u0905\u0923\u0935\u0903",
            "\u092a\u093f\u0915\u094d\u0938\u0947\u0932",
            "\u092a\u093f\u091f"
        ]
    },
    "sah": {
        "keywords": [
            "\u0430\u043b\u043b\u0430\u0440\u0430\u0430",
            "\u0430\u043b\u044b\u043d",
            "\u0431\u0435\u0437",
            "\u0431\u0435\u0437\u0440\u0430\u043c\u043a\u0438",
            "\u0433\u0440\u0430\u043d\u0438\u0446\u0430",
            "\u043a\u0438\u0440\u0431\u0438\u0438",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u043d\u0430\u0434",
            "\u043e\u0431\u0440\u0430\u043c\u0438\u0442\u044c",
            "\u043e\u0439\u0443\u0443\u0447\u0430\u0430\u043d",
            "\u043e\u043b\u043e\u0445-\u0434\u044c\u0443\u0440\u0430\u0430",
            "\u043e\u0440\u0442\u043e",
            "\u043e\u0440\u0442\u043e\u0442\u0443\u043d\u0430\u043d",
            "\u043e\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u0435",
            "\u043f\u043e\u0434",
            "\u043f\u043e\u0441\u0435\u0440\u0435\u0434\u0438\u043d\u0435",
            "\u0440\u0430\u0430\u043c\u043a\u0430",
            "\u0440\u0430\u0430\u043c\u043a\u0430\u0442\u0430_\u0441\u0443\u043e\u0445",
            "\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u043b\u0435\u0432\u0430",
            "\u0441\u043d\u0438\u0437\u0443",
            "\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u0443\u043e\u0445",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u043d\u0438\u0437\u0443",
            "\u0442\u0438\u044d\u043a\u0438\u0441-\u0430\u043b\u043b\u0430\u0440\u0430",
            "\u0442\u0438\u044d\u043a\u0438\u0441-\u04af\u0440\u0434\u04af\u0433\u044d\u0440",
            "\u0443\u04a5\u0430",
            "\u0445\u0430\u04a5\u0430\u0441",
            "\u0446\u0435\u043d\u0442\u0440",
            "\u04af\u0440\u0434\u04af\u043d\u044d\u043d",
            "\u04af\u0440\u04af\u0442",
            "\u04af\u04e9\u04bb\u044d\u044d\u0443\u04a5\u0430"
        ],
        "params": [
            "\u0430\u043b\u044c\u0442",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u043e\u0439\u0443\u0443\u0447\u0430\u0430\u043d",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u0438\u0433\u044d",
            "\u0441\u0438\u0440\u044d\u0439",
            "\u0441\u0441\u044b\u043b\u043a\u0430",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430",
            "\u04af\u04e9\u04bb\u044d\u044d\u0443\u04a5\u0430"
        ],
        "startswith": [
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430 ",
            "\u0441\u0438\u0440\u044d\u0439 ",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430 ",
            "\u04af\u04e9\u04bb\u044d\u044d\u0443\u04a5\u0430 "
        ],
        "endswith": [
            "\u043f\u043a\u0441"
        ]
    },
    "scn": {
        "keywords": [
            "bordo",
            "centro",
            "destra",
            "incorniciato",
            "met\u00e0",
            "min",
            "miniatura",
            "nessuno",
            "originale",
            "pedice",
            "riquadrato",
            "senza_cornice",
            "sinistra",
            "sopra",
            "sotto",
            "testo-sopra",
            "testo-sotto",
            "verticale"
        ],
        "params": [
            "min",
            "miniatura",
            "pagina",
            "verticale"
        ],
        "startswith": [
            "pagina_",
            "verticale_"
        ]
    },
    "sd": {
        "keywords": [
            "\u062a\u064e\u0631\u064f",
            "\u0633\u0627\u0684\u0648",
            "\u0633\u0650\u0631\u064f",
            "\u0645\u0631\u06aa\u0632",
            "\u0648\u0686",
            "\u06a9\u0627\u067b\u0648",
            "\u06aa\u062c\u0647\u0646\u0647"
        ],
        "endswith": [
            " \u0639\u06aa\u0633\u0644\u0648\u0646"
        ]
    },
    "se": {
        "keywords": [
            "alaindeksi",
            "alas",
            "alhaalla",
            "bunn",
            "gasku",
            "grunnlinje",
            "gurut",
            "h\u00f8yre",
            "ingen",
            "ingenramme",
            "kehykset\u00f6n",
            "kehys",
            "kehystetty",
            "keskell\u00e4",
            "keski",
            "keskitetty",
            "midt",
            "midtstilt",
            "mini",
            "miniatyr",
            "oikea",
            "olge\u0161",
            "perustaso",
            "pienois",
            "pienoiskuva",
            "portrett",
            "pysty",
            "ramme",
            "rammel\u00f8s",
            "reunus",
            "senter",
            "sentrer",
            "tekst-bunn",
            "topp",
            "tyhj\u00e4",
            "vasen",
            "venstre",
            "ylh\u00e4\u00e4ll\u00e4",
            "yl\u00e4indeksi",
            "yl\u00e4oikea",
            "yl\u00f6s"
        ],
        "params": [
            "lenke",
            "linkki",
            "li\u014bka",
            "mini",
            "miniatyr",
            "pienois",
            "pienoiskuva",
            "portrett",
            "pysty",
            "side",
            "sivu",
            "yl\u00e4oikea"
        ],
        "startswith": [
            "portrett_",
            "pysty_",
            "side ",
            "sivu_",
            "yl\u00e4oikea_"
        ]
    },
    "sg": {
        "keywords": [
            "bas",
            "bas-texte",
            "bas-txt",
            "base",
            "bordure",
            "cadre",
            "centr\u00e9",
            "droite",
            "encadre",
            "encadr\u00e9",
            "exp",
            "exposant",
            "gauche",
            "haut",
            "haut-texte",
            "haut-txt",
            "ind",
            "indice",
            "ligne-de-base",
            "milieu",
            "neant",
            "non_encadre",
            "non_encadr\u00e9",
            "n\u00e9ant",
            "redresse",
            "sans_cadre",
            "vignette"
        ],
        "params": [
            "classe",
            "langue",
            "lien",
            "redresse",
            "vignette"
        ],
        "startswith": [
            "redresse_"
        ]
    },
    "sh": {
        "keywords": [
            "bez",
            "bez_okvira",
            "bez_rama",
            "bezokvira",
            "bezrama",
            "c",
            "centar",
            "d",
            "desno",
            "dno",
            "dugme",
            "eks",
            "granica",
            "ind",
            "ivica",
            "l",
            "levo",
            "lijevo",
            "mini",
            "minijatura",
            "n",
            "na_gore",
            "natpis",
            "ni\u0161ta",
            "obrub",
            "odjeljak",
            "okvir",
            "osnova",
            "osnovnacrta",
            "pocetna_linija",
            "pod",
            "pola",
            "potpis",
            "po\u010detna_linija",
            "ram",
            "sredina",
            "sredina_teksta",
            "sredinateksta",
            "sredi\u0161te",
            "tekst-dno",
            "tekst-dugme",
            "tekst-vrh",
            "tekst_vrh",
            "umanjeno",
            "uspravno",
            "vrh",
            "vrh_teksta",
            "vrhteksta"
        ],
        "params": [
            "jezik",
            "mini",
            "minijatura",
            "na_gore",
            "poveznica",
            "strana",
            "stranica",
            "umanjeno",
            "uspravno",
            "veza"
        ],
        "startswith": [
            "na_gore_",
            "strana_",
            "stranica ",
            "stranica_",
            "uspravno ",
            "uspravno_"
        ],
        "endswith": [
            "p",
            "piksel",
            "piskel"
        ]
    },
    "shi": {
        "keywords": [
            "bas",
            "bas-texte",
            "bas-txt",
            "base",
            "bordure",
            "cadre",
            "centr\u00e9",
            "droite",
            "encadre",
            "encadr\u00e9",
            "exp",
            "exposant",
            "gauche",
            "haut",
            "haut-texte",
            "haut-txt",
            "ind",
            "indice",
            "ligne-de-base",
            "milieu",
            "neant",
            "non_encadre",
            "non_encadr\u00e9",
            "n\u00e9ant",
            "redresse",
            "sans_cadre",
            "vignette"
        ],
        "params": [
            "classe",
            "langue",
            "lien",
            "redresse",
            "vignette"
        ],
        "startswith": [
            "redresse_"
        ]
    },
    "si": {
        "keywords": [
            "\u0d8b\u0db4",
            "\u0daf\u0d9a\u0dd4\u0dab",
            "\u0daf\u0dcf\u0dbb\u0dba",
            "\u0db1\u0ddc\u0db8\u0dd0\u0dad",
            "\u0db8\u0db0\u0dca\u200d\u0dba\u0dba",
            "\u0db8\u0dd0\u0daf",
            "\u0dc0\u0db8"
        ],
        "endswith": [
            "\u0db4\u0dd2\u0d9a\u0dca"
        ]
    },
    "sk": {
        "keywords": [
            "bezr\u00e1mu",
            "n\u00e1hled",
            "n\u00e1h\u013ead",
            "n\u00e1h\u013eadobr\u00e1zka",
            "okraj",
            "r\u00e1m",
            "stred",
            "st\u0159ed",
            "vlevo",
            "vpravo",
            "v\u013eavo",
            "\u017eiadny",
            "\u017e\u00e1dn\u00e9"
        ],
        "params": [
            "jazyk",
            "n\u00e1hled",
            "odkaz",
            "strana",
            "t\u0159\u00edda"
        ],
        "startswith": [
            "strana_"
        ],
        "endswith": [
            "bod",
            "pixel\u016f"
        ]
    },
    "sl": {
        "keywords": [
            "brez",
            "brezokvirja",
            "desno",
            "dno",
            "dno-besedila",
            "levo",
            "nad",
            "nadpisano",
            "obroba",
            "okvir",
            "okvirjeno",
            "pod",
            "podpisano",
            "sli\u010dica",
            "sredina",
            "sredinsko",
            "vrh",
            "vrh-besedila",
            "zgorajdesno"
        ],
        "params": [
            "sli\u010dica",
            "stran",
            "zgorajdesno"
        ],
        "startswith": [
            "m_stran ",
            "zgorajdesno "
        ],
        "endswith": [
            "_pik"
        ]
    },
    "smn": {
        "keywords": [
            "alaindeksi",
            "alas",
            "alhaalla",
            "kehykset\u00f6n",
            "kehys",
            "kehystetty",
            "keskell\u00e4",
            "keski",
            "keskitetty",
            "oikea",
            "perustaso",
            "pienois",
            "pienoiskuva",
            "pysty",
            "reunus",
            "tyhj\u00e4",
            "vasen",
            "ylh\u00e4\u00e4ll\u00e4",
            "yl\u00e4indeksi",
            "yl\u00e4oikea",
            "yl\u00f6s"
        ],
        "params": [
            "linkki",
            "pienois",
            "pienoiskuva",
            "pysty",
            "sivu",
            "yl\u00e4oikea"
        ],
        "startswith": [
            "pysty_",
            "sivu_",
            "yl\u00e4oikea_"
        ]
    },
    "sq": {
        "keywords": [
            "asnj\u00eb",
            "djathtas",
            "fund",
            "i_kornizuar",
            "korniz\u00eb",
            "kufi",
            "lartdjathtas",
            "linjabaz\u00eb",
            "majtas",
            "mes",
            "n\u00ebn",
            "pa_korniz\u00eb",
            "pamje",
            "parapamje",
            "qendrore",
            "qend\u00ebr",
            "s'ka",
            "tekst-fund",
            "tekst-maj\u00eb",
            "tekst-top",
            "vertikale"
        ],
        "params": [
            "faqja",
            "lartdjathtas",
            "lidhja",
            "lidhje",
            "pamje",
            "parapamje",
            "vertikale"
        ],
        "startswith": [
            "faqja ",
            "lartdjathtas ",
            "vertikale "
        ]
    },
    "sr": {
        "keywords": [
            "c",
            "\u0431\u0435\u0437",
            "\u0431\u0435\u0437_\u043e\u043a\u0432\u0438\u0440\u0430",
            "\u0431\u0435\u0437_\u0440\u0430\u043c\u0430",
            "\u0431\u0435\u0437\u043e\u043a\u0432\u0438\u0440\u0430",
            "\u0431\u0435\u0437\u0440\u0430\u043c\u0430",
            "\u0432\u0440\u0445",
            "\u0432\u0440\u0445_\u0442\u0435\u043a\u0441\u0442\u0430",
            "\u0432\u0440\u0445\u0442\u0435\u043a\u0441\u0442\u0430",
            "\u0434",
            "\u0434\u0435\u0441\u043d\u043e",
            "\u0434\u043d\u043e",
            "\u0438\u0432\u0438\u0446\u0430",
            "\u043b",
            "\u043b\u0435\u0432\u043e",
            "\u043c\u0438\u043d\u0438",
            "\u043d",
            "\u043e\u0438\u0432\u0438\u0447\u0435\u043d\u043e",
            "\u043e\u043a\u0432\u0438\u0440",
            "\u043e\u0441\u043d\u043e\u0432\u0430",
            "\u043f\u043e\u0434",
            "\u0440\u0430\u043c",
            "\u0441\u0440\u0435\u0434\u0438\u043d\u0430",
            "\u0441\u0440\u0435\u0434\u0438\u043d\u0430_\u0442\u0435\u043a\u0441\u0442\u0430",
            "\u0441\u0440\u0435\u0434\u0438\u043d\u0430\u0442\u0435\u043a\u0441\u0442\u0430",
            "\u0441\u0443\u043f\u0435\u0440",
            "\u0443\u043c\u0430\u045a\u0435\u043d\u043e",
            "\u0443\u0441\u043f\u0440\u0430\u0432\u043d\u043e",
            "\u0446",
            "\u0446\u0435\u043d\u0442\u0430\u0440"
        ],
        "params": [
            "\u0430\u043b\u0442",
            "\u0432\u0435\u0437\u0430",
            "\u043c\u0438\u043d\u0438",
            "\u0441\u0442\u0440\u0430\u043d\u0430",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430",
            "\u0443\u043c\u0430\u045a\u0435\u043d\u043e",
            "\u0443\u0441\u043f\u0440\u0430\u0432\u043d\u043e"
        ],
        "startswith": [
            "\u0441\u0442\u0440\u0430\u043d\u0430_",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430_",
            "\u0443\u0441\u043f\u0440\u0430\u0432\u043d\u043e_"
        ],
        "endswith": [
            "p",
            "\u043f",
            "\u043f\u0438\u0441\u043a\u0435\u043b"
        ]
    },
    "srn": {
        "keywords": [
            "beneden",
            "boven",
            "gecentreerd",
            "geen",
            "grondlijn",
            "kaderloos",
            "links",
            "midden",
            "miniatuur",
            "omkaderd",
            "rand",
            "rechtop",
            "rechts",
            "tekst-beneden",
            "tekst-boven"
        ],
        "params": [
            "klasse",
            "koppeling",
            "miniatuur",
            "pagina",
            "rechtop",
            "taal",
            "verwijzing"
        ],
        "startswith": [
            "pagina_",
            "rechtop"
        ]
    },
    "stq": {
        "keywords": [
            "gerahmt",
            "grundlinie",
            "hoch",
            "hochgestellt",
            "hochkant",
            "links",
            "mini",
            "miniatur",
            "mitte",
            "oben",
            "ohne",
            "rahmenlos",
            "rand",
            "rechts",
            "text-oben",
            "text-unten",
            "tief",
            "tiefgestellt",
            "unten",
            "zentriert"
        ],
        "params": [
            "alternativtext",
            "hochkant",
            "klasse",
            "mini",
            "miniatur",
            "seite",
            "sprache",
            "verweis"
        ],
        "startswith": [
            "hochkant ",
            "hochkant_",
            "seite ",
            "seite_"
        ]
    },
    "su": {
        "keywords": [
            "atas",
            "atas-teks",
            "atek",
            "batas",
            "batek",
            "bawah",
            "bawah-teks",
            "bing",
            "bingkai",
            "gada",
            "garis_dasar",
            "jempol",
            "jmpl",
            "ka",
            "kanan",
            "ki",
            "kiri",
            "lurus",
            "mini",
            "miniatur",
            "nir",
            "nirbing",
            "pus",
            "pusat",
            "tanpa",
            "tanpabingkai",
            "tegak",
            "tengah",
            "tepi",
            "upa"
        ],
        "params": [
            "al",
            "alternatif",
            "bhs",
            "hal",
            "halaman",
            "jempol",
            "jmpl",
            "lurus",
            "mini",
            "miniatur",
            "pra",
            "pranala",
            "tegak"
        ],
        "startswith": [
            "hal_",
            "halaman_",
            "lurus_",
            "tegak_"
        ]
    },
    "sv": {
        "keywords": [
            "baslinje",
            "botten",
            "centrerad",
            "h\u00f6ger",
            "ingen",
            "inramad",
            "kantlinje",
            "mini",
            "miniatyr",
            "mitten",
            "ned",
            "ram",
            "raml\u00f6s",
            "st\u00e5ende",
            "text-botten",
            "text-topp",
            "topp",
            "upp",
            "v\u00e4nster"
        ],
        "params": [
            "l\u00e4nk",
            "mini",
            "miniatyr",
            "sida",
            "st\u00e5ende"
        ],
        "startswith": [
            "sida ",
            "st\u00e5ende "
        ]
    },
    "szl": {
        "keywords": [
            "bez_ramki",
            "bezramki",
            "brak",
            "centruj",
            "d\u00f3\u0142",
            "g\u00f3ra",
            "lewo",
            "ma\u0142y",
            "prawo",
            "ramka",
            "t\u0142o",
            "\u015brodek"
        ],
        "params": [
            "ma\u0142y",
            "strona"
        ]
    },
    "szy": {
        "keywords": [
            "\u4e0a\u6a19",
            "\u4e0b\u6a19",
            "\u4e2d\u95f4",
            "\u53f3",
            "\u53f3\u4e0a",
            "\u5782\u76f4\u7f6e\u4e2d",
            "\u5782\u76f4\u7f6e\u5e95",
            "\u5782\u76f4\u7f6e\u9802",
            "\u57fa\u7ebf",
            "\u5b50",
            "\u5c45\u4e2d",
            "\u5de6",
            "\u5e95\u90e8",
            "\u6587\u5b57\u5e95\u90e8",
            "\u6587\u5b57\u7f6e\u5e95",
            "\u6587\u5b57\u7f6e\u9802",
            "\u6587\u5b57\u9876\u90e8",
            "\u65e0",
            "\u65e0\u6846",
            "\u66ff\u4ee3\u6587\u5b57",
            "\u6709\u6846",
            "\u7121",
            "\u7121\u6846",
            "\u7e2e\u5716",
            "\u7f29\u7565\u56fe",
            "\u7f6e\u4e2d",
            "\u8d85",
            "\u8fb9\u6846",
            "\u908a\u6846",
            "\u9876\u90e8"
        ],
        "params": [
            "\u53f3\u4e0a",
            "\u66ff\u4ee3",
            "\u66ff\u4ee3\u6587\u672c",
            "\u7c7b",
            "\u7e2e\u5716",
            "\u7f29\u7565\u56fe",
            "\u8a9e\u8a00",
            "\u8bed\u8a00",
            "\u9023\u7d50",
            "\u94fe\u63a5",
            "\u9801",
            "\u985e\u5225",
            "\u9875\u6570"
        ],
        "startswith": [
            "\u53f3\u4e0a"
        ],
        "endswith": [
            "\u50cf\u7d20",
            "\u9801",
            "\u9875"
        ]
    },
    "ta": {
        "keywords": [
            "\u0b87\u0b9f\u0ba4\u0bc1",
            "\u0b92\u0ba9\u0bcd\u0bb1\u0bc1\u0bae\u0bbf\u0bb2\u0bcd\u0bb2\u0bc8",
            "\u0b95\u0bc0\u0bb4\u0bcd",
            "\u0bae\u0ba4\u0bcd\u0ba4\u0bbf\u0baf\u0bbf\u0bb2\u0bcd",
            "\u0bae\u0bc7\u0bb2\u0bcd",
            "\u0bae\u0bc8\u0baf\u0bae\u0bcd",
            "\u0bb5\u0bb2\u0ba4\u0bc1"
        ]
    },
    "tay": {
        "keywords": [
            "\u4e0a\u6a19",
            "\u4e0b\u6a19",
            "\u4e2d\u95f4",
            "\u53f3",
            "\u53f3\u4e0a",
            "\u5782\u76f4\u7f6e\u4e2d",
            "\u5782\u76f4\u7f6e\u5e95",
            "\u5782\u76f4\u7f6e\u9802",
            "\u57fa\u7ebf",
            "\u5b50",
            "\u5c45\u4e2d",
            "\u5de6",
            "\u5e95\u90e8",
            "\u6587\u5b57\u5e95\u90e8",
            "\u6587\u5b57\u7f6e\u5e95",
            "\u6587\u5b57\u7f6e\u9802",
            "\u6587\u5b57\u9876\u90e8",
            "\u65e0",
            "\u65e0\u6846",
            "\u66ff\u4ee3\u6587\u5b57",
            "\u6709\u6846",
            "\u7121",
            "\u7121\u6846",
            "\u7e2e\u5716",
            "\u7f29\u7565\u56fe",
            "\u7f6e\u4e2d",
            "\u8d85",
            "\u8fb9\u6846",
            "\u908a\u6846",
            "\u9876\u90e8"
        ],
        "params": [
            "\u53f3\u4e0a",
            "\u66ff\u4ee3",
            "\u66ff\u4ee3\u6587\u672c",
            "\u7c7b",
            "\u7e2e\u5716",
            "\u7f29\u7565\u56fe",
            "\u8a9e\u8a00",
            "\u8bed\u8a00",
            "\u9023\u7d50",
            "\u94fe\u63a5",
            "\u9801",
            "\u985e\u5225",
            "\u9875\u6570"
        ],
        "startswith": [
            "\u53f3\u4e0a"
        ],
        "endswith": [
            "\u50cf\u7d20",
            "\u9801",
            "\u9875"
        ]
    },
    "te": {
        "keywords": [
            "\u0c0e\u0c21\u0c2e",
            "\u0c15\u0c41\u0c21\u0c3f"
        ]
    },
    "tet": {
        "keywords": [
            "abaixo",
            "acima",
            "borda",
            "centro",
            "comborda",
            "commoldura",
            "direita",
            "esquerda",
            "linhadebase",
            "meio",
            "miniatura",
            "miniaturadaimagem",
            "nenhum",
            "semborda",
            "semmoldura",
            "superiordireito"
        ],
        "params": [
            "liga\u00e7\u00e3o",
            "miniatura",
            "miniaturadaimagem",
            "p\u00e1gina",
            "superiordireito"
        ],
        "startswith": [
            "p\u00e1gina ",
            "p\u00e1gina_",
            "superiordireito ",
            "superiordireito_"
        ]
    },
    "tg": {
        "keywords": [
            "\u0430\u0437_\u0431\u043e\u043b\u043e",
            "\u0430\u0441\u043e\u0441",
            "\u0431\u0435",
            "\u0431\u0435_\u0440\u0430\u043c\u043a\u0430",
            "\u0431\u0435_\u0447\u0430\u04b3\u043e\u0440\u0447\u04ef\u0431\u0430",
            "\u0431\u043e\u043b\u043e",
            "\u0431\u043e\u043b\u043e\u0440\u043e\u0441\u0442",
            "\u0434\u0430\u0440\u0431\u0430\u0439\u043d",
            "\u0434\u0430\u0440\u043f\u043e\u0451\u043d",
            "\u043c\u0430\u0440\u043a\u0430\u0437",
            "\u043c\u0430\u0442\u043d\u0431\u043e\u043b\u043e",
            "\u043c\u0430\u0442\u043d\u043f\u043e\u0451\u043d",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u043f\u043e\u0451\u043d",
            "\u0440\u0430\u043c\u043a\u0430",
            "\u0440\u043e\u0441\u0442",
            "\u0441\u0430\u0440\u04b3\u0430\u0434",
            "\u0447\u0430\u043f",
            "\u0447\u0430\u04b3\u043e\u0440\u0447\u04ef\u0431\u0430"
        ],
        "params": [
            "\u0430\u043b\u0442",
            "\u0431\u043e\u043b\u043e_\u0440\u043e\u0441\u0442",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u043f\u0430\u0439\u0432\u0430\u043d\u0434",
            "\u0441\u0430\u04b3\u0438\u0444\u0430"
        ],
        "startswith": [
            "\u0431\u043e\u043b\u043e\u0440\u043e\u0441\u0442 ",
            "\u0441\u0430\u04b3\u0438\u0444\u0430 "
        ],
        "endswith": [
            "\u043f\u043a\u0441"
        ]
    },
    "tr": {
        "keywords": [
            "alt",
            "alt\u00e7izgi",
            "dikey",
            "k\u00fc\u00e7\u00fck",
            "k\u00fc\u00e7\u00fckresim",
            "merkez",
            "metin-taban",
            "metin-tavan",
            "metin-tepe",
            "orta",
            "sa\u011f",
            "sol",
            "s\u0131n\u0131r",
            "taban",
            "taban\u00e7izgisi",
            "tavan",
            "tepe",
            "yok",
            "\u00e7er\u00e7eve",
            "\u00e7er\u00e7eveli",
            "\u00e7er\u00e7evesiz",
            "\u00fcs",
            "\u00fcst"
        ],
        "params": [
            "ba\u011flant\u0131",
            "dikey",
            "k\u00fc\u00e7\u00fck",
            "k\u00fc\u00e7\u00fckresim",
            "sayfa",
            "s\u0131n\u0131f"
        ],
        "startswith": [
            "dikey ",
            "sayfa "
        ],
        "endswith": [
            "pik",
            "piksel"
        ]
    },
    "trv": {
        "keywords": [
            "\u4e0a\u6a19",
            "\u4e0b\u6a19",
            "\u4e2d\u95f4",
            "\u53f3",
            "\u53f3\u4e0a",
            "\u5782\u76f4\u7f6e\u4e2d",
            "\u5782\u76f4\u7f6e\u5e95",
            "\u5782\u76f4\u7f6e\u9802",
            "\u57fa\u7ebf",
            "\u5b50",
            "\u5c45\u4e2d",
            "\u5de6",
            "\u5e95\u90e8",
            "\u6587\u5b57\u5e95\u90e8",
            "\u6587\u5b57\u7f6e\u5e95",
            "\u6587\u5b57\u7f6e\u9802",
            "\u6587\u5b57\u9876\u90e8",
            "\u65e0",
            "\u65e0\u6846",
            "\u66ff\u4ee3\u6587\u5b57",
            "\u6709\u6846",
            "\u7121",
            "\u7121\u6846",
            "\u7e2e\u5716",
            "\u7f29\u7565\u56fe",
            "\u7f6e\u4e2d",
            "\u8d85",
            "\u8fb9\u6846",
            "\u908a\u6846",
            "\u9876\u90e8"
        ],
        "params": [
            "\u53f3\u4e0a",
            "\u66ff\u4ee3",
            "\u66ff\u4ee3\u6587\u672c",
            "\u7c7b",
            "\u7e2e\u5716",
            "\u7f29\u7565\u56fe",
            "\u8a9e\u8a00",
            "\u8bed\u8a00",
            "\u9023\u7d50",
            "\u94fe\u63a5",
            "\u9801",
            "\u985e\u5225",
            "\u9875\u6570"
        ],
        "startswith": [
            "\u53f3\u4e0a"
        ],
        "endswith": [
            "\u50cf\u7d20",
            "\u9801",
            "\u9875"
        ]
    },
    "tt": {
        "keywords": [
            "\u0431\u0435\u0437",
            "\u0431\u0435\u0437\u0440\u0430\u043c\u043a\u0438",
            "\u0433\u0440\u0430\u043d\u0438\u0446\u0430",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u043d\u0430\u0434",
            "\u043e\u0431\u0440\u0430\u043c\u0438\u0442\u044c",
            "\u043e\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u0435",
            "\u043f\u043e\u0434",
            "\u043f\u043e\u0441\u0435\u0440\u0435\u0434\u0438\u043d\u0435",
            "\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u043b\u0435\u0432\u0430",
            "\u0441\u043d\u0438\u0437\u0443",
            "\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u0443\u043b\u0434\u0430",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u043d\u0438\u0437\u0443",
            "\u0443\u04a3\u0434\u0430",
            "\u0446\u0435\u043d\u0442\u0440",
            "\u044e\u043a",
            "\u04af\u0437\u04d9\u043a"
        ],
        "params": [
            "\u0430\u043b\u044c\u0442",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u0441\u044b\u043b\u043a\u0430",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430"
        ],
        "startswith": [
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430 ",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430 "
        ],
        "endswith": [
            "\u043f\u043a\u0441"
        ]
    },
    "ty": {
        "keywords": [
            "bas",
            "bas-texte",
            "bas-txt",
            "base",
            "bordure",
            "cadre",
            "centr\u00e9",
            "droite",
            "encadre",
            "encadr\u00e9",
            "exp",
            "exposant",
            "gauche",
            "haut",
            "haut-texte",
            "haut-txt",
            "ind",
            "indice",
            "ligne-de-base",
            "milieu",
            "neant",
            "non_encadre",
            "non_encadr\u00e9",
            "n\u00e9ant",
            "redresse",
            "sans_cadre",
            "vignette"
        ],
        "params": [
            "classe",
            "langue",
            "lien",
            "redresse",
            "vignette"
        ],
        "startswith": [
            "redresse_"
        ]
    },
    "tyv": {
        "keywords": [
            "\u0431\u0435\u0437",
            "\u0431\u0435\u0437\u0440\u0430\u043c\u043a\u0438",
            "\u0433\u0440\u0430\u043d\u0438\u0446\u0430",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u043d\u0430\u0434",
            "\u043e\u0431\u0440\u0430\u043c\u0438\u0442\u044c",
            "\u043e\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u0435",
            "\u043e\u04a3",
            "\u043f\u043e\u0434",
            "\u043f\u043e\u0441\u0435\u0440\u0435\u0434\u0438\u043d\u0435",
            "\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u043b\u0435\u0432\u0430",
            "\u0441\u043d\u0438\u0437\u0443",
            "\u0441\u043e\u043b\u0430\u0433\u0430\u0439",
            "\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u043d\u0438\u0437\u0443",
            "\u0442\u04e9\u043f",
            "\u0446\u0435\u043d\u0442\u0440"
        ],
        "params": [
            "\u0430\u043b\u044c\u0442",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u0441\u044b\u043b\u043a\u0430",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430"
        ],
        "startswith": [
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430 ",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430 "
        ],
        "endswith": [
            "\u043f\u043a\u0441"
        ]
    },
    "udm": {
        "keywords": [
            "\u0431\u0435\u0437",
            "\u0431\u0435\u0437\u0440\u0430\u043c\u043a\u0438",
            "\u0433\u0440\u0430\u043d\u0438\u0446\u0430",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u043d\u0430\u0434",
            "\u043e\u0431\u0440\u0430\u043c\u0438\u0442\u044c",
            "\u043e\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u0435",
            "\u043f\u043e\u0434",
            "\u043f\u043e\u0441\u0435\u0440\u0435\u0434\u0438\u043d\u0435",
            "\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u043b\u0435\u0432\u0430",
            "\u0441\u043d\u0438\u0437\u0443",
            "\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u043d\u0438\u0437\u0443",
            "\u0446\u0435\u043d\u0442\u0440"
        ],
        "params": [
            "\u0430\u043b\u044c\u0442",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u0441\u044b\u043b\u043a\u0430",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430"
        ],
        "startswith": [
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430 ",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430 "
        ],
        "endswith": [
            "\u043f\u043a\u0441"
        ]
    },
    "uk": {
        "keywords": [
            "\u0431\u0435\u0437",
            "\u0431\u0435\u0437\u0440\u0430\u043c\u043a\u0438",
            "\u0433\u0440\u0430\u043d\u0438\u0446\u0430",
            "\u0433\u0440\u0430\u043d\u0438\u0446\u044f",
            "\u0437\u0432\u0435\u0440\u0445\u0443",
            "\u0437\u0432\u0435\u0440\u0445\u0443\u043f\u0440\u0430\u0432\u043e\u0440\u0443\u0447",
            "\u0437\u043d\u0438\u0437\u0443",
            "\u043b\u0456\u0432\u043e\u0440\u0443\u0447",
            "\u043c\u0435\u0436\u0430",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u043c\u0456\u043d\u0456",
            "\u043c\u0456\u043d\u0456\u0430\u0442\u044e\u0440\u0430",
            "\u043d\u0430\u0434",
            "\u043e\u0431\u0440\u0430\u043c\u0438\u0442\u0438",
            "\u043e\u0431\u0440\u0430\u043c\u0438\u0442\u044c",
            "\u043e\u0441\u043d\u043e\u0432\u0430",
            "\u043e\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u0435",
            "\u043f\u043e\u0434",
            "\u043f\u043e\u0441\u0435\u0440\u0435\u0434\u0438\u043d\u0435",
            "\u043f\u043e\u0441\u0435\u0440\u0435\u0434\u0438\u043d\u0456",
            "\u043f\u0440\u0430\u0432\u043e\u0440\u0443\u0447",
            "\u043f\u0456\u0434",
            "\u0440\u0430\u043c\u043a\u0430",
            "\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u043b\u0435\u0432\u0430",
            "\u0441\u043d\u0438\u0437\u0443",
            "\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0442\u0435\u043a\u0441\u0442-\u0437\u0432\u0435\u0440\u0445\u0443",
            "\u0442\u0435\u043a\u0441\u0442-\u0437\u043d\u0438\u0437\u0443",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u043d\u0438\u0437\u0443",
            "\u0446\u0435\u043d\u0442\u0440"
        ],
        "params": [
            "\u0430\u043b\u044c\u0442",
            "\u0437\u0432\u0435\u0440\u0445\u0443\u043f\u0440\u0430\u0432\u043e\u0440\u0443\u0447",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u043c\u0456\u043d\u0456",
            "\u043c\u0456\u043d\u0456\u0430\u0442\u044e\u0440\u0430",
            "\u043f\u043e\u0441\u0438\u043b\u0430\u043d\u043d\u044f",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u0441\u044b\u043b\u043a\u0430",
            "\u0441\u0442\u043e\u0440\u0456\u043d\u043a\u0430",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430"
        ],
        "startswith": [
            "\u0437\u0432\u0435\u0440\u0445\u0443\u043f\u0440\u0430\u0432\u043e\u0440\u0443\u0447_",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430 ",
            "\u0441\u0442\u043e\u0440\u0456\u043d\u043a\u0430_",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430 "
        ],
        "endswith": [
            "\u043f\u043a\u0441"
        ]
    },
    "ur": {
        "keywords": [
            "\u0627\u06cc\u0633\u062a\u0627\u062f\u06c1",
            "\u0628\u0627\u0626\u06cc\u06ba",
            "\u0628\u0627\u0644\u0627",
            "\u0628\u062f\u0648\u0646",
            "\u0628\u062f\u0648\u0646_\u0686\u0648\u06a9\u06be\u0679\u0627",
            "\u0628\u063a\u06cc\u0631",
            "\u062a\u0635\u063a\u06cc\u0631",
            "\u062d\u062f\u0648\u062f",
            "\u062e\u0637_\u0627\u0633\u0627\u0633\u06cc",
            "\u062f\u0627\u0626\u06cc\u06ba",
            "\u062f\u0631\u0645\u06cc\u0627\u0646",
            "\u0632\u0628\u0631",
            "\u0632\u06cc\u0631",
            "\u0632\u06cc\u0631\u06cc\u06ba",
            "\u0645\u062a\u0646-\u0628\u0627\u0644\u0627",
            "\u0645\u062a\u0646-\u0632\u06cc\u0631\u06cc\u06ba",
            "\u0648\u0633\u0637",
            "\u0686\u0648\u06a9\u06be\u0679\u0627"
        ],
        "params": [
            "\u0627\u06cc\u0633\u062a\u0627\u062f\u06c1",
            "\u062a\u0635\u063a\u06cc\u0631",
            "\u062f\u0631\u062c\u06c1",
            "\u0631\u0628\u0637",
            "\u0632\u0628\u0627\u0646",
            "\u0635\u0641\u062d\u06c1",
            "\u0644\u0646\u06a9",
            "\u0645\u062a\u0628\u0627\u062f\u0644"
        ],
        "startswith": [
            "\u0627\u06cc\u0633\u062a\u0627\u062f\u06c1_",
            "\u0635\u0641\u062d\u06c1_"
        ],
        "endswith": [
            "\u067e\u06a9",
            "\u067e\u06a9\u0633\u0644"
        ]
    },
    "vec": {
        "keywords": [
            "bordo",
            "centro",
            "destra",
            "incorniciato",
            "met\u00e0",
            "min",
            "miniatura",
            "nessuno",
            "originale",
            "pedice",
            "riquadrato",
            "senza_cornice",
            "sinistra",
            "sopra",
            "sotto",
            "testo-sopra",
            "testo-sotto",
            "verticale"
        ],
        "params": [
            "min",
            "miniatura",
            "pagina",
            "verticale"
        ],
        "startswith": [
            "pagina_",
            "verticale_"
        ]
    },
    "vep": {
        "keywords": [
            "ala",
            "eile",
            "hura",
            "kesk",
            "keskel",
            "oiged",
            "paremal",
            "pisi",
            "pisipilt",
            "p\u00fcsti",
            "raam",
            "raamita",
            "r\u00f6un",
            "t\u00fchi",
            "vasakul",
            "\u00e4\u00e4ris",
            "\u00fcl\u00e4h"
        ],
        "params": [
            "keel",
            "lehek\u00fclg",
            "pisi",
            "pisipilt",
            "p\u00fcsti"
        ],
        "startswith": [
            "lehek\u00fclg_"
        ],
        "endswith": [
            "piks"
        ]
    },
    "vi": {
        "keywords": [
            "ch\u00e2n-ch\u1eef",
            "ch\u1ec9-s\u1ed1-d\u01b0\u1edbi",
            "ch\u1ec9-s\u1ed1-tr\u00ean",
            "d\u01b0\u1edbi",
            "d\u01b0\u1edbi-ch\u1eef",
            "gi\u1eefa",
            "khung",
            "kh\u00f4ng",
            "kh\u00f4ng_khung",
            "nh\u1ecf",
            "n\u1eeda-chi\u1ec1u-cao",
            "ph\u1ea3i",
            "tr\u00e1i",
            "tr\u00ean",
            "tr\u00ean-ch\u1eef",
            "vi\u1ec1n",
            "\u0111\u1ee9ng"
        ],
        "params": [
            "li\u00ean_k\u1ebft",
            "l\u1edbp",
            "ng\u00f4n_ng\u1eef",
            "nh\u1ecf",
            "thay_th\u1ebf",
            "th\u1ebf",
            "ti\u1ebfng",
            "trang",
            "\u0111\u1ee9ng"
        ],
        "startswith": [
            "trang_",
            "\u0111\u1ee9ng_"
        ]
    },
    "vls": {
        "keywords": [
            "beneden",
            "boven",
            "gecentreerd",
            "geen",
            "grondlijn",
            "kaderloos",
            "links",
            "midden",
            "miniatuur",
            "omkaderd",
            "rand",
            "rechtop",
            "rechts",
            "tekst-beneden",
            "tekst-boven"
        ],
        "params": [
            "klasse",
            "koppeling",
            "miniatuur",
            "pagina",
            "rechtop",
            "taal",
            "verwijzing"
        ],
        "startswith": [
            "pagina_",
            "rechtop"
        ]
    },
    "wa": {
        "keywords": [
            "bas",
            "bas-texte",
            "bas-txt",
            "base",
            "bordure",
            "cadre",
            "centr\u00e9",
            "droite",
            "encadre",
            "encadr\u00e9",
            "exp",
            "exposant",
            "gauche",
            "haut",
            "haut-texte",
            "haut-txt",
            "ind",
            "indice",
            "ligne-de-base",
            "milieu",
            "neant",
            "non_encadre",
            "non_encadr\u00e9",
            "n\u00e9ant",
            "redresse",
            "sans_cadre",
            "vignette"
        ],
        "params": [
            "classe",
            "langue",
            "lien",
            "redresse",
            "vignette"
        ],
        "startswith": [
            "redresse_"
        ]
    },
    "wo": {
        "keywords": [
            "bas",
            "bas-texte",
            "bas-txt",
            "base",
            "bordure",
            "cadre",
            "centr\u00e9",
            "droite",
            "encadre",
            "encadr\u00e9",
            "exp",
            "exposant",
            "gauche",
            "haut",
            "haut-texte",
            "haut-txt",
            "ind",
            "indice",
            "ligne-de-base",
            "milieu",
            "neant",
            "non_encadre",
            "non_encadr\u00e9",
            "n\u00e9ant",
            "redresse",
            "sans_cadre",
            "vignette"
        ],
        "params": [
            "classe",
            "langue",
            "lien",
            "redresse",
            "vignette"
        ],
        "startswith": [
            "redresse_"
        ]
    },
    "wuu": {
        "keywords": [
            "\u4e0a\u6a19",
            "\u4e0b\u6a19",
            "\u4e2d\u95f4",
            "\u53f3",
            "\u53f3\u4e0a",
            "\u5782\u76f4\u7f6e\u4e2d",
            "\u5782\u76f4\u7f6e\u5e95",
            "\u5782\u76f4\u7f6e\u9802",
            "\u57fa\u7ebf",
            "\u5b50",
            "\u5c45\u4e2d",
            "\u5de6",
            "\u5e95\u90e8",
            "\u6587\u5b57\u5e95\u90e8",
            "\u6587\u5b57\u7f6e\u5e95",
            "\u6587\u5b57\u7f6e\u9802",
            "\u6587\u5b57\u9876\u90e8",
            "\u65e0",
            "\u65e0\u6846",
            "\u66ff\u4ee3\u6587\u5b57",
            "\u6709\u6846",
            "\u7121",
            "\u7121\u6846",
            "\u7e2e\u5716",
            "\u7f29\u7565\u56fe",
            "\u7f6e\u4e2d",
            "\u8d85",
            "\u8fb9\u6846",
            "\u908a\u6846",
            "\u9876\u90e8"
        ],
        "params": [
            "\u53f3\u4e0a",
            "\u66ff\u4ee3",
            "\u66ff\u4ee3\u6587\u672c",
            "\u7c7b",
            "\u7e2e\u5716",
            "\u7f29\u7565\u56fe",
            "\u8a9e\u8a00",
            "\u8bed\u8a00",
            "\u9023\u7d50",
            "\u94fe\u63a5",
            "\u9801",
            "\u985e\u5225",
            "\u9875\u6570"
        ],
        "startswith": [
            "\u53f3\u4e0a"
        ],
        "endswith": [
            "\u50cf\u7d20",
            "\u9801",
            "\u9875"
        ]
    },
    "xal": {
        "keywords": [
            "\u0431\u0435\u0437",
            "\u0431\u0435\u0437\u0440\u0430\u043c\u043a\u0438",
            "\u0433\u0440\u0430\u043d\u0438\u0446\u0430",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u043d\u0430\u0434",
            "\u043e\u0431\u0440\u0430\u043c\u0438\u0442\u044c",
            "\u043e\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u0435",
            "\u043f\u043e\u0434",
            "\u043f\u043e\u0441\u0435\u0440\u0435\u0434\u0438\u043d\u0435",
            "\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u043b\u0435\u0432\u0430",
            "\u0441\u043d\u0438\u0437\u0443",
            "\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u0432\u0435\u0440\u0445\u0443",
            "\u0442\u0435\u043a\u0441\u0442-\u0441\u043d\u0438\u0437\u0443",
            "\u0446\u0435\u043d\u0442\u0440"
        ],
        "params": [
            "\u0430\u043b\u044c\u0442",
            "\u043c\u0438\u043d\u0438",
            "\u043c\u0438\u043d\u0438\u0430\u0442\u044e\u0440\u0430",
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430",
            "\u0441\u0441\u044b\u043b\u043a\u0430",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430"
        ],
        "startswith": [
            "\u0441\u0432\u0435\u0440\u0445\u0443\u0441\u043f\u0440\u0430\u0432\u0430 ",
            "\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430 "
        ],
        "endswith": [
            "\u043f\u043a\u0441"
        ]
    },
    "xmf": {
        "keywords": [
            "\u10d0\u10e0\u10d0",
            "\u10d6\u10d4\u10d3\u10d0",
            "\u10db\u10d0\u10e0\u10ea\u10ee\u10dc\u10d8\u10d5",
            "\u10db\u10d0\u10e0\u10ef\u10d5\u10dc\u10d8\u10d5",
            "\u10db\u10d8\u10dc\u10d8",
            "\u10db\u10d8\u10dc\u10d8\u10d0\u10e1\u10da\u10d8",
            "\u10db\u10d8\u10dc\u10d8\u10d0\u10e2\u10d8\u10e3\u10e0\u10d0",
            "\u10e1\u10d0\u10d6\u10e6\u10d5\u10d0\u10e0\u10d8",
            "\u10e5\u10d5\u10d4\u10d3\u10d0",
            "\u10e8\u10e3\u10d0",
            "\u10ea\u10d4\u10dc\u10e2\u10e0\u10d8",
            "\u10ea\u10d4\u10dc\u10e2\u10e0\u10e8\u10d8",
            "\u10ea\u10d4\u10e0\u10dd\u10d3\u10d4\u10dc\u10d0"
        ],
        "params": [
            "\u10d0\u10da\u10e2",
            "\u10d1\u10db\u10e3\u10da\u10d8",
            "\u10d2\u10d5\u10d4\u10e0\u10d3\u10d8",
            "\u10db\u10d8\u10dc\u10d8",
            "\u10db\u10d8\u10dc\u10d8\u10d0\u10e2\u10d8\u10e3\u10e0\u10d0"
        ],
        "startswith": [
            "\u10d2\u10d5\u10d4\u10e0\u10d3\u10d8_"
        ],
        "endswith": [
            "\u10de\u10e5"
        ]
    },
    "yi": {
        "keywords": [
            "\u05d0\u05d5\u05d9\u05d1\u05df",
            "\u05d0\u05d5\u05e0\u05d8\u05df",
            "\u05d0\u05d5\u05e0\u05d8\u05e2\u05e8",
            "\u05d0\u05d9\u05d1\u05e2\u05e8",
            "\u05d0\u05d9\u05e0\u05de\u05d9\u05d8\u05df",
            "\u05d0\u05df",
            "\u05d1\u05d0\u05de\u05e6\u05e2",
            "\u05d1\u05e8\u05d0\u05e9 \u05d4\u05d8\u05e7\u05e1\u05d8",
            "\u05d1\u05ea\u05d7\u05ea\u05d9\u05ea \u05d4\u05d8\u05e7\u05e1\u05d8",
            "\u05d2\u05d1\u05d5\u05dc",
            "\u05d2\u05d1\u05d5\u05dc\u05d5\u05ea",
            "\u05d9\u05de\u05d9\u05df",
            "\u05d9\u05de\u05d9\u05df \u05dc\u05de\u05e2\u05dc\u05d4",
            "\u05dc\u05d0 \u05de\u05de\u05d5\u05e1\u05d2\u05e8",
            "\u05dc\u05d9\u05e0\u05e7\u05e1",
            "\u05dc\u05dc\u05d0",
            "\u05dc\u05dc\u05d0 \u05de\u05e1\u05d2\u05e8\u05ea",
            "\u05dc\u05de\u05d8\u05d4",
            "\u05dc\u05de\u05e2\u05dc\u05d4",
            "\u05de\u05de\u05d5\u05d6\u05e2\u05e8",
            "\u05de\u05de\u05d5\u05e1\u05d2\u05e8",
            "\u05de\u05e1\u05d2\u05e8\u05ea",
            "\u05de\u05e8\u05db\u05d6",
            "\u05e2\u05d9\u05dc\u05d9",
            "\u05e6\u05e2\u05e0\u05d8\u05e2\u05e8",
            "\u05e7\u05dc\u05d9\u05d9\u05df",
            "\u05e8\u05e2\u05db\u05d8\u05e1",
            "\u05e9\u05d5\u05e8\u05ea \u05d4\u05d1\u05e1\u05d9\u05e1",
            "\u05e9\u05de\u05d0\u05dc",
            "\u05ea\u05d7\u05ea\u05d9"
        ],
        "params": [
            "\u05d3\u05e3",
            "\u05d8\u05e2\u05e7\u05e1\u05d8",
            "\u05d8\u05e7\u05e1\u05d8",
            "\u05d9\u05de\u05d9\u05df \u05dc\u05de\u05e2\u05dc\u05d4",
            "\u05dc\u05d9\u05e0\u05e7",
            "\u05de\u05de\u05d5\u05d6\u05e2\u05e8",
            "\u05e7\u05d9\u05e9\u05d5\u05e8",
            "\u05e7\u05dc\u05d9\u05d9\u05df"
        ],
        "startswith": [
            "\u05d3\u05e3 ",
            "\u05d9\u05de\u05d9\u05df \u05dc\u05de\u05e2\u05dc\u05d4 "
        ],
        "endswith": [
            " \u05e4\u05d9\u05e7\u05e1\u05dc\u05d9\u05dd",
            "\u05e4\u05d9\u05e7\u05e1"
        ]
    },
    "za": {
        "keywords": [
            "\u4e0a\u6a19",
            "\u4e0b\u6a19",
            "\u4e2d\u95f4",
            "\u53f3",
            "\u53f3\u4e0a",
            "\u5782\u76f4\u7f6e\u4e2d",
            "\u5782\u76f4\u7f6e\u5e95",
            "\u5782\u76f4\u7f6e\u9802",
            "\u57fa\u7ebf",
            "\u5b50",
            "\u5c45\u4e2d",
            "\u5de6",
            "\u5e95\u90e8",
            "\u6587\u5b57\u5e95\u90e8",
            "\u6587\u5b57\u7f6e\u5e95",
            "\u6587\u5b57\u7f6e\u9802",
            "\u6587\u5b57\u9876\u90e8",
            "\u65e0",
            "\u65e0\u6846",
            "\u66ff\u4ee3\u6587\u5b57",
            "\u6709\u6846",
            "\u7121",
            "\u7121\u6846",
            "\u7e2e\u5716",
            "\u7f29\u7565\u56fe",
            "\u7f6e\u4e2d",
            "\u8d85",
            "\u8fb9\u6846",
            "\u908a\u6846",
            "\u9876\u90e8"
        ],
        "params": [
            "\u53f3\u4e0a",
            "\u66ff\u4ee3",
            "\u66ff\u4ee3\u6587\u672c",
            "\u7c7b",
            "\u7e2e\u5716",
            "\u7f29\u7565\u56fe",
            "\u8a9e\u8a00",
            "\u8bed\u8a00",
            "\u9023\u7d50",
            "\u94fe\u63a5",
            "\u9801",
            "\u985e\u5225",
            "\u9875\u6570"
        ],
        "startswith": [
            "\u53f3\u4e0a"
        ],
        "endswith": [
            "\u50cf\u7d20",
            "\u9801",
            "\u9875"
        ]
    },
    "zea": {
        "keywords": [
            "beneden",
            "boven",
            "gecentreerd",
            "geen",
            "grondlijn",
            "kaderloos",
            "links",
            "midden",
            "miniatuur",
            "omkaderd",
            "rand",
            "rechtop",
            "rechts",
            "tekst-beneden",
            "tekst-boven"
        ],
        "params": [
            "klasse",
            "koppeling",
            "miniatuur",
            "pagina",
            "rechtop",
            "taal",
            "verwijzing"
        ],
        "startswith": [
            "pagina_",
            "rechtop"
        ]
    },
    "zh": {
        "keywords": [
            "\u4e0a\u6a19",
            "\u4e0b\u6a19",
            "\u4e2d\u95f4",
            "\u53f3",
            "\u53f3\u4e0a",
            "\u5782\u76f4\u7f6e\u4e2d",
            "\u5782\u76f4\u7f6e\u5e95",
            "\u5782\u76f4\u7f6e\u9802",
            "\u57fa\u7ebf",
            "\u5b50",
            "\u5c45\u4e2d",
            "\u5de6",
            "\u5e95\u90e8",
            "\u6587\u5b57\u5e95\u90e8",
            "\u6587\u5b57\u7f6e\u5e95",
            "\u6587\u5b57\u7f6e\u9802",
            "\u6587\u5b57\u9876\u90e8",
            "\u65e0",
            "\u65e0\u6846",
            "\u66ff\u4ee3\u6587\u5b57",
            "\u6709\u6846",
            "\u7121",
            "\u7121\u6846",
            "\u7e2e\u5716",
            "\u7f29\u7565\u56fe",
            "\u7f6e\u4e2d",
            "\u8d85",
            "\u8fb9\u6846",
            "\u908a\u6846",
            "\u9876\u90e8"
        ],
        "params": [
            "\u53f3\u4e0a",
            "\u66ff\u4ee3",
            "\u66ff\u4ee3\u6587\u672c",
            "\u7c7b",
            "\u7e2e\u5716",
            "\u7f29\u7565\u56fe",
            "\u8a9e\u8a00",
            "\u8bed\u8a00",
            "\u9023\u7d50",
            "\u94fe\u63a5",
            "\u9801",
            "\u985e\u5225",
            "\u9875\u6570"
        ],
        "startswith": [
            "\u53f3\u4e0a"
        ],
        "endswith": [
            "\u50cf\u7d20",
            "\u9801",
            "\u9875"
        ]
    },
    "zh-classical": {
        "keywords": [
            "\u4e0a\u6a19",
            "\u4e0b\u6a19",
            "\u4e2d\u95f4",
            "\u53f3",
            "\u53f3\u4e0a",
            "\u5782\u76f4\u7f6e\u4e2d",
            "\u5782\u76f4\u7f6e\u5e95",
            "\u5782\u76f4\u7f6e\u9802",
            "\u57fa\u7ebf",
            "\u5b50",
            "\u5c45\u4e2d",
            "\u5de6",
            "\u5e95\u90e8",
            "\u6587\u5b57\u5e95\u90e8",
            "\u6587\u5b57\u7f6e\u5e95",
            "\u6587\u5b57\u7f6e\u9802",
            "\u6587\u5b57\u9876\u90e8",
            "\u65e0",
            "\u65e0\u6846",
            "\u66ff\u4ee3\u6587\u5b57",
            "\u6709\u6846",
            "\u7121",
            "\u7121\u6846",
            "\u7e2e\u5716",
            "\u7f29\u7565\u56fe",
            "\u7f6e\u4e2d",
            "\u8d85",
            "\u8fb9\u6846",
            "\u908a\u6846",
            "\u9876\u90e8"
        ],
        "params": [
            "\u53f3\u4e0a",
            "\u66ff\u4ee3",
            "\u66ff\u4ee3\u6587\u672c",
            "\u7c7b",
            "\u7e2e\u5716",
            "\u7f29\u7565\u56fe",
            "\u8a9e\u8a00",
            "\u8bed\u8a00",
            "\u9023\u7d50",
            "\u94fe\u63a5",
            "\u9801",
            "\u985e\u5225",
            "\u9875\u6570"
        ],
        "startswith": [
            "\u53f3\u4e0a"
        ],
        "endswith": [
            "\u50cf\u7d20",
            "\u9801",
            "\u9875"
        ]
    },
    "zh-min-nan": {
        "keywords": [
            "\u4e0a\u6a19",
            "\u4e0b\u6a19",
            "\u4e2d\u95f4",
            "\u53f3",
            "\u53f3\u4e0a",
            "\u5782\u76f4\u7f6e\u4e2d",
            "\u5782\u76f4\u7f6e\u5e95",
            "\u5782\u76f4\u7f6e\u9802",
            "\u57fa\u7ebf",
            "\u5b50",
            "\u5c45\u4e2d",
            "\u5de6",
            "\u5e95\u90e8",
            "\u6587\u5b57\u5e95\u90e8",
            "\u6587\u5b57\u7f6e\u5e95",
            "\u6587\u5b57\u7f6e\u9802",
            "\u6587\u5b57\u9876\u90e8",
            "\u65e0",
            "\u65e0\u6846",
            "\u66ff\u4ee3\u6587\u5b57",
            "\u6709\u6846",
            "\u7121",
            "\u7121\u6846",
            "\u7e2e\u5716",
            "\u7f29\u7565\u56fe",
            "\u7f6e\u4e2d",
            "\u8d85",
            "\u8fb9\u6846",
            "\u908a\u6846",
            "\u9876\u90e8"
        ],
        "params": [
            "\u53f3\u4e0a",
            "\u66ff\u4ee3",
            "\u66ff\u4ee3\u6587\u672c",
            "\u7c7b",
            "\u7e2e\u5716",
            "\u7f29\u7565\u56fe",
            "\u8a9e\u8a00",
            "\u8bed\u8a00",
            "\u9023\u7d50",
            "\u94fe\u63a5",
            "\u9801",
            "\u985e\u5225",
            "\u9875\u6570"
        ],
        "startswith": [
            "\u53f3\u4e0a"
        ],
        "endswith": [
            "\u50cf\u7d20",
            "\u9801",
            "\u9875"
        ]
    }
}