# BSD 3-Clause License
#
# Copyright (c) 2022-Present, nxtlo
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""Abstractions for asynchronous programming."""

from __future__ import annotations

__all__ = ("spawn", "loop")

import asyncio
import typing

if typing.TYPE_CHECKING:
    import collections.abc as collections

    T_co = typing.TypeVar("T_co", covariant=True)
    T = typing.TypeVar("T", bound=collections.Callable[..., typing.Any])


async def spawn(
    *aws: collections.Awaitable[T_co],
    timeout: float | None = None,
    with_exception: bool = True,
) -> collections.Sequence[T_co]:
    """Spawn all given awaitables concurrently.

    Example
    -------
    ```py
    from sain import futures

    async def get(url: str) -> dict[str, Any]:
        return await http.get(url).json()

    async def main() -> None:
        tasks = await futures.spawn(*(get("url.com") for _ in range(10)))
        print(tasks)
    ```

    Parameters
    ----------
    *aws : `collections.Awaitable[T]`
        The awaitables to gather.
    timeout : `float | None`
        An optional timeout.
    with_exceptions : `bool`
        If `True` then exceptions will be returned. Default to `True`.

    Returns
    -------
    `Sequence[T]`
        A sequence of the results of the awaited coros.
    """

    if not aws:
        raise RuntimeError("No awaitables passed.", aws)

    tasks: list[asyncio.Task[T_co]] = []

    for future in aws:
        tasks.append(asyncio.ensure_future(future))  # type: ignore
    try:
        gatherer = asyncio.gather(*tasks, return_exceptions=with_exception)
        return await asyncio.wait_for(gatherer, timeout=timeout)

    except asyncio.CancelledError:
        raise asyncio.CancelledError("Gathered Futures were cancelled.") from None

    finally:
        for task in tasks:
            if not task.done() and not task.cancelled():
                task.cancel()


# source: hikari-py/aio.py
def loop() -> asyncio.AbstractEventLoop:
    """Get the current usable event loop or create a new one.

    Returns
    -------
    `asyncio.AbstractEventLoop`
    """
    try:
        loop = asyncio.get_event_loop_policy().get_event_loop()

        if not loop.is_closed():
            return loop

    except RuntimeError:
        pass

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop
