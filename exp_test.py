from litellm import token_counter, model_cost
import json

def truncate_to_fit(adk_messages, model_name, max_tokens):
    lite_messages = []
    preserved_messages = []  # system, function_call, function_response
    agent_messages = []      # candidate for truncation

    # Split messages into preserved + agent text
    for msg in adk_messages:
        role = msg.role
        for part in msg.parts:
            if hasattr(part, "text"):
                if role in ["assistant","system"] :  # candidate for truncation
                    agent_messages.append({"role": role, "content": part.text})
                else:  # user/system text preserved
                    preserved_messages.append({"role": role, "content": part.text})

            elif hasattr(part, "function_call"):
                fc = part.function_call
                fc_text = f"[FunctionCall] {fc.name} {json.dumps(fc.args)}"
                preserved_messages.append({"role": role, "content": fc_text})

            elif hasattr(part, "function_response"):
                fr = part.function_response
                fr_text = f"[FunctionResponse] {fr.name} {json.dumps(fr.response)}"
                preserved_messages.append({"role": role, "content": fr_text})

            elif hasattr(part, "data"):  # binary
                preserved_messages.append({"role": role, "content": f"[Binary: {len(part.data)} bytes]"})

    # Start with all preserved
    final_messages = preserved_messages + agent_messages
    total_tokens = token_counter(model=model_name, messages=final_messages)

    # Truncate agent text if needed
    while total_tokens > max_tokens and agent_messages:
        # drop oldest agent text message
        agent_messages.pop(0)
        final_messages = preserved_messages + agent_messages
        total_tokens = token_counter(model=model_name, messages=final_messages)

    return final_messages, total_tokens
