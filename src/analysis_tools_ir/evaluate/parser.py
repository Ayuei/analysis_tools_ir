import dataclasses
import os

import numpy
from trectools import TrecRun, TrecEval, TrecQrel
import pandas as pd
from typing import Union, Dict

from ..utils.cache import Cache
from ..utils.dummyfile import DummyFile


# Hijack for Recall @ K (which does not seem very useful)
def get_recall(evaluator: TrecEval, depth=1000, per_query=False, trec_eval=True, removeUnjudged=False):
    label = "Recall@%d" % (depth)

    run = evaluator.run.run_data
    qrels = evaluator.qrels.qrels_data

    # check number of queries
    nqueries = len(evaluator.run.topics())

    if removeUnjudged:
        onlyjudged = pd.merge(run, qrels[["query", "docid", "rel"]], how="left")
        onlyjudged = onlyjudged[~onlyjudged["rel"].isnull()]
        run = onlyjudged[["query", "q0", "docid", "rank", "score", "system"]]

    if trec_eval:
        trecformat = evaluator.run.run_data.sort_values(
            ["query", "score", "docid"], ascending=[True, False, False]
        ).reset_index()
        topX = (
            trecformat.groupby("query")[["query", "docid", "score"]]
            .head(depth)
            .reset_index(drop=True)
        )
    else:
        topX = (
            evaluator.run.run_data.groupby("query")[["query", "docid", "score"]]
            .head(depth)
            .reset_index(drop=True)
        )

    # gets the number of relevant documents per query
    n_relevant_docs = evaluator.get_relevant_documents(per_query=True)

    relevant_docs = qrels[qrels.rel > 0]
    selection = pd.merge(topX, relevant_docs[["query", "docid", "rel"]], how="left")
    selection = selection[~selection["rel"].isnull()]

    recall_per_query = selection.groupby("query")["docid"].count() / n_relevant_docs
    recall_per_query.name = label
    recall_per_query = recall_per_query.reset_index().set_index("query")

    if per_query:
        return recall_per_query

    return (recall_per_query.sum() / nqueries)[label]


TrecEval.get_recall = get_recall

text_attrs = {
    "ndcg": "get_ndcg",
    "p": "get_precision",
    "r": "get_relevant_documents",
    "recall": "get_recall",
    "rprec": "get_rprec",
    "bpref": "get_bpref",
}


@dataclasses.dataclass(init=True, repr=True)
class Run:
    run: Dict
    fp: str
    metric: str


def get_results(evaluator, metric, depth, **kwargs) -> float:
    results = None
    match metric.lower():
        case "ndcg":
            results = evaluator.get_ndcg(depth=depth, **kwargs)
        case "precision" | "p":
            results = evaluator.get_precision(depth=depth, **kwargs)
        case "recall" | "r":
            results = get_recall(evaluator, depth=depth, **kwargs)
        case "rprec" | "r-prec":
            results = evaluator.get_rprec(depth=depth, **kwargs)
        case "bpref" | "b-pref":
            results = evaluator.get_bpref(depth=depth, **kwargs)

    if isinstance(results, numpy.float64):
        results = results.tolist()
        if isinstance(results, float):
            return results

    results = results.to_dict()

    res_key = list(results.keys())[0]
    res = results.pop(res_key)

    return res


def _parse_run_python(fp, qrels, metric="NDCG", depth=10,
                  backend="python",
                  **kwargs) -> Run:
    if kwargs is None:
        kwargs = {"per_query": True}
    else:
        kwargs['per_query'] = True

    if isinstance(fp, list):
        fp = DummyFile.from_list(fp)

    run = TrecRun(fp.serialize() if isinstance(fp, DummyFile) else fp)

    if not isinstance(qrels, TrecQrel):
        qrels = TrecQrel(qrels)

    evaluator = TrecEval(run, qrels)

    res = get_results(evaluator, metric, depth, **kwargs)

    return Run(res, fp, metric + "@" + str(depth))


def _parse_run_binary(fp, qrels, metric, depth, **kwargs):
    raise NotImplementedError

@Cache
def parse_run(fp, qrels, metric="NDCG", depth=10,
              backend="python",
              **kwargs) -> Run:

    if backend == "python":
        _parse_run_python(fp, qrels, metric, depth, **kwargs)

    elif backend == "binary" or backend == "trec_binary":
        _parse_run_binary(fp, qrels, metric, depth, **kwargs)
    else:
        raise ValueError("Unknown backend specified: Use either trec_binary or python")
