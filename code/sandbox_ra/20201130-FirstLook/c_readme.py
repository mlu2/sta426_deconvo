# RA, 2020-12-21

from twig import log

from datetime import datetime, timezone
from contextlib import redirect_stdout
from pathlib import Path

from tcga.utils import relpath, First, unlist1

from datasource import datapath

time = datetime.now(tz=timezone.utc).strftime("%Z-%Y%m%d-%H%M%S")
this = Path(__file__)
find = First(datapath.glob).then(unlist1).then(relpath)

preambulations = F"""
Exploratory analysis on the ALS dataset 
[[1]]({find("**/20201128-FGCZ")}).

To compute the t-SNE embeddings,
the gene counts are first normalized to sum=1 for each sample,
then subset to the marker genes
from [here](https://github.com/sta426hs2020/material/blob/8c57e3b/week13-07dec2020/workflow.Rmd#L152),
see [a_exploratory.py](a_exploratory.py).

This file was generated by [{this.name}]({this.name}).
"""

with redirect_stdout((this.parent / "readme.md").open('w')):
    print(preambulations)
    print()


    def img(x):
        log.info(x)
        print(F"#### {str(x.stem).split('_')[2]}")
        print()
        # (F"![<img src='{x}' width='480px'/>]({x})")
        print(F"<img src='{x}' width='480px'/>")
        print()


    f = First((this.parent / "a_exploratory").glob).each(relpath).each(Path).then(sorted)

    print("### Histograms by condition")
    print()

    for x in f("hist*.png"):
        img(x)

    print("### T-SNE embeddings")
    print()

    for x in f("tsne*.png"):
        img(x)
