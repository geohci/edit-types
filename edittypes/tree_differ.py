import time

from anytree import PostOrderIter, NodeMixin
from anytree.util import leftsibling
import mwparserfromhell

MEDIA_PREFIXES = ['File', 'Image', 'Media']
CAT_PREFIXES = ['Category']

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

class OrderedNode(NodeMixin):  # Add Node feature
    def __init__(self, name, ntype='Text', text_hash=None, idx=-1, text='', char_offset=-1, section=None, parent=None, children=None):
        super(OrderedNode, self).__init__()
        self.name = name  # For debugging purposes
        self.ntype = ntype  # Different node types can be treated differently when computing equality
        self.text = str(text)  # Text that can then be passed to a diffing library
        # Used for quickly computing equality for most nodes.
        # Generally this just a simple hash of self.text (wikitext associated with a node) but
        # the text hash for sections and paragraphs is based on all the content within the section/paragraph
        # so it can be used for pruning while self.text is just the text that creates the section/paragraph
        # e.g., "==Section==\nThis is a section." would have as text "==Section==" but hash the full.
        # so the Differ doesn't identify a section/paragraph as changing when content within it is changed
        if text_hash is None:
            self.text_hash = hash(self.text)
        else:
            self.text_hash = hash(str(text_hash))
        self.idx = idx  # Used by Differ -- Post order on tree from 0...# nodes - 1
        self.char_offset = char_offset  # make it easy to find node in section text
        self.section = section  # section that the node is a part of -- useful for formatting final diff
        self.parent = parent
        if children:
            self.children = children

    def leftmost(self):
        return self.idx if self.is_leaf else self.children[0].leftmost()


def simple_node_class(node, lang='en'):
    """e.g., "<class 'mwparserfromhell.nodes.heading.Heading'>" -> "Heading"."""
    if type(node) == str:
        return 'Text'
    else:
        nc = str(type(node)).split('.')[-1].split("'")[0]
        if nc == 'Wikilink':
            n_prefix = node.title.split(':')[0]
            if n_prefix in MEDIA_PREFIXES + MEDIA_ALIASES.get(lang, []):
                nc = 'Media'
            elif n_prefix in CAT_PREFIXES + CAT_ALIASES.get(lang, []):
                nc = 'Category'
        return nc

def sec_to_name(s, idx):
    """Converts a section to an interpretible name."""
    return f'S#{idx}: {s.nodes[0].title} (L{s.nodes[0].level})'


def node_to_name(n, lang='en'):
    """Converts a mwparserfromhell node to an interpretible name."""
    n_txt = n.replace("\n", "\\n")
    if len(n_txt) > 13:
        return f'{simple_node_class(n, lang)}: {n_txt[:10]}...'
    else:
        return f'{simple_node_class(n, lang)}: {n_txt}'


def extract_text(node, lang='en'):
    """Extract what text would be displayed from any node."""
    ntype = simple_node_class(node, lang)
    if ntype == 'Text':
        return str(node)
    elif ntype == 'HTMLEntity':
        return node.normalize()
    elif ntype == 'Wikilink':
        if node.text:
            return node.text.strip_code()
        else:
            return node.title.strip_code()
    elif ntype == 'ExternalLink' and node.title:
        return node.title.strip_code()
    elif ntype == 'Tag':
        return node.contents.strip_code()
    else:  # Heading, Template, Comment, Argument, Category, Media
        return ''


def sec_node_tree(wt, lang='en'):
    """Build tree of document nodes from Wikipedia article.

    This approach builds a tree with an artificial 'root' node on the 1st level,
    all of the article sections on the 2nd level (including an artificial Lede section),
    and all of the text, link, template, etc. nodes nested under their respective sections.
    """
    root = OrderedNode('root', ntype="Article")
    secname_to_text = {}
    for sidx, s in enumerate(wt.get_sections(flat=True)):
        if s:
            sec_hash = sec_to_name(s, sidx)
            sec_text = ''.join([str(n) for n in s.nodes])
            secname_to_text[sec_hash] = sec_text
            s_node = OrderedNode(sec_hash, ntype="Heading", text=s.nodes[0], text_hash=sec_text, char_offset=0,
                                 section=sec_hash, parent=root)
            char_offset = len(s_node.text)
            for n in s.nodes[1:]:
                n_node = OrderedNode(node_to_name(n, lang), ntype=simple_node_class(n, lang), text=n, char_offset=char_offset,
                                     section=s_node.name, parent=s_node)
                char_offset += len(str(n))
    return root, secname_to_text


def rec_node_append(node, lang='en'):
    """Build tree of document nodes by recursing within a single wikitext node.

    This approach starts with a single wikitext node -- e.g., a single Tag node with nested link nodes etc.:
    <ref>{{cite web|title=[[Belveddere Gallery]]|url=http://digital.belvedere.at|publisher=Digitales Belvedere}}</ref>
    and splits it into its component pieces to then identify what has changed between revisions.

    Example above would take a Reference node as input and build the following tree (in-place):
    <--rest-of-tree-- Reference <--child-of-- Template (cite web) <--child-of-- WikiLink (Belveddere Gallery)
                                                            ^--------child-of-- External Link (http://digital...)
    """
    wt = mwparserfromhell.parse(node.text)
    root = node
    parent_node = root
    base_offset = root.char_offset
    parent_ranges = [(0, len(wt), root)]  # (start idx of node, end idx of node, node object)
    for idx, nn in enumerate(wt.ifilter(recursive=True)):
        if idx == 0:
            continue  # skip root node -- already set
        ntype = simple_node_class(nn, lang)
        if ntype != 'Text':  # skip Text nodes -- that's the standard content of the root node
            node_start = wt.find(str(nn), parent_ranges[0][0])  # start looking from the start of the latest node
            # identify direct parent of node
            for parent in parent_ranges:
                if node_start < parent[1]:  # falls within parent range
                    parent_node = parent[2]
                    break
            nn_node = OrderedNode(node_to_name(nn, lang=lang), ntype=ntype, text=nn, char_offset=base_offset+node_start, section=root.section, parent=parent_node)
            parent_ranges.insert(0, (node_start, node_start + len(nn), nn_node))

def format_diff(node):
    result = {'name':node.name,
              'type':node.ntype,
              'text':node.text,
              'offset':node.char_offset,
              'section':node.section}
    return result


def format_result(diff, sections1, sections2):
    result = {'remove':[], 'insert':[], 'change':[], 'move':[], 'sections-prev':{}, 'sections-curr':{}}
    for n in diff['remove']:
        n_res = format_diff(n)
        result['remove'].append(n_res)
        result['sections-prev'][n_res['section']] = sections1[n_res['section']]
    for n in diff['insert']:
        n_res = format_diff(n)
        result['insert'].append(n_res)
        result['sections-curr'][n_res['section']] = sections2[n_res['section']]
    for pn, cn in diff['change']:
        pn_res = format_diff(pn)
        cn_res = format_diff(cn)
        result['change'].append({'prev':pn_res, 'curr':cn_res})
        result['sections-prev'][pn_res['section']] = sections1[pn_res['section']]
        result['sections-curr'][cn_res['section']] = sections2[cn_res['section']]
    for pn, cn in diff['move']:
        pn_res = format_diff(pn)
        cn_res = format_diff(cn)
        result['move'].append({'prev':pn_res, 'curr':cn_res})
        result['sections-prev'][pn_res['section']] = sections1[pn_res['section']]
        result['sections-curr'][cn_res['section']] = sections2[cn_res['section']]
    return result

def detect_moves(diff):
    """Detect when nodes were moved (as opposed to removed + inserted)."""
    prev_moved = []
    curr_moved = []
    for i,pn in enumerate(diff['remove']):
        for j,cn in enumerate(diff['insert']):
            if pn.ntype == cn.ntype and pn.text_hash == cn.text_hash:
                prev_moved.append(i)
                curr_moved.append(j)
                break
    diff['move'] = []
    if prev_moved:
        for i in range(len(prev_moved)):
            pn = diff['remove'][prev_moved[i]]
            cn = diff['insert'][curr_moved[i]]
            diff['move'].append((pn, cn))
        prev_moved = sorted(prev_moved, reverse=True)
        for i in prev_moved:
            diff['remove'].pop(i)
        curr_moved = sorted(curr_moved, reverse=True)
        for i in curr_moved:
            diff['insert'].pop(i)


def section_mapping(result, s1, s2):
    """Build mapping of sections between previous and current versions of article."""
    prev = list(s1.keys())
    curr = list(s2.keys())
    p_to_c = {}
    c_to_p = {}
    removed = []
    for n in result['remove']:
        if n['type'] == 'Heading':
            for i, s in enumerate(prev):
                if s == n['name']:
                    removed.append(i)
                    break
    for idx in sorted(removed, reverse=True):
        p_to_c[prev[idx]] = None
        prev.pop(idx)
    inserted = []
    for n in result['insert']:
        if n['type'] == 'Heading':
            for i, s in enumerate(curr):
                if s == n['name']:
                    inserted.append(i)
                    break
    for idx in sorted(inserted, reverse=True):
        c_to_p[curr[idx]] = None
        curr.pop(idx)

    # changes happen in place so don't effect structure of doc and can be ignored

    for c in result['move']:
        pn = c['prev']
        cn = c['curr']
        if pn['type'] == 'Heading':
            prev_idx = None
            curr_idx = None
            for i, s in enumerate(prev):
                if s == pn['name']:
                    prev_idx = i
                    break
            for i, s in enumerate(curr):
                if s == cn['name']:
                    curr_idx = i
                    break
            if prev_idx is not None and curr_idx is not None:
                s = curr.pop(curr_idx)
                curr.insert(prev_idx, s)

    for i in range(len(prev)):
        p_to_c[prev[i]] = curr[i]
        c_to_p[curr[i]] = prev[i]

    return p_to_c, c_to_p


def merge_text_changes(result, s1, s2, lang='en'):
    """Replace isolated text changes with section-level text changes."""
    p_to_c, c_to_p = section_mapping(result, s1, s2)
    changes = []
    prev_secs_checked = set()
    curr_secs_checked = set()
    for idx in range(len(result['remove']) - 1, -1, -1):
        r = result['remove'][idx]
        if r['type'] == 'Text':
            prev_sec = r['section']
            if prev_sec not in prev_secs_checked:
                prev_secs_checked.add(prev_sec)
                prev_text = ''.join([extract_text(n, lang) for n in mwparserfromhell.parse(s1[prev_sec]).nodes])
                curr_sec = p_to_c[prev_sec]
                curr_secs_checked.add(curr_sec)
                if curr_sec is None:
                    changes.append({'prev': {'name': node_to_name(prev_text), 'type': 'Text', 'text': prev_text,
                                             'section': prev_sec, 'offset': 0}})
                else:
                    curr_text = ''.join([extract_text(n, lang) for n in mwparserfromhell.parse(s2[curr_sec]).nodes])
                    if prev_text != curr_text:
                        changes.append({'prev': {'name': node_to_name(prev_text), 'type': 'Text', 'text': prev_text,
                                                 'section': prev_sec, 'offset': 0},
                                        'curr': {'name': node_to_name(curr_text), 'type': 'Text', 'text': curr_text,
                                                 'section': curr_sec, 'offset': 0}})
            result['remove'].pop(idx)
    for idx in range(len(result['insert']) - 1, -1, -1):
        i = result['insert'][idx]
        if i['type'] == 'Text':
            curr_sec = i['section']
            if curr_sec not in curr_secs_checked:
                curr_secs_checked.add(curr_sec)
                curr_text = ''.join([extract_text(n, lang) for n in mwparserfromhell.parse(s2[curr_sec]).nodes])
                prev_sec = c_to_p[curr_sec]
                prev_secs_checked.add(prev_sec)
                if prev_sec is None:
                    changes.append({'curr': {'name': node_to_name(curr_text), 'type': 'Text', 'text': curr_text,
                                             'section': curr_sec, 'offset': 0}})
                else:
                    prev_text = ''.join([extract_text(n, lang) for n in mwparserfromhell.parse(s1[prev_sec]).nodes])
                    if prev_text != curr_text:
                        changes.append({'prev': {'name': node_to_name(prev_text), 'type': 'Text', 'text': prev_text,
                                                 'section': prev_sec, 'offset': 0},
                                        'curr': {'name': node_to_name(curr_text), 'type': 'Text', 'text': curr_text,
                                                 'section': curr_sec, 'offset': 0}})
            result['insert'].pop(idx)
    for idx in range(len(result['change']) - 1, -1, -1):
        pn = result['change'][idx]['prev']
        cn = result['change'][idx]['curr']
        if pn['type'] == 'Text':
            prev_sec = pn['section']
            if prev_sec not in prev_secs_checked:
                prev_secs_checked.add(prev_sec)
                prev_text = ''.join([extract_text(n, lang) for n in mwparserfromhell.parse(s1[prev_sec]).nodes])
                curr_sec = cn['section']
                curr_text = ''.join([extract_text(n, lang) for n in mwparserfromhell.parse(s2[curr_sec]).nodes])
                if prev_text != curr_text:
                    changes.append({'prev': {'name': node_to_name(prev_text), 'type': 'Text', 'text': prev_text,
                                             'section': prev_sec, 'offset': 0},
                                    'curr': {'name': node_to_name(curr_text), 'type': 'Text', 'text': curr_text,
                                             'section': curr_sec, 'offset': 0}})
            result['change'].pop(idx)

    for c in changes:
        if 'prev' in c and 'curr' in c:
            result['change'].append(c)
        elif 'prev' in c:
            result['remove'].append(c['prev'])
        elif 'curr' in c:
            result['insert'].append(c['curr'])


def get_diff(prev_wikitext, curr_wikitext, lang='en'):
    t1, sections1 = sec_node_tree(mwparserfromhell.parse(prev_wikitext), lang)
    t2, sections2 = sec_node_tree(mwparserfromhell.parse(curr_wikitext), lang)
    d = Differ(t1, t2)
    diff = d.get_corresponding_nodes()
    detect_moves(diff)
    formatted_diff = format_result(diff, sections1, sections2)
    merge_text_changes(formatted_diff, sections1, sections2, lang)
    return formatted_diff

class Differ:

    def __init__(self, t1, t2, timeout=2, expand_nodes=False):
        self.prune_trees(t1, t2, expand_nodes)
        self.t1 = []
        self.t2 = []
        for i,n in enumerate(PostOrderIter(t1)):
            n.idx = i
            self.t1.append(n)
        for i,n in enumerate(PostOrderIter(t2)):
            n.idx = i
            self.t2.append(n)
        self.timeout = time.time() + timeout
        self.ins_cost = 1
        self.rem_cost = 1
        self.chg_cost = 1
        self.nodetype_chg_cost = 10  # arbitrarily high to encourage remove+insert when node types change

        # Permanent store of transactions such that transactions[x][y] is the minimum
        # transactions to get from the sub-tree rooted at node x (in tree1) to the sub-tree
        # rooted at node y (in tree2).
        self.transactions = {None: {}}
        # Indices for each transaction, to avoid high performance cost of creating the
        # transactions multiple times
        self.transaction_to_idx = {None: {None: 0}}
        # All possible transactions
        self.idx_to_transaction = [(None, None)]

        idx_transaction = 1  # starts with nulls inserted

        transactions = {None: {None: []}}

        # Populate transaction stores
        for i in range(0, len(self.t1)):
            transactions[i] = {None: []}
            self.transaction_to_idx[i] = {None: idx_transaction}
            idx_transaction += 1
            self.idx_to_transaction.append((i, None))
            for j in range(0, len(self.t2)):
                transactions[None][j] = []
                transactions[i][j] = []
                self.transaction_to_idx[None][j] = idx_transaction
                idx_transaction += 1
                self.idx_to_transaction.append((None, j))
                self.transaction_to_idx[i][j] = idx_transaction
                idx_transaction += 1
                self.idx_to_transaction.append((i, j))
            self.transactions[i] = {}
        self.populate_transactions(transactions)

    def prune_trees(self, t1, t2, expand_nodes=False):
        """Quick heuristic preprocessing to reduce tree differ time by removing matching sections."""
        self.prune_sections(t1, t2)
        if expand_nodes:
            self.expand_nested(t1, t2)

    def expand_nested(self, t1, t2):
        """Expand nested nodes in tree -- e.g., Ref tags with templates/links contained in them."""
        for n in PostOrderIter(t1):
            if n.ntype != 'Heading' and n.name != 'root' and n.ntype != 'Text':  # tag, link, etc.
                rec_node_append(n)
        for n in PostOrderIter(t2):
            if n.ntype != 'Heading' and n.name != 'root' and n.ntype != 'Text':  # tag, link, etc.
                rec_node_append(n)

    def prune_sections(self, t1, t2):
        """Prune nodes from any sections that align across revisions"""
        t1_sections = [n for n in PostOrderIter(t1) if n.ntype == "Heading"]
        t2_sections = [n for n in PostOrderIter(t2) if n.ntype == "Heading"]
        for secnode1 in t1_sections:
            for sn2_idx in range(len(t2_sections)):
                secnode2 = t2_sections[sn2_idx]
                if secnode1.text_hash == secnode2.text_hash:
                    # assumes sections aren't hierarchical in tree
                    # or if they are, the text_hash must also include nested sections
                    secnode1.children = []
                    secnode2.children = []
                    t2_sections.pop(sn2_idx)  # only match once
                    break

    def get_key_roots(self, tree):
        """Get keyroots (node has a left sibling or is the root) of a tree"""
        for on in tree:
            if on.is_root or leftsibling(on) is not None:
                yield on

    def populate_transactions(self, transactions):
        """Populate self.transactions with minimum transactions between all possible trees"""
        for kr1 in self.get_key_roots(self.t1):
            # Make transactions for tree -> null
            i_nulls = []
            for ii in range(kr1.leftmost(), kr1.idx + 1):
                i_nulls.append(self.transaction_to_idx[ii][None])
                transactions[ii][None] = i_nulls.copy()
            for kr2 in self.get_key_roots(self.t2):
                # Make transactions of null -> tree
                j_nulls = []
                for jj in range(kr2.leftmost(), kr2.idx + 1):
                    j_nulls.append(self.transaction_to_idx[None][jj])
                    transactions[None][jj] = j_nulls.copy()

                # get the diff
                self.find_minimum_transactions(kr1, kr2, transactions)
                if time.time() > self.timeout:
                    self.transactions = None
                    return

        for i in range(0, len(self.t1)):
            for j in range(0, len(self.t2)):
                if self.transactions.get(i, {}).get(j) and len(self.transactions[i][j]) > 0:
                    self.transactions[i][j] = tuple([self.idx_to_transaction[idx] for idx in self.transactions[i][j]])

    def get_node_distance(self, n1, n2):
        """
        Get the cost of:
        * removing a node from the first tree,
        * inserting a node into the second tree,
        * or relabelling a node from the first tree to a node from the second tree.
        """
        if n1 is None and n2 is None:
            return 0
        elif n1 is None:
            return self.ins_cost
        elif n2 is None:
            return self.rem_cost
        # Inserts/Removes are easy. Changes are more complicated and should only be within same node type.
        # Use arbitrarily high-value for nodetype changes to effectively ban.
        elif n1.ntype != n2.ntype:
            return self.nodetype_chg_cost
        # next two functions check if both nodes are the same (criteria varies by nodetype)
        elif n1.ntype in ['Heading', "Paragraph"]:
            if n1.text == n2.text:
                return 0
            else:
                return self.chg_cost
        elif n1.text_hash == n2.text_hash:
            return 0
        # otherwise, same node types and not the same, then change cost
        else:
            return self.chg_cost

    def get_lowest_cost(self, rc, ic, cc):
        min_cost = rc
        index = 0
        if ic < min_cost:
            index = 1
            min_cost = ic
        if cc < min_cost:
            index = 2
        return index

    def find_minimum_transactions(self, kr1, kr2, transactions):
        """Find the minimum transactions to get from the first tree to the second tree."""
        for i in range(kr1.leftmost(), kr1.idx + 1):
            if i == kr1.leftmost():
                i_minus_1 = None
            else:
                i_minus_1 = i - 1
            n1 = self.t1[i]
            for j in range(kr2.leftmost(), kr2.idx + 1):
                if j == kr2.leftmost():
                    j_minus_1 = None
                else:
                    j_minus_1 = j - 1
                n2 = self.t2[j]

                if n1.leftmost() == kr1.leftmost() and n2.leftmost() == kr2.leftmost():
                    rem = transactions[i_minus_1][j]
                    ins = transactions[i][j_minus_1]
                    chg = transactions[i_minus_1][j_minus_1]
                    node_distance = self.get_node_distance(n1, n2)
                    # cost of each transaction
                    transaction = self.get_lowest_cost(len(rem) + self.rem_cost,
                                                       len(ins) + self.ins_cost,
                                                       len(chg) + node_distance)
                    if transaction == 0:
                        # record a remove
                        rc = rem.copy()
                        rc.append(self.transaction_to_idx[i][None])
                        transactions[i][j] = rc
                    elif transaction == 1:
                        # record an insert
                        ic = ins.copy()
                        ic.append(self.transaction_to_idx[None][j])
                        transactions[i][j] = ic
                    else:
                        # If nodes i and j are different, record a change, otherwise there is no transaction
                        transactions[i][j] = chg.copy()
                        if node_distance == 1:
                            transactions[i][j].append(self.transaction_to_idx[i][j])

                    self.transactions[i][j] = transactions[i][j].copy()
                else:
                    # Previous transactions, leading up to a remove, insert or change
                    rem = transactions[i_minus_1][j]
                    ins = transactions[i][j_minus_1]

                    if n1.leftmost() - 1 < kr1.leftmost():
                        k1 = None
                    else:
                        k1 = n1.leftmost() - 1
                    if n2.leftmost() - 1 < kr2.leftmost():
                        k2 = None
                    else:
                        k2 = n2.leftmost() - 1
                    chg = transactions[k1][k2]

                    transaction = self.get_lowest_cost(len(rem) + self.rem_cost,
                                                       len(ins) + self.ins_cost,
                                                       len(chg) + len(self.transactions[i][j]))
                    if transaction == 0:
                        # record a remove
                        rc = rem.copy()
                        rc.append(self.transaction_to_idx[i][None])
                        transactions[i][j] = rc
                    elif transaction == 1:
                        # record an insert
                        ic = ins.copy()
                        ic.append(self.transaction_to_idx[None][j])
                        transactions[i][j] = ic
                    else:
                        # record a change
                        cc = chg.copy()
                        cc.extend(self.transactions[i][j])
                        transactions[i][j] = cc

    def get_corresponding_nodes(self):
        """Explain transactions"""
        transactions = self.transactions[len(self.t1) - 1][len(self.t2) - 1]
        remove = []
        insert = []
        change = []
        for i in range(0, len(transactions)):
            if transactions[i][0] is None:
                ins_node = self.t2[transactions[i][1]]
                insert.append(ins_node)
            elif transactions[i][1] is None:
                rem_node = self.t1[transactions[i][0]]
                remove.append(rem_node)
            else:
                prev_node = self.t1[transactions[i][0]]
                curr_node = self.t2[transactions[i][1]]
                change.append((prev_node, curr_node))
        return {'remove': remove, 'insert': insert, 'change': change}