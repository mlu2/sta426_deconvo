# RA, 2020-12-21

from twig import log

from datetime import datetime, timezone
from contextlib import redirect_stdout
from pathlib import Path

from tcga.utils import relpath, First, unlist1

from datasource import darm, darm_meta, datapath

now = datetime.now(tz=timezone.utc).strftime("%Z-%Y%m%d-%H%M%S")

preamble = F"""
For each cell from 
Darmanis et al [[1]]({relpath(unlist1(datapath.glob("**/2015-Darmanis")))}),
as quoted in the title:

- The figure on the left shows the distribution
of the cosine similarity measure against
cells from Allen Brain M1 [[2]]({relpath(unlist1(datapath.glob("**/2019-AllenBrain-M1")))}).
The similarities above 95% quantile have been removed.
The thickness of the line scales with 
the average similarity (before removal). 

- The figure on the right shows the association
of the cell with the cells from Allen Brain M1
on the t-SNE plot by the same similarity measure.
""".strip()

with redirect_stdout((Path(__file__).parent / "readme.md").open('w')):
    print("This file was generated by", F"[{Path(__file__).name}]({Path(__file__).name})", F"({now}).")
    print("")

    print(preamble)
    print("")

    for (t, ii) in sorted(darm_meta.index.groupby(darm_meta['cell type'].str.lower()).items()):
        for i in ii:
            f = First((Path(__file__).parent / "b_cellwise").glob).then(unlist1).then(relpath).then(Path)

            (hist, tsne) = (f(F"hist/{i}*.png"), f(F"tsne/{i}*.png"))
            assert (hist.stem == tsne.stem)

            log.info(F"{i} ({t})")

            print(F"{i} ({t})")
            print("")
            print(F"![{hist.stem}]({hist})")
            print(F"![{tsne.stem}]({tsne})")
            print("")
