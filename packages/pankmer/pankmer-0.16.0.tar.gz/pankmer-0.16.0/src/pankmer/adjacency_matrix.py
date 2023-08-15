import numpy as np
import os.path
import pandas as pd
from pankmer.index import add_score_mat_np

# def get_adjacency_matrix(input_dir):
#     metadata_file = join(input_dir, 'metadata.json')
#     with open(metadata_file, 'rt') as infile:
#         metadata = json.load(infile)
#     k = metadata['kmer_size']
#     genomes = list(metadata['genomes'].keys())
#     genomes_count = len(genomes)
#     score_bitsize = math.ceil(genomes_count/8)
#     scores_counts = count_scores(join(input_dir, 'scores.b.gz'), score_bitsize)
#     dim = len(genomes)
#     mat = np.zeros((dim, dim), dtype=int)
#     for count, score in enumerate(scores_counts):
#         score_int = int.from_bytes(score, 'big', signed=False)
#         score_multi = np.array(list(bin(int(score_int))[2:]), dtype=int)*scores_counts[score]
#         mat = add_score_mat_np(score_multi, mat)
#     df = pd.DataFrame(mat, index=genomes[::-1], columns=genomes[::-1])
#     return df

def get_adjacency_matrix(results):
    """Generate an adjacency matrix from a PKResults object
    
    Parameters
    ----------
    results : PKResults
        a PKResults object
    
    Returns
    -------
    DataFrame
        an adjacency matrix    
    """

    score_counts = {}
    for _, score in results:
        score_counts[score] = score_counts.get(score, 0) + 1
    mat = np.zeros((results.number_of_genomes,
                    results.number_of_genomes), dtype=int)
    for score, count in score_counts.items():
        score_multi = np.array(results.decode_score(score), dtype=int) * count
        mat = add_score_mat_np(score_multi, mat)
    return pd.DataFrame(mat, index=results.genomes, columns=results.genomes)
