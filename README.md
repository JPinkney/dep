### Dep - Platform dependent depency installer

### How to use

1. First use either init, run, or reset. Either one of these will create the dependecy.dep file.
2. Add the platform specific dependency under the correct operating system header in the generated dependecy.dep file
    E.g. 
    ```
    OSX
    brew install <package>
    
    Linux
    npm install <package-name> 
    
    Windows
    
    Other
    ```
3. Use the run command to install dependencies for this computer

##### Available commands
init - Initilizes the file for the first time (optional as run with automatically initilze it if you haven't already)
run - Run the platform dependent depencies for the specific platform. Will also create the file if it does not exist
reset - Reset the dependecy.dep or create it if it doesn't exist

### Additional Support
1. If you are getting permission denied then you need to run chmod +x dep.py

### Developer support
1. Clone this repo 
2. All the code currently lives inside of dep.py 
