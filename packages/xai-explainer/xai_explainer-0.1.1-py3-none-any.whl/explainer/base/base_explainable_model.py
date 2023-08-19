from abc import abstractmethod
from typing import List

import torch


class ExplainedInput:
    def __init__(
        self,
        input_tensor: torch.Tensor,
        predicted_labels: List[int],
        explanations: List[torch.tensor],
        use_logits: bool = True,
        context: dict = None,
    ):
        """
        Args:
            input_tensor: The input tensor to the model [batch_size, c, h, w] or [batch_size, h, w]
            predicted_labels: A list of labels for each predicted class
            explanations: A list of tensors that have an explaination (heatmap) for each predicted class, same length as predicted_labels
            use_logits: Whether the output tensor is logits or probabilities (i.e. set to True if the output tensor is not normalized yet, e.g. by a sigmoid)
            context: A dictionary containing any additional information that might be useful

        Raises:
            AssertionError: If checks fail (see __check_init__)
        """

        # not sure if detach and clone is necessary
        self._input: torch.Tensor = input_tensor.clone().detach().cpu()
        self._predicted_labels: List[int] = [l for l in predicted_labels]
        self._use_logits: bool = use_logits
        self._explanations: List[torch.Tensor] = [
            e.clone().detach().cpu() for e in explanations
        ]
        self._context: dict = context or {}

        self.__check_init__()

    def __check_init__(self):
        # check devices, currently always on cpu (see __init__) but might change in the future
        assert (
            str(self.input_tensor.device) == "cpu"
        ), f"Input must be on CPU, but is on {self.input_tensor.device}"
        assert all(
            [str(e.device) == "cpu" for e in self.explanations]
        ), f"Explanations must be on CPU, but are on {[e.device for e in self.explanations]}"

        # further checks
        assert len(self.predicted_labels) == len(
            self.explanations
        ), "Number of explanations must match number of predicted labels"

    @property
    def input_tensor(self):
        return self._input

    @property
    def predicted_labels(self):
        return self._predicted_labels

    @property
    def explanations(self):
        return self._explanations

    @property
    def context(self):
        return self._context

    def __iter__(self):
        return zip(self.predicted_labels, self.explanations)

    def __getitem__(self, idx):
        try:
            return self.predicted_labels[idx], self.explanations[idx]
        except IndexError:
            # raise a more informative error
            raise IndexError(
                f"Index {idx} out of range for number of elements {len(self)}"
            )

    def __len__(self):
        return len(self.predicted_labels)

    def __repr__(self):
        return f"ExplainedInput(input_tensor={self.input_tensor.shape}, explanations={self.explanations}, context={self.context})"

    def __str__(self):
        return repr(self)


class BaseExplainableModel:
    """
    Base class for explainable models, i.e. models that can explain their predictions.
    Forces the implementation of the _explain method.
    Do not override the explain method, since it does some checks before calling _explain.
    """

    def explain(self, x: torch.Tensor, *args, **kwargs) -> List[ExplainedInput]:
        """
        Explain the model's prediction on the input

        Args:
            x: The input tensor to the model [batch_size, c, h, w] or [batch_size, h, w]
            *args: Additional arguments
            **kwargs: Additional keyword arguments

        Returns:
            A list of ExplainedInput objects, one for each predicted label

        """
        explanations = self._explain(x, *args, **kwargs)

        if not self._explainations_valid(x, explanations):
            raise Exception("Invalid explanations")

        return explanations

    def _explainations_valid(
        self, x: torch.Tensor, explanations: List[ExplainedInput]
    ) -> bool:
        # Here some checks can be done to ensure that the explanations are valid
        # For example, the heatmap should be the same size as the input

        # simple instance check for now
        for e in explanations:
            if not isinstance(e, ExplainedInput):
                return False

        return True

    @abstractmethod
    def _explain(self, x: torch.Tensor, *args, **kwargs) -> List[ExplainedInput]:
        """
        Needs to be implemented by the subclass
        """
        raise NotImplementedError("Explain method not implemented")
