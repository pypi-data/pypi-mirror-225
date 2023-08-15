# Message Schemas Python library

Message schemas library in Python. This contains the message schemas in Python. This is published to different registries:

1. Gitlab Package Registry
2. PyPI Package registry

Other registries could also be included

## Requirements

Ensure you have [Python 3](https://www.python.org/downloads/) installed in your local development machine & also [Pip](https://pypi.org/project/pip/) &  [virtualenv](https://virtualenv.pypa.io/)

## Setup

First create a virtual environment.

``` shell
virtualenv .venv
```

> This creates a virtual environment in the current directory

Now, you can install the dependencies with:

```shell
pip install -r requirements
```

Or with make:

```shell
make install
```

That should be it.

In order to build a package, the protobuf generated code needs to be build first. This can be done from the root directory of this project with:

```shell
buf generate
```

Or

```shell
make generate
```

Now, the package can be built with:

```shell
make build
```

Other commands can be viewed with:

```shell
make help
```

## Publishing Packages

Publishing packages can be done in a couple of ways depending on the registry that the package is being published to.

### Gitlab Package Registry

To publish to Gitlab, ensure that the above steps have been first completed.

Next, create a [Personal Access Token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html) with the scope set to api as stated [here](https://docs.gitlab.com/ee/user/packages/pypi_repository/#authenticate-with-the-package-registry).

Next step is to update your [pypirc](~/.pypirc) file. This will be in your home directory. If none is available ensure that you create one.

Now modify the file to look like this:

```pypirc
[distutils]
index-servers =
    pypi
    gitlab

[pypi]
  username = __token__
  password = <PYPI_TOKEN>

[gitlab]
  repository = https://gitlab.com/api/v4/projects/47231151/packages/pypi
  username = <GITLAB_PERSONAL_ACCESS_TOKEN_NAME>
  password = <GITLAB_PERSONAL_ACCESS_TOKEN>
```

> Note that this is in the instance of using 2 repositories/registries (PyPI & Gitlab).

You can name the `gitlab` registry anything else, just ensure that the `index-servers` block and the registry specific block match. For example, in the instance of naming it to `messageschemas-gitlab`:

```pypirc
[distutils]
index-servers =
    pypi
    messageschemas-gitlab

[pypi]
  username = __token__
  password = <PYPI_TOKEN>

[messageschemas-gitlab]
  repository = https://gitlab.com/api/v4/projects/47231151/packages/pypi
  username = <GITLAB_PERSONAL_ACCESS_TOKEN_NAME>
  password = <GITLAB_PERSONAL_ACCESS_TOKEN>
```

Additionally, ensure that the repository URL is setup correctly as well. In this case the `47231151` is the project ID. This can be found on Gitlab.

Now, with that setup, publishing a package to Gitlab Package registry can be done using the following command:

```shell
python3 -m twine upload --repository messageschemas-gitlab dist/*
```

> Ensure that the `--repository` flag is set correctly and matches the contents of the file in `~/.pypirc`

Optionally, if a `pypirc` file is not used, the below command should work:

```shell
TWINE_PASSWORD=<personal_access_token or deploy_token> TWINE_USERNAME=<username or deploy_token_username> python3 -m twine upload --repository-url https://gitlab.example.com/api/v4/projects/<project_id>/packages/pypi dist/*
```

> This should be sufficient as well. Ensure that the fields in `<>` brackets are filled correctly

NOTE: You can no publish a package of the same name and version to the Package Registry. The version has to be bumped up for it to work.

If all goes well, you should see a shell output like below:

```plain
INFO     Using configuration from /Users/lusina/.pypirc                                                                                                                           
Uploading distributions to https://gitlab.com/api/v4/projects/47231151/packages/pypi
INFO     dist/sanctumlabs_messageschema-0.1.dev0-py3-none-any.whl (23.5 KB)                                                                                                       
INFO     dist/sanctumlabs-messageschema-0.1.dev0.tar.gz (11.8 KB)                                                                                                                 
INFO     username set from config file                                                                                                                                            
INFO     password set from config file                                                                                                                                            
INFO     username: PackageRegistryToken                                                                                                                                           
INFO     password: <hidden>                                                                                                                                                       
Uploading sanctumlabs_messageschema-0.1.dev0-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 27.0/27.0 kB • 00:00 • 37.2 MB/s
INFO     Response from https://gitlab.com/api/v4/projects/47231151/packages/pypi:                                                                                                 
         201 Created                                                                                                                                                              
INFO     {"message":"201 Created"}                                                                                                                                                
Uploading sanctumlabs-messageschema-0.1.dev0.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 14.9/14.9 kB • 00:00 • ?
INFO     Response from https://gitlab.com/api/v4/projects/47231151/packages/pypi:                                                                                                 
         201 Created                                                                                                                                                              
INFO     {"message":"201 Created"} 
```

#### Usage

In order to use this library you could do the following:

```shell
pip install sanctumlabs-messageschema --index-url https://__token__:<your_personal_token>@gitlab.com/api/v4/projects/47231151/packages/pypi/simple
```

> Where `<your_personal_token>` is your personal access token with scope to read packages

## References

1. [Gitlab PyPI Repository](https://docs.gitlab.com/ee/user/packages/pypi_repository/)
