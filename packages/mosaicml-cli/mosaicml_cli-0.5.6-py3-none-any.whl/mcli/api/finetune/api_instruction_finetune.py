"""Instruction Finetuning API"""
from __future__ import annotations

from concurrent.futures import Future
from typing import Dict, List, Optional, Union, overload

from typing_extensions import Literal

from mcli.api.engine.engine import get_return_response, run_singular_mapi_request
from mcli.api.runs import Run
from mcli.models.finetune_config import FinetuneConfig

QUERY_FUNCTION = 'createFinetune'
VARIABLE_DATA_NAME = 'createFinetuneData'
# This returns the same data that the create_run function returns
# for consistency when rendering the describe output
QUERY = f"""
mutation CreateFinetune(${VARIABLE_DATA_NAME}: CreateFinetuneInput!) {{
  {QUERY_FUNCTION}({VARIABLE_DATA_NAME}: ${VARIABLE_DATA_NAME}) {{
    id
    name
    createdByEmail
    status
    createdAt
    startedAt
    completedAt
    updatedAt
    reason
    priority
    maxRetries
    preemptible
    retryOnSystemFailure
    resumptions {{
        clusterName
        cpus
        gpuType
        gpus
        nodes
        executionIndex
        startTime
        endTime
        status
    }}
    details {{
        originalRunInput
        metadata
        lastExecutionId
    }}
  }}
}}"""


@overload
def instruction_finetune(model: str,
                         train_data_path: str,
                         save_folder: str,
                         cluster: str,
                         eval_data_path: Optional[str] = None,
                         training_duration: Optional[str] = None,
                         learning_rate: Optional[float] = None,
                         context_length: Optional[int] = None,
                         experiment_trackers: Optional[List[Dict]] = None,
                         gpu_type: Optional[str] = None,
                         gpus: Optional[int] = None,
                         *,
                         timeout: Optional[float] = 10,
                         future: Literal[False] = False) -> Run:
    ...


@overload
def instruction_finetune(model: str,
                         train_data_path: str,
                         save_folder: str,
                         cluster: str,
                         eval_data_path: Optional[str] = None,
                         training_duration: Optional[str] = None,
                         learning_rate: Optional[float] = None,
                         context_length: Optional[int] = None,
                         experiment_trackers: Optional[List[Dict]] = None,
                         gpu_type: Optional[str] = None,
                         gpus: Optional[int] = None,
                         *,
                         timeout: Optional[float] = 10,
                         future: Literal[False] = False) -> Future[Run]:
    ...


def instruction_finetune(model: str,
                         train_data_path: str,
                         save_folder: str,
                         cluster: str,
                         eval_data_path: Optional[str] = None,
                         training_duration: Optional[str] = None,
                         learning_rate: Optional[float] = None,
                         context_length: Optional[int] = None,
                         experiment_trackers: Optional[List[Dict]] = None,
                         gpu_type: Optional[str] = None,
                         gpus: Optional[int] = None,
                         *,
                         timeout: Optional[float] = 10,
                         future: Literal[False] = False) -> Union[Run, Future[Run]]:
    """Finetunes a model on a small dataset and converts an MPT composer checkpoint to a
    hugging face checkpoint for inference.

    The provided :class:`finetune <mcli.models.finetune_config.FinetuneInput>` must contain
    enough information to fully detail the run

    Args:
        finetune: A fully-configured finetuning config to launch. The run will be queued and persisted
            in the run database.
        timeout: Time, in seconds, in which the call should complete. If the run creation
            takes too long, a TimeoutError will be raised. If ``future`` is ``True``, this
            value will be ignored.
        future: Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to `create_run` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the :type Run: output, use ``return_value.result()``
            with an optional ``timeout`` argument.

    Returns:
        A Run that includes the launched finetuning run details and the run status
    """
    config = FinetuneConfig.from_dict({
        'model': model,
        'train_data_path': train_data_path,
        'save_folder': save_folder,
        'cluster': cluster,
        'eval_data_path': eval_data_path,
        'training_duration': training_duration,
        'experiment_trackers': experiment_trackers,
        'gpu_type': gpu_type,
        'gpus': gpus,
        'learning_rate': learning_rate,
        'context_length': context_length,
    })
    finetune_config = config.to_create_finetune_api_input()
    variables = {
        VARIABLE_DATA_NAME: finetune_config,
    }

    response = run_singular_mapi_request(
        query=QUERY,
        query_function=QUERY_FUNCTION,
        return_model_type=Run,
        variables=variables,
    )
    return get_return_response(response, future=future, timeout=timeout)
