from typing import Dict, List, overload


@overload
def convert_to_trec_format(corpus: List[Dict[str, float]], run_name="EMPTY"):
    """
    Expected format of corpus:
        List[Topic_Num] -> Dict[Doc_id, Score]
    """

    trec_output = []

    for topic_num, ranked_list in enumerate(corpus):
        for rank, doc_id, score in ranked_list:
            trec_output.append(f"{topic_num}\tQ0\t{doc_id}\t{rank}\t{score}\t{run_name}\n")

    return trec_output


def convert_to_trec_format(corpus: Dict[str, Dict[str, float]], run_name="EMPTY"):
    """
    Expected format of corpus:
        Dict[Topic Number] -> Dict[Doc_id, Score]
    """

    trec_output = []

    for topic_num, ranked_list in corpus.items():
        for rank, doc_id, score in ranked_list:
            trec_output.append(f"{topic_num}\tQ0\t{doc_id}\t{rank}\t{score}\t{run_name}\n")

    return trec_output
