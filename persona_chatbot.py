"""
=============================================================
  Persona Chatbot — powered by af1tang/personaGPT
  Uses HuggingFace Transformers (runs 100% locally, no API)
=============================================================

HOW TO RUN
----------
1. Install dependencies:
      pip install transformers torch

2. Run the script:
      python persona_chatbot.py

3. On first run the model (~1.4 GB) will be downloaded automatically
   from HuggingFace and cached locally for future use.

ABOUT THE MODEL
---------------
  • af1tang/personaGPT — built on DialoGPT-medium + GPT-2
  • Trained on the Persona-Chat dataset
  • You define the bot's personality as plain-English facts
  • Supports GPU (CUDA) automatically if available
"""

import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel

# ── Pre-built persona profiles ────────────────────────────────────────────────

PERSONAS = {
    "1": {
        "name": "Sherlock Holmes",
        "facts": [
            "I am a brilliant consulting detective living at 221B Baker Street.\n",
            "I speak in a sharp, deductive, and sometimes condescending manner.\n",
            "I have an encyclopaedic knowledge of crime and human behaviour.\n",
            "I am a close companion of Dr Watson and often work with Scotland Yard.\n",
            "I find mundane conversation tedious and prefer intellectual challenges.\n",
        ],
    },
    "2": {
        "name": "Master Yoda",
        "facts": [
            "I am a 900-year-old Jedi Grand Master and guardian of the Force.\n",
            "I speak with inverted sentence structure, placing the verb at the end.\n",
            "I am wise, patient, and deeply connected to all living things.\n",
            "I have trained many Jedi Knights, including Luke Skywalker.\n",
            "I believe that fear and anger lead to the dark side of the Force.\n",
        ],
    },
    "3": {
        "name": "Tony Stark",
        "facts": [
            "I am Tony Stark, genius billionaire, philanthropist, and Iron Man.\n",
            "I speak with confidence, sarcasm, and quick wit.\n",
            "I created a powered suit of armour and use it to protect the world.\n",
            "I co-founded the Avengers and have saved the world multiple times.\n",
            "I am always the smartest person in the room and I know it.\n",
        ],
    },
    "4": {
        "name": "Custom — define your own",
        "facts": [],   # filled in interactively
    },
}

# ── Utility helpers ───────────────────────────────────────────────────────────

flatten = lambda lst: [item for sublist in lst for item in sublist]


def to_var(x, device):
    """Convert list/numpy array to a GPU/CPU tensor."""
    if not torch.is_tensor(x):
        x = torch.tensor(x)
    return x.to(device)


def generate_reply(model, tokenizer, bot_input_ids, device,
                   do_sample=True, top_k=10, top_p=0.92, max_length=1000):
    """Run the model and return only the newly generated token IDs."""
    with torch.no_grad():
        output = model.generate(
            bot_input_ids,
            do_sample=do_sample,
            top_k=top_k,
            top_p=top_p,
            max_length=max_length,
            pad_token_id=tokenizer.eos_token_id,
        )
    # Strip the prompt tokens — keep only the new reply
    new_tokens = output[:, bot_input_ids.shape[-1]:][0]
    return new_tokens.tolist()


def display_history(dialog_history, tokenizer, persona_name):
    """Pretty-print the full conversation so far."""
    print("\n" + "─" * 55)
    for idx, token_ids in enumerate(dialog_history):
        text = tokenizer.decode(token_ids, skip_special_tokens=True)
        speaker = "You" if idx % 2 == 0 else persona_name
        print(f"  {speaker:>14}: {text}")
    print("─" * 55 + "\n")


# ── Main chatbot loop ─────────────────────────────────────────────────────────

def main():
    print("\n" + "=" * 55)
    print("        PERSONA CHATBOT  (af1tang/personaGPT)")
    print("=" * 55)

    # 1. Choose device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"\n  Device : {device}")

    # 2. Load model
    print("  Model  : af1tang/personaGPT")
    print("  (Downloading ~1.4 GB on first run — please wait...)\n")
    tokenizer = GPT2Tokenizer.from_pretrained("af1tang/personaGPT")
    model     = GPT2LMHeadModel.from_pretrained("af1tang/personaGPT").to(device)
    model.eval()
    print("  ✓ Model loaded.\n")

    # 3. Pick a persona
    print("  Choose a persona:")
    for key, p in PERSONAS.items():
        print(f"    [{key}]  {p['name']}")
    print()

    while True:
        choice = input("  Your choice (1-4): ").strip()
        if choice in PERSONAS:
            break
        print("  ⚠  Please enter 1, 2, 3, or 4.")

    persona = PERSONAS[choice]

    # 4. If custom, collect personality facts
    if choice == "4":
        persona_name = input("\n  Enter a name for your persona: ").strip() or "Bot"
        persona["name"] = persona_name
        print(f'\n  Enter up to 5 personality facts about "{persona_name}".')
        print('  Example: "I love hiking in the mountains."')
        print('  Press Enter with no text to finish early.\n')
        for i in range(1, 6):
            fact = input(f"  Fact {i}: ").strip()
            if not fact:
                break
            persona["facts"].append(fact + "\n")
        if not persona["facts"]:
            persona["facts"] = ["I am a friendly and helpful chatbot.\n"]

    persona_name = persona["name"]
    persona_facts = persona["facts"]

    print(f'\n  ✓ Persona set: "{persona_name}"')
    print("  Personality facts:")
    for f in persona_facts:
        print(f"      • {f.strip()}")

    # 5. Encode persona prefix using special tokens
    #    Format: <|p2|> fact1 fact2 ... <|sep|> <|start|>
    persona_token_ids = tokenizer.encode(
        "".join(["<|p2|>"] + persona_facts + ["<|sep|>", "<|start|>"])
    )

    # 6. Chat loop
    print()
    print("─" * 55)
    print(f'  Chatting with {persona_name}. Type "quit" to exit.')
    print('  Type "history" to see the full conversation.')
    print("─" * 55 + "\n")

    dialog_history = []   # list of token-id lists, alternating user/bot

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in {"quit", "exit", "bye"}:
            print(f'\n  {persona_name}: Farewell! Until we meet again.\n')
            break

        if user_input.lower() == "history":
            if dialog_history:
                display_history(dialog_history, tokenizer, persona_name)
            else:
                print("  (No messages yet.)\n")
            continue

        # Encode user message
        user_token_ids = tokenizer.encode(user_input + tokenizer.eos_token)
        dialog_history.append(user_token_ids)

        # Build the full input:  persona prefix + flattened dialog history
        bot_input_ids = to_var(
            [persona_token_ids + flatten(dialog_history)], device
        )

        # Truncate if we're approaching the 1 000-token limit
        if bot_input_ids.shape[-1] > 900:
            # Drop oldest exchange (2 turns) to free space
            if len(dialog_history) >= 2:
                dialog_history = dialog_history[2:]
            bot_input_ids = to_var(
                [persona_token_ids + flatten(dialog_history)], device
            )

        # Generate reply
        reply_ids = generate_reply(model, tokenizer, bot_input_ids, device)
        dialog_history.append(reply_ids)

        reply_text = tokenizer.decode(reply_ids, skip_special_tokens=True)
        print(f"\n{persona_name}: {reply_text}\n")


if __name__ == "__main__":
    main()
