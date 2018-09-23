import ctypes
import configparser
import os
import subprocess

#Default fifa Paths
defaultFifaExecPath = "C:\\Program Files (x86)\\Origin Games\\FIFA 18\\FIFA18.exe"
defaultFifaConfigPath = "~\\Documents\\FIFA 18\\fifasetup.ini"

# Load or create the settings file, containing the paths of
# the fifa exe file, and fifa config file
config = configparser.ConfigParser()

if not os.path.exists('settings.ini'):

    # Ff the file doesn't exists, create the file, and close the program
    config['settings'] = {
        'fifa_exe_path': defaultFifaExecPath, 
        'fifa_config_path': defaultFifaConfigPath
        }

    config.write(open('settings.ini', 'w'))

    exit()

else:

    # Load paths from the file
    config.read('settings.ini')
    defaultFifaExecPath = config.get('settings', 'fifa_exe_path')
    defaultFifaConfigPath = config.get('settings', 'fifa_config_path')

# Expand path
defaultFifaConfigPathExpanded = os.path.expanduser(defaultFifaConfigPath)

# Get current resolution
user32 = ctypes.windll.user32
resolutionWidth = user32.GetSystemMetrics(0)
resolutionHeight = user32.GetSystemMetrics(1)

# Print infoThe current resolution is
print("The current resolution is", resolutionWidth , " x ", resolutionHeight)
print("The config file path is ", defaultFifaConfigPathExpanded)
print("The exec path is", defaultFifaExecPath)

# Open file, and add dummy section, to avoid errors
with open(defaultFifaConfigPathExpanded, 'r') as f:
    config_string = '[dummy_section]\n' + f.read()
config = configparser.ConfigParser()
config.optionxform = str
config.read_string(config_string)

#Update resolution values
config.set("dummy_section", "RESOLUTIONHEIGHT", str(resolutionHeight))
config.set("dummy_section", "RESOLUTIONWIDTH", str(resolutionWidth))

# Write updated file
with open(defaultFifaConfigPathExpanded, 'w') as f:
    config.write(f)

# remove dummy section
with open(defaultFifaConfigPathExpanded, 'r') as fin:
    data = fin.read().splitlines(True)
with open(defaultFifaConfigPathExpanded, 'w') as fout:
    fout.writelines(data[1:])

# Start fifa exec
print("Starting FIFA18 ...")
subprocess.call([defaultFifaExecPath])

