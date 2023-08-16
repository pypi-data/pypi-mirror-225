# AA Fleet Finder

[![Version](https://img.shields.io/pypi/v/aa-fleetfinder?label=release)](https://pypi.org/project/aa-fleetfinder/)
[![License](https://img.shields.io/github/license/ppfeufer/aa-fleetfinder)](https://github.com/ppfeufer/aa-fleetfinder/blob/master/LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/aa-fleetfinder)](https://pypi.org/project/aa-fleetfinder/)
[![Django](https://img.shields.io/pypi/djversions/aa-fleetfinder?label=django)](https://pypi.org/project/aa-fleetfinder/)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)
[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](http://black.readthedocs.io/en/latest/)
[![Discord](https://img.shields.io/discord/790364535294132234?label=discord)](https://discord.gg/zmh52wnfvM)
[![Checks](https://github.com/ppfeufer/aa-fleetfinder/actions/workflows/automated-checks.yml/badge.svg)](https://github.com/ppfeufer/aa-fleetfinder/actions/workflows/automated-checks.yml)
[![codecov](https://codecov.io/gh/ppfeufer/aa-fleetfinder/branch/master/graph/badge.svg?token=GFOR9GWRNQ)](https://codecov.io/gh/ppfeufer/aa-fleetfinder)
[![Translation Status](https://weblate.ppfeufer.de/widgets/alliance-auth-apps/-/aa-fleetfinder/svg-badge.svg)](https://weblate.ppfeufer.de/engage/alliance-auth-apps/)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](https://github.com/ppfeufer/aa-fleetfinder/blob/master/CODE_OF_CONDUCT.md)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/N4N8CL1BY)

Control access to your fleets through Alliance Auth.

---

<!-- TOC -->
* [AA Fleet Finder](#aa-fleet-finder)
  * [Installation](#installation)
    * [Step 1: Install the Package](#step-1-install-the-package)
    * [Step 2: Configure Alliance Auth](#step-2-configure-alliance-auth)
    * [Step 3: Add the Scheduled Task](#step-3-add-the-scheduled-task)
    * [Step 4: Finalizing the Installation](#step-4-finalizing-the-installation)
    * [Step 4: Setup Permissions](#step-4-setup-permissions)
  * [Changelog](#changelog)
  * [Contributing](#contributing)
<!-- TOC -->

---


## Installation

### Step 1: Install the Package

Make sure you're in the virtual environment (venv) of your Alliance Auth installation Then install the latest release directly from PyPi.

```shell
pip install aa-fleetfinder
```


### Step 2: Configure Alliance Auth

This is fairly simple, just add the following to the `INSTALLED_APPS` of your `local.py`

Configure your AA settings (`local.py`) as follows:

- Add `"fleetfinder",` to `INSTALLED_APPS`


### Step 3: Add the Scheduled Task

To set up the scheduled task, add the following code to your `local.py`:

```python
# AA Fleetfinder - https://github.com/ppfeufer/aa-fleetfinder
if "fleetfinder" in INSTALLED_APPS:
    CELERYBEAT_SCHEDULE["fleetfinder_check_fleet_adverts"] = {
        "task": "fleetfinder.tasks.check_fleet_adverts",
        "schedule": crontab(minute="*/1"),
    }
```


### Step 4: Finalizing the Installation

Run static files collection and migrations

```shell
python manage.py collectstatic
python manage.py migrate
```


### Step 4: Setup Permissions

Now it's time to set up access permissions for your new Fleetfinder module.

| ID                    | Description                        | Notes                                                                                                        |
|:----------------------|:-----------------------------------|:-------------------------------------------------------------------------------------------------------------|
| `access_fleetfinder`  | Can access the Fleetfinder module  | Your line members should have this permission, together with everyone you want to have access to he module.  |
| `manage_fleets`       | Can manage fleets                  | Everyone with this permission can open and edit fleets                                                       |


## Changelog

See [CHANGELOG.md](https://github.com/ppfeufer/aa-fleetfinder/blob/master/CHANGELOG.md)


## Contributing

You want to contribute to this project? That's cool!

Please make sure to read the [Contribution Guidelines](https://github.com/ppfeufer/aa-fleetfinder/blob/master/CONTRIBUTING.md) (I promise, it's not much,
just some basics)
