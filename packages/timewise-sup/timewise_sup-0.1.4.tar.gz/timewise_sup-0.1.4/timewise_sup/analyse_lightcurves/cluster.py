import argparse
import os
import subprocess
import logging
import time
import numpy as np

from timewise_sup.environment import environment_variable_defaults, load_environment
from timewise_sup.ampel_conf import ampel_conf_filename
from timewise_sup.analyse_lightcurves.create_job_file_yaml import make_ampel_job_file


logger = logging.getLogger(__name__)
tsup_data_dir = load_environment("TIMEWISE_SUP_DATA")
db_port = load_environment("TIMEWISE_SUP_MONGODB_PORT")


class Submitter:

    username = os.path.basename(os.environ["HOME"])
    status_cmd = f"condor_q {username}"
    scratch_on_nodes = "$TMPDIR"
    python_script = os.path.join(os.path.abspath(os.path.dirname(__file__)), "bayesian_blocks.py")

    def __init__(
            self,
            base_name,
            node_memory: str | None = None,
            manual_submit: bool = False,
            max_materialized_jobs: int = 10,
            **ampel_options
    ):

        self.base_name = base_name
        self.ampel_options = ampel_options

        self.dir = os.path.join(tsup_data_dir, "cluster", base_name)
        self.script_dir = os.path.join(self.dir, "scripts")
        self.log_dir = os.path.join(self.dir, "logs")
        for d in [self.dir, self.script_dir, self.log_dir]:
            if not os.path.isdir(d):
                os.makedirs(d)

        self.executable_filename = os.path.join(self.script_dir, "job.sh")
        self.ampel_job_files: dict[int, str] = dict()

        self.manual_submit = manual_submit
        self.node_memory = node_memory
        self.max_materialized_jobs = max_materialized_jobs

        self.job_id: str | None = None
        self._status_output = None

    def make_ampel_job_files(
            self,
            chunks: int | list[int],
    ):
        for c in np.atleast_1d(chunks):
            fn = make_ampel_job_file(base_name=self.base_name, chunk=c, concurrent=True, **self.ampel_options)
            self.ampel_job_files[c] = fn

    def make_executable_file(self):
        """
        Produces the executable that will be submitted to the NPX cluster.
        """

        txt = (
            f"eval \"$({os.environ['CONDA_EXE']} shell.bash hook)\" \n"
            f"conda activate {os.environ['CONDA_PREFIX']} \n"
            f"ssh -Nfl $(whoami) -L localhost:$TIMEWISE_SUP_MONGODB_PORT:localhost:$TIMEWISE_SUP_MONGODB_PORT "
            f"$(whoami)@ztf-wgs.zeuthen.desy.de \n"
            f"ampel job -config {ampel_conf_filename()} -schema $1 -task $2"
        )

        logger.debug("writing executable to " + self.executable_filename)
        with open(self.executable_filename, "w") as f:
            f.write(txt)

    def condor_submit_filename(self):
        return os.path.join(self.script_dir, f"job.submit")

    def make_condor_submit_files(
            self,
            # tasks: list[int],
            # njobs: list[int],
            # chunks: int | list[int],
    ):
        """
        Produces the submit file that will be submitted to the NPX cluster.
        """

        env_str = " ".join([f"{k}={load_environment(k)}" for k in environment_variable_defaults.keys()])
        log_base = os.path.join(self.log_dir, "chunk$(chunk)_task$(task)_$(cluster)_$(process)job")

        text = (
            f"executable = {self.executable_filename} \n"
            f"environment = \"{env_str}\" \n"
            f"log = {log_base}.log \n"
            f"output = {log_base}.out \n"
            f"error = {log_base}.err \n"
            f"should_transfer_files   = YES \n"
            f"when_to_transfer_output = ON_EXIT \n"
            f"arguments = $(ampel_job_file) $(task) \n"
            f"RequestMemory = {self.node_memory} \n"
            f"max_materialized = {self.max_materialized_jobs} \n"
            f"\n"
            f"queue $(njobs)"
        )

        fn = self.condor_submit_filename()
        logger.debug(f"writing submitfile at {fn}")
        with open(fn, "w") as f:
            f.write(text)

    def dagman_filename(
            self,
            chunks: list[int],
            tasks: list[int]
    ):
        _c = "_".join([str(c) for c in chunks])
        _t = "_".join([str(t) for t in tasks])
        _a = ""
        if len(self.ampel_options) > 0:
            for k, v in self.ampel_options.items():
                _a += f"_{k}{v}"

        return os.path.join(self.script_dir, f"chunks{_c}{_a}_tasks{_t}job.dag")

    def make_dagman_file(
            self,
            chunks: list[int],
            tasks: list[int],
            njobs: list[int]
    ):
        txt = ""
        for c in chunks:
            for i, (t, n) in enumerate(zip(tasks, njobs)):
                txt += f"JOB {c}{t} {self.condor_submit_filename()} \n"
                txt += (
                    f"VARS {c}{t} "
                    f"chunk=\"{c}\" "
                    f"ampel_job_file=\"{self.ampel_job_files[c]}\" "
                    f"task=\"{t}\" "
                    f"njobs=\"{n}\"\n"
                )

            for i in range(len(tasks) - 1):
                if i < len(tasks) - 1:
                    txt += f"PARENT {c}{tasks[i]} CHILD {c}{tasks[i+1]}\n"

            txt += "\n\n"

        fn = self.dagman_filename(chunks, tasks)
        logger.debug(f"writing dagfile to {fn}")
        with open(fn, "w") as f:
            f.write(txt)

    def submit_cluster(        
            self,
            tasks: list[int],
            njobs: list[int],
            chunks: int | list[int],
    ):
        """Submits the job to the cluster"""

        _chunks = list(np.atleast_1d(chunks))
        self.make_ampel_job_files(_chunks)
        self.make_executable_file()
        self.make_condor_submit_files()
        self.make_dagman_file(_chunks, tasks, njobs)

        if not self.manual_submit:
            cmd = f"condor_submit_dag {self.dagman_filename(_chunks, tasks)}"
            logger.debug(f"command is {cmd}")
            with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE) as prc:
                msg = prc.stdout.read().decode()  # type: ignore
            logger.info(msg)

            self.job_id = str(msg).split("cluster ")[-1].split(".")[0]

        else:
            print(
                f"You selected manual submit mode: \n"
                f"\tThe submit file can be found here: \n"
                f"\t{self.dagman_filename(_chunks, tasks)} \n"
                f"\tPlease submit this to the cluster. \n"
            )

    @staticmethod
    def get_condor_status():
        """
        Queries condor to get cluster status.
        :return: str, output of query command
        """
        cmd = "condor_q"
        return subprocess.check_output(cmd).decode()

    def collect_condor_status(self):
        """Gets the condor status and saves it to private attribute"""
        self._status_output = self.get_condor_status()

    @property
    def condor_status(self):
        """
        Get the status of jobs running on condor.
        :return: number of jobs that are done, running, waiting, total, held
        """
        status_list = [
            [y for y in ii.split(" ") if y]
            for ii in self._status_output.split("\n")[4:-6]
        ]
        done = running = waiting = total = held = None

        for li in status_list:
            if li[2] == self.job_id:
                done, running, waiting = li[5:8]
                held = 0 if len(li) == 10 else li[8]
                total = li[-2]

        return done, running, waiting, total, held

    def wait_for_job(self):

        if self.job_id:
            logger.info("waiting for job with ID " + str(self.job_id))
            time.sleep(5)

            self.collect_condor_status()
            j = 0
            while not np.all(np.array(self.condor_status) == None):
                d, r, w, t, h = self.condor_status
                logger.info(
                    f"{time.asctime(time.localtime())} - Job{self.job_id}: "
                    f"{d} done, {r} running, {w} waiting, {h} held of total {t}"
                )
                j += 1
                if j > 7:
                    logger.info(self._status_output)
                    j = 0
                time.sleep(90)
                self.collect_condor_status()

            logger.info("Done waiting for job with ID " + str(self.job_id))

        else:
            logger.info(f"No Job ID!")

    @staticmethod
    def get_pending_ids():
        condor_status = Submitter.get_condor_status()
        ids = np.array([ii.split(" ")[2] for ii in condor_status.split("\n")[4:-6]])
        return ids


def run_bayesian_blocks_on_cluster(
        base_name: str,
        tasks: list[int],
        njobs: list[int],
        chunks: int | list[int],
        node_memory: str,
        manual_submit: bool = False,
        max_materialized_jobs: int = 10,
        **bayesian_blocks_kwargs
):
    logger.info("running bayesian blocks on cluster")
    submitter = Submitter(
        base_name=base_name,
        node_memory=node_memory,
        manual_submit=manual_submit,
        max_materialized_jobs=max_materialized_jobs,
        **bayesian_blocks_kwargs
    )
    logger.debug("submitting to cluster")
    submitter.submit_cluster(chunks=chunks, tasks=tasks, njobs=njobs)
    logger.debug("waiting for job to finish")
    submitter.wait_for_job()
