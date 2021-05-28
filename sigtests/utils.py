from trec_wrapper import parse_run
from trectools import TrecQrel


def get_parsed_runs(*args, qrels_fp: str, metric: str, depth: int):
    qrel = TrecQrel(qrels_fp)
    parsed = []

    for arg in args:
        parsed.append(parse_run(arg,
                                qrels=qrel,
                                metric=metric,
                                depth=depth))

    return args
