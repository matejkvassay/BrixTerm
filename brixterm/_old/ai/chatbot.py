import pyperclip
from llmbrix.chat_history import ChatHistory
from llmbrix.gemini_model import GeminiModel
from llmbrix.tool_agent import ToolAgent

from brixterm._old.ai.tools import PasteToClipboard

SYS_PROMPT = (
    "You are terminal chatbot assistant `BrixTerm`."
    "User is developer who can ask any kind of questions. "
    "Your answers will be printed into terminal. "
    "Make sure they are easily readable in small window. "
    "Use nice bullet points, markdown and emojis. "
    "If user asks you to write or generate something they might want to copy it with CTRL+C "
    "(e.g. code, list, SQL query, documentation, email, etc.). "
    "Always paste raw content to user's clipboard, no extra markdown tags wrapping it."
    "Always ask user for approval before you copy something to user's clipboard."
)


class ChatBot:
    def __init__(self, gpt: GeminiModel, chat_hist_size: int = 10):
        self.agent = ToolAgent(
            gemini_model=gpt,
            chat_history=ChatHistory(max_turns=chat_hist_size),
            system_instruction=SYS_PROMPT,
            tools=[PasteToClipboard()],
        )

    def chat(self, user_input: str, clipboard=False) -> str:
        print(user_input)
        if clipboard:
            user_input += f"\n\nBelow is copy of relevant context from my clipboard:\n\n{pyperclip.paste()}"
        assistant_msg = self.agent.chat(user_input)
        print(assistant_msg)
        return "🤖💬 " + assistant_msg.text
