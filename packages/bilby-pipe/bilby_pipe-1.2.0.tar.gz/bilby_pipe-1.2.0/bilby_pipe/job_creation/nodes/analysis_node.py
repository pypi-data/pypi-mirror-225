import os
from pathlib import Path

from ...utils import check_directory_exists_and_if_not_mkdir, logger
from ..node import Node


class AnalysisNode(Node):
    # If --osg, run analysis nodes on the OSG
    run_node_on_osg = True

    def __init__(self, inputs, generation_node, detectors, sampler, parallel_idx, dag):
        super().__init__(inputs, retry=3)
        self.dag = dag
        self.generation_node = generation_node
        self.detectors = detectors
        self.parallel_idx = parallel_idx
        self.request_cpus = inputs.request_cpus

        data_label = generation_node.job_name
        base_name = data_label.replace("generation", "analysis")
        self.base_job_name = f"{base_name}_{''.join(detectors)}"
        if parallel_idx != "":
            self.job_name = f"{self.base_job_name}_{parallel_idx}"
        else:
            self.job_name = self.base_job_name
        self.label = self.job_name

        if self.inputs.use_mpi:
            self.setup_arguments(
                parallel_program=self._get_executable_path(
                    self.inputs.analysis_executable
                )
            )

        else:
            self.setup_arguments()

        if self.inputs.transfer_files or self.inputs.osg:
            data_dump_file = generation_node.data_dump_file
            input_files_to_transfer = (
                [
                    str(data_dump_file),
                    str(self.inputs.complete_ini_file),
                ]
                + touch_checkpoint_files(
                    os.path.join(inputs.outdir, "result"),
                    self.job_name,
                    inputs.sampler,
                    inputs.result_format,
                )
                + inputs.additional_transfer_paths
            )
            self.extra_lines.extend(
                self._condor_file_transfer_lines(
                    input_files_to_transfer,
                    [self._relative_topdir(self.inputs.outdir, self.inputs.initialdir)],
                )
            )
            self.arguments.add("outdir", os.path.relpath(self.inputs.outdir))

        for det in detectors:
            self.arguments.add("detectors", det)
        self.arguments.add("label", self.label)
        self.arguments.add("data-dump-file", generation_node.data_dump_file)
        self.arguments.add("sampler", sampler)

        self.extra_lines.extend(self._checkpoint_submit_lines())
        env_vars = []
        if self.request_cpus > 1:
            env_vars.append("OMP_NUM_THREADS=1")
            # see https://git.ligo.org/computing/helpdesk/-/issues/3837#note_707110
            env_vars.append("KMP_AFFINITY='reset'")
        if self.disable_hdf5_locking:
            env_vars.append("USE_HDF5_FILE_LOCKING=FALSE")
        if env_vars:
            self.extra_lines.append(f"environment = \"{' '.join(env_vars)}\"")

        self.process_node()
        self.job.add_parent(generation_node.job)

    @property
    def executable(self):
        if self.inputs.use_mpi:
            return self._get_executable_path("mpiexec")
        elif self.inputs.analysis_executable:
            return self._get_executable_path(self.inputs.analysis_executable)
        else:
            return self._get_executable_path("bilby_pipe_analysis")

    @property
    def request_memory(self):
        return self.inputs.request_memory

    @property
    def log_directory(self):
        return self.inputs.data_analysis_log_directory

    @property
    def result_file(self):
        return f"{self.inputs.result_directory}/{self.job_name}_result.{self.inputs.result_format}"

    @property
    def slurm_walltime(self):
        """Default wall-time for base-name"""
        # Seven days
        return self.inputs.scheduler_analysis_time


def touch_checkpoint_files(directory, label, sampler, result_format="hdf5"):
    """
    Figure out the pathnames required to recover from a checkpoint.

    These may change due to upstream changes in Bilby.
    """

    def touch_pickle_file(filename):
        import dill

        if not Path(filename).exists():
            with open(filename, "wb") as ff:
                dill.dump(dict(), ff)

    abbreviations = dict(
        ptmcmcsampler="ptmcmc_temp",
        pymultinest="pm",
        ultranest="ultra",
    )

    check_directory_exists_and_if_not_mkdir(directory=directory)
    result_file = Path(directory) / f"{label}_result.{result_format}"
    result_file.touch()
    filenames = [str(result_file)]
    if sampler.lower() == "dynesty":
        for kind in ["resume", "dynesty"]:
            filename = f"{directory}/{label}_{kind}.pickle"
            touch_pickle_file(filename)
            filenames.append(filename)
    elif sampler.lower() == "bilby_mcmc":
        filename = f"{directory}/{label}_resume.pickle"
        touch_pickle_file(filename)
        filenames.append(filename)
    elif sampler.lower == "ptemcee":
        filename = f"{directory}/{label}_checkpoint_resume.pickle"
        touch_pickle_file(filename)
        filenames.append(filename)
    elif sampler.lower() == "nessai":
        dirname = f"{directory}/{label}_nessai"
        check_directory_exists_and_if_not_mkdir(directory=dirname)
        filenames.append(dirname)
        subdirectories = ["proposal", "diagnostics"]
        for sd in subdirectories:
            subdir = os.path.join(dirname, sd)
            check_directory_exists_and_if_not_mkdir(subdir)
            filenames.append(dirname)

    elif sampler.lower() in [
        "cpnest",
        "emcee",
        "kombine",
        "ultranest",
        "ptmcmcsampler",
        "pymultinest",
        "zeus",
    ]:
        name = abbreviations.get(sampler.lower(), sampler.lower())
        dirname = f"{directory}/{name}_{label}"
        check_directory_exists_and_if_not_mkdir(directory=dirname)
        filenames.append(dirname)
    elif sampler.lower() == "pypolychord":
        dirname = f"{directory}/chains"
        check_directory_exists_and_if_not_mkdir(directory=dirname)
        filenames.append(dirname)
    else:
        logger.warning(f"Unable to predict resume files for {sampler}")
    return filenames
