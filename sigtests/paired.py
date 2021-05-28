from scipy.stats import ttest_rel
import plac
from sigtests.utils import get_parsed_runs


def paired_t_test(file_a: str, file_b: str, qrel_fp, metric='NDCG', depth=10):
    a, b = get_parsed_runs(file_a, file_b,
                           qrels_fp=qrel_fp,
                           metric=metric,
                           depth=depth)

    return ttest_rel(a, b)


if __name__ == "__main__":
    print(plac.call(paired_t_test))
