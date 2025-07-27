import pyperclip
from llmbrix.agent import Agent
from llmbrix.chat_history import ChatHistory
from llmbrix.gpt_openai import GptOpenAI
from llmbrix.msg import SystemMsg, UserMsg

from brixterm.constants import INTRODUCTION_MSG

SYS_PROMPT = (
    "You are terminal chatbot assistant `BrixTerm`. \n\n"
    "User is developer who can ask any kind of questions. "
    "Your answers will be printed into terminal. "
    "Make sure they are easily readable in small window. "
    "Use nice bullet points, markdown and emojis.\n\n"
    "Here is also terminal introductory message user already saw. "
    "It describes some special commands in this BrixTerm terminal:\n"
    f"\n{INTRODUCTION_MSG}"
)


class ChatBot:
    def __init__(self, gpt_model: str, chat_hist_size: int = 10):
        self.agent = Agent(
            gpt=GptOpenAI(model=gpt_model),
            chat_history=ChatHistory(max_turns=chat_hist_size),
            system_msg=SystemMsg(content=SYS_PROMPT),
        )

    def chat(self, user_input: str, clipboard=False) -> str:
        if clipboard:
            user_input += f"\n\nBelow is copy of relevant context from my clipboard:\n\n{pyperclip.paste()}"
        assistant_msg = self.agent.chat(UserMsg(content=user_input))
        return "🤖💬 " + assistant_msg.content
