import numpy as np

from jina.executors.evaluators.embedding import BaseEmbeddingEvaluator, expand_vector


class InfiniteNormEvaluator(BaseEmbeddingEvaluator):
    """
    :class:`InfiniteNormEvaluator` evaluates distance between actual and desired
    embeddings computing the Infinite Norm between them.
    """

    def evaluate(self, actual: 'np.array', desired: 'np.array', *args, **kwargs) -> float:
        """"
        :param actual: the embedding of the document
            (resulting from an Encoder)
        :param desired: the expected embedding of the document
        :return: the evaluation metric value for the request document
        :param args:  Additional positional arguments
        :param kwargs: Additional keyword arguments
        """
        actual = expand_vector(actual)
        desired = expand_vector(desired)
        return _infinitenorm(actual, desired)


def _get_ones(x, y):
    return np.ones((x, y))


def _ext_A(A):
    nA, dim = A.shape
    A_ext = _get_ones(nA, dim * 3)
    A_ext[:, dim:2 * dim] = A
    A_ext[:, 2 * dim:] = A ** 2
    return A_ext


def _ext_B(B):
    nB, dim = B.shape
    B_ext = _get_ones(dim * 3, nB)
    B_ext[:dim] = (B ** 2).T
    B_ext[dim:2 * dim] = -2.0 * B.T
    del B
    return B_ext


def _infinitenorm(A, B):
    return np.linalg.norm((A - B), ord=np.inf)


def _norm(A):
    return A / np.linalg.norm(A, ord=2, axis=1, keepdims=True)