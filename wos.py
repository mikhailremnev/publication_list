#! /usr/bin/env python3

# from ROOT import RooFit as rf
# from ROOT import *
# import ROOT as r
import sys
import os
# import glob
# import math as m
# import datetime
# import numpy as np
# npa = np.array
# from array import array
# import re
# import matplotlib as ml
# import matplotlib.pyplot as plt
# from PIL import Image
# import socket

# import argparse

# R.gSystem.Load('libRooFit')

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

def main():
    sco = get_scopus()
    fin = open( 'savedrecs.txt' )
    pp, title, forma, source, pages, authors = [1], [''], [''], [''], [''], ['']
    doi = ['']
    i = 0
    AU = False
    TI = False
    for line in fin:
        if len( line ) < 2:
            if doi[i] in sco['doi']:
                title[i] += ', Scopus'
                sco['doi_wos_check'][ sco['doi'].index( doi[i] ) ] = 1
            i += 1
            pp.append( i+1 )
            title.append( '' )
            forma.append( '' )
            source.append( '' )
            pages.append( '' )
            authors.append( '' )
            doi.append( '' )
            continue
        if 'AU ' == line[:3]:
            AU = True
            AUn = 1
            authors[i] += line[3:].split( ',' )[0]
            continue
        if 'TI ' == line[:3]:
            TI = True
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
                title[i] += ', WoS'
                TI = False
    for i in range( len( pp ) ):
        # print( pp[i], title[i], forma[i], source[i], pages[i], authors[i] )
        # print( '{} {} {} {} {} {}'.format( pp[i], title[i], forma[i], source[i], pages[i], authors[i] ) )
        # print( '\33[0m{} \33[33m{} \33[37m{} \33[33m{} \33[37m{} \33[33m{}\33[0m'.format( pp[i], title[i], forma[i], source[i], pages[i], authors[i] ) )
        print( '\33[0m{} \33[33m{} \33[37m{} \33[33m{} \33[37m{} \33[33m{} \33[32m{}\33[0m'.format( pp[i], title[i], forma[i], source[i], pages[i], authors[i], doi[i] ) )

    if False:
        for aa in [pp, title, forma, source, pages, authors]:
            print( '\n' )
            for a in aa:
                print( a, '\n' )

    for i in range( len( pp ) ):
        print( '{} & {} & {} & {} & {} & {} \\\\'.format( pp[i], title[i], forma[i], source[i], pages[i], authors[i] ) )

    print( '\n', sco )


if __name__ == '__main__':
    main()

