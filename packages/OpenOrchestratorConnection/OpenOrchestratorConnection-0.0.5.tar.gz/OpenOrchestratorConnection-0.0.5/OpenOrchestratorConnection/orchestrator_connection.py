from . import DB_util, Crypto_util
import sys

class OrchestratorConnection:
    def __init__(self, process_name:str, connection_string:str, crypto_key:str):
        self.process_name = process_name
        Crypto_util.set_key(crypto_key)
        DB_util.connect(connection_string)
    
    def __repr__(self):
        return f"OrchestratorConnection - Process name: {self.process_name}"
    
   
    def log_trace(self, message:str):
        """Create a message in the Orchestrator log with a level of 'trace'.
        The log is automatically annotated with the current time and name of the process"""
        DB_util.create_log(self.process_name, 0, message)

    def log_info(self, message:str):
        """Create a message in the Orchestrator log with a level of 'info'.
        The log is automatically annotated with the current time and name of the process
        """
        DB_util.create_log(self.process_name, 1, message)
    
    def log_error(self, message:str):
        """Create a message in the Orchestrator log with a level of 'error'.
        The log is automatically annotated with the current time and name of the process
        """
        DB_util.create_log(self.process_name, 2, message)
    
    def get_constant(constant_name:str) -> str:
        """Get a constant from the Orchestrator with the given name.
        return: The value of the named constant."""
        return DB_util.get_constant(constant_name)
    
    def get_credential(credential_name:str) -> tuple[str, str]:
        """Get a credential from the Orchestrator with the given name.
        return: tuple(username, password)
        """
        return DB_util.get_credential(credential_name)
    
    def update_constant(constant_name:str, new_value:str):
        """Update an Orchestrator constant with a new value.
        Raises an error if no constant with the given name exists.
        """
        DB_util.update_constant(constant_name, new_value)
    
    def update_credential(credential_name:str, new_username:str, new_password:str):
        """Update an Orchestrator credential with a new username and password.
        Raises an error if no credential with the given name exists.
        """
        DB_util.update_credential(credential_name, new_username, new_password)

def create_connection_from_args():
    """Create an OrchestRator Connection object using the arguments passed to sys.argv"""
    process_name = sys.argv[1]
    connection_string = sys.argv[2]
    crypto_key = sys.argv[3]
    return OrchestratorConnection(process_name, connection_string, crypto_key)

