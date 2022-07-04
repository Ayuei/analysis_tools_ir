from scipy.stats import ttest_ind
import plac
from .utils import get_parsed_runs


def independent_t_test(file_a: str, file_b: str, qrel_fp, metric="NDCG", depth=10):
    a, b = get_parsed_runs(file_a, file_b, qrels_fp=qrel_fp, metric=metric, depth=depth)

    return ttest_ind(a, b)


if __name__ == "__main__":
    print(plac.call(independent_t_test))
