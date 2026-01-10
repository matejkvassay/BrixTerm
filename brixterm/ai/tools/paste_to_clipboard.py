import pyperclip
from llmbrix.tool_calling import BaseTool, ToolOutput, ToolParam, ToolParamTypes

NAME = "paste_to_users_clipboard"
DESC = "Takes provided content and pastes it to users clipboard, equivalent to CTRL+C."
PARAM = ToolParam(
    name="content_to_copy", description="This content will be copied to users clipboard.", type=ToolParamTypes.STRING
)


class PasteToClipboard(BaseTool):
    def __init__(self):
        super().__init__(name=NAME, description=DESC, params=[PARAM])

    def execute(self, content_to_copy: str) -> ToolOutput:
        pyperclip.copy(content_to_copy)
        return ToolOutput(success=True, result={"status": "Successfully copied content to user's clipboard."})
