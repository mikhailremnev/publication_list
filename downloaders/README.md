The scripts to download publication list from various sources.

To adjust them for your use-case, just edit corresponding ID to your author ID
(at the start of the script)

1. [01_download_scopus.py](01_download_scopus.py) — [Scopus](https://www.scopus.com/home.uri), uses Selenium webdriver.


 

2. [02_download_wos.py](02_download_wos.py) — [Web of Science](https://clarivate.com/products/web-of-science/), uses Selenium webdriver.
3. [03_download_elib.py](03_download_elib.py) — [ELibrary](https://elibrary.ru/) (РИНЦ, Russian Index of Scentific Citations), uses simple HTTP requests.
4. <s>[04_download_google_sch.py](04_download_google_sch.py)</s> — Downloader for [Google Scholar](https://scholar.google.com/) is partially implemented but there are some complications, so better to get citation data manually for that case.

They save data to either TXT or CSV files, this can be changed fairly easily.

Most of the scripts require selenium, install it with pip (
`pip install selenium` or `pip install --user selenium`)
or use the attached `00_download_selenium.sh` script to put the module in a local directory.
(it will also download geckodriver to use automated firefox)
