# Copyright 2023 OpenC3, Inc.
# All Rights Reserved.
#
# This program is free software; you can modify and/or redistribute it
# under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation; version 3 with
# attribution addendums as found in the LICENSE.txt
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# This file may also be used under the terms of a commercial license
# if purchased from OpenC3, Inc.

import os
import sys
import threading
import time
import traceback
from openc3.utilities.logger import Logger


class HazardousError(Exception):
    def __init__(self):
        self.target_name = ""
        self.cmd_name = ""
        self.cmd_params = ""
        self.hazardous_description = ""
        self.formatted = ""
        super().__init__()

    def __str__(self):
        string = (
            f"{self.target_name} {self.cmd_name} with {self.cmd_params} is Hazardous"
        )
        if self.hazardous_description:
            string += f"due to '{self.hazardous_description}'"
        # Pass along the original formatted command so it can be resent
        string += f".\n{self.formatted}"
        return string


# Adds a path to the global Ruby search path
#
# @param path [String] Directory path
def add_to_search_path(path, front=True):
    path = os.path.abspath(path)
    if path not in sys.path:
        if front:
            sys.path.insert(0, path)
        else:  # Back
            sys.path.append(path)


# Attempt to gracefully kill a thread
# @param owner Object that owns the thread and may have a graceful_kill method
# @param thread The thread to gracefully kill
# @param graceful_timeout Timeout in seconds to wait for it to die gracefully
# @param timeout_interval How often to poll for aliveness
# @param hard_timeout Timeout in seconds to wait for it to die ungracefully
def kill_thread(
    owner, thread, graceful_timeout=1, timeout_interval=0.01, hard_timeout=1
):
    if thread:
        if owner and hasattr(owner, "graceful_kill"):
            if threading.current_thread() != thread:
                owner.graceful_kill()
                end_time = time.time() + graceful_timeout
                while thread.is_alive() and ((end_time - time.time()) > 0):
                    time.sleep(timeout_interval)
            else:
                Logger.warn("Threads cannot graceful_kill themselves")
        elif owner:
            Logger.info(
                f"Thread owner {owner.__class__.__name__} does not support graceful_kill"
            )
        if thread.is_alive():
            # If the thread dies after alive? but before backtrace, bt will be nil.
            trace = []
            for filename, lineno, name, line in traceback.extract_stack(
                sys._current_frames()[thread.ident]
            ):
                trace.append(f"{filename}:{lineno}:{name}:{line}")
            caller_trace = []
            for filename, lineno, name, line in traceback.extract_stack(
                sys._current_frames()[threading.current_thread().ident]
            ):
                caller_trace.append(f"{filename}:{lineno}:{name}:{line}")

            # Graceful failed
            caller_trace_string = "\n  ".join(caller_trace)
            trace_string = "\n  ".join(trace)
            msg = "Failed to gracefully kill thread:\n"
            msg = msg + f"  Caller Backtrace:\n  {caller_trace_string}\n"
            msg = msg + f"  \n  Thread Backtrace:\n  {trace_string}\n\n"
            Logger.warn(msg)
