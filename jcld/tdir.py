import sys
import re

from sqlalchemy import create_engine
from xlrd import open_workbook
from path import path
from bs4 import BeautifulSoup as bs

from clld.db.meta import DBSession
from clld.db.models import common


DATA_DIR = path('/home/robert/venvs/clld/data/tdir-data/TDIR')


def read(type_):
    assert type_ in ['glosses', 'examples', 'languages', 'references']
    wb = open_workbook(DATA_DIR.joinpath('tdir.%s.comp.xls' % type_))
    for s in wb.sheets():
        break

    fields = [s.cell(0, i).value for i in range(s.ncols)]

    for row in range(1, s.nrows):
        values = []
        for i in range(s.ncols):
            value = s.cell(row, i).value
            if value in ['NULL', '--', #'%'
                         ]:
                value = None
            if isinstance(value, float):
                value = unicode(int(value))
            values.append(value)
        yield dict(zip(fields, values))


EXAMPLE_MAP = {
    u'idem': '',  # 1
    u'own': 'own',
    u'adv inclusive': '',  # 27
    u'reflexive': 'refl',
    u'scalar focus particle': 'sfp',
    u'focus particle': 'sfp',
    u'scalar focus particl': 'sfp',
    None: '',  # 13
    u'adv exclusive': 'ave',
    u'refllexive': 'refl',
    u'refl': 'refl',
    u'same': '',  # 1
    u'adnominal': 'adn',
    u'negative polarity item': '',  # 1
}

#<option value="adnom">adnominal intensifier</option>
#      <option value="excl">adverbial-exclusive intensifier</option>
#      <option value="incl">adverbial-inclusive intensifier</option>
#      <option value="refl">reflexive</option>
#      <option value="own">attributive intensifier ('own')</option>
#      <option value="scal">scalar focus particle</option>

PARAMS = {
    u'sort': u'Sortal restrictions of primary adnominal intensifier',
    #u'otherint': None,
    u'own': u"Attributive intensifier ('own')",
    u'sfp': u"Scalar focus particle ('even')",
    #u'otherrefl': u'-t&#642;&#601;&#768;-',
    u'lex': u'Lexical source of primary adnominal intensifier',
    u'refl': u'Primary reflexive marker',
    u'adn': u'Primary adnominal intensifier',
    u'ave': u'Exclusive intensifier',
}

#Primary adnominal intensifier:
#	Sortal restrictions:
#	Lexical source:
#Other intensifiers:
#Exclusive intensifier:
#Primary reflexive marker
#Other reflexive markers
#Attributive intensifier ('own'):
#Scalar focus particle ('even'):


def fix_example(e, repl='\t'):
    return unicode(bs(e.replace('</td><td>', repl)))


def load():
    wals = create_engine('postgresql://robert@/wals3')

    contributor = common.Contributor(id='gastvolker', name='Volker Gast')
    contribution = common.Contribution(
        id='tdir', name='Typological Database of Intensifiers and Reflexives')
    cc = common.ContributionContributor(
        contribution=contribution, contributor=contributor)
    DBSession.add(cc)

    for row in read('glosses'):
        DBSession.add(common.GlossAbbreviation(id=row['gloss'], name=row['explanation']))

    params = {}
    for id_, name in PARAMS.items():
        params[id_] = common.Parameter(id='tdir-' + id_, name=name)
        DBSession.add(params[id_])
        #
        # TODO: domain for sortal restrictions!
        #

    values = {}
    languages = {}
    for row in read('languages'):
        if row['adn'] and '<br>' in row['adn']:
            row['adn'], other = row['adn'].split('<br>', 1)
            if not row['otherint']:
                row['otherint'] = ''
            row['otherint'] = '\n'.join(filter(None, row['otherint'].split('<br>') + other.split('<br>')))

        row['sil'] = row['sil'].lower()
        row['sil'] = {
            'arm': 'hye',
            'vmn': 'mig',
            'gli': 'gle',
            'grk': 'ell',
            'hbr': 'heb',
            'ltn': 'lat',
            'chn': 'cmn',
            'ota': 'ote',
            'pnj': 'pan',
            'pba': 'rap',
            'esg': 'kal',
            'vla': 'zea',
            'lat': 'lav',
        }.get(row['sil'], row['sil'])

        l = common.Language(id=row['sil'].lower(), name=row['language'])
        languages[row['language']] = l
        res = wals.execute("select l.latitude, l.longitude from language as l, languageidentifier as li, identifier as i where l.pk = li.language_pk and li.identifier_pk = i.pk and i.id = '%s' and i.type = 'iso639-3';" \
                           % row['sil']).fetchone()
        if not res:
            res = wals.execute("select latitude, longitude from language where name = '%s';" % row['language']).fetchone()

        if res:
            l.latitude, l.longitude = res
        else:
            print(row['language'], row['sil'])
#(u'Classical Nahuatl', u'nci')   ???
#(u'Ancient Greek', u'gko')

        for pid in params.keys():
            value = row[pid]
            if value:
                value = common.Value(
                    id='tdir-%s-%s' % (pid, l.id),
                    name=unicode(bs(value)),
                    contribution=contribution,
                    parameter=params[pid],
                    language=l)
                values['%s-%s' % (pid, row['language'])] = value
                DBSession.add(value)

    def normalize_ref(ref):
        ref = re.sub('\s+', ' ', ref).strip()
        return unicode(bs(ref)).replace('<i>', '"').replace('</i>', '"')

    """
Ogawa, A. (1998)
Wali, K. et al. (2000)

Lyutikova. -> Lyutikova,
se-Bertit -> se-Berit

missing refs:
Sengupta, G. (2000). Lexical anaphors and pronouns in Bangla. In Lust et al. (eds.), <i>Lexical Anaphors and Pronouns in Selected South Asian Languages</i>. Berlin: Mouton de Gruyter.
Davison, A. Mistry (2000). Lexical anaphors and pronouns in Hindi/Urdu. In Lust et al. (eds.), <i>Lexical Anaphors and Pronouns in Selected South Asian Languages</i>. Berlin: Mouton de Gruyter.

"""

    refs = {}
    for row in read('references'):
        name = re.sub('\s+', ' ', row['entry'].split(').')[0].strip()) + ')'
        src = common.Source(
            id=row['ref'].strip(), name=name, description=normalize_ref(row['entry']))
        refs[name] = src
        DBSession.add(src)

    for row in read('examples'):
        if row['language'] not in languages:
            print('example for unknown language "%s"' % row['language'])
            continue

        s = common.Sentence(
            id=row['Nr'].strip(),
            name=fix_example(row['original'], repl=' '),
            language=languages[row['language']],
            analyzed=fix_example(row['original']),
            gloss=fix_example(row['gloss']),
            description=row['translation'],
            source=row['source'],
            comment=row['comments'])

        has_refs = False
        for ref in refs:
            if ref in row['source']:
                if normalize_ref(row['source']) != refs[ref].description:
                    print('-->')
                    print(row['source'])
                has_refs = True
                common.SentenceReference(sentence=s, source=refs[ref])

        if not has_refs:
            print('+++++')
            print(row['source'])

        pid = EXAMPLE_MAP[row['pov']]
        if pid:
            # associate with value!
            o = common.ValueSentence(value=values['%s-%s' % (pid, row['language'])], sentence=s)

        DBSession.add(s)
