'''Model the background Event Loop processing.
'''
import typing
import logging
from dataclasses import dataclass
from datetime import datetime
import time

import threading
from queue import Queue, Empty
# TODO: Use SimpleQueue
if typing.TYPE_CHECKING:
    import tkinter as tk

from . import exception

logger = logging.getLogger(__name__)


@dataclass
class ELCallback:
    '''Event Loop Callback definition.

    Args:
        widget: Widget to attach the ``callback`` to
        callback: Function to call with the `response <ELRes>`.
        idle: Choose ``after_idle`` over ``after``. Defaults to `True`.
            See ``Tcl`` :tcl:`after <after.html#M6>` and :tcl:`after idle
            <after.html#M9>` documentation.
        afterMS: If ``idle`` is `False`, delay execution.
            See ``Tcl`` :tcl:`after <after.html#M6>` documentation.
    '''
    widget: 'typing.Union[tk.Widget, tk.Tk]'
    callback: 'typing.Callable[[EventLoop, typing.Optional[int], typing.Union[ELRes, bool]], typing.Any]'
    idle: bool = True
    afterMS: int = 0

    if __debug__:
        def __post_init__(self):
            if not self.idle:
                assert self.afterMS >= 0, f'Invalid afterMS config: {self.afterMS}'

    def trigger(self,
                eventloop: 'EventLoop',
                ridx: typing.Optional[int],
                response: 'typing.Union[ELRes, bool]',
                ) -> str:
        '''Trigger the callback using the given response.

        See `EventLoop` for the kinds of responses produced.

        Args:
            eventloop: The corresponding `EventLoop` object.
            ridx: The response index. See `EventLoop`.
            response: The response payload.

        Returns:
            Return the ``after``/``after idle`` ID.
        '''
        if self.idle:
            return self.widget.after_idle(self.callback, eventloop, ridx, response)
        else:
            return self.widget.after(self.afterMS, self.callback, eventloop, ridx, response)


@dataclass(frozen=True)
class ELReq:
    '''Event Loop Request.

    Usually represents a task to be performed on an `EventLoop`.

    See `EventLoop` to see how to use this.
    '''
    pass


@dataclass(frozen=True)
class ELRes:
    '''Event Loop Response.

    See `EventLoop` to see how to use this.
    '''
    pass


class EventLoop:
    '''Event Loop Object

    Represent all Event Loop settings and necessary references.

    An event loop is basically a big ``while True:`` loop. The tasks to process
    are `ELReq` objects, and that processing produces a stream of responses.

    There are two kinds of responses:

    - A "signal", index is `None`, payload is `bool`.
        This signals the Event Loop started or stopped task processing.
    - A "response", index is `int`, payload is `ELRes`.
        The index indicates the count of the current processing task.

    Internally uses the :py:mod:`threading` functions. This means the threading
    model is cooperative, that is, the task processing functions must yield
    their time, not hog the processing time for themselves.

    The event loop itself is single-threaded, meaning there's only at most a
    single task is being executed.

    You can choose between two different response parsing behaviours, depending
    on the arguments you give:

    - ``qoutput``: Define the response output as a queue, possibly given from outside.
    - ``wcallback``: Define some a ``Tk`` callback function to be called.
        Even though ``Tk`` is not thread-safe, some specific functions are, and
        this is used to "merge" the event process loop with the existing ``Tk``
        event loop. See `ELCallback` for more information on how those
        functions are defined.

    Note that ``qoutput`` is the default, when you do not choose one or the
    other.

    Avoid using `time.sleep` directly when implementing the tasks. Use
    `isleep`/`usleep` for precise control over interruptible behaviour.

    Args:
        qinput: `Queue <queue.Queue>` with `ELReq` to consume
            Optional, created a new queue when not given.
        qoutput: `Queue <queue.Queue>` with `ELRes` to produce
            Optional, created a new queue when not given.
            See above for the interaction with ``wcallback``.
        wcallback: `Callback Configuration <ELCallback>` object.
            Optional.
            See above for the interaction with ``qoutput``.

    .. note::
        This object should be created on the Main Thread, not from any
        sub-thread.

    .. note::
        In case ``qoutput`` is chosen, the main ``Tk`` processing loop for
        `responses <ELRes>` must implement something like this, using an `Interval
        <tkmilan.model.Interval>`:

        .. code:: python

            def setup_defaults(self):
                # Process Events every 500ms
                tkmilan.model.Interval(self, self.onProcessEvents, 500,
                                    immediate=True)

            def onProcessEvents(self):
                el = self.bg_el['sleep']
                for response in el.responses(chunk=10):
                    logger.debug('Response: %r', response)
    '''
    name: typing.Optional[str] = None
    '''Thread Name, for all instances in the class.

    This is the per-class setting, can be overriden. See `tName` for the
    per-instance name.
    '''
    thread: typing.Optional[threading.Thread]
    '''Event Loop Thread Object.

    `None` when the event loop is not alive, points to the Event Loop `Thread
    <threading.Thread>` otherwise.
    See `is_running`.

    Automatically managed by `start`/`stop`.
    '''
    tName: str
    '''Thread Name'''
    cntProcessed: int
    '''Counter for correctly processed `ELReq` tasks.

    This is incremented right after the processing function run successfully.
    It can be safely used from within the `process` function, in the Event Loop
    Thread, but not from other threads (no locking is implemented).
    '''

    def __init__(self, *,
                 qinput: typing.Optional[Queue] = None,
                 qoutput: typing.Optional[Queue] = None, wcallback: typing.Optional[ELCallback] = None,
                 name: typing.Optional[str] = None):
        self.qinput: Queue = qinput or Queue()
        self.qoutput: typing.Optional[Queue]
        self.wcallback: typing.Optional[ELCallback]
        # Default to `qoutput` setup
        if wcallback is None:
            self.qoutput = qoutput or Queue()
            self.wcallback = None
        elif qoutput is None:
            self.qoutput = None
            self.wcallback = wcallback
        else:
            raise ValueError('EventLoop: Choose between `qoutput` and `wcallback`')
        self.lockThread = threading.Lock()
        self.eStopped: threading.Event = threading.Event()
        with self.lockThread:
            self.thread = None
            self.eStopped.set()  # Start stopped
        self.cntProcessed = 0
        self.tName = name or self.name or ''
        if __debug__:
            # TODO: `raise exception.EventLoopError`?
            if threading.current_thread() is not threading.main_thread():
                logger.warning('EL[%s]: Creating the EventLoop from a sub-thread', self.tName)

    def is_running(self) -> bool:
        '''Check if the Event Loop is running.

        This means the thread is ready to process tasks.

        Once the thread is `stopped <stop>`, it stops running, but the thread
        itself might remain `alive <threading.Thread.is_alive>` for a while for
        cleanup.
        '''
        with self.lockThread:
            return self.thread is not None

    def is_paused(self) -> bool:
        '''Check if the event loop is paused.

        This means a dead event loop that has some requests to be processed.

        This means the corresponding thread was alive at some point, but no
        longer. It can be `restarted <start>` once again, to keep processing
        the remaining events.

        See Also:
            The `is_running` should be used on most situations.
        '''
        with self.lockThread:
            return self.thread is None and not self.qinput.empty()

    def start(self, *, daemon: bool = True) -> threading.Thread:
        '''Start executing the Event Loop, in a background thread.

        There will be a single thread processing event at a time. If you try to
        "start" a running Event Loop, this raises an `exception
        <exception.EventLoopConcurrencyError>`.

        Args:
            daemon: Set the `daemon <threading.Thread.daemon>` option for
                thread creation. Defaults to `True`.

        .. note::
            This should be called from the Main Thread, not from any
            sub-thread.
            It can be called from any thread, but that is usually a logic
            error.
        '''
        if self.is_running():
            raise exception.EventLoopConcurrencyError(f'EL[{self.tName}]: Starting a running EventLoop')
        if __debug__:
            if threading.current_thread() is not threading.main_thread():
                logger.warning('EL[%s]: Starting the EventLoop from a sub-thread', self.tName)
        ctime = datetime.now().isoformat()
        with self.lockThread:
            thread = threading.Thread(name=f'{self.tName}@{ctime}', daemon=daemon,
                                      target=self.run)
            thread.start()
        return thread

    def stop(self, *, join: bool = False):
        '''Stop execution the Event Loop, ASAP.

        If you try to "stop" a non-running Event Loop, this raises an
        `exception <exception.EventLoopConcurrencyError>`.

        Since the threading model is cooperative, the currently executing task
        (if any) is not interrupted.
        The only exception is the `isleep` process, that is interrupted.

        Args:
            join: Wait for the thread to finish.
                Defaults to `False`, fully asynchronous behaviour.

        .. note::
            This should be called from the Main Thread, not from any
            sub-thread.
            It can be called from any thread, including the `Event Loop Thread
            <thread>`, but that is usually a logic error.
        '''
        if not self.is_running():
            raise exception.EventLoopConcurrencyError(f'EL[{self.tName}]: Stopping a non-running EventLoop')
        if __debug__:
            if self.thread is threading.current_thread():
                logger.warning('EL[%s]: Stopping the EventLoop from itself', self.tName)
            if self.eStopped.is_set():
                logger.warning('EL[%s]: Stopping a stopped EventLoop', self.tName)
        with self.lockThread:
            thread = self.thread   # Save a reference to the thread, in case is disappears
        self.eStopped.set()    # Mark as stopped
        if self.qinput.empty():
            self.qinput.put(None)  # Make sure to unwedge the queue processing code
        if thread is not None and join:
            thread.join()

    def toggle(self) -> typing.Optional[threading.Thread]:
        '''Toggle Event Loop execution.

        If `is_running`, `stop` it, otherwise `start` it. Useful to have a
        single button for controlling the Event Loop execution state.

        Returns:
            Returns `None` if the Event Loop was stopped, or the next Event
            Loop Thread Object otherwise.
        '''
        if self.is_running():
            self.stop()
            return None
        else:
            return self.start()

    def isleep(self, duration: float) -> bool:
        '''Suspend the thread execution for a while, interruptible.

        This suspension can be interrupted by calling `stop`.

        .. note::
            This is called from the `Event Loop Thread <thread>`, when
            implementing the processing functions. See `process`.

            Do not use this in other contexts.

        See Also:
            For a non-interuptible thread suspension, see `usleep`.
        '''
        assert self.thread is threading.current_thread()
        return self.eStopped.wait(timeout=duration) is not True

    def usleep(self, duration: float) -> bool:
        '''Suspend the thread execution for a while, interruptible.

        This suspension cannot be interrupted; when calling `stop`, the event
        loop will only stop after this suspension ends.

        .. note::
            This is called from the `Event Loop Thread <thread>`, when
            implementing the processing functions. See `process`.

            Do not use this in other contexts.

        See Also:
            For an interuptible thread suspension, see `isleep`.
        '''
        assert self.thread is threading.current_thread()
        time.sleep(duration)
        return True

    def run(self):
        '''Run the EventLoop.

        This is the target function for the `thread object <EventLoop.thread>`.

        Do not use this directly, see `start`.
        '''
        assert not self.is_running()
        # Starting
        # - Manipulate, then signal
        if __debug__:
            logger.debug('> SET THREAD')
        with self.lockThread:
            self.thread = threading.current_thread()
            assert self.thread.daemon, '{self.tName}: Unsupported `daemon=False`'
            self.eStopped.clear()
        if __debug__:
            logger.debug('> > HAS THREAD: %r', self.thread)
        self.signal(True)  # Started
        if __debug__:
            logger.debug('> START')
        # Loop through events
        # # If `daemon` is False, `qinput.get` MUST have a timeout, or it will
        # # deadlock once the parent process exits. Other possiblity is
        # # processing signals.
        # Loop while not stopped, and there are tasks to process
        while self.eStopped.is_set() is False:
            if __debug__:
                logger.debug('> > GET TASK')
            task = self.qinput.get()
            if __debug__:
                logger.debug('> > HAS TASK')
            if task is None:
                pass  # Re-Check for stopped state
            else:
                try:
                    assert isinstance(task, ELReq)
                    if __debug__:
                        logger.debug('> > START TASK')
                    self.process(task)
                    if __debug__:
                        logger.debug('> >   END TASK')
                    self.cntProcessed += 1
                except Exception as e:
                    # Stop processing
                    logger.critical('Processing Error: %r', e)
                    # TODO: Mark EventLoop as broken?
                    break
        # Stopping
        # - Signal then manipulate
        if __debug__:
            logger.debug('> STOP')
        self.signal(False)  # Stopped
        if __debug__:
            logger.debug('> > RM THREAD: %r', self.thread)
        with self.lockThread:
            self.thread = None
        if __debug__:
            logger.debug('> END')

    def process(self, task: ELReq):
        '''Process a single task.

        Defaults to doing nothing, subclasses should redefine this.
        See `singledispatchmethod <functools.singledispatchmethod>` for a
        possible solution for polymorphism based on `ELReq` subclasses.

        The `cntProcessed` counter is unique for each task during this call,
        and it is attached to the responses queued during this call. This means
        it can be used to match request and respond, even though everything
        happens asynchronously.

        Do not use this directly, see `queue`.

        .. note::

            This is called from the `Event Loop Thread <thread>`,
            automatically.
        '''
        if __debug__:
            raise NotImplementedError
        pass

    def queue(self, task: ELReq):
        '''Queue a new task on the event loop.

        Append a new `task <ELReq>` to the Event Loop.

        It is possible to queue tasks into a dead event loop. This will be
        processed once the event loop restarts.

        .. note::
            This should be called from the Main Thread, not from any
            sub-thread.
            It can be called from any thread, including the `Event Loop Thread
            <thread>`, but that is usually a logic error.
        '''
        assert task is not None
        self.qinput.put(task)

    def signal(self, signal: bool):
        '''Signal a new internal event on the output.

        Should append a `bool` signal on the output queue, or equivalent.

        .. note::
            This is called from the `Event Loop Thread <thread>`, when
            implementing the processing functions. See `process`.

            Do not use this in other contexts.
        '''
        assert self.thread is threading.current_thread()
        if self.qoutput is None:
            assert self.wcallback is not None
            self.wcallback.trigger(self, None, signal)
        else:
            self.qoutput.put((None, signal))

    def respond(self, response: ELRes):
        '''Add a new response on the output.

        Append a new `response <ELRes>` on the Event Loop output queue, or
        equivalent.

        .. note::
            This is called from the `Event Loop Thread <thread>`, when
            implementing the processing functions. See `process`.

            Do not use this in other contexts.
        '''
        assert self.thread is threading.current_thread()
        if self.qoutput is None:
            assert self.wcallback is not None
            self.wcallback.trigger(self, self.cntProcessed, response)
        else:
            self.qoutput.put((self.cntProcessed, response))

    def responses(self, chunk: int = 10) -> typing.Iterable[typing.Tuple[typing.Optional[int], typing.Union[bool, ELRes]]]:
        '''Retrieve responses from the event loop.

        Args:
            chunk: Retrive at most this amount of responses.

        Returns:
            This is a generator that produces data tuples. See `EventLoop` for
            the kinds of responses produced here, the format is a tuple
            ``(index, payload)``.

        .. note::
            This should be called from the Main Thread, not from any
            sub-thread.
            It can be called from any thread, including the `Event Loop Thread
            <thread>`, but that is usually a logic error.
        '''
        if self.qoutput is None:
            raise exception.EventLoopError('Reading responses when no output queue is defined')
        if threading.current_thread() is not threading.main_thread():
            logger.warning('EL[%s]: Reading responses from a sub-thread', self.tName)
        for eidx in range(chunk):
            try:
                ridx, response = self.qoutput.get(block=False)
                if __debug__:
                    if ridx is None:  # Signal
                        assert ridx is None
                        assert isinstance(response, bool)
                    else:             # Response
                        assert isinstance(ridx, int)
                        assert isinstance(response, ELRes), f'Weird Response: {response}'
                yield ridx, response
            except Empty:
                break  # Nothing to do

    def cntRequests(self) -> int:
        '''Return the approximate size of the request queue.

        This indicates unprocessed tasks.
        See the upstream function `qsize <queue.Queue.qsize>`.

        .. note::
            This should be called from the Main Thread, not from any
            sub-thread.
            It can be called from any thread, including the `Event Loop Thread
            <thread>`, but that is usually a logic error.
        '''
        return self.qinput.qsize()

    def cntResponses(self) -> typing.Optional[int]:
        '''Return the approximate size of the response queue, if exists.

        This indicates unprocessed responses.
        See the upstream function `qsize <queue.Queue.qsize>`.

        Returns:
            Returns `None` if there is no output queue (connected to a ``Tk``
            event loop directly).

        .. note::
            This should be called from the Main Thread, not from any
            sub-thread.
            It can be called from any thread, including the `Event Loop Thread
            <thread>`, but that is usually a logic error.
        '''
        if self.qoutput is None:
            return None
        else:
            return self.qoutput.qsize()
