#! /usr/bin/env python3

"""
Combine the publications from Scopus, Google Scholar, Web of Science, ELibrary
into a single CSV with a column that specifies if a specific publication
is indexed in each of those citation databases

Last time, I had to use an option "Export CV" from the Web Of Science,
saved it to wos_raw.txt and converted to wos.txt uses fix_wos_raw.py
"""

import sys, os, re

# TODO: CSV format for Google Scholar is terrible (unicode characters instead of latex formulae)

# Using https://stackoverflow.com/a/17904977
# for imprecise string comparison

import difflib
import csv
from pylatexenc.latexencode import unicode_to_latex, UnicodeToLatexConversionRule, get_builtin_conversion_rules, UnicodeToLatexEncoder, RULE_REGEX
latex_cyrillic_rule = UnicodeToLatexConversionRule(
        rule_type = RULE_REGEX,
        rule = [ 
            # Do not modify cyrillic characters into something like \CYRA
            (re.compile(r'([а-яА-Я]+)'), r'\1'),
            ## # Do not modify non-unicode characters related to LaTeX syntax
            ## (re.compile(r'([\\\{\}\$]+)'), r'\1'),
        ]
    )
latex_rules = [latex_cyrillic_rule, 'defaults']
latex_converter = UnicodeToLatexEncoder(conversion_rules=latex_rules, non_ascii_only=True)

def get_scopus():
    fscopus = open( 'scopus.txt' )
    o = { 'doi' : [], 'doi_wos_check' : [], 'year' : [] }
    for line in fscopus:
        if len(line) < 2:
            continue
        if line[0] == '#':
            continue
        if 'DOI: ' == line[:5]:
            o['doi'].append( line.rstrip()[5:] )
            o['doi_wos_check'].append( 0 )
        if '(' == line[0] and ')' == line[5]:
            o['year'].append( line[1:5] )
    return o

def get_gscholar():
    gscholar = open( 'scholar.csv' )
    csv_reader = csv.reader(gscholar, delimiter=',', quotechar='"')
    o = { 'title' : [], 'year' : [], 'title_wos_check' : [], 'authors': [], 'pages': [], 'publication': [],
          'title_suffix' : [] }
    for row in csv_reader:
        if row[0].endswith('Authors'): continue
        if len(row) < 7: continue
        authors = row[0]
        title = row[1]
        publication = row[2]
        pages = row[5]
        year = row[6]

        # Change list of author to include only last names
        # and use comma as a separator instead of semicolon
        authors_list = [author_name for author_name in authors.split(';') if len(author_name) > 2]
        authors = ' '.join([author_name.split()[0] for author_name in authors_list[:5]])
        authors = authors.strip(',')
        if len(authors_list) > 5:
            authors += f' и др., всего {len(authors_list)} человек'

        o['title'].append(title)
        o['year'].append(year)
        o['title_wos_check'].append(0)
        o['title_suffix'].append(', Google Scholar')
        o['authors'].append(authors)
        o['pages'].append(pages)
        if year != '': publication = f'{year} г., {publication}'
        o['publication'].append(publication)
    return o

def get_elibrary():
    elibrary = open( 'elibrary.csv' )
    csv_reader = csv.reader(elibrary, delimiter=',', quotechar='"')
    o = { 'title' : [], 'year' : [], 'title_wos_check' : [], 'authors': [], 'pages': [], 'publication': [],
          'title_suffix' : [] }
    for row in csv_reader:
        if len(row) < 3: continue
        title = row[0]
        authors = row[1]
        publication = row[2]

        # Change list of author to include only last names
        # and use comma as a separator
        authors_list = [author_name for author_name in authors.split(',') if len(author_name) > 2]
        authors = ', '.join([author_name.split()[0] for author_name in authors_list[:5]])
        authors = authors.strip(',')
        if len(authors_list) > 5:
            authors += f' и др., всего {len(authors_list)} человек'

        o['title'].append(title)
        o['title_suffix'].append(', РИНЦ')
        o['authors'].append(authors)
        o['publication'].append(publication)
        o['title_wos_check'].append(0)
    return o

def main():
    gsc = get_gscholar()
    sco = get_scopus()
    eli = get_elibrary()
    fin = open( 'wos.txt' )
    pp, title, title_suffix, forma, source, pages, authors = [1], [''], [''], [''], [''], [''], ['']
    doi = ['']
    i = 0
    AU, TI = False, False
    for line in fin:
        if len( line ) < 2:
            AU = False
            if forma[i] == '': forma[i] = 'печ.'
            title_suffix[i] += ', WoS'

            # Try to find corresponding entry in Scopus
            try:
                idx = [x.lower() for x in sco['doi']].index(doi[i].lower())
                title_suffix[i] += ', Scopus'
                sco['doi_wos_check'][ idx ] = 1
            except: pass
            i += 1
            pp.append( i + 1 )
            title.append( '' )
            title_suffix.append( '' )
            forma.append( '' )
            source.append( '' )
            pages.append( '' )
            authors.append( '' )
            doi.append( '' )
            continue
        if 'AU ' == line[:3]:
            TI, AU = False, True
            AUn = 1
            authors[i] += line[3:].split( ',' )[0]
            continue
        if 'TI ' == line[:3]:
            TI, AU = True, False
            title[i] += line[3:].rstrip()
            continue
        if 'DI ' == line[:3]:
            doi[i] += line[3:].rstrip()
            continue
        if 'J9 ' == line[:3]:
            source[i] += line[3:].rstrip()
            continue
        if 'PY ' == line[:3]:
            source[i] += ' ' + line[3:].rstrip() + ' г.'
            continue
        if 'BP ' == line[:3]:
            source[i] += ' с. ' + line[3:].rstrip()
            continue
        if 'EP ' == line[:3]:
            source[i] += '-' + line[3:].rstrip()
            continue
        if 'VL ' == line[:3]:
            source[i] += ' т. ' + line[3:].rstrip()
            continue
        if 'AR ' == line[:3]:
            source[i] += ' ' + line[3:].rstrip()
            continue
        if 'PG ' == line[:3]:
            pages[i] += line[3:].rstrip() + '/{:.3f}'.format( float(line[3:].rstrip()) / AUn )
            continue
        if 'DT ' == line[:3]:
            if 'Proceedings Paper' in line:
                forma[i] += 'тез.'
            elif 'Article' in line:
                forma[i] += 'печ.'
            continue
        if AU:
            if line[:3] == '   ':
                if AUn < 5:
                    AUn += 1
                    authors[i] += ', ' + line[3:].split( ',' )[0]
                elif AUn == 6:
                    AUn += 1
                    authors[i] += ' и др.'
                else:
                    AUn += 1
            else:
                if AUn > 5:
                    authors[i] += ', всего {} чел.'.format( AUn )
                AU = False
        if TI:
            if line[:3] == '   ':
                title[i] += line.rstrip()[2:]
            else:
                TI = False

    ################################################
    # CROSS-COMPARISON
    ################################################

    # english characters
    accepted_characters  = [chr(x) for x in range(ord('a'), ord('z') + 1)]
    # russian characters
    accepted_characters += [chr(x) for x in range(ord('а'), ord('я') + 1)]

    def titles_match(title1, title2):
        if len(title1) < 2 or len(title2) < 2:
            return False
        # Clean up some common names for latex symbols
        for x in ['over-bar']:
            title1 = title1.replace(x, '')
            title2 = title2.replace(x, '')
        title1 = title1.replace('ν', 'nu')
        title2 = title2.replace('ν', 'nu')
        #
        diff = difflib.ndiff(title1.lower(), title2.lower())
        diff_count = len([x for x in diff if x[0] != ' ' and x[-1] in accepted_characters])
        if 'Inclusive' in title1 and 'Inclusive' in title2:
            print(title1, title2, diff_count)
            print(diff_count / len(title1), diff_count, len(title1))
        if diff_count / len(title1) > 0.05:
            # More than 5% difference in titles
            return False
        return True
    def suffix_exists(title1, title2, title_suffix, category1, category2):
        if category2 in title_suffix:
            print(f'Error: {category2} might contain duplicate entries')
            print(f'{title1} from {category1} is similar to {title2} but is already ' +\
                  f'associated to other {category2} article')
            return True
        return False


    ########################
    # Cross-comparison:
    # WoS    vs    Google Scholar 
    ########################
    for i in range(len(title)):
        for j in range( len(gsc['title']) ):
            title1, title2 = title[i], gsc['title'][j]
            if gsc['title_wos_check'][j] != 0:
                continue
            if not titles_match(title1, title2):
                continue
            gsc['title_wos_check'][j] = 1
            if suffix_exists(title1, title2, title_suffix[i], 'WoS', 'Google Scholar'):
                continue
            title_suffix[i] += ', Google Scholar'

    ########################
    # Cross-comparison:
    # WoS    vs    РИНЦ
    ########################
    for i in range(len(title)):
        for j in range( len(eli['title']) ):
            title1, title2 = title[i], eli['title'][j]
            if eli['title_wos_check'][j] != 0:
                continue
            if not titles_match(title1, title2):
                continue
            eli['title_wos_check'][j] = 1
            if suffix_exists(title1, title2, title_suffix[i], 'WoS', 'РИНЦ'):
                continue
            title_suffix[i] += ', РИНЦ'

    ########################
    # Cross-comparison:
    # Google Scholar    vs    РИНЦ
    ########################
    for i in range( len(gsc['title']) ):
        for j in range( len(eli['title']) ):
            title1, title2 = gsc['title'][i], eli['title'][j]
            if eli['title_wos_check'][j] != 0:
                continue
            if not titles_match(title1, title2):
                continue
            eli['title_wos_check'][j] = 2
            if suffix_exists(title1, title2, gsc['title_suffix'][i], 'Google Scholar', 'РИНЦ'):
                continue
            gsc['title_suffix'][i] += ', РИНЦ'
    # TODO: Cross-comparison between all sources (C_4^2 -> 6 different ways)

    ################################################
    # Print the list of articles from WoS

    # Add ", WoS, Scopus, Google Scholar" suffixes
    for i in range( len( pp ) ):
        title[i] += title_suffix[i]

    def print_list(format_string):
        def highlight_sources(title):
            return title.replace('Google Scholar', r'\textbf{Google Scholar}').replace('Scopus', r'\textbf{Scopus}').replace('WoS', r'\textbf{WoS}').replace('РИНЦ', r'\textbf{РИНЦ}')

        idx = '\\addtocounter{publicationID}{1}\\thepublicationID'
        # Articles loaded from Web of Science
        for i in range( len( pp ) ):
            if len(title[i]) < 2: continue
            title[i] = highlight_sources(latex_converter.unicode_to_latex(title[i]))
            print( format_string.format( idx, title[i], forma[i], source[i], pages[i], authors[i], doi[i] ) )
        # Articles not found in WoS but found in Google Scholar
        for i in range( len( gsc['title'] ) ):
            if gsc['title_wos_check'][i] != 0: continue
            full_title = gsc['title'][i] + gsc['title_suffix'][i]
            full_title = highlight_sources(latex_converter.unicode_to_latex(full_title))
            print( format_string.format(
                   idx, full_title, 'печ.', gsc['publication'][i], gsc['pages'][i], gsc['authors'][i], '???' ) )
        # Articles not found in both of the above but found in elibrary
        for i in range( len( eli['title'] ) ):
            if eli['title_wos_check'][i] != 0: continue
            full_title = eli['title'][i] + eli['title_suffix'][i]
            full_title = highlight_sources(latex_converter.unicode_to_latex(full_title))
            print( format_string.format(
                   idx, full_title, 'печ.', eli['publication'][i], '', eli['authors'][i], '???' ) )
        # TODO: Might be useful to get Scopus as well

    # Pretty print the list of publications
    print_list('\33[0m{} \33[33m{} \33[37m{} \33[33m{} \33[37m{} \33[33m{} \33[32m{}\33[0m')
    print('\n')
    # Then print the same list for LaTeX, I guess?
    print_list('{} & {} & {} & {} & {} & {} \\\\')

    # for i in range( len( pp ) ):
    #     print( '\33[0m{} \33[33m{} \33[37m{} \33[33m{} \33[37m{} \33[33m{} \33[32m{}\33[0m'.format( pp[i], title[i], forma[i], source[i], pages[i], authors[i], doi[i] ) )

    # for i in range( len( pp ) ):
    #     print( '{} & {} & {} & {} & {} & {} \\\\'.format( pp[i], title[i], forma[i], source[i], pages[i], authors[i], doi[i] ) )

    print( '\n', sco )

################################################



################################################

if __name__ == '__main__':
    main()

