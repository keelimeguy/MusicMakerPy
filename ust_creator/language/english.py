import eng_to_ipa as ipa
import inflect
import logging
import re

from .language import Language

logger = logging.getLogger(__name__)


# https://docs.google.com/spreadsheets/d/1uTKrbOmxWxi12DZ3E3xAxTrt8H0hAQcTw4T9YjKNiRg
class English(Language):
    # Not all combinations are necessarily possible, despite existing here

    _vowels = [

        # VOWELS

        'a',  # bot or bar
        'e',  # bet
        'i',  # bit
        'o',  # boot
        'u',  # but
        'E',  # bead
        '9',  # bought or soft
        '3',  # bi[r]d
        '@',  # bat
        'A',  # bake
        'I',  # bike
        'O',  # boat
        '8',  # bout
        'Q',  # boy
        '6',  # book
        'x',  # about
        '&',  # band
        '8n',  # bound
        'ar',  # are
        'Ar',  # air
        'Er',  # ear
        # '3r',  # rural
        'Ir',  # ire
        '1',  # (1ng/1nk) blink
        'Ang',  # bank
        '0',  # (0r/0l) bore/bowl
        '9l',  # ball
        'll',  # sill
        'mm',  # sim
        'nn',  # sin
        'nng',  # sing
    ]

    _consonants = [

        # CCV CONSONANTS

        'bl',  # bleed
        'fl',  # flick
        'gl',  # glass
        'kl',  # clown
        'pl',  # plural
        'sl',  # sleep
        'spl',  # splash
        'br',  # bread
        'dr',  # dream
        'fr',  # free
        'gr',  # great
        'kr',  # crazy
        'pr',  # press
        'tr',  # tree
        'shr',  # shriek
        'skr',  # scream
        'spr',  # spree
        'str',  # stress
        'thr',  # three
        'sf',  # sphere
        'dw',  # dwell
        'gw',  # bagworm
        'kw',  # quite
        'sw',  # sweet
        'tw',  # twelve
        'vw',  # reservoir
        'skw',  # square
        'thw',  # thwack
        'by',  # beautiful
        'fy',  # few
        'gy',  # figure
        'ky',  # cute
        'py',  # puny
        'my',  # muse
        'ny',  # when you
        'vy',  # view
        'zy',  # was you
        'sky',  # skewer
        'spy',  # spew

        # CV CONSONANTS

        # 'b',  # bet
        # 'd',  # debt
        # 'f',  # fed
        # 'g',  # get
        # 'j',  # jet
        # 'k',  # kept
        # 'p',  # pet
        # 's',  # set
        # 't',  # ten
        # 'v',  # vet
        # 'z',  # zed
        # 'ch',  # check
        # 'dh',  # this
        # 'sh',  # shed
        # 'th',  # think
        # 'zh',  # genre/treasure
        # 'ng',  # sing
        # 'l',  # let
        # 'm',  # met
        # 'n',  # net
        # 'r',  # red
        # /'h',  # head
        # /'w',  # wet
        # /'y',  # yet
        # /'dd',  # meddle
        # /'sk',  # skill
        # /'sp',  # spill
        # /'st',  # still
        # /'sm',  # smell
        # /'sn',  # sniff
        # /'nk',  # sink

        # VCC CONSONANTS

        'bd',  # grabbed
        'bz',  # grabs
        'ft',  # raft
        'fts',  # rafts
        'fs',  # riffs
        'gd',  # legged
        'gz',  # legs
        'ks',  # flex
        'kt',  # reflect
        'kst',  # texts
        # 'ps',  # taps
        'pt',  # tapped
        'vz',  # lives
        'vd',  # lived
        'zd',  # phased
        'znt',  # wasn't
        'cht',  # matched
        # 'chz',  # arches
        'ts',  # cats
        'dz',  # kids
        'jd',  # edged
        'dhd',  # bathed
        'sht',  # wished
        'ths',  # fifths
        'md',  # teamed
        'mf',  # triumph
        'mfs',  # triumphs
        'mp',  # temp
        'mps',  # temps
        'mpt',  # attempt
        'mz',  # gems
        'ngz',  # kings
        'nk',  # thank
        'nks',  # thanks
        'nkth',  # length
        'sk',  # desk
        'st',  # test
        'sts',  # tests
        'sks',  # asks
        'skt',  # asked
        'nd',  # and
        'ns',  # once
        'nt',  # tent
        'nts',  # tents
        'nz',  # lens
        'nj',  # lunge
        'njd',  # lunged
        'nch',  # pinch
        'ncht',  # pinched
        'nth',  # tenth
        'lb',  # bulb
        'ld',  # build
        'lf',  # self
        'lk',  # milk
        'lp',  # help
        'ls',  # else
        'lt',  # felt
        'lv',  # shelve
        'lz',  # tells
        'lch',  # belch
        'lsh',  # welsh
        'lth',  # health
    ]

    _combined = [

        # VOWELS + CV CONSONANTS

        'ab', 'ad', 'af', 'ag', 'aj', 'ak', 'ap', 'as', 'at', 'av', 'az',
        'ach', 'adh', 'ash', 'ath', 'azh', 'am', 'an', 'ar',  # 'al', 'ang',
        'eb', 'ed', 'ef', 'eg', 'ej', 'ek', 'ep', 'es', 'et', 'ev', 'ez',
        'ech', 'edh', 'esh', 'eth', 'ezh', 'el', 'em', 'en', 'eng',  # 'er',
        'ib', 'id', 'if', 'ig', 'ij', 'ik', 'ip', 'is', 'it', 'iv', 'iz',
        'ich', 'idh', 'ish', 'ith', 'izh', 'il', 'im', 'in',  # 'ir', 'ing',
        'ob', 'od', 'of', 'og', 'oj', 'ok', 'op', 'os', 'ot', 'ov', 'oz',
        'och', 'odh', 'osh', 'oth', 'ozh', 'ol', 'om', 'on', 'or', 'ong',
        'ub', 'ud', 'uf', 'ug', 'uj', 'uk', 'up', 'us', 'ut', 'uv', 'uz',
        'uch', 'udh', 'ush', 'uth', 'uzh', 'ul', 'um', 'un',  'ung',  # 'ur',
        'Eb', 'Ed', 'Ef', 'Eg', 'Ej', 'Ek', 'Ep', 'Es', 'Et', 'Ev', 'Ez',
        'Ech', 'Edh', 'Esh', 'Eth', 'Ezh', 'El', 'Em', 'En', 'Er',  # 'Eng',
        '9b', '9d', '9f', '9g', '9j', '9k', '9p', '9s', '9t', '9v', '9z',
        '9ch', '9dh', '9sh', '9th', '9zh', '9l', '9m', '9n', '9ng',  # '9r',
        '3b', '3d', '3f', '3g', '3j', '3k', '3p', '3s', '3t', '3v', '3z',
        '3ch', '3dh', '3sh', '3th', '3zh', '3l', '3m', '3n',  # '3r', '3ng',
        '@b', '@d', '@f', '@g', '@j', '@k', '@p', '@s', '@t', '@v', '@z',
        '@ch', '@dh', '@sh', '@th', '@zh', '@l',  # '@m', '@n', '@r', '@ng',
        'Ab', 'Ad', 'Af', 'Ag', 'Aj', 'Ak', 'Ap', 'As', 'At', 'Av', 'Az',
        'Ach', 'Adh', 'Ash', 'Ath', 'Azh', 'Al', 'Am', 'An', 'Ar', 'Ang',
        'Ib', 'Id', 'If', 'Ig', 'Ij', 'Ik', 'Ip', 'Is', 'It', 'Iv', 'Iz',
        'Ich', 'Idh', 'Ish', 'Ith', 'Izh', 'Il', 'Im', 'In', 'Ir',  # 'Ing',
        'Ob', 'Od', 'Of', 'Og', 'Oj', 'Ok', 'Op', 'Os', 'Ot', 'Ov', 'Oz',
        'Och', 'Odh', 'Osh', 'Oth', 'Ozh', 'Om', 'On',  # 'Or', 'Ong', 'Ol',
        '8b', '8d', '8f', '8g', '8j', '8k', '8p', '8s', '8t', '8v', '8z',
        '8ch', '8dh', '8sh', '8th', '8zh', '8l', '8m', '8n', '8r',  # '8ng',
        'Qb', 'Qd', 'Qf', 'Qg', 'Qj', 'Qk', 'Qp', 'Qs', 'Qt', 'Qv', 'Qz',
        'Qch', 'Qdh', 'Qsh', 'Qth', 'Qzh', 'Qng',  # 'Ql', 'Qm', 'Qn', 'Qr',
        '6b', '6d', '6f', '6g', '6j', '6k', '6p', '6s', '6t', '6v', '6z',
        '6ch', '6dh', '6sh', '6th', '6zh', '6l', '6m', '6n',  # '6r', '6ng',
        'xb', 'xd', 'xf', 'xg', 'xj', 'xk', 'xp', 'xs', 'xt', 'xv', 'xz',
        'xch', 'xdh', 'xsh', 'xth', 'xzh', 'xl', 'xm', 'xn',  # 'xr', 'xng',
        # '&b', '&d', '&f', '&g', '&j', '&k', '&p', '&s', '&t', '&v', '&z',
        '&m', '&n',  # '&ch', '&dh', '&sh', '&th', '&zh', '&l', '&r', '&ng',
        # '8nb', '8nd', '8nf', '8ng', '8nj', '8nk', '8np', '8ns', '8nt', '8nv', '8nz',
        # '8nch', '8ndh', '8nsh', '8nth', '8nzh', '8nl', '8nm', '8nn', '8nr', '8nng',
        'arb', 'ard', 'arf', 'arg', 'arj', 'ark', 'arp', 'ars', 'art', 'arv', 'arz',
        'arch', 'arsh', 'arth', 'arl', 'arm', 'arn',  # 'arr', 'arng', #'ardh', 'arzh',
        # 'Arb', 'Ard', 'Arf', 'Arg', 'Arj', 'Ark', 'Arp', 'Ars', 'Art', 'Arv', 'Arz',
        # 'Arch', 'Ardh', 'Arsh', 'Arth', 'Arzh', 'Arl', 'Arm', 'Arn', 'Arr', 'Arng',
        # 'Erb', 'Erd', 'Erf', 'Erg', 'Erj', 'Erk', 'Erp', 'Ers', 'Ert', 'Erv', 'Erz',
        # 'Erch', 'Erdh', 'Ersh', 'Erth', 'Erzh', 'Erl', 'Erm', 'Ern', 'Err', 'Erng',
        # 'Irb', 'Ird', 'Irf', 'Irg', 'Irj', 'Irk', 'Irp', 'Irs', 'Irt', 'Irv', 'Irz',
        # 'Irch', 'Irdh', 'Irsh', 'Irth', 'Irzh', 'Irl', 'Irm', 'Irn', 'Irr', 'Irng',
        # '1b', '1d', '1f', '1g', '1j', '1k', '1p', '1s', '1t', '1v', '1z',
        '1ng',  # '1ch', '1dh', '1sh', '1th', '1zh', '1l', '1m', '1n', '1r',
        # 'Angb', 'Angd', 'Angf', 'Angg', 'Angj', 'Angk', 'Angp', 'Angs', 'Angt', 'Angv', 'Angz',
        # 'Angch', 'Angdh', 'Angsh', 'Angth', 'Angzh', 'Angl', 'Angm', 'Angn', 'Angr', 'Angng',
        # '0b', '0d', '0f', '0g', '0j', '0k', '0p', '0s', '0t', '0v', '0z',
        '0l', '0r', '0ng',  # '0ch', '0dh', '0sh', '0th', '0zh', '0m', '0n',
        # '9lb', '9ld', '9lf', '9lg', '9lj', '9lk', '9lp', '9ls', '9lt', '9lv', '9lz',
        # '9lch', '9ldh', '9lsh', '9lth', '9lzh', '9ll', '9lm', '9ln', '9lr', '9lng',
        # 'llb', 'lld', 'llf', 'llg', 'llj', 'llk', 'llp', 'lls', 'llt', 'llv', 'llz',
        # 'llch', 'lldh', 'llsh', 'llth', 'llzh', 'lll', 'llm', 'lln', 'llr', 'llng',
        # 'mmb', 'mmd', 'mmf', 'mmg', 'mmj', 'mmk', 'mmp', 'mms', 'mmt', 'mmv', 'mmz',
        # 'mmch', 'mmdh', 'mmsh', 'mmth', 'mmzh', 'mml', 'mmm', 'mmn', 'mmr', 'mmng',
        'nng',  # 'nnb', 'nnd', 'nnf', 'nnj', 'nnk', 'nnp', 'nns', 'nnt', 'nnv', 'nnz',
        # 'nnch', 'nndh', 'nnsh', 'nnth', 'nnzh', 'nnl', 'nnm', 'nnn', 'nnr', 'nnng',
        # 'nngb', 'nngd', 'nngf', 'nngg', 'nngj', 'nngk', 'nngp', 'nngs', 'nngt', 'nngv', 'nngz',
        # 'nngch', 'nngdh', 'nngsh', 'nngth', 'nngzh', 'nngl', 'nngm', 'nngn', 'nngr', 'nngng',

        'ba', 'be', 'bi', 'bo', 'bu', 'bE', 'b9', 'b3', 'b@', 'bA', 'bI', 'bO', 'b8', 'bQ', 'b6', 'bx',
        'b&', 'b8n', 'b1', 'bAng', 'b0', 'b9l',  # 'bll', 'bmm', 'bnn', 'bnng', 'bar', 'bAr', 'bEr', 'bIr',
        'da', 'de', 'di', 'do', 'du', 'dE', 'd9', 'd3', 'd@', 'dA', 'dI', 'dO', 'd8', 'dQ', 'd6', 'dx',
        'd&', 'd8n', 'd1', 'dAng', 'd0', 'd9l',  # 'dll', 'dmm', 'dnn', 'dnng', 'dar', 'dAr', 'dEr', 'dIr',
        'fa', 'fe', 'fi', 'fo', 'fu', 'fE', 'f9', 'f3', 'f@', 'fA', 'fI', 'fO', 'f8', 'fQ', 'f6', 'fx',
        'f&', 'f8n', 'f1', 'fAng', 'f0', 'f9l',  # 'fll', 'fmm', 'fnn', 'fnng', 'far', 'fAr', 'fEr', 'fIr',
        'ga', 'ge', 'gi', 'go', 'gu', 'gE', 'g9', 'g3', 'g@', 'gA', 'gI', 'gO', 'g8', 'gQ', 'g6', 'gx',
        'g&', 'g8n', 'g1', 'gAng', 'g0', 'g9l',  # 'gll', 'gmm', 'gnn', 'gnng', 'gar', 'gAr', 'gEr', 'gIr',
        'ja', 'je', 'ji', 'jo', 'ju', 'jE', 'j9', 'j3', 'j@', 'jA', 'jI', 'jO', 'j8', 'jQ', 'j6', 'jx',
        'j&', 'j8n', 'j1', 'jAng', 'j0', 'j9l',  # 'jll', 'jmm', 'jnn', 'jnng', 'jar', 'jAr', 'jEr', 'jIr',
        'ka', 'ke', 'ki', 'ko', 'ku', 'kE', 'k9', 'k3', 'k@', 'kA', 'kI', 'kO', 'k8', 'kQ', 'k6', 'kx',
        'k&', 'k8n', 'k1', 'kAng', 'k0', 'k9l',  # 'kll', 'kmm', 'knn', 'knng', 'kar', 'kAr', 'kEr', 'kIr',
        'pa', 'pe', 'pi', 'po', 'pu', 'pE', 'p9', 'p3', 'p@', 'pA', 'pI', 'pO', 'p8', 'pQ', 'p6', 'px',
        'p&', 'p8n', 'p1', 'pAng', 'p0', 'p9l',  # 'pll', 'pmm', 'pnn', 'pnng', 'par', 'pAr', 'pEr', 'pIr',
        'sa', 'se', 'si', 'so', 'su', 'sE', 's9', 's3', 's@', 'sA', 'sI', 'sO', 's8', 'sQ', 's6', 'sx',
        's&', 's8n', 's1', 'sAng', 's0', 's9l',  # 'sll', 'smm', 'snn', 'snng', 'sar', 'sAr', 'sEr', 'sIr',
        'ta', 'te', 'ti', 'to', 'tu', 'tE', 't9', 't3', 't@', 'tA', 'tI', 'tO', 't8', 'tQ', 't6', 'tx',
        't&', 't8n', 't1', 'tAng', 't0', 't9l',  # 'tll', 'tmm', 'tnn', 'tnng', 'tar', 'tAr', 'tEr', 'tIr',
        'va', 've', 'vi', 'vo', 'vu', 'vE', 'v9', 'v3', 'v@', 'vA', 'vI', 'vO', 'v8', 'vQ', 'v6', 'vx',
        'v&', 'v8n', 'v1', 'vAng', 'v0', 'v9l',  # 'vll', 'vmm', 'vnn', 'vnng', 'var', 'vAr', 'vEr', 'vIr',
        'za', 'ze', 'zi', 'zo', 'zu', 'zE', 'z9', 'z3', 'z@', 'zA', 'zI', 'zO', 'z8', 'zQ', 'z6', 'zx',
        'z&', 'z8n', 'z1', 'zAng', 'z0', 'z9l',  # 'zll', 'zmm', 'znn', 'znng', 'zar', 'zAr', 'zEr', 'zIr',
        'cha', 'che', 'chi', 'cho', 'chu', 'chE', 'ch9', 'ch3', 'ch@', 'chA', 'chI', 'chO', 'ch8', 'chQ', 'ch6', 'chx',
        'ch&', 'ch8n', 'ch1', 'chAng', 'ch0', 'ch9l',  # 'chll', 'chmm', 'chnn', 'chnng', 'char', 'chAr', 'chEr', 'chIr',
        'dha', 'dhe', 'dhi', 'dho', 'dhu', 'dhE', 'dh9', 'dh3', 'dh@', 'dhA', 'dhI', 'dhO', 'dh8', 'dhQ', 'dh6', 'dhx',
        'dh&', 'dh8n', 'dh1', 'dhAng', 'dh0', 'dh9l',  # 'dhll', 'dhmm', 'dhnn', 'dhnng', 'dhar', 'dhAr', 'dhEr', 'dhIr',
        'sha', 'she', 'shi', 'sho', 'shu', 'shE', 'sh9', 'sh3', 'sh@', 'shA', 'shI', 'shO', 'sh8', 'shQ', 'sh6', 'shx',
        'sh&', 'sh8n', 'sh1', 'shAng', 'sh0', 'sh9l',  # 'shll', 'shmm', 'shnn', 'shnng', 'shar', 'shAr', 'shEr', 'shIr',
        'tha', 'the', 'thi', 'tho', 'thu', 'thE', 'th9', 'th3', 'th@', 'thA', 'thI', 'thO', 'th8', 'thQ', 'th6', 'thx',
        'th&', 'th8n', 'th1', 'thAng', 'th0', 'th9l',  # 'thll', 'thmm', 'thnn', 'thnng', 'thar', 'thAr', 'thEr', 'thIr',
        'zha', 'zhe', 'zhi', 'zho', 'zhu', 'zhE', 'zh9', 'zh3', 'zh@', 'zhA', 'zhI', 'zhO', 'zh8', 'zhQ', 'zh6', 'zhx',
        'zh&', 'zh8n', 'zh1', 'zhAng', 'zh0', 'zh9l',  # 'zhll', 'zhmm', 'zhnn', 'zhnng', 'zhar', 'zhAr', 'zhEr', 'zhIr',
        # 'nga', 'nge', 'ngi', 'ngo', 'ngu', 'ngE', 'ng9', 'ng3', 'ng@', 'ngA', 'ngI', 'ngO', 'ng8', 'ngQ', 'ng6', 'ngx',
        # 'ng&', 'ng8n', 'ng1', 'ngAng', 'ng0', 'ng9l', 'ngll', 'ngmm', 'ngnn', 'ngnng', 'ngar', 'ngAr', 'ngEr', 'ngIr',
        'la', 'le', 'li', 'lo', 'lu', 'lE', 'l9', 'l3', 'l@', 'lA', 'lI', 'lO', 'l8', 'lQ', 'l6', 'lx',
        'l&', 'l8n', 'l1', 'lAng', 'l0', 'l9l',  # 'lll', 'lmm', 'lnn', 'lnng', 'lar', 'lAr', 'lEr', 'lIr',
        'ma', 'me', 'mi', 'mo', 'mu', 'mE', 'm9', 'm3', 'm@', 'mA', 'mI', 'mO', 'm8', 'mQ', 'm6', 'mx',
        'm&', 'm8n', 'm1', 'mAng', 'm0', 'm9l',  # 'mll', 'mmm', 'mnn', 'mnng', 'mar', 'mAr', 'mEr', 'mIr',
        'na', 'ne', 'ni', 'no', 'nu', 'nE', 'n9', 'n3', 'n@', 'nA', 'nI', 'nO', 'n8', 'nQ', 'n6', 'nx',
        'n&', 'n8n', 'n1', 'nAng', 'n0', 'n9l',  # 'nll', 'nmm', 'nnn', 'nnng', 'nar', 'nAr', 'nEr', 'nIr',
        'ra', 're', 'ri', 'ro', 'ru', 'rE', 'r9', 'r3', 'r@', 'rA', 'rI', 'rO', 'r8', 'rQ', 'r6', 'rx',
        'r&', 'r8n', 'r1', 'rAng', 'r0', 'r9l',  # 'rll', 'rmm', 'rnn', 'rnng', 'rar', 'rAr', 'rEr', 'rIr',
        'ha', 'he', 'hi', 'ho', 'hu', 'h9', 'h3', 'h@', 'hA', 'hI', 'hO', 'h8', 'hQ', 'h6', 'hx',  # 'hE',
        'h&', 'h8n', 'h1', 'hAng', 'h0', 'h9l',  # 'hll', 'hmm', 'hnn', 'hnng', 'har', 'hAr', 'hEr', 'hIr',
        'wa', 'we', 'wi', 'wo', 'wu', 'wE', 'w9', 'w3', 'w@', 'wA', 'wI', 'wO', 'w8', 'wQ', 'w6', 'wx',
        'w&', 'w8n', 'w1', 'wAng', 'w0', 'w9l',  # 'wll', 'wmm', 'wnn', 'wnng', 'war', 'wAr', 'wEr', 'wIr',
        'ya', 'ye', 'yi', 'yo', 'yu', 'yE', 'y9', 'y3', 'y@', 'yA', 'yI', 'yO', 'y8', 'yQ', 'y6', 'yx',
        'y&', 'y8n', 'y1', 'yAng', 'y0', 'y9l',  # 'yll', 'ymm', 'ynn', 'ynng', 'yar', 'yAr', 'yEr', 'yIr',
        'dda', 'dde', 'ddi', 'ddo', 'ddu', 'ddE', 'dd9', 'dd3', 'dd@', 'ddA', 'ddI', 'ddO', 'dd8', 'ddQ', 'dd6', 'ddx',
        'dd&', 'dd8n', 'dd1', 'ddAng', 'dd0', 'dd9l',  # 'ddll', 'ddmm', 'ddnn', 'ddnng', 'ddar', 'ddAr', 'ddEr', 'ddIr',
        'ska', 'ske', 'ski', 'sko', 'sku', 'skE', 'sk9', 'sk3', 'sk@', 'skA', 'skI', 'skO', 'sk8', 'skQ', 'sk6', 'skx',
        'sk&', 'sk8n', 'sk1', 'skAng', 'sk0', 'sk9l',  # 'skll', 'skmm', 'sknn', 'sknng', 'skar', 'skAr', 'skEr', 'skIr',
        'spa', 'spe', 'spi', 'spo', 'spu', 'spE', 'sp9', 'sp3', 'sp@', 'spA', 'spI', 'spO', 'sp8', 'spQ', 'sp6', 'spx',
        'sp&', 'sp8n', 'sp1', 'spAng', 'sp0', 'sp9l',  # 'spll', 'spmm', 'spnn', 'spnng', 'spar', 'spAr', 'spEr', 'spIr',
        'sta', 'ste', 'sti', 'sto', 'stu', 'stE', 'st9', 'st3', 'st@', 'stA', 'stI', 'stO', 'st8', 'stQ', 'st6', 'stx',
        'st&', 'st8n', 'st1', 'stAng', 'st0', 'st9l',  # 'stll', 'stmm', 'stnn', 'stnng', 'star', 'stAr', 'stEr', 'stIr',
        'sma', 'sme', 'smi', 'smo', 'smu', 'smE', 'sm9', 'sm3', 'sm@', 'smA', 'smI', 'smO', 'sm8', 'smQ', 'sm6', 'smx',
        'sm&', 'sm8n', 'sm1', 'smAng', 'sm0', 'sm9l',  # 'smll', 'smmm', 'smnn', 'smnng', 'smar', 'smAr', 'smEr', 'smIr',
        'sna', 'sne', 'sni', 'sno', 'snu', 'snE', 'sn9', 'sn3', 'sn@', 'snA', 'snI', 'snO', 'sn8', 'snQ', 'sn6', 'snx',
        'sn&', 'sn8n', 'sn1', 'snAng', 'sn0', 'sn9l',  # 'snll', 'snmm', 'snnn', 'snnng', 'snar', 'snAr', 'snEr', 'snIr',
        # 'nka', 'nke', 'nki', 'nko', 'nku', 'nkE', 'nk9', 'nk3', 'nk@', 'nkA', 'nkI', 'nkO', 'nk8', 'nkQ', 'nk6', 'nkx',
        # 'nk&', 'nk8n', 'nk1', 'nkAng', 'nk0', 'nk9l', 'nkll', 'nkmm', 'nknn', 'nknng', 'nkar', 'nkAr', 'nkEr', 'nkIr',
    ]

    _charset = _vowels + _consonants + _combined + ['R']

    _as_valid = {
        '\n': ['R']*4, ' ': ['R']*2
    }

    _conversion_list = [
        ('.', ''),
        (',', ''),
        ('-', ' '),
        (':', ' '),
    ]

    @classmethod
    def is_conversion_section(cls, line: str) -> bool:
        return line in [
            '[TO_IPA]',
            '[DEFAULT]',
        ]

    @classmethod
    def convert_section(cls, line: str, conversion_key: str) -> str:
        if not conversion_key or conversion_key == '[DEFAULT]':
            pass

        elif conversion_key == '[TO_IPA]':
            line = cls._prepare_ipa(line)
            line = ipa.convert(line, keep_punct=False)
            line = cls._clean_ipa(line)

        else:
            logger.info(f"Unknown conversion_key: {conversion_key}")

        return line

    @classmethod
    def _clean_ipa(cls, line: str) -> str:
        # https://en.wikipedia.org/wiki/Help:IPA/English
        ipa_removal_list = [
            ('x', ''),
            ('ʔ', ''),
            ('ɒ̃', ''),
            ('æ̃', ''),
            ('ɜː', ''),
            ('ˈ', ''),
            ('ˌ', ''),
            ('*', ''),
        ]

        ipa_ordered_conversion_arr = [
            ('ɔɪ.ər', 'QEr'),
            ('aɪ.ər', 'Ir'),
            ('aʊ.ər', '83'),
            ('eɪər', '&Er'),
            ('iːər', 'Er'),
            ('oʊər', 'O3'),
            ('aʊər', '8r'),
            ('ɔːər', '93'),
            ('ɔɪər', 'QEr'),
            ('uːər', 'o3'),
            ('aɪər', 'Ir'),
            ('ɛər', 'Ar'),
            ('ɔːr', '93'),
            ('ɜːr', 'u3'),
            ('ɑːr', 'ar'),
            ('ʊər', 'o3'),
            ('ɪər', 'Er'),
            ('ɒr', 'Q3'),
            ('ær', 'Ar'),
            ('ɪr', 'Er'),
            ('ʊr', '63'),
            ('ʌr', 'u3'),
            ('iə', 'Eu'),
            ('ən', 'en'),
            ('əl', 'el'),
            ('əm', 'em'),
            ('aʊ', '8'),
            ('eɪ', 'A'),
            ('ɔɪ', 'Q'),
            ('ɔː', '9'),
            ('iː', 'E'),
            ('oʊ', 'O'),
            ('ɛr', '3'),
            ('ər', '3'),
            ('uː', 'o'),
            ('uə', 'o'),
            ('aɪ', 'I'),
            ('ɑː', 'a'),
            ('hw', 'w'),
            ('lj', 'l'),
            ('nj', 'n'),
            ('θj', 'th'),
            ('dj', 'd'),
            ('sj', 's'),
            ('tj', 't'),
            ('zj', 'z'),
            ('ŋg', 'ŋ'),
            ('b', 'b'),
            ('d', 'd'),
            ('f', 'f'),
            ('h', 'h'),
            ('i', 'E'),
            ('j', 'y'),
            ('k', 'k'),
            ('l', 'll'),
            ('m', 'mm'),
            ('n', 'nn'),
            ('p', 'p'),
            ('r', 'r'),
            ('s', 's'),
            ('t', 't'),
            ('u', 'o'),
            ('v', 'v'),
            ('w', 'w'),
            ('z', 'z'),
            ('ɑ', 'a'),
            ('ə', 'a'),
            ('ʧ', 'ch'),
            ('ð', 'dh'),
            ('ɛ', 'e'),
            ('ɡ', 'g'),
            ('ɪ', 'i'),
            ('ʤ', 'jd'),
            ('ŋ', 'nng'),
            ('ʃ', 'sh'),
            ('θ', 'th'),
            ('ʌ', 'u'),
            ('ʒ', 'zh'),
            ('ʊ', '6'),
            ('ɒ', '9'),
            ('ɔ', '9'),
            ('æ', '@'),
        ]

        ipa_ordered_fixes = [
            ('llb', 'lb'),
            ('lld', 'ld'),
            ('llf', 'lf'),
            ('llk', 'lk'),
            ('llp', 'lp'),
            ('lls', 'ls'),
            ('llt', 'lt'),
            ('llv', 'lv'),
            ('llz', 'lz'),
            ('llch', 'lch'),
            ('lla', 'la'),
            ('lle', 'le'),
            ('lli', 'li'),
            ('llo', 'lo'),
            ('llu', 'lu'),
            ('llE', 'lE'),
            ('ll9', 'l9'),
            ('ll3', 'l3'),
            ('ll@', 'l@'),
            ('llA', 'lA'),
            ('llI', 'lI'),
            ('llO', 'lO'),
            ('ll8', 'l8'),
            ('llQ', 'lQ'),
            ('ll6', 'l6'),
            ('llx', 'lx'),
            ('ll&', 'l&'),
            ('ll1', 'l1'),
            ('ll0', 'l0'),

            ('mmy', 'my'),
            ('mmd', 'md'),
            ('mmf', 'mf'),
            ('mmp', 'mp'),
            ('mmz', 'mz'),
            ('mma', 'ma'),
            ('mme', 'me'),
            ('mmi', 'mi'),
            ('mmo', 'mo'),
            ('mmu', 'mu'),
            ('mmE', 'mE'),
            ('mm9', 'm9'),
            ('mm3', 'm3'),
            ('mm@', 'm@'),
            ('mmA', 'mA'),
            ('mmI', 'mI'),
            ('mmO', 'mO'),
            ('mm8', 'm8'),
            ('mmQ', 'mQ'),
            ('mm6', 'm6'),
            ('mmx', 'mx'),
            ('mm&', 'm&'),
            ('mm1', 'm1'),
            ('mm0', 'm0'),

            ('nny', 'ny'),
            ('nngz', 'ngz'),
            ('nnk', 'nk'),
            ('nnd', 'nd'),
            ('nns', 'ns'),
            ('nnt', 'nt'),
            ('nnz', 'nz'),
            ('nnj', 'nj'),
            ('nnch', 'nch'),
            ('nnng', 'nng'),
            ('nna', 'na'),
            ('nne', 'ne'),
            ('nni', 'ni'),
            ('nno', 'no'),
            ('nnu', 'nu'),
            ('nnE', 'nE'),
            ('nn9', 'n9'),
            ('nn3', 'n3'),
            ('nn@', 'n@'),
            ('nnA', 'nA'),
            ('nnI', 'nI'),
            ('nnO', 'nO'),
            ('nn8', 'n8'),
            ('nnQ', 'nQ'),
            ('nn6', 'n6'),
            ('nnx', 'nx'),
            ('nn&', 'n&'),
            ('nn1', 'n1'),
            ('nn0', 'n0'),

            # ('enn', 'en'),
            # ('ell', 'el'),
            # ('emm', 'em'),

            ('awA', 'aA'),
            ('ngk', 'nk'),
            ('gh', ''),
            ('hEr', 'h3'),
            ('hE', 'h1'),
            ('rz', '3z'),
            ('sc', 'sk'),
            ('zz', 'z'),
            ('1z', 'Ez'),
            ('9r', '93'),
        ]

        logger.debug('========================')
        logger.debug('========================')
        logger.debug(f"converting from ipa: {line}")

        for src, dest in ipa_removal_list + ipa_ordered_conversion_arr + ipa_ordered_fixes:
            logger.debug(f"{src} -> {dest}")
            line = line.replace(src, dest)

        logger.debug(f"converted line: {line}")
        logger.debug('========================')
        logger.debug('========================')

        return line

    @classmethod
    def _prepare_ipa(cls, line: str) -> str:
        for src, dest in cls._conversion_list:
            logger.debug(f"{src} -> {dest}")
            line = line.replace(src, dest)

        if re.search(r'\d', line):
            p = inflect.engine()
            for word in line.split():
                try:
                    replace = p.number_to_words(int(word))
                    line = line.replace(word, replace, 1)
                    logger.debug(f"number to word: {word} -> {replace}")
                except Exception:
                    pass

        for src, dest in cls._conversion_list:
            logger.debug(f"{src} -> {dest}")
            line = line.replace(src, dest)

        return line
