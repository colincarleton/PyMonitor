class MonitoringException(Exception):
    """
    Base exception class
    """


class ConfigurationError(MonitoringException):
    """
    Exception raised when a misconfiguration is detected
    """
