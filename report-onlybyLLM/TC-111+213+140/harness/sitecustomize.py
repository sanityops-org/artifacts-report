"""Compatibility shim for deeplogic-cli 1.18.0 and defect-check 1.2.8."""

import inspect
import os


if os.environ.get("DEEPLOGIC_COMPAT") == "1":
    import defect_check

    _OriginalDefectChecker = defect_check.DefectChecker
    _OriginalDefectCheckOptions = defect_check.DefectCheckOptions

    class CompatDefectCheckOptions(_OriginalDefectCheckOptions):
        """Accept CLI-only force_permission while preserving SDK checks."""

        def __init__(self, *args, force_permission=False, **kwargs):
            super().__init__(*args, **kwargs)

    class CompatDefectChecker(_OriginalDefectChecker):
        """Adapt CLI-only timeout and async closing to the installed SDK."""

        def __init__(self, *args, timeout=None, **kwargs):
            super().__init__(*args, **kwargs)

        async def close(self):
            result = super().close()
            if inspect.isawaitable(result):
                await result

    defect_check.DefectChecker = CompatDefectChecker
    defect_check.DefectCheckOptions = CompatDefectCheckOptions
