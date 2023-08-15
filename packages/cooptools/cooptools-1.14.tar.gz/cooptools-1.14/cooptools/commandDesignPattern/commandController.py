from dataclasses import dataclass, field
from cooptools.commandDesignPattern.commandProtocol import CommandProtocol
from cooptools.commandDesignPattern.exceptions import ResolveStateException
from typing import List, Tuple, TypeVar, Dict, Protocol, Callable
import threading
import copy
import logging
import pprint

logger = logging.getLogger('cooptools.CommandController')

T = TypeVar('T')

# @dataclass
# class CommandStoreOperations:
#     add_commands_callback: Callable
#     delete_commands_callback: Callable
#     add_cache_at_cursor_callback: Callable
#     remove_cached_at_cursor: Callable
#     get_cached: Callable
#

class CommandStore(Protocol):
    def __init__(self, reset_state: bool = False):
        if reset_state:
            self.clear_all_state()

    def add_command(self, command: CommandProtocol, cursor: int) -> List[CommandProtocol]:
        ...

    def remove_commands(self, start_cursor: int) -> List[CommandProtocol]:
        ...

    def get_commands(self, start_cursor: int = None, end_cursor: int = None) -> List[CommandProtocol]:
        ...

    def add_cached(self, state: T, cursor: int) -> Dict[int, T]:
        ...

    def remove_cached_at_cursor(self, cursor: int) -> Dict[int, T]:
        ...

    def get_cached(self) -> Dict[int, T] :
        ...

    def _get_last_cached(self, max_idx = None) -> Tuple[T, int]:
        ...

    def add_update_cached(self, state: T, cursor: int):
        self.remove_cached_at_cursor(cursor)
        self.add_cached(state, cursor)

    def last_cached(self, max_idx = None) -> Tuple[T, int]:
        try:
            return self._get_last_cached(max_idx)
        except:
            cached = self.get_cached()
            max_cached_idx = max(x for x in cached.keys() if max_idx is None or x <= max_idx)
            last_cached_state = cached[max_cached_idx]
            return last_cached_state, max_cached_idx

    def clear_cache(self):
        cached = self.get_cached()
        for cursor in cached.keys():
            self.remove_cached_at_cursor(cursor)

    def clear_commands(self):
        self.remove_commands(0)

    def clear_all_state(self):
        self.clear_commands()
        self.clear_cache()


@dataclass
class InMemoryCommandStore(CommandStore):
    command_stack: List[CommandProtocol] = field(default_factory=list, init=False)
    _cached_states: Dict[int, T] = field(default_factory=dict, init=False)

    def add_command(self, command: CommandProtocol, cursor: int) -> List[CommandProtocol]:
        self.command_stack.append(command)
        return self.command_stack

    def remove_commands(self, start_cursor: int) -> List[CommandProtocol]:
        self.command_stack = self.command_stack[:start_cursor]
        return self.command_stack

    def get_commands(self, start_cursor: int = None, end_cursor: int = None) -> List[CommandProtocol]:
        return self.command_stack[start_cursor: end_cursor]

    def add_cached(self, state: T, cursor: int) -> Dict[int, T]:
        self._cached_states[cursor] = state
        return self._cached_states

    def remove_cached_at_cursor(self, cursor: int) -> Dict[int, T]:
        del self._cached_states[cursor]
        return self._cached_states

    def get_cached(self) -> Dict[int, T]:
        return self._cached_states


@dataclass
class CommandController:
    init_state: T = None
    # command_stack: List[CommandProtocol] = field(default_factory=list, init=False)
    cache_interval: int = 100
    command_store: CommandStore = field(default_factory=InMemoryCommandStore)
    # _cached_states: List[Tuple[T, int]] = field(default_factory=list, init=False)
    cursor: int = field(default=0, init=False)
    _lock: threading.RLock = field(default_factory=threading.RLock, init=False)

    def __post_init__(self):
        cached = self.command_store.get_cached()
        has_init = len(cached) > 0

        if not has_init and self.init_state is None:
            raise ValueError(f"The init state must be set for command stores that have not been initialized")

        if not has_init and self.init_state is not None:
            self.command_store.add_cached(self.init_state, self.cursor)

        latest_cached, idx = self.command_store.last_cached()

        logger.info(f"Init State: {pprint.pformat(latest_cached)}")

    # def _cache_state(self, state):

    #     # self._cached_states.append((state, self.cursor))

    def _needsLock(foo):
        def magic(self, *args, **kwargs):
            with self._lock:
                logger.info(f"lock acquired")
                ret = foo(self, *args, **kwargs)
            logger.info(f"Lock released")
            return ret
        return magic

    @_needsLock
    def execute(self, commands: List[CommandProtocol]) -> T:
        # delete any registered commands after the current cursor
        # del self.command_stack[self.cursor + 1:]
        self.command_store.remove_commands(self.cursor + 1)

        # delete any cached states after the current cursor
        # for ii, cache in [(ii, x) for ii, x in enumerate(self._cached_states) if x[1] > self.cursor]:
            # del self._cached_states[ii]
        for ii, cache in self.command_store.get_cached().items():
            if ii > self.cursor:
                self.command_store.remove_cached_at_cursor(ii)


        # add new commands
        for command in commands:
            # self.command_stack.append(command)
            self.cursor += 1
            self.command_store.add_command(command, self.cursor)


        logger.info(f"Executing commands {pprint.pformat(commands)} [idx: {self.cursor}]")

        # resolve
        latest_state = self.resolve()

        # determine to cache
        # if self.cursor - self._cached_states[-1][1] > self.cache_interval:
        #     self._cache_state(latest_state)

        if self.cursor - max(x for x in self.command_store.get_cached().keys()) > self.cache_interval:
            self.command_store.add_cached(self.init_state, self.cursor)

        return latest_state

    def resolve(self, idx: int = None) -> T:
        command = None

        if idx is None:
            idx = self.cursor

        if idx == 0:
            return self.init_state

        try:
            # Get latest cached
            # last_cached_state, cached_idx = next(iter(reversed([(x, cached_idx) for x, cached_idx in self._cached_states if cached_idx < idx])))

            last_cached_state, last_cached_idx  = self.command_store.last_cached(max_idx=idx)

            last_cached_state = copy.deepcopy(last_cached_state)

            # execute the commands in the stack up to the cursor
            # for command in self.command_stack[cached_idx:idx]:
            #     last_cached_state = command.execute(last_cached_state)
            #     if last_cached_state is None:
            #         raise Exception("The command.execute() operation returned a None value")

            for command in self.command_store.get_commands(last_cached_idx, idx):
                last_cached_state = command.execute(last_cached_state)
                if last_cached_state is None:
                    raise Exception("The command.execute() operation returned a None value")


            logger.info(pprint.pformat(last_cached_state))
            return last_cached_state
        except Exception as e:
            # raise the exception on the command that failed
            raise ResolveStateException(command=command, inner=e)

    @_needsLock
    def undo(self) -> T:
        # move cursor back in time
        if self.cursor > 0:
            self.cursor -= 1

        logger.info(f"Undo - [idx: {self.cursor}]")

        state = self.resolve()
        logger.info(pprint.pformat(state))
        return state


    @_needsLock
    def redo(self) -> T:
        # move cursor forward in time
        # if self.cursor < len(self.command_stack):
        #     self.cursor += 1
        if self.cursor < len(self.command_store.get_commands()):
            self.cursor += 1

        logger.info(f"Redo - [idx: {self.cursor}]")

        state = self.resolve()
        logger.info(pprint.pformat(state))
        return state


    @property
    def CachedStates(self) -> List[Tuple[T, int]]:
        # return self._cached_states
        return [(k, v) for k, v in self.command_store.get_cached().items()]

    @property
    def ActiveCommands(self):
        # return self.command_stack[:self.cursor + 1]
        return self.command_store.get_commands(0, self.cursor)

    @property
    def State(self) -> T:
        return self.resolve()