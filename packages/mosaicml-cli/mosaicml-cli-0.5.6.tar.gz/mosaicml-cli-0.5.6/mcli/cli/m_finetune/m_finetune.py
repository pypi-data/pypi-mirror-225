""" mcli finetune Entrypoint """
import argparse
import logging
from http import HTTPStatus
from typing import Optional

from mcli.api.exceptions import MAPIException, cli_error_handler
from mcli.api.finetune import instruction_finetune
from mcli.cli.m_run.m_run import finish_run, run_entrypoint
from mcli.models.finetune_config import FinetuneConfig
from mcli.utils import utils_completers
from mcli.utils.utils_cli import configure_bool_arg
from mcli.utils.utils_spinner import console_status
from mcli.utils.utils_yaml import load_yaml

logger = logging.getLogger(__name__)


def print_help(**kwargs) -> int:
    del kwargs
    mock_parser = argparse.ArgumentParser()
    _configure_parser(mock_parser)
    mock_parser.print_help()
    return 1


@cli_error_handler('mcli finetune')
# pylint: disable-next=too-many-statements
def finetune_entrypoint(
    file: Optional[str] = None,
    clone: Optional[str] = None,
    follow: bool = True,
    override_model: Optional[str] = None,
    override_train_data_path: Optional[str] = None,
    override_training_duration: Optional[str] = None,
    override_save_folder: Optional[str] = None,
    override_cluster: Optional[str] = None,
    override_gpu_type: Optional[str] = None,
    override_gpu_num: Optional[int] = None,
    override_learning_rate: Optional[float] = None,
    override_context_length: Optional[int] = None,
    **kwargs,
) -> int:
    del kwargs

    runs_to_modify = sum([file is not None, clone is not None])
    if runs_to_modify != 1:
        print_help()
        raise MAPIException(HTTPStatus.BAD_REQUEST, "Must specify a file, a run to clone, or a run to restart.")
    if file:
        config_dict = load_yaml(file)
        # command line overrides
        # only supports basic format for now and not structured params
        if override_model is not None:
            config_dict['model'] = override_model

        if override_train_data_path is not None:
            config_dict['train_data_path'] = override_train_data_path

        if override_save_folder is not None:
            config_dict['save_folder'] = override_save_folder

        if override_cluster is not None:
            config_dict['cluster'] = override_cluster

        if override_gpu_type is not None:
            config_dict['gpu_type'] = override_gpu_type

        if override_gpu_num is not None:
            config_dict['gpus'] = override_gpu_num

        if override_training_duration is not None:
            config_dict['training_duration'] = override_training_duration

        if override_learning_rate is not None:
            config_dict['learning_rate'] = override_learning_rate

        if override_context_length is not None:
            config_dict['context_length'] = override_context_length

        with console_status('Submitting run...'):
            config_dict = FinetuneConfig.validate_dict(dict_to_use=config_dict)
            run = instruction_finetune(**config_dict)
        return finish_run(run, follow)

    elif clone:
        return run_entrypoint(
            clone=clone,
            follow=follow,
            override_cluster=override_cluster,
            override_gpu_type=override_gpu_type,
            override_gpu_num=override_gpu_num,
        )
    else:
        return print_help()


def add_finetune_argparser(subparser: argparse._SubParsersAction) -> None:
    finetune_parser: argparse.ArgumentParser = subparser.add_parser(
        'finetune',
        help='Launch a run in the MosaicML platform',
    )
    finetune_parser.set_defaults(func=finetune_entrypoint)
    _configure_parser(finetune_parser)


def _configure_parser(parser: argparse.ArgumentParser):
    parser.add_argument(
        '-f',
        '--file',
        dest='file',
        help='File from which to load arguments.',
    )

    clone_parser = parser.add_argument(
        '--clone',
        dest='clone',
        help='Copy the run config from an existing run',
    )
    clone_parser.completer = utils_completers.RunNameCompleter()  # pyright: ignore

    configure_bool_arg(
        parser=parser,
        field='follow',
        variable_name='follow',
        default=False,
        true_description='Follow the logs of an in-progress run.',
        false_description='Do not automatically try to follow the run\'s logs. This is the default behavior')

    parser.add_argument(
        '--model',
        dest='override_model',
        help='Optional override for model',
    )

    parser.add_argument(
        '--train-data-path',
        dest='override_train_data_path',
        help='Optional override for training data path',
    )

    parser.add_argument(
        '--save-folder',
        dest='override_save_folder',
        help='Optional override for checkpoint save folder',
    )

    cluster_parser = parser.add_argument(
        '--cluster',
        dest='override_cluster',
        help='Optional override for MCLI cluster',
    )
    cluster_parser.completer = utils_completers.ClusterNameCompleter()  # pyright: ignore

    gpu_type_parser = parser.add_argument(
        '--gpu-type',
        dest='override_gpu_type',
        help='Optional override for GPU type. Valid GPU type depend on'
        ' the cluster and GPU number requested',
    )
    gpu_type_parser.completer = utils_completers.GPUTypeCompleter()  # pyright: ignore

    parser.add_argument(
        '--gpus',
        type=int,
        dest='override_gpu_num',
        help='Optional override for number of GPUs. Valid GPU numbers '
        'depend on the cluster and GPU type',
    )

    parser.add_argument(
        '--training-duration',
        dest='override_training_duration',
        help='Optional override for training duration',
    )

    parser.add_argument(
        '--learning-rate',
        type=float,
        dest='override_learning_rate',
        help='Optional override for learning rate (float)',
    )

    parser.add_argument(
        '--context-length',
        type=int,
        dest='override_context_length',
        help='Optional override for context length',
    )
