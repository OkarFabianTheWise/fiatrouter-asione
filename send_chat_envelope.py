"""Patched send_chat_envelope with self-sign guard and --force-sign.

This is a drop-in alternative to `send_chat_envelope.py` that avoids
signing the envelope when the signing identity equals the target address
to prevent recursive self-processing loops. Use `--force-sign` to override.
"""

import argparse
import json
import sys
from uuid import uuid4
from datetime import datetime, timezone

import requests

from uagents_core.models import Model as CoreModel
from uagents_core.envelope import Envelope
from uagents_core.identity import generate_user_address, Identity
from uagents_core.contrib.protocols.chat import ChatMessage, TextContent


def get_agent_info(base_url: str):
    url = f"{base_url.rstrip('/')}/agent_info"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()


def build_chat_message(text: str) -> ChatMessage:
    return ChatMessage(
        timestamp=datetime.now(timezone.utc),
        msg_id=uuid4(),
        content=[TextContent(type="text", text=text)],
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="Base URL for the agent (overrides HEROKU_URL env)")
    parser.add_argument("--text", help="Text to send to the agent", default="Hello from test client!")
    parser.add_argument("--target", help="Explicit target agent address (bech32). Overrides /agent_info")
    parser.add_argument("--sync", help="Request synchronous response (x-uagents-connection: sync)", action="store_true")
    parser.add_argument("--sign-with-agent", help="Sign envelope with local agent identity (read from private_keys.json) or provide --private-key-hex", action="store_true")
    parser.add_argument("--force-sign", help="Force signing even when identity equals target (may cause loops)", action="store_true")
    parser.add_argument("--private-key-hex", help="Hex-encoded identity private key to sign the envelope (overrides private_keys.json)")
    parser.add_argument("--agent-name", help="Agent name key in private_keys.json (default: fiatrouter-icm)", default="fiatrouter-icm")
    args = parser.parse_args()

    base_url = args.url or ("http://localhost:8008")

    agent_address = None
    if args.target:
        agent_address = args.target
        print(f"Using explicit target address: {agent_address}")
    else:
        print(f"Querying agent info at {base_url}/agent_info ...")
        try:
            info = get_agent_info(base_url)
        except Exception as e:
            print("Failed to fetch /agent_info:", e)
            sys.exit(1)

        agent_address = info.get("address")
        if not agent_address:
            print("/agent_info did not return an 'address' field. Response:", info)
            sys.exit(1)
        print(f"Discovered agent address: {agent_address}")

    chat = build_chat_message(args.text)

    schema_digest = CoreModel.build_schema_digest(ChatMessage)
    print("Using schema digest:", schema_digest)

    # Determine sender and whether to sign
    sender_address = generate_user_address()
    identity_to_sign = None

    if args.sign_with_agent:
        # load identity from provided hex or from private_keys.json
        if args.private_key_hex:
            try:
                identity = Identity.from_string(args.private_key_hex)
            except Exception as e:
                print("Failed to create identity from provided hex:", e)
                sys.exit(1)
        else:
            # try to read private_keys.json in repo root
            try:
                with open("private_keys.json", "r") as f:
                    keys = json.load(f)
                entry = keys.get(args.agent_name)
                if not entry or "identity_key" not in entry:
                    print(f"private_keys.json missing identity for {args.agent_name}")
                    sys.exit(1)
                identity = Identity.from_string(entry["identity_key"])
            except FileNotFoundError:
                print("private_keys.json not found and no --private-key-hex supplied")
                sys.exit(1)
            except Exception as e:
                print("Failed to read identity from private_keys.json:", e)
                sys.exit(1)

        # Safety: avoid signing when the identity address equals the target address
        # because that often causes the server/agent to treat the message as
        # originating from itself and can trigger recursive processing loops.
        if agent_address and identity.address == agent_address and not args.force_sign:
            print("Warning: identity address equals target agent address; not signing to avoid processing loops. Use --force-sign to override.")
            identity_to_sign = None
        else:
            sender_address = identity.address
            identity_to_sign = identity

    # Build envelope
    env = Envelope(
        version=1,
        sender=sender_address,
        target=agent_address,
        session=uuid4(),
        schema_digest=schema_digest,
    )

    env.encode_payload(chat.model_dump_json())

    submit_url = f"{base_url.rstrip('/')}/submit"
    headers = {"Content-Type": "application/json"}
    if args.sync:
        headers["x-uagents-connection"] = "sync"
        print("Requesting synchronous response (x-uagents-connection: sync)")

    print(f"Posting chat envelope to {submit_url} ...")

    try:
        body = env.model_dump()

        # sign if requested
        if identity_to_sign is not None:
            env.sign(identity_to_sign)
            body = env.model_dump()

        # Convert UUIDs and other non-serializable types to strings
        if body.get("session") is not None:
            body["session"] = str(body["session"])
        if body.get("version") is not None:
            body["version"] = int(body["version"]) if not isinstance(body["version"], int) else body["version"]

        # log debug info (don't print payload in production)
        print(f"Envelope sender: {body.get('sender')}")
        print(f"Envelope target: {body.get('target')}")

        resp = requests.post(submit_url, headers=headers, json=body, timeout=30)
        print("Status:", resp.status_code)
        try:
            print("Response JSON:", resp.json())
        except Exception:
            print("Response text:", resp.text)
    except Exception as e:
        print("Failed to post envelope:", e)


if __name__ == "__main__":
    main()
