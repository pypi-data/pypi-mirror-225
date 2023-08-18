import subprocess
def evaluate_response(response: subprocess.CompletedProcess) -> str:
    if response.returncode == 0:
        message = "Dataflow template has been created successfully."
    else:
        message = (
            f"It couldn't be completed\n"
            f"It finished with response: {response.returncode}\n"
            f"Command error output:\n\n{response.stderr.decode('utf-8')}"
        )
        raise ValueError(message)
    return message