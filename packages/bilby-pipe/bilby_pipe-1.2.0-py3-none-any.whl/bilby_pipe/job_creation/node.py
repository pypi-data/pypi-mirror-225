import os
import re
import shutil
import subprocess
from pathlib import Path

import pycondor

from ..utils import CHECKPOINT_EXIT_CODE, ArgumentsString, BilbyPipeError, logger


class Node(object):
    """Base Node object, handles creation of arguments, executables, etc"""

    # Flag to not run on the OSG - overwritten in child nodes
    run_node_on_osg = False

    def __init__(self, inputs, retry=None):
        self.inputs = inputs
        self._universe = "vanilla"
        self.request_disk = self.inputs.request_disk
        self.getenv = True
        self.notification = inputs.notification
        self.retry = retry
        self.verbose = 0
        self.condor_job_priority = inputs.condor_job_priority
        self.disable_hdf5_locking = inputs.disable_hdf5_locking
        self.extra_lines = list(self.inputs.extra_lines)
        self.requirements = (
            [self.inputs.requirements] if self.inputs.requirements else []
        )

    @property
    def universe(self):
        return self._universe

    def process_node(self):
        self.create_pycondor_job()

        if self.inputs.run_local:
            logger.info(
                "Running command: "
                + " ".join([self.executable] + self.arguments.argument_list)
            )
            subprocess.run([self.executable] + self.arguments.argument_list, check=True)

    def _get_executable_path(self, exe_name):
        if self.inputs._conda_path is not None:
            exe_name = f"{self.inputs._conda_path}/bin/{exe_name}"

        exe = shutil.which(exe_name)
        if exe is not None:
            return exe
        else:
            raise OSError(f"{exe_name} not installed on this system, unable to proceed")

    def setup_arguments(
        self,
        parallel_program=None,
        add_command_line_args=True,
        add_ini=True,
        add_unknown_args=True,
    ):
        self.arguments = ArgumentsString()
        if parallel_program is not None:
            self.arguments.add("np", self.inputs.request_cpus)
            self.arguments.add_positional_argument(parallel_program)
        if add_ini:
            self.arguments.add_positional_argument(self.inputs.complete_ini_file)
        if add_unknown_args:
            self.arguments.add_unknown_args(self.inputs.unknown_args)
        if add_command_line_args:
            self.arguments.add_command_line_arguments()

    @property
    def log_directory(self):
        raise NotImplementedError()

    def create_pycondor_job(self):
        job_name = self.job_name
        self.extra_lines.extend(
            _log_output_error_submit_lines(self.log_directory, job_name)
        )

        if self.inputs.scheduler.lower() == "condor":
            self.add_accounting()

        self.extra_lines.append(f"priority = {self.condor_job_priority}")
        if self.inputs.email is not None:
            self.extra_lines.append(f"notify_user = {self.inputs.email}")

        if self.inputs.queue is not None:
            self.extra_lines.append(f"+{self.inputs.queue} = True")
            self.requirements.append(f"((TARGET.{self.inputs.queue} =?= True))")

        if self.universe != "local" and self.inputs.osg:
            if self.run_node_on_osg:
                _osg_lines, _osg_reqs = self._osg_submit_options(
                    self.executable, has_ligo_frames=False
                )
                self.extra_lines.extend(_osg_lines)
                self.requirements.append(_osg_reqs)
            else:
                osg_local_node_lines = [
                    "+flock_local = True",
                    '+DESIRED_Sites = "nogrid"',
                    "should_transfer_files = NO",
                ]
                self.extra_lines.extend(osg_local_node_lines)

        if self.run_node_on_osg and self.inputs.desired_sites is not None:
            self.extra_lines.extend([f'+DESIRED_Sites = "{self.inputs.desired_sites}"'])
            self.requirements.append("IS_GLIDEIN=?=True")

        self.job = pycondor.Job(
            name=job_name,
            executable=self.executable,
            submit=self.inputs.submit_directory,
            request_memory=self.request_memory,
            request_disk=self.request_disk,
            request_cpus=self.request_cpus,
            getenv=self.getenv,
            universe=self.universe,
            initialdir=self.inputs.initialdir,
            notification=self.notification,
            requirements=" && ".join(self.requirements),
            extra_lines=self.extra_lines,
            dag=self.dag.pycondor_dag,
            arguments=self.arguments.print(),
            retry=self.retry,
            verbose=self.verbose,
        )

        # Hack to allow passing walltime down to slurm
        setattr(self.job, "slurm_walltime", self.slurm_walltime)

        logger.debug(f"Adding job: {job_name}")

    def add_accounting(self):
        """Add the accounting-group and accounting-group-user extra lines"""
        if self.inputs.accounting:
            self.extra_lines.append(f"accounting_group = {self.inputs.accounting}")
            # Check for accounting user
            if self.inputs.accounting_user:
                self.extra_lines.append(
                    f"accounting_group_user = {self.inputs.accounting_user}"
                )
        else:
            raise BilbyPipeError(
                "No accounting tag provided - this is required for condor submission"
            )

    @staticmethod
    def _checkpoint_submit_lines():
        return [
            f"checkpoint_exit_code = {CHECKPOINT_EXIT_CODE}",
        ]

    @staticmethod
    def _condor_file_transfer_lines(inputs, outputs):
        return [
            "should_transfer_files = YES",
            f"transfer_input_files = {','.join(inputs)}",
            f"transfer_output_files = {','.join(outputs)}",
            "when_to_transfer_output = ON_EXIT_OR_EVICT",
            "preserve_relative_paths = True",
            "stream_error = True",
            "stream_output = True",
        ]

    @staticmethod
    def _relative_topdir(path, reference):
        """Returns the top-level directory name of a path relative
        to a reference
        """
        try:
            return str(Path(path).resolve().relative_to(reference))
        except ValueError as exc:
            exc.args = (f"cannot format {path} relative to {reference}",)
            raise

    def _osg_submit_options(self, executable, has_ligo_frames=False):
        """Returns the extra submit lines and requirements to enable running
        a job on the Open Science Grid

        Returns
        -------
        lines : list
            the list of extra submit lines to include
        requirements : str
            the extra requirements line to include
        """
        # required for OSG submission
        lines = []
        requirements = []

        # if we need GWF data:
        if has_ligo_frames:
            requirements.append("(HAS_LIGO_FRAMES=?=True)")

        # if need a /cvmfs repo for the software:
        # NOTE: this should really be applied to _all_ workflows
        #       that need CVMFS, not just distributed ones, but
        #       not all local pools advertise the CVMFS repo flags
        if executable.startswith("/cvmfs"):
            repo = executable.split(os.path.sep, 3)[2]
            requirements.append(f"(HAS_CVMFS_{re.sub('[.-]', '_', repo)}=?=True)")

        return lines, " && ".join(requirements)

    @property
    def slurm_walltime(self):
        """Default wall-time for base-name"""
        # One hour
        return "1:00:00"


def _log_output_error_submit_lines(logdir, prefix):
    """Returns the filepaths for condor log, output, and error options

    Parameters
    ----------
    logdir : str
        the target directory for the files
    prefix : str
        the prefix for the files

    Returns
    -------
    log, output, error : list of str
        the list of three file paths to be passed to pycondor.Job

    Examples
    --------
    >>> Dag._log_output_error_submit_lines("test", "job")
    ['log = test/job.log',
     'output = test/job.out',
     'error = test/job.err']
    """
    logpath = Path(logdir)
    filename = f"{prefix}.{{}}"
    return [
        f"{opt} = {str(logpath / filename.format(opt[:3]))}"
        for opt in ("log", "output", "error")
    ]
