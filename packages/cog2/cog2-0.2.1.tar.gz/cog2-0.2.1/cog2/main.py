import webbrowser
import os
from typing import List
import typer
import requests
from typing_extensions import Annotated
import platform
import subprocess
import os
import openai

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

app = typer.Typer()


def check_os_cog():
    if platform.system() == 'Darwin' or platform.system() == "Linux":
        rc = subprocess.call(['which', 'cog'])
        if rc == 0:
            pass
        else:
            typer.echo("Setting up cog2 for the first time")
            if platform.system() == 'Darwin':
                os.system('brew install cog')
            if platform.system() == 'Linux':
                os.system(
                    "sudo curl -o /usr/local/bin/cog -L https://github.com/replicate/cog/releases/latest/download/cog_`uname -s`_`uname -m`")
                os.system("sudo chmod +x /usr/local/bin/cog")

    if platform.system() == 'Darwin' or platform.system() == "Linux":
        rc = subprocess.call(['which', 'openai'])
        if rc == 0:
            pass
        else:
            typer.echo("Setting up cog2 for the first time")
            if platform.system() == 'Darwin':
                os.system('pip install openai')
            if platform.system() == 'Linux':
                os.system('pip install openai')


check_os_cog()


def save_string_to_file(file_path, content):
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        typer.echo("Config saved to {} successfully.".format(file_path))
    except IOError as e:
        typer.echo(f"Error saving the config: {e}")


@app.command()
def config():
    url = "https://wizmodel-file-stroage.s3.ap-northeast-1.amazonaws.com/base.yaml"
    local_filename = "base.yaml"

    response = requests.get(url)
    if response.status_code == 200:
        with open(local_filename, "wb") as file:
            file.write(response.content)
        typer.echo("config init success")
    else:
        typer.echo("config init failed")
    typer.echo(
        "Welcome to prompt config generation(BETA)\nPlease enter your prompt"
    )
    typer.echo(
        "you can say things like \"add numpy,matplotlib,pytorch to python library, turn on gpu, and use system library ffmpeg...\"\n or just tell what python library you used and which sytem library you need to install, also given an wizmodel user and a model name")

    prompt = typer.prompt("Enter your prompt here")
    config_string = ""
    with open("base.yaml", "r") as file:
        config_string = file.read()

    gpt_prompt = 'generate a new yaml file, python_requirements and python_packages are mutually exclusive so you should comment one out, if no system_packages is given then comment out the system_packages section, ' + prompt + ', just output the yaml, do not include any explanations in your responses,Respond with only the yaml without explanation'
    chat_completion = openai.ChatCompletion.create(model="gpt-4-0613", messages=[
        {"role": "user",
         "content": "Help me write yaml code, given a base template yaml file, this file content is: {},{}".format(
             config_string, gpt_prompt)}])

    typer.echo("Generation done,saving to {} in current directory".format('generated_cog.yaml'))
    string_to_save = chat_completion['choices'][0]['message']['content']
    # string_to_save = ""
    file_path = "generated_cog.yaml"
    save_string_to_file(file_path, string_to_save)
    typer.echo("Config save success")
    local_filename = "base.yaml"

    if os.path.exists(local_filename):
        os.remove(local_filename)
        typer.echo("All temp file generated during config deleted success")
    else:
        typer.echo("All temp file generated during config deleted failed")


# Example usage


@app.command()
def login():
    typer.echo(
        "This command will authenticate Docker with WizModel's Docker registry. You will need a WizModel.com account."
    )
    input(
        "Hit enter to get started. A browser will open with an authentication token that you need to paste here."
    )
    webbrowser.open("https://www.wizmodel.com/models")
    token = typer.prompt("Paste your token here and press Enter to login")
    data = {"token": token}
    response = requests.post(url="https://api.wizmodel.com/cog/v1/verify-token", json=data).json()
    user_name = response['username']
    password = response['docker_token']
    os.system("docker login -u {} -p {} registry.wizmodel.com".format(user_name, password))  # noqa: E501


@app.command()
def build(
        tag: Annotated[str, typer.Option("--tag", "-t")] = "",
        no_cache: bool = typer.Option(False),
        separate_weights: bool = typer.Option(False),
        secret: Annotated[str, typer.Option("--secret")] = ""
):  # noqa: E501
    typer.echo("Building image with tag %s" % tag)
    prefix_cmd = "cog build"
    if tag != "":
        prefix_cmd = prefix_cmd + " -t {}".format(tag)
    if no_cache:
        prefix_cmd = prefix_cmd + " --no-cache"
    if separate_weights:
        prefix_cmd = prefix_cmd + " --separate-weights"
    if len(secret) > 0:
        prefix_cmd = prefix_cmd + " --secret {}".format(secret)
    os.system(prefix_cmd)
    typer.echo("Build cmd finish: " + prefix_cmd)


@app.command()
def push(
        no_cache: bool = typer.Option(False),
        separate_weights: bool = typer.Option(False),
        secret: Annotated[str, typer.Option("--secret")] = ""
):
    prefix_cmd = "cog push"
    if no_cache:
        prefix_cmd = prefix_cmd + " --no-cache"
    if separate_weights:
        prefix_cmd = prefix_cmd + " --separate-weights"
    if len(secret) > 0:
        prefix_cmd = prefix_cmd + " --secret {}".format(secret)
    os.system(prefix_cmd)
    typer.echo("Push cmd finish: " + prefix_cmd)


@app.command()
def predict(input: Annotated[List[str], typer.Option("--input", "-i")] = [],
            output: Annotated[str, typer.Option("--output", "-o")] = ""):  # noqa: E501
    prefix_cmd = "cog predict"
    if len(input) > 0:
        for item in input:
            prefix_cmd = prefix_cmd + " -i {}".format(item)
    if output != "":
        prefix_cmd = prefix_cmd + " --output {}".format(output)
    os.system(prefix_cmd)
    typer.echo("Predict cmd finished: " + prefix_cmd)


@app.command()
def run(publish: Annotated[str, typer.Option("--publish", "-p")] = ""):
    prefix_cmd = "cog run"
    if len(publish) > 0:
        prefix_cmd = prefix_cmd + " -p {}".format(publish)
    os.system(prefix_cmd)
    typer.echo("Run cmd finished: " + prefix_cmd)


@app.command()
def version():
    typer.echo('0.2.1')


@app.command()
def debug():
    os.system("cog debug")
