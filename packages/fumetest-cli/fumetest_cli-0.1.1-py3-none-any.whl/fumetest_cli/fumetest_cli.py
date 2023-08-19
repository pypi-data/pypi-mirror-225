import click
from functions.run_tests import run_tests
from functions.setup_test import setup_test
from functions.replay_case import replay_case
from functions.setup_login import setup_login

def hidden_prompt(text):
    return click.prompt(text, hide_input=True)

def multiple_choice_menu(options, prompt="Please choose:"):
    for i, option in enumerate(options, 1):
        click.echo(f"{i}. {option}")

    choice = click.prompt(prompt, type=click.IntRange(1, len(options)))
    return options[choice - 1]

@click.group()
def cli():
    """A CLI tool to run tests."""
    pass

@click.command()
@click.option('--url', required=True, type=str, help='The URL to run the tests against.', prompt='Enter URL')
@click.option('--project-id', required=True, type=str, help='The ID of the project you want to run tests on.', prompt='Enter Project ID')
@click.option('--username', prompt='Please enter your username', type=str, help='Your Fume username to login')
@click.option('--timeout', default=30, type=int, help='The timeout value in seconds.', prompt='Enter Timeout (in seconds)')
def run(url, project_id, timeout, username):
    """Run tests for a given URL and project name with the specified timeout."""
    password = click.prompt('Please enter your password', hide_input=True)

    authToken, userID, testID = setup_test(username=username, password=password, project_id=project_id)

    run_tests(url, project_id, timeout, username, password, 0, userID, authToken, testID)

@click.command()
@click.option('--url', required=True, type=str, help='The URL to run the tests against.', prompt='Enter URL')
@click.option('--case-id', required=True, type=str, help='The ID of the case you want to run tests on.', prompt='Enter Case ID')
@click.option('--username', prompt='Please enter your username', type=str, help='Your Fume username to login')
def replay(url, case_id, username):
    password = click.prompt('Please enter your password', hide_input=True)

    choices = ["Fast", "Normal", "Slow", "Very Slow"]
    speed = multiple_choice_menu(choices)
    authToken, userID = setup_login(username=username, password=password)
    replay_case(authToken=authToken, url=url, caseID=case_id, speed=speed)

cli.add_command(run)
cli.add_command(replay)

if __name__ == '__main__':
    cli()
