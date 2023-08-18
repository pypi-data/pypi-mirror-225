import json
import tempfile
from typing import Any

import strangeworks as sw
from dimod import SampleSet
from strangeworks.core.client.jobs import Job

from strangeworks_optimization_models.problem_models import (
    StrangeworksModel,
    StrangeworksModelFactory,
)
from strangeworks_optimization_models.solution_models import (
    StrangeworksSolution,
    StrangeworksSolutionFactory,
)
from strangeworks_optimization_models.solver_models import (
    StrangeworksSolver,
    StrangeworksSolverFactory,
)
from strangeworks_optimization_models.strangeworks_models import (
    StrangeworksOptimizationJob,
    StrangeworksOptimizationModel,
    StrangeworksOptimizationSolution,
    StrangeworksOptimizationSolver,
)


class StrangeworksOptimizer:
    """Strangeworks optimization controller."""

    model: StrangeworksModel | None = None
    solver: StrangeworksSolver | None = None
    solution: StrangeworksSolution | None = None
    job: Job | None = None

    def __init__(
        self,
        model: Any | None = None,
        solver: Any | None = None,
        options: dict | None = None,
        solution: Any | None = None,
        resource_slug: str | None = None,
    ) -> None:
        self.model = StrangeworksModelFactory.from_model(model)
        self.solver = StrangeworksSolverFactory.from_solver(solver)
        self.options = options
        self.solution = StrangeworksSolutionFactory.from_solution(solution)
        self.resource_slug = resource_slug  # This is here so a user can pass in a resource slug if they want to

        self._init_resource()

    def _init_resource(self):
        if self.resource_slug:
            self.resource = sw.resources(slug=self.resource_slug)[0]
        else:
            rsc_list = sw.resources()
            for rr in range(len(rsc_list)):
                if rsc_list[rr].product.slug == "optimization":
                    self.resource = rsc_list[rr]

        product = self.solver.provider
        rsc_list = sw.resources()
        for rr in range(len(rsc_list)):
            if product.lower() in rsc_list[rr].product.name.lower():
                self.sub_rsc = rsc_list[rr]

        self.solver.strangeworks_parameters = {
            "sub_product_slug": self.sub_rsc.product.slug,
            "sub_resource_slug": self.sub_rsc.slug,
        }

    def run(self) -> Job | None:
        solver = StrangeworksOptimizationSolver.from_solver(self.solver)
        solver.solver_options = json.dumps(self.options) if self.options else json.dumps(None)

        strangeworks_optimization_job = StrangeworksOptimizationJob(
            model=StrangeworksOptimizationModel.from_model(self.model),
            solver=solver,
            solution=StrangeworksOptimizationSolution.from_solution(self.solution) if self.solution else None,
        )
        res = sw.execute(self.resource, payload=strangeworks_optimization_job.dict(), endpoint="run")

        job_slug = json.loads(res["solution"]["strangeworks_parameters"])["job_slug"]
        self.job = sw.jobs(slug=job_slug)[0]
        return self.job

    def results(self, sw_job=None):
        sw_job = sw_job or self.job
        # TODO: check job is complete using new status() function
        # either raise error or return empty results
        # if self.status() != "COMPLETED":
        #    raise ValueError("Job is not complete")

        endpoint = f"results/{sw_job.slug}"
        result = sw.execute(self.resource, endpoint=endpoint)

        # TODO: get rid of this and deserialize the solution with
        # StrangeworksOptimizationSolution methods
        sw_solution = StrangeworksOptimizationJob(**result).solution
        solution = json.loads(sw_solution.solution)
        match solution["type"]:
            case "SampleSet":
                return SampleSet.from_serializable(solution)
            # case "MPS":
            # MPS Solutions
            # return soln

    def status(self, sw_job=None):
        sw_job = sw_job or self.job

        endpoint = f"status/{sw_job.slug}"
        result = sw.execute(self.resource, endpoint=endpoint)
        return result["job_status"]

    # def get_results(self, sw_job):
    #     sw_job = sw_job or self.job
    #     current_status = self.get_status(sw_job)
    #     if current_status != "COMPLETED":
    #         new_status = self.update_status(sw_job)

    #     if current_status == "COMPLETED" or new_status == "COMPLETED":
    #         if type(sw_job) is dict:
    #             job_slug = sw_job["slug"]
    #         else:
    #             job_slug = sw_job.slug

    #         result = sw.execute(self.rsc, endpoint=f"jobs/{job_slug}")
    #         result = json.loads(result["samples_url"])

    #         try:
    #             return SampleSet.from_serializable(result)
    #         except Exception:
    #             try:
    #                 # Gurobi BQM/QUBO Solutions
    #                 return SampleSet.from_serializable(result["results"])
    #             except Exception:
    #                 # MPS Solutions
    #                 return result
    #     else:
    #         return new_status

    def upload_model(self, model=None) -> str | None:
        strangeworks_optimization_model = StrangeworksOptimizationModel.from_model(model=model or self.model)
        with tempfile.NamedTemporaryFile(mode="w+") as t:
            t.write(strangeworks_optimization_model.json())

            f = sw.upload_file(t.name)
        return f.url if isinstance(f.url, str) else None

    def get_status(self, sw_job=None):
        # Will get the current status of the job
        sw_job = sw_job or self.job
        if type(sw_job) is dict:
            job_slug = sw_job.get("slug")
        else:
            job_slug = sw_job.slug

        return sw.jobs(slug=job_slug)[0].status

    def update_status(self, sw_job):
        # Will contact the backends API to refresh/update the status of the job
        sw_job = sw_job or self.job
        if type(sw_job) is dict:
            job_slug = sw_job.get("slug")
        else:
            job_slug = sw_job.slug

        if sw.jobs(slug=job_slug)[0].status != "COMPLETED":
            res = sw.execute(self.rsc, endpoint=f"jobs/{job_slug}")
            return res["job_status"]
        else:
            return sw.jobs(slug=job_slug)[0].status

    def backends(self):
        """
        To-Do: Add cross check as to which backends the current user actually has
          access to.
                Currently, this just lists all backends that could work with the qaoa
                  service.
        """

        self.backends = sw.backends(backend_type_slugs=["optimization"])

        return self.backends
