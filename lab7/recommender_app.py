import numpy as np
import tensorflow as tf
import tensorflow_recommenders as tfrs

ITEM_IDS = np.array(["a", "b", "c", "d", "e"])
ITEM_EMB = np.array([[1.0, 0.0],
                     [0.9, 0.1],
                     [0.5, 0.5],
                     [0.1, 0.9],
                     [0.0, 1.0]], dtype="float32")
USER_EMB = {"u1": np.array([[1.0, 0.0]], dtype="float32")}
USER_HISTORY = {"u1": {"a"}}  # items u1 already consumed


def build_index(k):
    index = tfrs.layers.factorized_top_k.BruteForce(k=k)
    index.index(candidates=tf.constant(ITEM_EMB),
                identifiers=tf.constant(ITEM_IDS))
    return index


def recommend(user_id, k=3):
    """Changed: exclude items the user already consumed, still return k items."""
    consumed = USER_HISTORY.get(user_id, set())
    index = build_index(k + len(consumed))
    scores, ids = index(tf.constant(USER_EMB[user_id]))
    out = [(i.decode(), s)
           for i, s in zip(ids.numpy()[0], scores.numpy()[0].tolist())
           if i.decode() not in consumed]
    out = out[:k]
    return [i for i, _ in out], [s for _, s in out]