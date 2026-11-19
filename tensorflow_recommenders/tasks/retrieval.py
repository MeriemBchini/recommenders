
# Copyright 2026 The TensorFlow Recommenders Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint-as: python3
"""A factorized retrieval task."""

from typing import List, Optional, Sequence, Text, Union

import numpy as np
import tensorflow as tf
from tensorflow_recommenders import layers
from tensorflow_recommenders import metrics as tfrs_metrics
from tensorflow_recommenders.tasks import base

MIN_FLOAT = np.finfo(np.float32).min / 100.0


class Retrieval(tf.keras.layers.Layer, base.Task):
  """A factorized retrieval task.

  Recommender systems are often composed of two components:
  - a retrieval model, retrieving O(thousands) candidates from a corpus of
    O(millions) candidates.
  - a ranker model, scoring the candidates retrieved by the retrieval model
    to return a ranked shortlist of a few dozen candidates.

  This task defines models that facilitate efficient retrieval of candidates
  from large corpora by maintaining a two-tower, factorized structure:
  separate query and candidate representation towers, joined at the top
  via a lightweight scoring function.
  """

  def __init__(
      self,
      loss: Optional[tf.keras.losses.Loss] = None,
      metrics: Optional[
          Union[
              Sequence[tfrs_metrics.Factorized],
              tfrs_metrics.Factorized
          ]
      ] = None,
      batch_metrics: Optional[List[tf.keras.metrics.Metric]] = None,
      loss_metrics: Optional[List[tf.keras.metrics.Metric]] = None,
      temperature: Optional[float] = None,
      num_hard_negatives: Optional[int] = None,
      remove_accidental_hits: bool = False,
      name: Optional[Text] = None,
  ) -> None:
    """Initializes the task."""

    super().__init__(name=name)

    self._loss = (
        loss
        if loss is not None
        else tf.keras.losses.CategoricalCrossentropy(
            from_logits=True,
            reduction=tf.keras.losses.Reduction.SUM,
        )
    )

    if metrics is None:
      metrics = []
    if not isinstance(metrics, Sequence):
      metrics = [metrics]

    self._factorized_metrics = metrics
    self._batch_metrics = batch_metrics or []
    self._loss_metrics = loss_metrics or []
    self._temperature = temperature
    self._num_hard_negatives = num_hard_negatives
    self._remove_accidental_hits = remove_accidental_hits

  @property
  def factorized_metrics(
      self,
  ) -> Optional[Sequence[tfrs_metrics.Factorized]]:
    """The metrics object used to compute retrieval metrics."""

    return self._factorized_metrics

  @factorized_metrics.setter
  def factorized_metrics(
      self,
      value: Optional[
          Union[
              Sequence[tfrs_metrics.Factorized],
              tfrs_metrics.Factorized
          ]
      ],
  ) -> None:
    """Sets factorized metrics."""

    if not isinstance(value, Sequence):
      value = []

    self._factorized_metrics = value

  def call(
      self,
      query_embeddings: tf.Tensor,
      candidate_embeddings: tf.Tensor,
      sample_weight: Optional[tf.Tensor] = None,
      candidate_sampling_probability: Optional[tf.Tensor] = None,
      candidate_ids: Optional[tf.Tensor] = None,
      compute_metrics: bool = True,
      compute_batch_metrics: bool = True,
      score_mask: Optional[tf.Tensor] = None,
  ) -> tf.Tensor:
    """Computes the task loss and metrics."""

    if len(tf.shape(query_embeddings)) == 3:
      scores = tf.einsum(
          "qne,ce->qnc", query_embeddings, candidate_embeddings
      )
      scores = tf.math.reduce_max(scores, axis=1)
    else:
      scores = tf.linalg.matmul(
          query_embeddings,
          candidate_embeddings,
          transpose_b=True,
      )

    num_queries = tf.shape(scores)[0]
    num_candidates = tf.shape(scores)[1]

    labels = tf.eye(num_queries, num_candidates)

    if self._temperature is not None:
      scores = scores / self._temperature

    if candidate_sampling_probability is not None:
      scores = layers.loss.SamplingProbablityCorrection()(
          scores, candidate_sampling_probability
      )

    if self._remove_accidental_hits:
      if candidate_ids is None:
        raise ValueError(
            "When accidental hit removal is enabled, candidate ids "
            "must be supplied."
        )
      scores = layers.loss.RemoveAccidentalHits()(
          labels, scores, candidate_ids
      )

    if score_mask is not None:
      scores = tf.where(score_mask, scores, MIN_FLOAT)

    if self._num_hard_negatives is not None:
      scores, labels = layers.loss.HardNegativeMining(
          self._num_hard_negatives
      )(scores, labels)

    loss = self._loss(
        y_true=labels,
        y_pred=scores,
        sample_weight=sample_weight,
    )

    update_ops = []

    for metric in self._loss_metrics:
      update_ops.append(metric.update_state(loss))

    if compute_metrics and len(tf.shape(query_embeddings)) == 2:
      for metric in self._factorized_metrics:
        update_ops.append(
            metric.update_state(
                query_embeddings,
                candidate_embeddings[:tf.shape(query_embeddings)[0]],
                true_candidate_ids=candidate_ids,
                sample_weight=sample_weight,
            )
        )

    if compute_batch_metrics:
      for metric in self._batch_metrics:
        update_ops.append(
            metric.update_state(
                labels,
                scores,
                sample_weight=sample_weight,
            )
        )

    with tf.control_dependencies(update_ops):
      return tf.identity(loss)


def _cross_replica_concat(values: tf.Tensor) -> tf.Tensor:
  """Combine tensors, one from each TPU core, into a single concatenated
  tensor.

  The resulting tensor's elements are in the order of the IDs of the cores
  that contributed them, but offset so that the first element on each core
  is the one contributed by that core.

  Args:
    values: The current TPU core's contribution to the concatenated tensor.

  Returns:
    A concatenated tensor that is made up of one tensor from each TPU core.

  Raises:
    ValueError: The current TPU core's tensor is dynamically shaped in the
      batch dimension.
  """

  if values.shape[0] is None:
    raise ValueError(
        f"Tensor {values} should not be dynamically shaped in the batch "
        "dimension."
    )

  context = tf.distribute.get_replica_context()
  gathered = context.all_gather(values, axis=0)

  return tf.roll(
      gathered,
      -context.replica_id_in_sync_group * values.shape[0],
      axis=0,
  )
