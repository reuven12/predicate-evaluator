class PredicateError(Exception):
    pass

class RemotePredicateFetchError(PredicateError):
    def __init__(self, message: str):
        super().__init__(f"Remote fetch error: {message}")

class InvalidOperatorError(PredicateError):
    def __init__(self, operator: str):
        super().__init__(f"Invalid operator: '{operator}'")

class EvaluationError(PredicateError):
    def __init__(self, reason: str):
        super().__init__(f"Evaluation failed: {reason}")

class FeatureResolutionError(PredicateError):
    def __init__(self, path: str):
        super().__init__(f"Feature path '{path}' could not be resolved")

class MissingEnvironmentVariableError(PredicateError):
    def __init__(self, var_name: str):
        super().__init__(f"Missing environment variable: {var_name}")