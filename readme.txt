directory should be structured like this

|/project-folder/        (make sure you set this as your working project directory so the venv isnt in the repo)
|
|---/.venv/       (the virtual environment outside of the repo)
|---/Headliners/  (the repository)
|---/---/website/
|       ...
|       ...


make virtual environment (outside of repo)
    py -3 -m venv .venv
activate venv
    .venv/Scripts/activate
install packages
    pip install -r <project-folder>/requirements.txt
run main.py