
class NoActivityLogFile(Exception):
    ''' Exception raised when no activity log file(s) provided '''
    pass


class NoStudentResultsFile(Exception):
    ''' Exception raised when no student results file(s) provided '''
    pass


class InvalidDataInFile(Exception):
    """Exception raised for invalid data in the files uploaded"""
    pass