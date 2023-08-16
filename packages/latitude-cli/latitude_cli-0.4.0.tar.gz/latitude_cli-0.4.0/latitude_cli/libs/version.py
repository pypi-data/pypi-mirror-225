import pkg_resources
import requests
import typer
from colorama import Fore
from colorama import Style
from packaging import version


def getVerison():
    version = 0
    try:
        version = pkg_resources.get_distribution("latitude55").version
    except pkg_resources.DistributionNotFound:
        print("{} not installed".format("latitude55"))

    return version


def getLatestPyPiVersion():
    package = "latitude55"

    response = requests.get(f"https://pypi.org/pypi/{package}/json")

    if response.status_code == 404:
        print("Package not deployed yet")
        return

    latest_pypi_version = response.json()["info"]["version"]

    installed_version = getVerison()

    if version.parse(latest_pypi_version) > version.parse(installed_version):
        upgradeCliMessage(latest_pypi_version, installed_version)


def upgradeCliMessage(latest_pypi_version, installed_version):
    upgrade_message = (
        "\n"
        f"{Fore.YELLOW}{'-'*42}{Style.RESET_ALL}\n"
        " New version of latitude CLI available!  \n"
        f"           {Fore.RED} {latest_pypi_version} {Style.RESET_ALL} -> {Fore.GREEN} {installed_version}    \n"  # noqa: E501
        f"{Style.RESET_ALL} Run {Fore.GREEN}pip install -U latitude{Style.RESET_ALL} to update!\n"  # noqa: E501
        f"{Fore.YELLOW}{'-'*42}{Style.RESET_ALL}\n"
    )
    typer.echo(upgrade_message)
