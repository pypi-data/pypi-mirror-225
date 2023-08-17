from __future__ import annotations
"""
TPDS Qt Based Process Management Utiltities
"""

import enum
from typing import Callable, Sequence, Literal, Tuple, Union, Any, List
from PySide6.QtCore import Slot, QProcess

# TPDS Common Resources
from tpds.helper import LogFacility

class ErrorHandling(enum.IntEnum):
    LOG = 1
    CAPTURE = 2
    DISCARD = 3

__allowed_handling = Literal[ErrorHandling.DISCARD, ErrorHandling.CAPTURE, ErrorHandling.LOG]


class TpdsProcessTimeout(Exception):
    """Timeout occured while executing the process """


class TpdsProcess():
    def __init__(self, parent: Union[Any, None] = None, err_handling: __allowed_handling = ErrorHandling.DISCARD,
                stdout_callback: Callable[[Any], None] = None, stderr_callback: Callable[[Any], None] = None,
                started_callback: Callable[[Any], None] = None) -> None:
        self._process = QProcess(parent)
        self._stdout = stdout_callback
        self._stderr = stderr_callback
        self._started = started_callback
        self._stderr_handling = err_handling
        self._stdout_buffer = ''
        self._stderr_buffer = ''
        self.returncode = 0
        self.pid = 0

        if err_handling == ErrorHandling.CAPTURE:
            self._process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)

        self._process.readyReadStandardOutput.connect(self.__stdout_signal)

        # QProcess emits `readyReadStandardError` when there is data
        # to be read from stderr
        self._process.readyReadStandardError.connect(self.__stderr_signal)

        # QProcess emits `started` when process starts
        self._process.started.connect(self.__started_signal)

        # QProcess emits `finished` when process ends
        self._process.finished.connect(self.__finished_signal)

        # QProcess emits `errors` when process encounters errors
        self._process.errorOccurred.connect(self.__error_signal)

        # QProcess emits state whenever it changes
        self._process.stateChanged.connect(self.__state_signal)

    def start(self, *args, **kwargs):
        self._process.start(*args, **kwargs)
        self.pid = self._process.processId()

    def wait(self, timeout: Union[int, None] = None) -> Tuple[str, str]:
        """
        Wait for the process to complete - will timeout if the timeout value is not None
        """
        result = self._process.waitForFinished(msecs=timeout * 1000 if timeout else -1)
        error_data = self._stderr_buffer + str(self._process.readAllStandardError(), encoding='utf-8')
        self.returncode = int(self._process.exitCode())

        if result:
            out_data = self._stdout_buffer + str(self._process.readAllStandardOutput(), encoding='utf-8')
            return out_data, error_data
        else:
            raise TpdsProcessTimeout()

    def kill(self):
        self._process.kill()

    @Slot()
    def __stdout_signal(self):
        update = str(self._process.readAllStandardOutput(), encoding='utf-8')
        if self._stdout:
            self._stdout(update)
        self._stdout_buffer += update

    @Slot()
    def __stderr_signal(self):
        if self._stderr_handling != ErrorHandling.DISCARD:
            update = str(self._process.readAllStandardError(), encoding='utf-8')
            if self._stderr:
                self._stderr(update)
            self._stderr_buffer += update

    @Slot()
    def __started_signal(self):
        if self._started:
            self._started(self._process)

    @Slot(QProcess.ProcessState)
    def __state_signal(self, state):
        pass

    @Slot(int, QProcess.ExitStatus)
    def __finished_signal(self, exitcode, exitstate):
        pass

    @Slot(QProcess.ProcessError)
    def __error_signal(self, status):
        pass


class TpdsAppProcessing():
    """
    Qt based processing utiltities
    """
    __shared_state: dict[str, Any] = {}
    DISCARD = ErrorHandling.DISCARD
    CAPTURE = ErrorHandling.CAPTURE
    LOG = ErrorHandling.LOG

    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        instance = super().__new__(cls)
        instance.__dict__ = cls.__shared_state
        return instance

    def __init__(self, parent: Any = None) -> None:
        self._processes: List[QProcess] = []
        self._parent = parent
        self._log = LogFacility()
    
    def get_processes(self)-> None:
        return self._processes

    def _get_process(self, pid: int) -> Union[QProcess, None]:
        for proc in self._processes:
            if proc.pid() == pid:
                    return proc
        return None

    def start(self, cmd: Sequence[str], err_handling: __allowed_handling = ErrorHandling.DISCARD, \
                log_args: bool = True, **kwargs: Any) -> QProcess:
        """
        Start an external process
        """
        process = TpdsProcess(self._parent, err_handling=err_handling, **kwargs)

        if log_args:
            self._log.log('Started "{}" with pid {}'.format(' '.join(cmd), process.pid))
        else:
            self._log.log('Started "{}" with pid {}'.format(cmd[0], process.pid))

        # Start process
        process.start(cmd[0], cmd[1:])

        self._processes += [process]
        return process

    def wait(self, process: TpdsProcess, timeout: Union[int, None] = None) -> Tuple[str, int]:
        """
        Wait for the process to complete - will timeout if the timeout value is not None
        """
        try:
            out_data, error_data = process.wait(timeout=timeout)
            self._log.log('Process ({}) ended with code ({})'.format(process.pid, process.returncode))
        except TpdsProcessTimeout as e:
            process.kill()
            out_data = process._stdout_buffer
            error_data = process._stderr_buffer
            self._log.log('Process ({}) Timed out after running for {}'.format(process.pid, timeout))
        finally:
            returncode = process.returncode
            if error_data:
                self._log.log(error_data)
            if process in self._processes:
                self._processes.remove(process)
            return out_data, returncode

    def run_cmd(self, cmd: Sequence[str], timeout: Union[int, None]=None,
                err_handling: __allowed_handling = ErrorHandling.DISCARD,
                **kwargs: Any) -> Tuple[str, int]:
        """
        Generic function to run a command and return the
        """
        process = self.start(cmd, err_handling=err_handling, **kwargs)
        return self.wait(process, timeout)

    def kill(self, process: Union[TpdsProcess, int, None]) -> None:
        """
        Kill a process that was started
        """
        if isinstance(process, int):
            process = self._get_process(process)

        if isinstance(process, TpdsProcess):
            process.kill()

    def terminate_all(self) -> None:
        """
        Terminate all running process
        """
        self._log.log('Terminating {} processes'.format(len(self._processes)))
        # Loop through and kill all processes
        for process in self._processes:
            try:
                self.kill(process)
            except Exception as e:
                # Process is probably already dead
                pass
            finally:
                self._processes.remove(process)


__all__ = ['TpdsAppProcessing', 'ErrorHandling']
