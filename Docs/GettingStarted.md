# Getting Started

Welcome to the SpectraSolis Project! In this Doc we will cover the basics of getting a development environment setup for contributing to the SpectraSolis Project.

## Getting The Code

In order to begin working in your own environment, we need to get the code. We will follow a pretty standard contribution process.

### Prerequisites

1) [Create](https://docs.github.com/en/get-started/start-your-journey/creating-an-account-on-github) a GitHub account
2) Request contribution permissions from Breeze A. with github account in discord.
3) [download git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) and brush up on [usage](https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository) (we will walk through basic usage)


### Forking a repository

To keep things tidy, and afford you the most flexibility in your development, we will be [forking the main Git repository](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) into your own personal repository. This ensures that whatever changes you make to your own code, it does not propagate into the main rpository until you are absolutely certain that it is ready. If you make a mistake in your personal repository, no biggie! The absolute worst case scenario is that you simply have to re-fork the SpectraSolis repo.

To accomplish this, ensure you have completed the [prerequisites](#prerequisites) and follow these steps:

1) navigate to the [SpectraSolis repository](https://github.com/breezeaguilar/HASP-2025)
2) follow the instructions for [forking a Git repository](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo)
3) once finished, you should now see a private fork of the repository in your personal repositories tab

### Cloning

We will now download the code to our local computer. If you are comfortable with the cloning process, just clone your forked repository into the ~/development/ folder. This path is important, as we will be using virtual computers to create a dev environment below, and we need a known path to mount the virtual machine to.

#### Step 1
Open a command terminal on your local machine. On [Windows](https://learn.microsoft.com/en-us/powershell/scripting/windows-powershell/starting-windows-powershell?view=powershell-7.4) you can search for "Windows PowerShell" from the start menu and select the PowerShell option. On [linux](https://ubuntu.com/tutorials/command-line-for-beginners#1-overview#3-opening-a-terminal) you can use the keyboard shortcut: Ctrl-Alt-T. 

#### Step 2
Next paste the following command into the terminal and press enter:

```Shell
git --version
```

You should see a response similar to:

```
git version 2.33.0.windows.2
```
Dont worry too much about the actual git version, so long as the command is recognized by the system, you can continue. If the command throws an error, try following this video tutorial on [installing git](https://www.youtube.com/watch?v=lt9oDAvpG4I), close and reopen the terminal to refresh the PATH variable, and check that the git --version command works.

#### Step 3

copy the following to the command terminal to create a development folder on your machine:

```Shell
mkdir ~/development/ && cd ~/development
```
you should now see that you have created and changed into the development folder.

Windows PowerShell terminal should look similar to:
```PowerShell
PS C:\Users\Username\development>
```
Linux terminal should look like:
```Shell
Username:~/development$
```

#### Step 4

From here, we will clone our development folder. Copy the following command into a text editor:

```Shell
git clone replace/with/your/HASP-2025/fork.git ./HASP-2025
```

Navigate to your personal fork of the HASP-2025 repository, and click on the drop down menu labled "Code". This will bring up a small window with an https link which looks something like: 

```
https://github.com/YourUserName/HASP-2025.git
```
modify the section of the command which says "replace/with/your/HASP-2025/fork.git" with your copied github repo link. 

#### Step 5

Finally, copy your modified command into the terminal and run it. This will clone your forked repo into the folder on your machine: ~/development/HASP-2025.

#### Step 6

We are now ready to start developing!

## Developing

We will be using Docker and VSCode to standardize development environments across the team. This simplifies setup and ensures that each teammember has the same tools at their disposal.

### Prerequisites:

1) [install VSCode](https://code.visualstudio.com/docs/setup/setup-overview)
2) [install docker](https://docs.docker.com/desktop/) for your machine


### Ready, Set, Go! (In development!!!! not complete yet!)

once you have downloaded docker, you're almost ready to start developing!

#### Step 1: Ready
open vscode and click on the Extensions tab on the left hand side. 

Search for the "Dev Containers" extension from microsoft, and install it.

#### Step 2: Set
Now, open a command terminal as above (if on windows ensure you are in PowerShell) and type the following command:

```Shell
code ~/development/HASP-2025
```
this will open up your VSCode ide in the Hasp-2025 folder.

#### Step 3: GO!
Ensure Docker is running by searching for and running the docker desktop application.

return to VSCode and press the command shortcut: CTR+SHIFT+P

search for and select the command "Dev Containers: Reopen in Container"

Select the platform you wish to develop in, either rpi, propeller, or frontend

Wait for the container to spin up, and then you're ready to start working!
