import logging
import re
from typing import Dict, Iterable, Optional, Union, cast

from pdfminer.glyphlist import glyphname2unicode
from pdfminer.latin_enc import ENCODING
from pdfminer.pdfexceptions import PDFKeyError
from pdfminer.psparser import PSLiteral, literal_name

HEXADECIMAL = re.compile(r"[0-9a-fA-F]+")

log = logging.getLogger(__name__)


def name2unicode(name: str) -> str:
    """Converts Adobe glyph names to Unicode numbers.

    In contrast to the specification, this raises a KeyError instead of return
    an empty string when the key is unknown.
    This way the caller must explicitly define what to do
    when there is not a match.

    Reference:
    https://github.com/adobe-type-tools/agl-specification#2-the-mapping

    :returns unicode character if name resembles something,
    otherwise a KeyError
    """
    if not isinstance(name, str):
        raise PDFKeyError(
            'Could not convert unicode name "%s" to character because '
            "it should be of type str but is of type %s" % (name, type(name)),
        )

    name = name.split(".")[0]
    components = name.split("_")

    if len(components) > 1:
        return "".join(map(name2unicode, components))

    elif name in glyphname2unicode:
        return glyphname2unicode[name]

    elif name.startswith("uni"):
        name_without_uni = name.strip("uni")

        if HEXADECIMAL.match(name_without_uni) and len(name_without_uni) % 4 == 0:
            unicode_digits = [
                int(name_without_uni[i : i + 4], base=16)
                for i in range(0, len(name_without_uni), 4)
            ]
            for digit in unicode_digits:
                raise_key_error_for_invalid_unicode(digit)
            characters = map(chr, unicode_digits)
            return "".join(characters)

    elif name.startswith("u"):
        name_without_u = name.strip("u")

        if HEXADECIMAL.match(name_without_u) and 4 <= len(name_without_u) <= 6:
            unicode_digit = int(name_without_u, base=16)
            raise_key_error_for_invalid_unicode(unicode_digit)
            return chr(unicode_digit)

    raise PDFKeyError(
        'Could not convert unicode name "%s" to character because '
        "it does not match specification" % name,
    )


def raise_key_error_for_invalid_unicode(unicode_digit: int) -> None:
    """Unicode values should not be in the range D800 through DFFF because
    that is used for surrogate pairs in UTF-16

    :raises KeyError if unicode digit is invalid
    """
    if 55295 < unicode_digit < 57344:
        raise PDFKeyError(
            "Unicode digit %d is invalid because "
            "it is in the range D800 through DFFF" % unicode_digit,
        )


class EncodingDB:
    std2unicode: Dict[int, str] = {}
    mac2unicode: Dict[int, str] = {}
    win2unicode: Dict[int, str] = {}
    pdf2unicode: Dict[int, str] = {}
    for name, std, mac, win, pdf in ENCODING:
        if std:
            std2unicode[std] = name
        if mac:
            mac2unicode[mac] = name
        if win:
            win2unicode[win] = name
        if pdf:
            pdf2unicode[pdf] = name

    encodings = {
        "StandardEncoding": std2unicode,
        "MacRomanEncoding": mac2unicode,
        "WinAnsiEncoding": win2unicode,
        "PDFDocEncoding": pdf2unicode,
    }

    @classmethod
    def get_encoding(
        cls,
        base: Union[PSLiteral, Dict[int, str]],
        diff: Optional[Iterable[object]] = None,
    ) -> Dict[int, str]:
        if isinstance(base, PSLiteral):
            encoding = cls.encodings.get(literal_name(base), cls.std2unicode)
        else:
            encoding = base
        if diff:
            encoding = encoding.copy()
            cid = 0
            for x in diff:
                if isinstance(x, int):
                    cid = x
                elif isinstance(x, PSLiteral):
                    encoding[cid] = cast(str, x.name)
                    cid += 1
        return encoding


def cid2unicode_from_encoding(encoding: Dict[int, str]) -> Dict[int, str]:
    cid2unicode = {}
    for cid, name in encoding.items():
        try:
            cid2unicode[cid] = name2unicode(name)
        except (KeyError, ValueError) as e:
            log.debug(str(e))
    return cid2unicode


ZAPFDINGBATS_BUILTIN_ENCODING = {
    32: "space",
    33: "a1",
    34: "a2",
    35: "a202",
    36: "a3",
    37: "a4",
    38: "a5",
    39: "a119",
    40: "a118",
    41: "a117",
    42: "a11",
    43: "a12",
    44: "a13",
    45: "a14",
    46: "a15",
    47: "a16",
    48: "a105",
    49: "a17",
    50: "a18",
    51: "a19",
    52: "a20",
    53: "a21",
    54: "a22",
    55: "a23",
    56: "a24",
    57: "a25",
    58: "a26",
    59: "a27",
    60: "a28",
    61: "a6",
    62: "a7",
    63: "a8",
    64: "a9",
    65: "a10",
    66: "a29",
    67: "a30",
    68: "a31",
    69: "a32",
    70: "a33",
    71: "a34",
    72: "a35",
    73: "a36",
    74: "a37",
    75: "a38",
    76: "a39",
    77: "a40",
    78: "a41",
    79: "a42",
    80: "a43",
    81: "a44",
    82: "a45",
    83: "a46",
    84: "a47",
    85: "a48",
    86: "a49",
    87: "a50",
    88: "a51",
    89: "a52",
    90: "a53",
    91: "a54",
    92: "a55",
    93: "a56",
    94: "a57",
    95: "a58",
    96: "a59",
    97: "a60",
    98: "a61",
    99: "a62",
    100: "a63",
    101: "a64",
    102: "a65",
    103: "a66",
    104: "a67",
    105: "a68",
    106: "a69",
    107: "a70",
    108: "a71",
    109: "a72",
    110: "a73",
    111: "a74",
    112: "a203",
    113: "a75",
    114: "a204",
    115: "a76",
    116: "a77",
    117: "a78",
    118: "a79",
    119: "a81",
    120: "a82",
    121: "a83",
    122: "a84",
    123: "a97",
    124: "a98",
    125: "a99",
    126: "a100",
    128: "a89",
    129: "a90",
    130: "a93",
    131: "a94",
    132: "a91",
    133: "a92",
    134: "a205",
    135: "a85",
    136: "a206",
    137: "a86",
    138: "a87",
    139: "a88",
    140: "a95",
    141: "a96",
    161: "a101",
    162: "a102",
    163: "a103",
    164: "a104",
    165: "a106",
    166: "a107",
    167: "a108",
    168: "a112",
    169: "a111",
    170: "a110",
    171: "a109",
    172: "a120",
    173: "a121",
    174: "a122",
    175: "a123",
    176: "a124",
    177: "a125",
    178: "a126",
    179: "a127",
    180: "a128",
    181: "a129",
    182: "a130",
    183: "a131",
    184: "a132",
    185: "a133",
    186: "a134",
    187: "a135",
    188: "a136",
    189: "a137",
    190: "a138",
    191: "a139",
    192: "a140",
    193: "a141",
    194: "a142",
    195: "a143",
    196: "a144",
    197: "a145",
    198: "a146",
    199: "a147",
    200: "a148",
    201: "a149",
    202: "a150",
    203: "a151",
    204: "a152",
    205: "a153",
    206: "a154",
    207: "a155",
    208: "a156",
    209: "a157",
    210: "a158",
    211: "a159",
    212: "a160",
    213: "a161",
    214: "a163",
    215: "a164",
    216: "a196",
    217: "a165",
    218: "a192",
    219: "a166",
    220: "a167",
    221: "a168",
    222: "a169",
    223: "a170",
    224: "a171",
    225: "a172",
    226: "a173",
    227: "a162",
    228: "a174",
    229: "a175",
    230: "a176",
    231: "a177",
    232: "a178",
    233: "a179",
    234: "a193",
    235: "a180",
    236: "a199",
    237: "a181",
    238: "a200",
    239: "a182",
    241: "a201",
    242: "a183",
    243: "a184",
    244: "a197",
    245: "a185",
    246: "a194",
    247: "a198",
    248: "a186",
    249: "a195",
    250: "a187",
    251: "a188",
    252: "a189",
    253: "a190",
    254: "a191",
}

SYMBOL_BUILTIN_ENCODING = {
    32: "space",
    33: "exclam",
    34: "universal",
    35: "numbersign",
    36: "existential",
    37: "percent",
    38: "ampersand",
    39: "suchthat",
    40: "parenleft",
    41: "parenright",
    42: "asteriskmath",
    43: "plus",
    44: "comma",
    45: "minus",
    46: "period",
    47: "slash",
    48: "zero",
    49: "one",
    50: "two",
    51: "three",
    52: "four",
    53: "five",
    54: "six",
    55: "seven",
    56: "eight",
    57: "nine",
    58: "colon",
    59: "semicolon",
    60: "less",
    61: "equal",
    62: "greater",
    63: "question",
    64: "congruent",
    65: "Alpha",
    66: "Beta",
    67: "Chi",
    68: "Delta",
    69: "Epsilon",
    70: "Phi",
    71: "Gamma",
    72: "Eta",
    73: "Iota",
    74: "theta1",
    75: "Kappa",
    76: "Lambda",
    77: "Mu",
    78: "Nu",
    79: "Omicron",
    80: "Pi",
    81: "Theta",
    82: "Rho",
    83: "Sigma",
    84: "Tau",
    85: "Upsilon",
    86: "sigma1",
    87: "Omega",
    88: "Xi",
    89: "Psi",
    90: "Zeta",
    91: "bracketleft",
    92: "therefore",
    93: "bracketright",
    94: "perpendicular",
    95: "underscore",
    96: "radicalex",
    97: "alpha",
    98: "beta",
    99: "chi",
    100: "delta",
    101: "epsilon",
    102: "phi",
    103: "gamma",
    104: "eta",
    105: "iota",
    106: "phi1",
    107: "kappa",
    108: "lambda",
    109: "mu",
    110: "nu",
    111: "omicron",
    112: "pi",
    113: "theta",
    114: "rho",
    115: "sigma",
    116: "tau",
    117: "upsilon",
    118: "omega1",
    119: "omega",
    120: "xi",
    121: "psi",
    122: "zeta",
    123: "braceleft",
    124: "bar",
    125: "braceright",
    126: "similar",
    160: "Euro",
    161: "Upsilon1",
    162: "minute",
    163: "lessequal",
    164: "fraction",
    165: "infinity",
    166: "florin",
    167: "club",
    168: "diamond",
    169: "heart",
    170: "spade",
    171: " arrowboth",
    172: "arrowleft",
    173: "arrowup",
    174: "arrowright",
    175: "arrowdown",
    176: "degree",
    177: "plusminus",
    178: "second",
    179: "greaterequal",
    180: "multiply",
    181: "proportional",
    182: "partialdiff",
    183: "bullet",
    184: "divide",
    185: "notequal",
    186: "equivalence",
    187: "approxequal",
    188: " ellipsis",
    189: "arrowvertex",
    190: " arrowhorizex",
    191: "carriagereturn",
    192: "aleph",
    193: "Ifraktur",
    194: "Rfraktur",
    195: "weierstrass",
    196: "circlemultiply",
    197: "circleplus",
    198: "emptyset",
    199: "intersection",
    200: "union",
    201: "propersuperset",
    202: "reflexsuperset",
    203: "notsubset",
    204: "propersubset",
    205: "reflexsubset",
    206: "element",
    207: "notelement",
    208: "angle",
    209: "gradient",
    210: "registerserif",
    211: "copyrightserif",
    212: "trademarkserif",
    213: "product",
    214: "radical",
    215: "dotmath",
    216: "logicalnot",
    217: "logicaland",
    218: "logicalor",
    219: " arrowdblboth",
    220: "arrowdblleft",
    221: "arrowdblup",
    222: "arrowdblright",
    223: "arrowdbldown",
    224: "lozenge",
    225: "angleleft",
    226: "registersans",
    227: "copyrightsans",
    228: "trademarksans",
    229: "summation",
    230: "parenlefttp",
    231: "parenleftex",
    232: "parenleftbt",
    233: "bracketlefttp",
    234: "bracketleftex",
    235: "bracketleftbt",
    236: "bracelefttp",
    237: "braceleftmid",
    238: "braceleftbt",
    239: "braceex",
    241: "angleright",
    242: "integral",
    243: "integraltp",
    244: "integralex",
    245: "integralbt",
    246: "parenrighttp",
    247: "parenrightex",
    248: "parenrightbt",
    249: "bracketrighttp",
    250: "bracketrightex",
    251: "bracketrightbt",
    252: "bracerighttp",
    253: "bracerightmid",
    254: "bracerightbt",
    -1: "apple",
}