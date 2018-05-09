# -*- coding: utf-8 -*-
"""
    inflection
    ~~~~~~~~~~~~

    A port of Ruby on Rails' inflector to Python.

    :copyright: (c) 2012-2015 by Janne Vanhala

    :license: MIT, see LICENSE for more details.
"""
import re

__version__ = '0.3.1'

PLURALS = [
    (r"(?i)(quiz)$", r'\1zes'),
    (r"(?i)^(oxen)$", r'\1'),
    (r"(?i)^(ox)$", r'\1en'),
    (r"(?i)(m|l)ice$", r'\1ice'),
    (r"(?i)(m|l)ouse$", r'\1ice'),
    (r"(?i)(matr|vert|ind)(?:ix|ex)$", r'\1ices'),
    (r"(?i)(x|ch|ss|sh)$", r'\1es'),
    (r"(?i)([^aeiouy]|qu)y$", r'\1ies'),
    (r"(?i)(hive)$", r'\1s'),
    (r"(?i)([lr])f$", r'\1ves'),
    (r"(?i)([^f])fe$", r'\1ves'),
    (r"(?i)sis$", 'ses'),
    (r"(?i)([ti])a$", r'\1a'),
    (r"(?i)([ti])um$", r'\1a'),
    (r"(?i)(buffal|potat|tomat)o$", r'\1oes'),
    (r"(?i)(bu)s$", r'\1ses'),
    (r"(?i)(alias|status)$", r'\1es'),
    (r"(?i)(octop|vir)i$", r'\1i'),
    (r"(?i)(octop|vir)us$", r'\1i'),
    (r"(?i)^(ax|test)is$", r'\1es'),
    (r"(?i)s$", 's'),
    (r"$", 's'),
]

SINGULARS = [
    (r"(?i)(database)s$", r'\1'),
    (r"(?i)(quiz)zes$", r'\1'),
    (r"(?i)(matr)ices$", r'\1ix'),
    (r"(?i)(vert|ind)ices$", r'\1ex'),
    (r"(?i)^(ox)en", r'\1'),
    (r"(?i)(alias|status)(es)?$", r'\1'),
    (r"(?i)(octop|vir)(us|i)$", r'\1us'),
    (r"(?i)^(a)x[ie]s$", r'\1xis'),
    (r"(?i)(cris|test)(is|es)$", r'\1is'),
    (r"(?i)(shoe)s$", r'\1'),
    (r"(?i)(o)es$", r'\1'),
    (r"(?i)(bus)(es)?$", r'\1'),
    (r"(?i)(m|l)ice$", r'\1ouse'),
    (r"(?i)(x|ch|ss|sh)es$", r'\1'),
    (r"(?i)(m)ovies$", r'\1ovie'),
    (r"(?i)(s)eries$", r'\1eries'),
    (r"(?i)([^aeiouy]|qu)ies$", r'\1y'),
    (r"(?i)([lr])ves$", r'\1f'),
    (r"(?i)(tive)s$", r'\1'),
    (r"(?i)(hive)s$", r'\1'),
    (r"(?i)([^f])ves$", r'\1fe'),
    (r"(?i)(t)he(sis|ses)$", r"\1hesis"),
    (r"(?i)(s)ynop(sis|ses)$", r"\1ynopsis"),
    (r"(?i)(p)rogno(sis|ses)$", r"\1rognosis"),
    (r"(?i)(p)arenthe(sis|ses)$", r"\1arenthesis"),
    (r"(?i)(d)iagno(sis|ses)$", r"\1iagnosis"),
    (r"(?i)(b)a(sis|ses)$", r"\1asis"),
    (r"(?i)(a)naly(sis|ses)$", r"\1nalysis"),
    (r"(?i)([t])a$", r'\1um'),
    (r"(?i)(n)ews$", r'\1ews'),
    (r"(?i)(ss)$", r'\1'),
    (r"(?i)s$", ''),
]

UNCOUNTABLES = set([
    'corpus',
    'data',
    'equipment',
    'fish',
    'focus',
    'information',
    'jeans',
    'money',
    'previous',
    'rice',
    'sameas',
    'series',
    'sheep',
    'species',
])

LIGATURES = [
    (r'ﬁ', r'fi'),
    (r'ﬂ', r'fl'),
    (r'ﬀ', r'ff'),
    (r'ﬃ', r'ffi'),
    (r'ﬄ', r'ffl')
]


def _irregular(singular, plural):
    """
    A convenience function to add appropriate rules to plurals and singular
    for irregular words.

    :param singular: irregular word in singular form
    :param plural: irregular word in plural form
    """
    def caseinsensitive(string):
        return ''.join('[' + char + char.upper() + ']' for char in string)

    if singular[0].upper() == plural[0].upper():
        PLURALS.insert(0, (
            r"(?i)(%s)%s$" % (singular[0], singular[1:]),
            r'\1' + plural[1:]
        ))
        PLURALS.insert(0, (
            r"(?i)(%s)%s$" % (plural[0], plural[1:]),
            r'\1' + plural[1:]
        ))
        SINGULARS.insert(0, (
            r"(?i)(%s)%s$" % (plural[0], plural[1:]),
            r'\1' + singular[1:]
        ))
    else:
        PLURALS.insert(0, (
            r"%s%s$" % (singular[0].upper(), caseinsensitive(singular[1:])),
            plural[0].upper() + plural[1:]
        ))
        PLURALS.insert(0, (
            r"%s%s$" % (singular[0].lower(), caseinsensitive(singular[1:])),
            plural[0].lower() + plural[1:]
        ))
        PLURALS.insert(0, (
            r"%s%s$" % (plural[0].upper(), caseinsensitive(plural[1:])),
            plural[0].upper() + plural[1:]
        ))
        PLURALS.insert(0, (
            r"%s%s$" % (plural[0].lower(), caseinsensitive(plural[1:])),
            plural[0].lower() + plural[1:]
        ))
        SINGULARS.insert(0, (
            r"%s%s$" % (plural[0].upper(), caseinsensitive(plural[1:])),
            singular[0].upper() + singular[1:]
        ))
        SINGULARS.insert(0, (
            r"%s%s$" % (plural[0].lower(), caseinsensitive(plural[1:])),
            singular[0].lower() + singular[1:]
        ))

def singularize(word):
    """
    Return the singular form of a word, the reverse of :func:`pluralize`.
    """
    for inflection in UNCOUNTABLES:
        if re.search(r'(?i)\b(%s)\Z' % inflection, word):
            return word

    for rule, replacement in SINGULARS:
        if re.search(rule, word):
            return re.sub(rule, replacement, word)
    return word


def remove_ligatures(word):
    for rule, replacement in LIGATURES:
        if re.search(rule, word):
            return re.sub(rule, replacement, word)
    return word


