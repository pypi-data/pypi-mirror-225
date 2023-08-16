from typing_extensions import Annotated, TypeAlias
from typing import Any, Dict, List, Type, Union, TypeVar, Callable, Optional, overload

from nonebot.typing import T_State
from tarina import run_always_await
from nonebot.internal.adapter import Bot, Message
from arclet.alconna import Empty, Arparma, Duplication
from nonebot.internal.params import Depends as Depends
from arclet.alconna.builtin import generate_duplication
from nonebot.internal.matcher import Matcher as Matcher

from .adapters import Segment
from .model import T, Match, Query, CommandResult
from .consts import (
    SEGMATCH_MSG,
    ALCONNA_RESULT,
    ALCONNA_ARG_KEY,
    SEGMATCH_RESULT,
    ALCONNA_EXEC_RESULT,
)

T_Duplication = TypeVar("T_Duplication", bound=Duplication)
TS = TypeVar("TS", bound=Union[Segment, str])
MIDDLEWARE: TypeAlias = Callable[[Bot, T_State, Any], Any]


def _alconna_result(state: T_State) -> CommandResult:
    return state[ALCONNA_RESULT]


def AlconnaResult() -> CommandResult:
    return Depends(_alconna_result, use_cache=False)


def _alconna_exec_result(state: T_State) -> Dict[str, Any]:
    return state[ALCONNA_EXEC_RESULT]


def AlconnaExecResult() -> Dict[str, Any]:
    return Depends(_alconna_exec_result, use_cache=False)


def _alconna_matches(state: T_State) -> Arparma:
    return _alconna_result(state).result


def AlconnaMatches() -> Arparma:
    return Depends(_alconna_matches, use_cache=False)


def AlconnaMatch(name: str, middleware: Optional[MIDDLEWARE] = None) -> Match:
    async def _alconna_match(state: T_State, bot: Bot) -> Match:
        arp = _alconna_result(state).result
        mat = Match(arp.all_matched_args.get(name, Empty), name in arp.all_matched_args)
        if middleware and mat.available:
            mat.result = await run_always_await(middleware, bot, state, mat.result)
        return mat

    return Depends(_alconna_match, use_cache=False)


def AlconnaQuery(
    path: str,
    default: Union[T, Empty] = Empty,
    middleware: Optional[MIDDLEWARE] = None,
) -> Query[T]:
    async def _alconna_query(state: T_State, bot: Bot) -> Query:
        arp = _alconna_result(state).result
        q = Query(path, default)
        result = arp.query(path, Empty)
        q.available = result != Empty
        if q.available:
            q.result = result
        elif default != Empty:
            q.available = True
        if middleware and q.available:
            q.result = await run_always_await(middleware, bot, state, q.result)
        return q

    return Depends(_alconna_query, use_cache=False)


@overload
def AlconnaDuplication() -> Duplication:
    ...


@overload
def AlconnaDuplication(__t: Type[T_Duplication]) -> T_Duplication:
    ...


def AlconnaDuplication(__t: Optional[Type[T_Duplication]] = None) -> Duplication:
    def _alconna_match(state: T_State) -> Duplication:
        res = _alconna_result(state)
        gt = __t or generate_duplication(res.source)
        return gt(res.result)

    return Depends(_alconna_match, use_cache=False)


def AlconnaArg(path: str) -> Any:
    def _alconna_arg(state: T_State) -> Any:
        return state[ALCONNA_ARG_KEY.format(key=path)]

    return Depends(_alconna_arg, use_cache=False)


# def AlconnaArg(path: str, middleware: Optional[MIDDLEWARE] = None) -> Any:
#     async def _alconna_arg(state: T_State, bot: Bot) -> Any:
#         arg = state[ALCONNA_ARG_KEY.format(key=path)]
#         if middleware:
#             return await run_always_await(middleware, bot, state, arg)
#         return arg
#
#     return Depends(_alconna_arg, use_cache=False)


def _seg_match_msg(state: T_State) -> Message:
    return state[SEGMATCH_MSG]


def SegMatchMessage() -> Message:
    return Depends(_seg_match_msg, use_cache=False)


@overload
def SegMatchResult() -> List[Segment]:
    ...


@overload
def SegMatchResult(target: Type[TS], index: int = 0) -> TS:
    ...


def SegMatchResult(
    target: Optional[Type[TS]] = None, index: int = 0
) -> Union[List[Segment], TS]:
    def _seg_match_result(state: T_State):
        result = state[SEGMATCH_RESULT]
        return result[index] if target else result

    return Depends(_seg_match_result, use_cache=False)


AlcResult = Annotated[CommandResult, AlconnaResult()]
AlcExecResult = Annotated[Dict[str, Any], AlconnaExecResult()]
AlcMatches = Annotated[Arparma, AlconnaMatches()]
SegMsg = Annotated[Message, SegMatchMessage()]


def match_path(path: str):
    """
    当 Arpamar 解析成功后, 依据 path 是否存在以继续执行事件处理

    当 path 为 ‘$main’ 时表示认定当且仅当主命令匹配
    """

    def wrapper(result: Arparma):
        if path == "$main":
            return not result.components
        else:
            return result.query(path, "\0") != "\0"

    return wrapper


def match_value(path: str, value: Any, or_not: bool = False):
    """
    当 Arpamar 解析成功后, 依据查询 path 得到的结果是否符合传入的值以继续执行事件处理

    当 or_not 为真时允许查询 path 失败时继续执行事件处理
    """

    def wrapper(result: Arparma):
        if result.query(path, "\0") == value:
            return True
        return or_not and result.query(path, "\0") == "\0"

    return wrapper


_seminal = type("_seminal", (object,), {})


def assign(
    path: str, value: Any = _seminal, or_not: bool = False
) -> Callable[[Arparma], bool]:
    if value != _seminal:
        return match_value(path, value, or_not)
    if or_not:
        return lambda x: match_path("$main") or match_path(path)  # type: ignore
    return match_path(path)


def Check(fn: Callable[[Arparma], bool]) -> bool:
    def _arparma_check(state: T_State, matcher: Matcher) -> bool:
        arp = _alconna_result(state).result
        if not (ans := fn(arp)):
            matcher.skip()
        return ans

    return Depends(_arparma_check, use_cache=False)
