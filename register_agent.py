import os
from uagents_core.utils.registration import (
    register_chat_agent,
    RegistrationRequestCredentials,
)

# --- Config ---
AGENT_NAME = "fr-icm"  # must match your Agentverse handle name
AGENT_ENDPOINT = "https://opened-promote-purposes-ricky.trycloudflare.com"  # your tunnel URL

# --- Run registration ---
register_chat_agent(
    AGENT_NAME,
    AGENT_ENDPOINT,
    active=True,
    credentials=RegistrationRequestCredentials(
        agentverse_api_key="agent1qfz6f3a4tmk68dmxlvkkskn3hxl70t0kv6v870kev5tl9j9rs24q5y7605k",
        agent_seed_phrase="want human trial stomach room begin fever minimum east shoulder trumpet electric",
    ),
)
