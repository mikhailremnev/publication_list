#!/usr/bin/env python

"""
In case you have free Web of Science account, you cannot directly export
the list of your publications into csv/txt/anything else.

However, from your WoS profile you can use "Download CV" function and
generate PDF file with the list of all your recent publications. Then,
copy it into the wos_raw.txt file and reprocess it into proper format
with this script.
"""

from collections import defaultdict

out_f = open('wos.txt', 'w')

title = ''
# This is necessary because title, authors and publisher sections can span multiple lines
current_section = ''

for line in open('wos_raw.txt').readlines():
    line = line.strip()
    # Section name -> if it was modified
    modified = defaultdict(lambda: False)

    if line.startswith('Authors '):
        # Smith, J; Smith2, H; ... -> Smith J, Smith2 H
        author_list = line.split(': ', 1)[1].replace(';', '\n  ').replace(' ... ', '\n   ')
        out_f.write('AU ' + author_list + '\n')
        current_section = 'AU'
        modified['AU'] = True
    elif line.startswith('Published: '):
        data = line.split(': ', 1)[1]
        date, publisher = data.split(' in ', 1)
        month, year = date.split()
        out_f.write('PD ' + month + '\n')
        out_f.write('PY ' + year + '\n')

        current_section = 'PD'
        modified['PD'] = True
    elif line.startswith('DOI: '):
        doi = line.split(': ', 1)[1]
        out_f.write('DI ' + doi + '\n')
    elif current_section == 'AU':
        author_list = line.replace(';', '\n  ').replace(' ... ', '\n   ')
        out_f.write('   ' + author_list + '\n')
        modified['AU'] = True
    elif current_section == 'TI':
        out_f.write('   ' + line + '\n')
        modified['TI'] = True
    elif current_section == 'PD':
        # Probably do not print next publisher lines, we don't really need them
        out_f.write('SO ' + line + '\n')
        modified['PD'] = True
    else:
        # Move to the next publication
        out_f.write('ER\n\n')

        current_section = 'TI'
        out_f.write('TI ' + line + '\n')
        modified['TI'] = True

    if not modified[current_section]:
        current_section = ''

out_f.close()

