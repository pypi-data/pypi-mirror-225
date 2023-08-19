"""Contains the definition of the base Exploration class."""

import os
from typing import Optional, Union

import numpy as np

from libensemble.libE import libE
from libensemble.tools import save_libE_output, add_unique_random_streams
from libensemble.alloc_funcs.start_only_persistent import only_persistent_gens
from libensemble.executors.mpi_executor import MPIExecutor
from libensemble.resources.resources import Resources
from libensemble.executors.executor import Executor
from libensemble.logger import LogConfig

from optimas.generators.base import Generator
from optimas.evaluators.base import Evaluator


class Exploration():
    """Base class in charge of launching an exploration (i.e., an optimization
    or parameter scan).

    Parameters
    ----------
    generator : Generator
        The generator used to suggest new Trials.
    evaluator : Evaluator
        The evaluator that will execute the Trials.
    max_evals : int
        Maximum number of trials that will be evaluated in the exploration.
    sim_workers : int
        Number of parallel workers performing simulations.
    run_async : bool, optional
        Whether the evaluators should be performed asynchronously (i.e.,
        without waiting for all workers to finish before staring a new
        evaluation). By default, True.
    history : str, optional
        Path to a history file of a past exploration from which to restart
        the new one. By default, None.
    history_save_period : int, optional
        Periodicity, in number of evaluated Trials, with which to save the
        history file to disk. By default equals to ``sim_workers``.
    exploration_dir_path : str, optional.
        Path to the exploration directory. By default, ``'./exploration'``.
    libe_comms :  {'local', 'mpi'}, optional.
        The communication mode for libEnseble. Determines whether to use
        Python ``multiprocessing`` (local mode) or MPI for the communication
        between the manager and workers. If running in ``'mpi'`` mode, the
        Optimas script should be launched with ``mpirun`` or equivalent, for
        example, ``mpirun -np N python myscript.py``. This will launch one
        manager and ``N-1`` simulation workers. In this case, the
        ``sim_workers`` parameter is ignored. By default, ``'local'`` mode
        is used.
    """
    def __init__(
        self,
        generator: Generator,
        evaluator: Evaluator,
        max_evals: int,
        sim_workers: int,
        run_async: Optional[bool] = True,
        history: Optional[str] = None,
        history_save_period: Optional[int] = None,
        exploration_dir_path: Optional[str] = './exploration',
        libe_comms: Optional[str] = 'local'
    ) -> None:
        self.generator = generator
        self.evaluator = evaluator
        self.max_evals = max_evals
        self.sim_workers = sim_workers
        self.run_async = run_async
        if history_save_period is None:
            self.history_save_period = sim_workers
        else:
            self.history_save_period = history_save_period
        self.exploration_dir_path = exploration_dir_path
        self.libe_comms = libe_comms
        self._load_history(history)
        self._create_alloc_specs()
        self._create_executor()
        self._initialize_evaluator()
        self._set_default_libe_specs()

    def run(self) -> None:
        """Run the exploration."""
        # Set exit criteria to maximum number of evaluations.
        exit_criteria = {'sim_max': self.max_evals}

        # Create persis_info.
        persis_info = add_unique_random_streams({}, self.sim_workers + 2)

        # If specified, allocate dedicated resources for the generator.
        if self.generator.dedicated_resources and self.generator.use_cuda:
            persis_info['gen_resources'] = 1
            persis_info['gen_use_gpus'] = True
        else:
            self.libE_specs['zero_resource_workers'] = [1]

        # Get gen_specs and sim_specs.
        run_params = self.evaluator.get_run_params()
        gen_specs = self.generator.get_gen_specs(self.sim_workers, run_params)
        sim_specs = self.evaluator.get_sim_specs(
            self.generator.varying_parameters,
            self.generator.objectives,
            self.generator.analyzed_parameters
        )

        # Launch exploration with libEnsemble.
        history, persis_info, flag = libE(
            sim_specs,
            gen_specs,
            exit_criteria,
            persis_info,
            self.alloc_specs,
            self.libE_specs,
            H0=self.history
        )

        # Update history.
        self.history = history

        # Update generator with the one received from libE.
        self.generator._update(persis_info[1]['generator'])

        # Determine if current rank is master.
        if self.libE_specs["comms"] == "local":
            is_master = True
            nworkers = self.sim_workers + 1
        else:
            from mpi4py import MPI
            is_master = (MPI.COMM_WORLD.Get_rank() == 0)
            nworkers = MPI.COMM_WORLD.Get_size() - 1

        # Save history.
        if is_master:
            save_libE_output(
                history, persis_info, __file__, nworkers,
                dest_path=os.path.abspath(self.exploration_dir_path))

        # Reset state of libEnsemble.
        self._reset_libensemble()

    def _create_executor(self) -> None:
        """Create libEnsemble executor."""
        self.executor = MPIExecutor()

    def _initialize_evaluator(self) -> None:
        """Initialize exploration evaluator."""
        self.evaluator.initialize()

    def _load_history(
        self,
        history: Union[str, np.ndarray, None]
    ) -> None:
        """Load history file."""
        if isinstance(history, str):
            if os.path.exists(history):
                # Load array.
                history = np.load(history)
                # Only include runs that completed
                history = history[history['sim_ended']]
            else:
                raise ValueError(
                    'History file {} does not exist.'.format(history))
        assert history is None or isinstance(history, np.ndarray), (
            'Type {} not valid for `history`'.format(type(history))
        )
        # Incorporate history into generator.
        if history is not None:
            self.generator.incorporate_history(history)
        self.history = history

    def _set_default_libe_specs(self) -> None:
        """Set default exploration libe_specs."""
        libE_specs = {}
        # Save H to file every N simulation evaluations
        # default value, if not defined
        libE_specs['save_every_k_sims'] = self.history_save_period
        # Force central mode
        libE_specs['dedicated_mode'] = False
        # Set communications and corresponding number of workers.
        libE_specs["comms"] = self.libe_comms
        if self.libe_comms == 'local':
            libE_specs["nworkers"] = self.sim_workers + 1
        elif self.libe_comms == 'mpi':
            # Warn user if openmpi is being used.
            # When running with MPI communications, openmpi cannot be used as
            # it does not support nesting MPI.
            # MPI is only imported here to avoid issues with openmpi when
            # running with local communications.
            from mpi4py import MPI
            if 'openmpi' in MPI.Get_library_version().lower():
                raise RuntimeError(
                    'Running with mpi communications is not supported with '
                    'openMPI. Please use MPICH (linux and macOS) or MSMPI '
                    '(Windows) instead.')
        else:
            raise ValueError(
                "Communication mode '{}'".format(self.libe_comms)
                + " not recognized. Possible values are 'local' or 'mpi'."
            )
        # Set exploration directory path.
        libE_specs['ensemble_dir_path'] = 'evaluations'
        libE_specs['use_workflow_dir'] = True
        libE_specs['workflow_dir_path'] = self.exploration_dir_path

        # get specs from generator and evaluator
        gen_libE_specs = self.generator.get_libe_specs()
        ev_libE_specs = self.evaluator.get_libe_specs()
        self.libE_specs = {**gen_libE_specs, **ev_libE_specs, **libE_specs}

    def _create_alloc_specs(self) -> None:
        """Create exploration alloc_specs."""
        self.alloc_specs = {
            'alloc_f': only_persistent_gens,
            'out': [('given_back', bool)],
            'user': {
                'async_return': self.run_async
            }
        }

    def _reset_libensemble(self) -> None:
        """Reset the state of libEnsemble.

        After calling `libE`, some libEnsemble attributes do not come back to
        their original states. This leads to issues if another `Exploration`
        run is launched within the same script. This method resets the
        necessary libEnsemble attributes to their original state.
        """
        if Resources.resources is not None:
            del Resources.resources
            Resources.resources = None
        if Executor.executor is not None:
            del Executor.executor
            Executor.executor = None
        LogConfig.config.logger_set = False
