"""
Copyright 2023 Impulse Innovations Limited


Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations

import json
import uuid
from inspect import Parameter, isclass, signature
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    TypedDict,
    TypeVar,
    Union,
)

from pydantic import BaseModel, validator

from dara.core.base_definitions import BaseTask, CacheType, PendingTask
from dara.core.interactivity.actions import TriggerVariable
from dara.core.interactivity.any_variable import AnyVariable
from dara.core.interactivity.non_data_variable import NonDataVariable
from dara.core.internal.store import Store
from dara.core.internal.tasks import MetaTask, Task, TaskManager
from dara.core.internal.utils import CacheScope, get_cache_scope, run_user_handler
from dara.core.logging import dev_logger, eng_logger
from dara.core.metrics import RUNTIME_METRICS_TRACKER

VariableType = TypeVar('VariableType')


class DerivedVariableResult(TypedDict):
    cache_key: str
    value: Union[Any, BaseTask]


class DerivedVariable(NonDataVariable, Generic[VariableType]):
    """
    A DerivedVariable allows a value to be derived (via a function) from the current value of a set of other
    variables with a python function. This is one of two primary ways that python logic can be embedded into the
    application (the other being the @py_component decorator).

    DerivedVariables can be chained together to form complex data flows whilst keeping everything organized and
    structured in an easy to follow way. DerivedVariable results are cached automatically and will only be
    recalculated when necessary.
    """

    cache: Optional[CacheType]
    variables: List[AnyVariable]
    polling_interval: Optional[int]
    deps: Optional[List[AnyVariable]]
    nested: List[str] = []
    uid: str

    class Config:
        extra = 'forbid'
        use_enum_values = True

    def __init__(
        self,
        func: Callable[..., VariableType],
        variables: List[AnyVariable],
        cache: Optional[CacheType] = CacheType.GLOBAL,
        run_as_task: bool = False,
        polling_interval: Optional[int] = None,
        deps: Optional[List[AnyVariable]] = None,
        uid: Optional[str] = None,
    ):
        """
        A DerivedVariable allows a value to be derived (via a function) from the current value of a set of other
        variables with a python function. This is one of two primary ways that python logic can be embedded into the
        application (the other being the @py_component decorator).

        DerivedVariables can be chained together to form complex data flows whilst keeping everything organized and
        structured in an easy to follow way. DerivedVariable results are cached automatically and will only be
        recalculated when necessary.

        :param func: the function to derive a new value from the input variables.
        :param variables: a set of input variables that will be passed to the deriving function
        :param cache: whether to cache the result, defaults to global caching. Other options are to cache per user
                      session, per user or to not cache at all
        :param run_as_task: whether to run the calculation in a separate process, recommended for any CPU intensive
                            tasks, defaults to False
        :param polling_interval: an optional polling interval for the DerivedVariable. Setting this will cause the
                             component to poll the backend and refresh itself every n seconds.
        :param deps: an optional array of variables, specifying which dependant variables changing should trigger a
                        recalculation of the derived variable
        - `deps = None` - `func` is ran everytime (default behaviour),
        - `deps = []` - `func` is ran once on initial startup,
        - `deps = [var1, var2]` - `func` is ran whenever one of these vars changes
        - `deps = [var1.get('nested_property')]` - `func` is ran only when the nested property changes, other changes to the variable are ignored
        :param uid: the unique identifier for this variable; if not provided a random one is generated
        """
        # Explicitly disallow run_as_task within a Jupyter environment
        if run_as_task:
            try:
                from IPython import get_ipython
            except ImportError:
                pass
            else:
                if get_ipython() is not None:
                    raise RuntimeError('run_as_task is not supported within a Jupyter environment')

        super().__init__(cache=cache, uid=uid, variables=variables, polling_interval=polling_interval, deps=deps)

        # Import the registry of variables and register the function at import
        from dara.core.internal.registries import derived_variable_registry

        deps_indexes: Optional[List[int]] = None

        # If deps is provided, compute list of indexes of values which are present in deps
        if deps is not None:
            variables_uids = [str(var.uid) for var in variables]
            deps_uids = [str(dep.uid) for dep in deps]
            deps_indexes = [variables_uids.index(d_uid) for d_uid in deps_uids]

        derived_variable_registry.register(
            str(self.uid),
            DerivedVariableRegistryEntry(
                cache=cache,
                func=func,
                polling_interval=polling_interval,
                run_as_task=run_as_task,
                uid=str(self.uid),
                variables=variables,
                deps=deps_indexes,
            ),
        )

    @validator('deps', pre=True, always=True)
    @classmethod
    def validate_deps(cls, deps: Any, values: Dict) -> List[AnyVariable]:
        """
        If deps is not specified, set deps to include all variables used
        """
        if deps is None:
            # This will always be set on the variable with the type verified by pydantic
            return values.get('variables')   # type: ignore

        return deps

    def get(self, key: str):
        return self.copy(update={'nested': [*self.nested, key]}, deep=True)

    def trigger(self, force: bool = True):
        """
        Get a TriggerVariable action for the variable that can be used to force a recalculation.

        :param force: whether the recalculation should ignore any caching settings, defaults to True
        """
        return TriggerVariable(variable=self, force=force)

    @staticmethod
    def _get_cache_key(*args, uid: str, deps: Optional[List[int]] = None):
        """
        Convert the set of args that will be passed into the function to a string for use as the cache key. For now this
        assumes that no classes will be passed in as the underlying values will come from the UI.

        :param args: current values of arguments sent to DV
        :param uid: uid of a DerivedVariable
        :param deps: list of indexes of dependencies
        """
        key = f'{uid}'

        filtered_args = [arg for idx, arg in enumerate(args) if idx in deps] if deps is not None else args

        for arg in filtered_args:
            if isinstance(arg, dict):
                key = f'{key}:{json.dumps(arg, sort_keys=True, default=str)}'
            else:
                key = f'{key}:{arg}'
        return key

    @staticmethod
    def _restore_pydantic_models(func: Callable[..., Any], *args):
        parsed_args = []
        parameters = list(signature(func).parameters.values())
        # Scan the list for any var arg or kwarg arguments
        var_arg_idx = [i for i, val in enumerate(parameters) if val.kind == Parameter.VAR_POSITIONAL]
        var_kwarg_idx = [i for i, val in enumerate(parameters) if val.kind == Parameter.VAR_KEYWORD]

        if len(var_kwarg_idx) > 0:
            dev_logger.debug('**kwargs is not supported by DerivedVariables and will be ignored')

        # If there is no *args argument then zip the signature with the args
        if len(var_arg_idx) == 0:
            for param, arg in zip(parameters, args):
                typ = param.annotation
                if typ is not None and isclass(typ) and issubclass(typ, BaseModel) and arg is not None:
                    parsed_args.append(typ(**arg))
                    continue
                parsed_args.append(arg)
            return parsed_args

        # If there is a *args argument then zip the signature and args up to that point, then spread the rest
        for param, arg in zip(parameters[: var_arg_idx[0]], args[: var_arg_idx[0]]):
            typ = param.annotation
            if typ is not None and isclass(typ) and issubclass(typ, BaseModel) and arg is not None:
                parsed_args.append(typ(**arg))
                continue
            parsed_args.append(arg)

        parsed_args.extend(args[var_arg_idx[0] :])
        return parsed_args

    @classmethod
    def add_latest_value(cls, cache_type: Optional[CacheType], uid: str, cache_key: str):
        """
        Adds the latest value of this DerivedVariable to the registry. This method considers the cache_type of this DerivedVariable and adds or updates its entry in the registry.

        :param cache_type: the cache type for the DerivedVariable
        :param uid: the DerivedVariable uid
        :param value: the latest value to be added for that cache for that DerivedVariable
        """

        from dara.core.internal.registries import latest_value_registry

        registry_entry = get_cache_scope(cache_type)

        # Tries to register the DerivedVariable to registry, if it ValueErrors then gets the existing value and updates it
        try:
            latest_value_registry.register(
                str(uid),
                LatestValueRegistryEntry(uid=str(uid), cache_keys={registry_entry: cache_key}),
            )
        except ValueError:
            latest_value = latest_value_registry.get(str(uid))
            latest_value.cache_keys[registry_entry] = cache_key
            latest_value_registry.set(
                str(uid),
                latest_value,
            )

    @classmethod
    async def get_value(
        cls,
        var_entry: DerivedVariableRegistryEntry,
        store: Store,
        task_mgr: TaskManager,
        args: List[Any],
        force: bool = False,
    ) -> DerivedVariableResult:
        """
        Get the value of this DerivedVariable. This method will check the main app store for an appropriate response
        first, if it does not find one then it will run the underlying function in a separate process and return the
        result. Adding it to the cache in the process.

        :param var: the registry entry for the derived variable
        :param store: the store instance to check for cached values
        :param task_mgr: task manager instance
        :param args: the arguments to call the underlying function with
        :param force: whether to ignore cache
        """
        histogram = RUNTIME_METRICS_TRACKER.get_dv_histogram(var_entry.uid)

        if var_entry.run_as_task:
            from dara.core.internal.registries import utils_registry

            if utils_registry.get('TaskPool') is None:
                raise RuntimeError(
                    'Task module is not configured. Set config.task_module path to a tasks.py module to run a derived variable as task.'
                )

        with histogram.time():
            # Shortened UID used for logging
            _uid_short = f'{var_entry.uid[:3]}..{var_entry.uid[-3:]}'

            # Extract and process nested derived variables
            values = []

            # dynamic import due to circular import
            from dara.core.internal.dependency_resolution import (
                is_resolved_derived_variable,
                resolve_dependency,
            )

            eng_logger.info(f'Derived Variable {_uid_short} get_value', {'uid': var_entry.uid, 'args': args})

            for val in args:
                # Don't force nested DVs
                if is_resolved_derived_variable(val):
                    val['force'] = False

                var_value = await resolve_dependency(val, store, task_mgr)
                values.append(var_value)

            eng_logger.debug(
                f'DerivedVariable {_uid_short}', 'resolved arguments', {'values': values, 'uid': var_entry.uid}
            )

            # Loop over the passed arguments and if the expected type is a BaseModel and arg is a dict then convert the dict
            # to an instance of the BaseModel class.
            parsed_args = DerivedVariable._restore_pydantic_models(var_entry.func, *values)

            dev_logger.debug(f'DerivedVariable {_uid_short}', 'executing', {'args': parsed_args, 'uid': var_entry.uid})

            # Check if there are any Tasks to be run in the args
            has_tasks = any(isinstance(arg, BaseTask) for arg in parsed_args)

            cache_key = DerivedVariable._get_cache_key(*args, uid=var_entry.uid, deps=var_entry.deps)
            DerivedVariable.add_latest_value(var_entry.cache, var_entry.uid, cache_key)

            cache_type = var_entry.cache

            # If deps is not None, force session use
            # Note: this is temporarily commented out as no tests were broken by removing it;
            # once we find what scenario this fixes, we should add a test to cover that scenario and move this snippet
            # to constructors of DerivedVariable and DerivedDataVariable
            # if cache_type == CacheType.GLOBAL and (var_entry.deps is not None and len(var_entry.deps) > 0):
            #     cache_type = CacheType.SESSION

            eng_logger.debug(
                f'DerivedVariable {_uid_short}',
                f'using cache: {cache_type}',
                {'uid': var_entry.uid},
            )

            ignore_cache = (
                var_entry.cache is None
                or var_entry.polling_interval
                or DerivedVariable.check_polling(var_entry.variables)
            )
            value = store.get(cache_key, cache_type) if not ignore_cache else None

            eng_logger.debug(
                f'DerivedVariable {_uid_short}',
                'retrieved value from cache',
                {'uid': var_entry.uid, 'cached_value': value},
            )

            # If it's a PendingTask then return that task so it can be awaited later by a MetaTask
            if isinstance(value, PendingTask):
                eng_logger.info(
                    f'DerivedVariable {_uid_short} waiting for pending task',
                    {'uid': var_entry.uid, 'pending_task': value.task_id},
                )
                value.add_subscriber()
                return {'cache_key': cache_key, 'value': value}

            # If it's a PendingValue then wait for the value and return it
            if isinstance(value, store.PendingValue):
                eng_logger.info(
                    f'DerivedVariable {_uid_short} waiting for pending value',
                    {'uid': var_entry.uid, 'pending_value': value},
                )
                return {'cache_key': cache_key, 'value': await store.get_or_wait(cache_key, cache_type)}

            # If there is a value that is not pending then we have the result so return it
            # If force is True, don't return even if value is found and recalculate
            if not force and value is not None:
                eng_logger.info(
                    f'DerivedVariable {_uid_short} returning cached value directly',
                    {'uid': var_entry.uid, 'cached_value': value},
                )
                return {'cache_key': cache_key, 'value': value}

            # If deps is set, delete previous cache entries for the DV
            if var_entry.deps is not None:
                eng_logger.warning(
                    f'DerivedVariable {_uid_short} deleting previous cache entries', {'uid': var_entry.uid}
                )
                store.remove_starting_with(f'{var_entry.uid}:', cache_type)

            # Setup pending task if it needs it and then return the task
            if var_entry.run_as_task or has_tasks:
                var_uid = var_entry.uid or str(uuid.uuid4())

                if has_tasks:
                    task_id = f'{var_uid}_MetaTask_{str(uuid.uuid4())}'

                    extra_notify_channels = [
                        channel for arg in parsed_args if isinstance(arg, BaseTask) for channel in arg.notify_channels
                    ]
                    eng_logger.debug(
                        f'DerivedVariable {_uid_short}',
                        'running has tasks',
                        {'uid': var_entry.uid, 'task_id': task_id},
                    )
                    meta_task = MetaTask(
                        var_entry.func,
                        parsed_args,
                        notify_channels=list(set(extra_notify_channels)),
                        process_as_task=var_entry.run_as_task,
                        cache_key=cache_key,
                        task_id=task_id,
                        cache_type=cache_type,
                    )

                    return {'cache_key': cache_key, 'value': meta_task}

                task_id = f'{var_uid}_Task_{str(uuid.uuid4())}'

                eng_logger.debug(
                    f'DerivedVariable {_uid_short}',
                    'running as a task',
                    {'uid': var_entry.uid, 'task_id': task_id},
                )
                task = Task(
                    var_entry.func,
                    parsed_args,
                    cache_key=cache_key,
                    task_id=task_id,
                    cache_type=cache_type,
                )
                return {'cache_key': cache_key, 'value': task}

            store.set_pending_value(cache_key, cache_type)

            try:
                result = await run_user_handler(var_entry.func, args=parsed_args)
            except Exception as e:
                # Set the store value to None before raising, so subsequent requests don't hang on a PendingValue
                store.set(cache_key, None, cache_type, error=e)
                raise

            # If a task is returned then update pending value to pending task and return it
            if isinstance(result, BaseTask):
                eng_logger.info(
                    f'DerivedVariable {_uid_short} returning task as a result',
                    {'uid': var_entry.uid, 'task_id': result.task_id},
                )
                # Make sure cache settings are set on the task
                result.cache_key = cache_key
                result.cache_type = cache_type

                return {'cache_key': cache_key, 'value': result}

            store.set(cache_key, result, cache_type)

            eng_logger.info(
                f'DerivedVariable {_uid_short} returning result',
                {'uid': var_entry.uid, 'result': result},
            )
            return {'cache_key': cache_key, 'value': result}

    @classmethod
    def check_polling(cls, variables: List[AnyVariable]):
        for variable in variables:
            if isinstance(variable, DerivedVariable) and (
                variable.polling_interval or cls.check_polling(variables=variable.variables)
            ):
                return True
        return False

    def dict(self, *args, **kwargs):
        parent_dict = super().dict(*args, **kwargs)
        return {**parent_dict, '__typename': 'DerivedVariable', 'uid': str(parent_dict['uid'])}


class DerivedVariableRegistryEntry(BaseModel):
    cache: Optional[CacheType]
    deps: Optional[List[int]]
    func: Callable[..., Any]
    run_as_task: bool
    uid: str
    variables: List[AnyVariable]
    polling_interval: Optional[int]

    class Config:
        extra = 'forbid'


class LatestValueRegistryEntry(BaseModel):
    uid: str
    cache_keys: Dict[CacheScope, str]
