# progress.py

import sys
import datetime as dt
import time
import warnings
from time import strftime
from time import gmtime

import threading
from typing import (
    Optional, Type, Generator, Iterable,
    Union, Any, Callable, Literal
)

from represent import represent, Modifiers

__all__ = [
    "Spinner",
    "spinner",
    "format_seconds"
]

def format_seconds(
        seconds: float,
        length: Optional[int] = None,
        side: Optional[Literal['left', 'right', 'center']] = None) -> str:
    """
    Formats the time in seconds.

    :param seconds: The seconds.
    :param length: The length of the string.
    :param side: The side to set the message in the padding.

    :return: The time message.
    """

    message = strftime("%H:%M:%S", gmtime(seconds))

    if side is None:
        return message
    # end if

    if length is None:
        length = len(message)

    else:
        length = max(length, len(message))
    # end if

    length -= len(message)

    if side.lower() == "right":
        message = f"{0: <{length}}{message}"

    elif side.lower() == "left":
        message = f"{message}{0: <{length}}"

    elif side.lower() == "center":
        message = f"{0: <{length / 2}}{message}{0: <{length / 2 + length % 2}}"

    else:
        raise ValueError(
            f"side must be one of 'left', 'right', "
            f"or 'center', not: {side}."
        )
    # end if

    return message
# end format_seconds

@represent
class Spinner:
    """
    A class to create a terminal spinning wheel.

    Using this object it is able to create a context manager for
    continuously print a progress wheel, and a message.

    attributes:

    - delay:
        The delay between output updates of iterations.

    - message:
        The printed message with the progress wheel.

    - silence:
        The value to silence the output.

    >>> with Spinner(message="Processing")
    >>>     while True:
    >>>         pass
    >>>     # end while
    >>> # end Spinner
    """

    modifiers = Modifiers(excluded=["spinner_generator"])

    RUNNING = False

    DELAY = 0.25

    instances = []

    ELEMENTS = '/-\\|'

    def __init__(
            self,
            title: Optional[str] = None,
            message: Optional[str] = None,
            delay: Optional[Union[int, float, dt.timedelta]] = None,
            silence: Optional[bool] = None,
            stay: Optional[Callable[[], bool]] = None,
            counter: Optional[bool] = False,
            clean: Optional[bool] = True,
            elements: Optional[Iterable[str]] = None,
            complete: Optional[Union[bool, str]] = None
    ) -> None:
        """
        Defines the class attributes.

        :param title: The title of the process.
        :param message: The message to display.
        :param delay: The delay value.
        :param silence: The value to hide the progress bar.
        :param stay: A function to keep or break the loop.
        :param counter: The value to add a counter of seconds to the message.
        :param clean: The value to clean the message after exiting.
        :param elements: The elements to show.
        :param complete: The value for a complete message.
        """

        if complete is True:
            complete = "Complete"
        # end if

        if elements is None:
            elements = self.ELEMENTS
        # end if

        self.message = message
        self.complete = complete
        self.silence = silence
        self.stay = stay
        self.counter = counter
        self.clean = clean
        self.elements = elements

        self.title = title or ""
        self.delay = delay or self.DELAY
        self.cursor = elements[0]

        self._paused = False

        self._spinner_generator = self._spinning_cursor()

        self._running = False

        self.start: Optional[float] = None
        self.time: Optional[float] = None
        self.output: Optional[str] = None
    # end __init__

    def __enter__(self) -> Any:
        """
        Enters the object to run the task.

        :return: The object.
        """

        self.spin()

        return self
    # end __enter__

    def __exit__(
            self,
            exception_type: Type[Exception],
            exception: Exception,
            traceback
    ) -> Optional[bool]:
        """
        Exists the spinner object and ends the task.

        :param exception_type: The exception type.
        :param exception: The exception value.
        :param traceback: The traceback of the exception.

        :return: The status value
        """

        self.stop()

        if exception is not None:
            raise exception
        # end if

        return True
    # end __exit__

    @property
    def paused(self) -> bool:
        """Returns the value of the property."""

        return self._paused
    # end paused

    @property
    def running(self) -> bool:
        """Returns the value of the property."""

        return self._running
    # end running

    def pause(self) -> None:
        """Pauses the process."""

        if self.paused:
            warnings.warn(
                f"Attempting to pause {self} "
                f"when the process is paused."
            )
        # end if

        self._paused = True

        if self.silence:
            next_output = ''

        else:
            next_output = self.create_message(text="Paused")
        # end if

        if self.output and next_output:
            sys.stdout.write(
                (
                    (
                        ('\b' * len(self.output)) +
                        (' ' * len(self.output)) +
                        ('\b' * len(self.output))
                    ) if self.output else ''
                ) +
                ((next_output + "\n") if next_output else '')
            )
            sys.stdout.flush()
        # end if
    # end pause

    def unpause(self) -> None:
        """Unpauses the process."""

        if not self.paused:
            warnings.warn(
                f"Attempting to unpause {self} "
                f"when the process is running."
            )
        # end if

        self._paused = False
    # end unpause

    def stop(self) -> None:
        """Stops the spinning process."""

        self._running = False

        Spinner.instances.remove(self)

        Spinner.RUNNING = bool(Spinner.instances)

        if Spinner.instances and Spinner.instances[-1].running:
            Spinner.instances[-1].unpause()
        # end if

        if self.delay:
            time.sleep(self.delay)
        # end if

        self.output = self.output or ''

        if self.output and (self.clean or self.complete):
            sys.stdout.write(
                ('\b' * len(self.output)) +
                (' ' * len(self.output)) +
                ('\b' * len(self.output))
            )
            sys.stdout.flush()
        # end if

        if self.complete:
            if self.silence:
                self.output = ''

            else:
                self.output = self.create_message(
                    cursor="", text=self.complete
                )
            # end if

            if self.output:
                sys.stdout.write(self.output + "\n")
                sys.stdout.flush()
            # end if
        # end if
    # ene stop

    def spin(self) -> None:
        """Runs the spinner."""

        if Spinner.instances and Spinner.instances[-1].running:
            Spinner.instances[-1].pause()
        # end if

        self._running = True

        Spinner.RUNNING = True

        self.start = time.time()
        self.time = time.time()

        threading.Thread(target=self._run).start()

        Spinner.instances.append(self)
    # end spin

    def create_message(
            self,
            cursor: Optional[str] = None,
            text: Optional[str] = None
    ) -> str:
        """
        Creates the message to display.

        :param cursor: The current spinner cursor.
        :param text: The text message.

        :return: The total output message.
        """

        text = text or ""
        cursor = cursor or ""

        message = self.title

        if not message:
            message = ""

        else:
            message += ": "
        # end if

        message += text

        if not message:
            message = ""

        else:
            message += " "
        # end if

        if self.counter:
            current = self.time - self.start

            message += format_seconds(current)
        # end if

        if not cursor:
            return message + " "
        # end if

        return message + " " + cursor + " "
    # end create_message

    def _spinning_cursor(self) -> Generator[str, None, None]:
        """
        Returns the current spinner value.

        :return: The current state of the cursor.
        """

        while True:
            for cursor in self.elements:
                self.time = time.time()

                self.cursor = cursor

                if self.silence:
                    yield ""
                # end if

                self.output = self.create_message(
                    cursor=cursor, text=self.message
                )

                yield self.output
            # end for
        # end while
    # end _spinning_cursor

    def step(self) -> None:
        """Runs the spinning wheel."""

        delay = self.delay

        if isinstance(delay, dt.timedelta):
            delay = delay.total_seconds()
        # end if

        next_output = ""

        if not self.paused:
            next_output = next(self._spinner_generator)

            if not self.silence:
                sys.stdout.write(next_output)
                sys.stdout.flush()
            # end if
        # end if

        if delay:
            time.sleep(delay)
        # end if

        if not (self.paused or self.silence):
            sys.stdout.write('\b' * len(next_output))
            sys.stdout.flush()
        # end if
    # end step

    def _run(self) -> None:
        """Runs the spinning wheel."""

        if not self.silence:
            sys.stdout.write(
                ('\b' * 200)
            )
            sys.stdout.flush()
        # end if

        while (
            self._running and
            (
                (self.stay is None) or
                (callable(self.stay) and self.stay())
            )
        ):
            self.step()
        # end while
    # end _run
# end Spinner

spinner = Spinner