# Seaborn Grasshopper

A Rhino Remote library that brings Seaborn (Matplotlib) inside of Grasshopper using [Hops](https://github.com/mcneel/compute.rhino3d/tree/master/src/ghhops-server-py).

This second version is a complete refactor of the seaborn-grasshopper implementation. This approach greatly improves from the first version in the following ways:

- Additional fuctions added
  - `despine` Dictionary with "Despine" functions arguments, that removes top and right axis lines.
  - `add_args` Use additional figure arguments are not implemented in Grasshopper.
  - `ax_args` Implement axis arguments to the matplotlib.Axis element. (Set title, x and y limits, etc )
  - `fig_size` Change figure size
- Ready for web deployment using Heroku and gunicorn
- Export image as a encoded b64 string
- Less code duplication
- Correct handling of defaults
- Style improvement

## Typical workflow

![Seaborn Grasshopper](https://i.imgur.com/MUZLQhk.gif)
Author : Pablo Arango

## Result examples

![image](https://user-images.githubusercontent.com/39027094/181036912-2712bd6c-5ec7-4969-8260-b261391a7485.png)
Author : MaesAntoine

# How to Deploy Your Own Local Server with Seaborn for Grasshopper 3D in 5 minutes

**Requirements**

- Git: Version control is an important tool when working on projects, and Git is one of the most popular and widely-used version control systems. You can download Git [here](https://git-scm.com/downloads).
- Virtual Environment Manager: This guide uses conda, but you can also use miniconda or other virtual environment managers. You can download conda [here](https://docs.conda.io/en/latest/miniconda.html).

### Step by step guide

1. Clone the repository using the following command:

```bash
git clone https://github.com/monsieurpablo/seaborn_grasshopper
```

The command above will download the repository containing the code for the server and its dependencies.

2. Navigate to the repository

```bash
cd seaborn_grasshopper
```

This command will take you inside the repository's folder, where you will be able to access the files and folders required to run the server.

3. Create a virtual environment with `Python 3.9` using `conda`

```bash
conda create --name ghseaborn python=3.9
conda activate ghseaborn
```

Conda allows you to create virtual environments, which are isolated spaces where you can install packages and dependencies without interfering with your system's Python installation. The first command creates an environment named ghseaborn with Python 3.10, and the second command activates the environment so that any packages you install will be installed in that environment.

4. Install the dependencies listed in the requirements file:

```bash
pip install -r requirements.txt
```

This command will install all the packages and dependencies required to run the server, as listed in the requirements.txt file.

5. Install `waitress` as a server handler (Windows only)

```bash
pip install waitress
```

Waitress is a lightweight web server that can be used to run the server. This command installs the waitress package, which is required to run the server on Windows.

6. Start the server

```bash
waitress-serve --threads 6 --listen=*:5000 app:app
```

This command starts the server and makes it available on the localhost at port 5000. The --threads flag specifies the number of threads to use and the --listen flag specifies the IP address and port to listen on.

Now you can connect to the server in grasshopper by using the following url address [`http://127.0.0.1:5000/`](http://127.0.0.1:5000/)

7. Connect to the server in Grasshopper
   Use the the following URL address: http://127.0.0.1:5000/ in the panel asking for the server address.

Congratulations!!!!! You can now connect to the server using the URL address provided and start using Seaborn with Grasshopper 3D.

# Deployment

Follow [this tutorial](https://www.youtube.com/watch?v=SiCAIRc0pEI). The code is already set-up to work with Heroku.
