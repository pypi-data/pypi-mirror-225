from typing import Optional, Tuple, Union, List
from datetime import datetime
import logging
import time
import os

try:
    import slack
    from slack.errors import SlackApiError
except ImportError:
    _has_slack = False
else:
    _has_slack = True

from commands.command import Command
from command_sequence import CommandSequence
from commands.utility_commands import DelayPauseCommand


format = '[%(asctime)s] [%(levelname)-5s]: %(message)s'
log_formatter = logging.Formatter(format)
logging.basicConfig(level=logging.INFO, format=format)


class CommandInvoker:
    """Handles the execution and logging of a command sequence"""
    log_directory = ""

    def __init__(
            self, 
            command_seq: CommandSequence,
            log_to_file: bool = True, 
            log_filename: Optional[str] = None,
            alert_slack: bool = False) -> None:

        if not _has_slack and alert_slack:
            raise ImportError("slackclient module is required to alert slack.")
            
        self._command_seq = command_seq
        self._log_to_file = log_to_file
        self._alert_slack = alert_slack
        self._log_filename = log_filename
        self.log = logging.getLogger(__name__)

        if self._log_to_file:
            if self._log_filename is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                self._log_filename = "logs/" +timestamp

            if not self._log_filename[-4:] == '.log':
                self._log_filename += '.log'
            
            # self._log_filename = self.log_directory + self._log_filename
            
            self._file_handler = logging.FileHandler(self._log_filename)
            self._file_handler.setFormatter(log_formatter)
            if not len(self.log.handlers):
                self.log.addHandler(self._file_handler)

        if self._alert_slack:
            self._slack_token = os.environ.get('SLACK_BOT_TOKEN')
            self._slack_client = slack.WebClient(token=self._slack_token)

    def invoke_commands(self) -> bool:
        """Iterate through the command sequence and execute each command.

        Returns
        -------
        bool
            Whether all the commands executed successfully or not
        """
        # go through each device and make sure uninitialized?
        if self._log_to_file:
            print("")
            print("Log messages will be saved to: " + str(self._log_filename))
            print("")
        else:
            print("")
            print("Log messages will not be saved")
            print("")

        has_error = False

        self.log.info("")
        self.log_command_names(unloop=False)
        self.log.info("="*20 + "BEGINNING OF COMMAND SEQUENCE EXECUTION" + "="*20)

        command_generator = self._command_seq.yield_next_command()

        for command in command_generator:
            # Check the command is a Command otherwise the generator yielded a (False, error message)
            if not isinstance(command, Command):
                error_message = command[1]
                self.log.error("Command sequence error: " + error_message)
                if self._alert_slack:
                    self.log.info("Sending command details to slack.")
                    self.alert_slack_message("Command sequence error: " + error_message)
                    self.upload_log_slack()
                has_error = True
                break

            # Process the command's start delay
            delay = command._params['delay']
            if isinstance(delay, float) or isinstance(delay, int):
                if delay > 0.0:
                    self.log.info("DELAY   -> " + str(delay))
                    time.sleep(delay)
            elif delay == "PAUSE" or delay == "P":
                self.log.info("PAUSE   -> Waiting for user to press enter")
                print('')
                print("Press ENTER to continue, type 'quit' to terminate execution immediately:")
                userinput = input()
                if userinput == "quit":
                    self.log.info("PAUSE   -> User terminated execution early by entering 'quit'")
                    has_error = True # Not really an error but returning False since an early termination (even if intentional) may disrupt a higher workflow
                    break
                else:
                    self.log.info("PAUSE   -> User continued command execution")

            # If it is a delay or pause command skip to next loop to suppress its COMMAND ->, RESULT -> logging
            if isinstance(command, DelayPauseCommand):
                continue

            # Execute the command
            self.log.info("COMMAND -> " + command.name)
            command.execute()

            # Check result
            if command.result.was_successful:
                self.log.info("RESULT  -> " + str(command.result.was_successful) + ", " + command.result.message)
            else:
                self.log.error("RESULT  -> " + str(command.result.was_successful) + ", " + command.result.message)
                self.log.error("Received False result. Terminating command execution early!")
                if self._alert_slack:
                    self.log.info("Sending command details to slack.")
                    self.alert_slack_command(command)
                    self.upload_log_slack()
                has_error = True
                break
            # Go to next command
        # Finished command list execution
        self.log.info("="*20 + "END OF COMMAND SEQUENCE EXECUTION" + "="*20)
        self.log.info("")
        if self._log_to_file:
            print("")
            print("Log messages saved to: " + str(self._log_filename))
            print("")
        else:
            print("")
            print("Log messages were not saved")
            print("")

        if has_error:
            return False
        else:
            return True

    def alert_slack_command(self, command: Command):
        """Attempt to send an error message regarding a command's failure to a designated slack channel.

        Parameters
        ----------
        command : Command
            The command that failed its execution.
        """
        try:
            response = self._slack_client.chat_postMessage(
                channel="printer-bot-test",
                text=("Error in the following command execution:\n" 
                    "COMMAND -> " + command.name + "\n" 
                    "RESULT  -> " + str(command.result.was_successful) + ", " + command.result.message + "\n" 
                    "See log file \"" + str(self._log_filename) + "\" for more details.")
                    )  
        except SlackApiError as inst:
            self.log.error("Could not send message to slack: " + inst.response['error'])

    def alert_slack_message(self, message: str):
        """Attempt to send a message to a designated slack channel.

        Parameters
        ----------
        message : str
            The message to send
        """
        try:
            response = self._slack_client.chat_postMessage(
                channel="printer-bot-test",
                text=message)  
        except SlackApiError as inst:
            self.log.error("Could not send message to slack: " + inst.response['error'])
    
    def upload_log_slack(self):
        """Attempt to upload the invoker's log file to a designated slack channel."""
        try:
            response = self._slack_client.files_upload(    
                file=self._log_filename,
                initial_comment='Uploading log file with error: ' + self._log_filename,
                channels='printer-bot-test'
            )
        except SlackApiError as inst:
            self.log.error("Could not upload log file: " + inst.response['error'])

    def log_command_names(self, unloop: bool = False):
        """Log the names of each command in the sequence

        Parameters
        ----------
        unloop : bool, optional
            Whether to unloop the commands sequence or not, by default False
        """
        self.log.info("="*20 + "LIST OF COMMAND NAMES" + "="*20)
        for name in self._command_seq.get_command_names(unloop):
            self.log.info(name)
        self.log.info("")
        self.log.info("(Number of iterations: " + str(self._command_seq.num_iterations) + ")")
        self.log.info("="*20 + "END OF COMMAND NAMES" + "="*20)

    def log_command_names_descriptions(self, unloop: bool = False):
        """Log the names and descriptions of each command in the sequence

        Parameters
        ----------
        unloop : bool, optional
            Whether to unloop the commands sequence or not, by default False
        """
        self.log.info("="*20 + "LIST OF COMMAND NAMES/DESCRIPTIONS" + "="*20)
        for name_desc in self._command_seq.get_command_names_descriptions(unloop):
            self.log.info(name_desc[0])
            self.log.info(name_desc[1])
        self.log.info("")
        self.log.info("(Number of iterations: " + str(self._command_seq.num_iterations) + ")")
        self.log.info("="*20 + "END OF COMMAND NAMES/DESCRIPTIONS" + "="*20)

    def get_log_messages(self):
        """Get all log messages as a list.

        Returns
        -------
        list
            List of log messages
        """
        log_messages = []
        for handler in self.log.handlers:
            if isinstance(handler, logging.FileHandler):
                handler.flush()  # Ensure all messages are written to the log file
                with open(handler.baseFilename, 'r') as log_file:
                    log_messages.extend(log_file.readlines())
        return log_messages

    def clear_log_file(self):
        """Clear the log file by truncating its content."""
        if self._log_to_file:
            if os.path.exists(self._log_filename):
                with open(self._log_filename, 'w') as log_file:
                    log_file.truncate(0)
                self.log.info("Log file cleared.")
            else:
                self.log.warning("Log file does not exist.")
        else:
            self.log.warning("Log file is not being used.")



# experiment name, id
# is logging, log file, delay between commands, or delay list
# delay list can have a value like -1 or a str to indicate that 
# we wait for user input before proceeding or type quit to terminate early 
# this could also be implemented as a Command that waits for input and returns
#  consider also ctrl c exception termination, safely terminate and log
# invoker observer/inspecter for more complex bookkeeping?

# for params such as experiment name, id, logfile, should these be passed to the invoker constructor OR to the invoke_command method

# for parallel processes with threading consider branches and loop done with the follow command nodes: jump, conditional jump, label, end (ala assembly, exapunks)
# example of conditional jump, prompt user for y/n to jump to a previous label to loop, or jump to a future label to skip some commands
# on loops we can either do the same thing or change the arguments to command (e.g. to explore how printing speed changes each loop). 
# This can be done with a preset that is passed (e.g. a list of parameters corresponding to each loop)
# or this can be done live, e.g. based on equation/condition or based on user input or based on input from a machine learning optimizer
# how to check against infinite loop
# how to check that an execution in a branch doesnt interfere with another branch? the root cannot proceed until its next branch no longer uses receivers that the root will need, and so forth
#  and the root can go as far as it can as long as it uses receivers not used by the next branch?
# how to control threading?, an invoked can call a new thread when it hits a new branch node (or the node is a command itself to start a new thread)
# or an invoker manager or the client sees a new branch node and creates a new invoker and passes it the branch list
# but what if a branch within a branch? need some sort of composite/recursive approach

# how to deal with commands with arguments that change every loop? 
# Should we have command objects that persist throughout loops? if so, should they keep track of their own execution count? (this probably makes writing command classes more complicated)
# should we generate new commands instead, cloning the loop section on each iteration with new commands?
# whose job is it to change the command or generate new commands, the client or invoker
# and how do we deal with commands with arguments that come from user input on each loop?
# how can we make the user input argument and preset list argument methods as similar as possible?
# are commands changable after instantiation or should we just destroy and remake them? 
# if changable then we need update functions/getters to update name/description when arguments change which makes them more complicated
# if we should destroy and remake, we might as well make them when we are ready (after taking user input). 
# But this means the client doesnt have a singular invoker_command method call, and we should always push new commands to the stack/queue and have invoker invoke them
# this means the invoker needs to wait when reaching the end of its current command list, meaning the client needs a definite way to terminate invoking on the invoker
