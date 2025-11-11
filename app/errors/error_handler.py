from antlr4.error.ErrorListener import ErrorListener
from antlr4.error.Errors import ParseCancellationException


class RPLErrorListener(ErrorListener):
    """
    Custom error listener that collects errors instead of printing them.
    """

    def __init__(self):
        super().__init__()
        self.errors = []

    def syntaxError(self, recognizer, offender_symbol, line, column, msg, e):
        """Called when a syntax error occurs."""
        error_msg = f"Line {line}:{column} - Syntax Error: {msg}"
        self.errors.append({
            'line': line,
            'column': column,
            'message': msg,
            'symbol': offender_symbol.text if offender_symbol else None
        })
        print(f"❌ {error_msg}")

    def reportAmbiguity(self, recognizer, dfa, start_index, stop_index,
                        exact, ambiguity_alts, configs):
        """Called when parser detects ambiguity."""
        msg = f"Ambiguity detected at indices {start_index}-{stop_index}"
        self.errors.append({'type': 'ambiguity', 'message': msg})
        print(f"⚠️  {msg}")

    def reportAttemptingFullContext(self, recognizer, dfa, start_index,
                                    stop_index, conflicting_alts, configs):
        """Called when parser attempts full context."""
        pass  # Usually not critical

    def reportContextSensitivity(self, recognizer, dfa, start_index,
                                 stop_index, prediction, configs):
        """Called when parser detects context sensitivity."""
        pass  # Usually not critical

    def has_errors(self):
        """Check if any errors were collected."""
        return len(self.errors) > 0

    def get_error_report(self):
        """Get formatted error report."""
        if not self.errors:
            return "No errors found"

        report = f"Found {len(self.errors)} error(s):\n"
        for i, error in enumerate(self.errors, 1):
            if 'line' in error:
                report += f"  {i}. Line {error['line']}:{error['column']} - "
                report += f"{error['message']}\n"
            else:
                report += f"  {i}. {error['message']}\n"
        return report


class ThrowingErrorListener(ErrorListener):
    """
    Error listener that throws exceptions immediately on errors.
    Useful for fail-fast scenarios.
    """

    def syntaxError(self, recognizer, offender_symbol, line, column, msg, e):
        ex = ParseCancellationException(
            f"Line {line}:{column} - {msg}"
        )
        ex.line = line
        ex.column = column
        raise ex