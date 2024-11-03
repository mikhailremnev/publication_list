The scripts to download publication list from various sources.

To adjust them for your use-case, just edit corresponding ID to your author ID
(at the start of the script).

NOTE: In case of both Scopus and Web of Science, it is necessary to make sure
that you can access your author profile. See "Access" section for details.

1. [01_download_scopus.py](01_download_scopus.py) — [Scopus](https://www.scopus.com/home.uri), uses Selenium webdriver. Saves citations in `scopus.csv` file.
2. [02_download_wos.py](02_download_wos.py) — [Web of Science](https://clarivate.com/products/web-of-science/), uses Selenium webdriver. Saves citations in `wos.txt` file. **Seems to be irrecoverably broken**, as it is now not possible to view user profiles without authentication.
3. [03_download_elib.py](03_download_elib.py) — [ELibrary](https://elibrary.ru/) (РИНЦ, Russian Index of Scentific Citations), uses simple HTTP requests.
4. <s>[04_download_google_sch.py](04_download_google_sch.py)</s> — Downloader for [Google Scholar](https://scholar.google.com/) is partially implemented but there are some complications, so better to get citation data manually for that case.

They save data to either TXT or CSV files, this can be changed fairly easily.

# Prerequisites

Most of the scripts require selenium, install it with pip (
`pip install selenium` or `pip install --user selenium`)
or use the attached `00_download_selenium.sh` script to put the module in a local directory.
(it will also download geckodriver to use automated firefox)

## Access

First two scripts, `01_download_scopus.py` and `02_download_wos.py` have to
either be run from inside institution network or have proxy settings configured
in the script, see the comments in the code for details.

# Troubleshooting Selenium

Most of Selenium scripts contain `-headless` option. If you remove it,
you will see bot actions in the browser window.

