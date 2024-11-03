This was supposed to be an end-to-end set of scripts that, given your IDs in
various citation databases, produces a list of publications, ready to be
exported into LaTeX.

1. Download all relevant publication information files:
    - [Google Scholar](https://scholar.google.com/citations?hl=en&user=v9pTs7IAAAAJ&view_op=list_works&sortby=pubdate): scholar.csv (this one necessary to download manually, for others you can use downloader scripts)
    - Scopus -> scopus.txt
    - Web Of Science -> wos.txt
    - ELibrary -> elibrary.csv

For downloading, see [downloaders/README.md](downloaders/README.md). Chances are, it
will break at some point due to the changes in the web page layout, so
you will need to download the list manually.

2. Merge all citations into one CSV file using the `./combine_citations.py`
    - The files wos.txt, scholar.csv, scopus.txt, elibrary.csv should all be in the same directory as the script.

The script will output three blocks of output, separated by empty line:
<br>
warnings about incorrect publication format and pretty-printed list of publications
<br>
table of publications in LaTeX markup.
<br>
debug data

3. Put LaTeX table of publications into tex_pub_list/table_body.tex

4. Compile the PDF document: `pdflatex main.tex`. At this step, it is likely that
you will need to apply some minor adjustments to table_body.tex

