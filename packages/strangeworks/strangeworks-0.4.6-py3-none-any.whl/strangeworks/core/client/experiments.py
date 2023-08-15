import concurrent.futures
from dataclasses import dataclass, field
from typing import Callable, Optional, Union

from strangeworks_core.batch.utils import send_batch_request
from strangeworks_core.platform.gql import API, Operation
from strangeworks_core.types.func import Func


@dataclass
class ExperimentConfiguration:
    """
    Configuration for the experiment.

    Attributes
    ----------
    requirements_path : Optional[str], optional
        Path to a requirements.txt file, by default None
        The requirements.txt defines the dependencies required to run
        the experiment.
    local_run : bool, optional
        If True, run the experiment locally, by default False
        This allows you to test the experiment locally before submitting.
    """

    requirements_path: Optional[str] = None
    local_run: bool = False


@dataclass
class ExperimentInput:
    """
    Input to the experiment.

    Attributes
    ----------
    experiment_name : str
        Name of the experiment.
    trial_name : str
        Name of the trial.
    fargs : tuple[any], optional
        Positional arguments to the function, by default ()
    fkwargs : dict[str, any], optional
        Keyword arguments to the function, by default {}
    """

    experiment_name: str
    trial_name: str
    fargs: tuple[any] = ()
    fkwargs: dict[str, any] = field(default_factory=dict)


@dataclass
class TrialSubmission:
    """
    Output of the experiment.

    Attributes
    ----------
    success : bool
        Whether the experiment was successfully submitted.
    message : str
        Message about the experiment.
    output : Optional[any], optional
        Output of the experiment, by default None
        This output is only available if the experiment was run locally.
    """

    success: bool
    message: str
    output: Optional[any] = None


def run(
    api: API,
    func: Callable[..., any],
    input: Union[ExperimentInput, list[ExperimentInput]],
    cfg: ExperimentConfiguration = ExperimentConfiguration(),
    **kwargs,
) -> dict[str, TrialSubmission]:
    """
    Run a function as a batch job on the Strangeworks platform.

    Parameters
    ----------
    api : API
        Strangeworks API object.
    func : Callable[..., any]
        The function to run.
    input : Union[ExperimentInput, list[ExperimentInput]]
        The input to the function. If a list is provided, each element will be
        run as a separate batch job.
    cfg : ExperimentConfiguration, optional
        Configuration for the experiment, by default ExperimentConfiguration()

    Returns
    -------
    dict[str, TrialSubmission]
        A dictionary of trial names to TrialSubmission objects.

    """
    if not isinstance(input, list):
        input = [input]

    if cfg.local_run:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(
                    func, *inp.fargs, **inp.fkwargs
                ): f"trial_{inp.trial_name}_{i}"
                for i, inp in enumerate(input)
            }

            msg = "locally executed. result from function call are in output field."
            return {
                futures[future]: TrialSubmission(
                    success=True,
                    message=msg,
                    output=future.result(),
                )
                for future in concurrent.futures.as_completed(futures)
            }

    init_batch_job = Operation(
        query="""
        mutation batchJobInitiateCreate(
            $init: InitiateBatchJobCreateInput!
            $experiment_name: String!
            $trial_name: String
        ){
            batchJobInitiateCreate(
                input: {
                    initiate: $init
                    experimentName: $experiment_name
                    trialName: $trial_name
                }
            ) {
                batchJobSlug
                signedURL
            }
        }
        """
    )

    decorator_name = kwargs.get("decorator_name", "")
    out = {}
    for i, inp in enumerate(input):
        try:
            send_batch_request(
                api,
                init_batch_job,
                decorator_name,
                Func(func, inp.fargs, inp.fkwargs, cfg.requirements_path),
                experiment_name=inp.experiment_name,
                trial_name=inp.trial_name,
            )
        except Exception as e:
            out[f"trial_{inp.trial_name}_{i}"] = TrialSubmission(
                success=False,
                message="failed to submit. exception in output field.",
                output=e,
            )
        else:
            out[f"trial_{inp.trial_name}_{i}"] = TrialSubmission(
                success=True, message="successfully submitted"
            )

    return out
