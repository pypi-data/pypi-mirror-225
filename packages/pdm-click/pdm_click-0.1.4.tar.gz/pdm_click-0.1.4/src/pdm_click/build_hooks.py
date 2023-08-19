from __future__ import annotations

# import subprocess
from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from pathlib import Path

    from pdm.backend.hooks import Context


class ClickBuildHook:
    DEFAULT_TARGET_DIR = "completions"
    SHELLS: Final[list[str]] = ["bash", "zsh", "fish"]

    def pdm_build_initialize(self, context: Context):
        pass

    def pdm_build_update_files(self, context: Context, files: dict[str, Path]):
        metadata = context.config.metadata
        print(f"pdm-click: metadata: {metadata.items()!r}")
        # for shell in ClickBuildHook.SHELLS:
        #     subprocess.run(["pdm", "run", ])
