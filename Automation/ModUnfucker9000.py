from pathlib import Path
import platform
import requests as http
from shutil import rmtree
import sys


# This script intended to automate the super annoying full reset process:
# 01. Open drg.mod.io in a web browser and unsubscribe from all mods.
# 02. Run DRG and they should all uninstall.
# 03. Repeat if any mods exist (as possible).
# 04. Close DRG and delete the following folders: C:\Users\Public\mod.io\2475 and C:\Users\__KARL__\AppData\Local\mod.io
# 05. Run DRG and begin installing mods with modio as normal.

args = list(sys.argv)
num = len(args)
pause = ''

if num != 2 and num != 4 and num != 5:
    readme = """
    To use this script, you'll need to go to https://mod.io/oauth and generate an Access Token. Enter the token as the 
    first argument of this script. If you've manually selected where mod.io installs mods, if you use Linux for some 
    reason, or if the script fails for some other reason, enter the public folder and the user folder for mod.io as the
    optional second and third arguments, respectively, for the script. Add the -y flag as an optional fourth argument to 
    skip verification that the file folders are affiliated with mod.io. In general, you can omit these and it'll use the 
    default values (on Windows, C:\\Users\\Public\\mod.io\\2475 and C:\\Users\\__Karl__\\AppData\\Local\\mod.io\\2475).
    
    WARNING: Entering something stupid could delete far, far more than you want. DON'T BE STUPID. If you enter 
    "ModUnfucker9000.py [token] C:\\ D:\\ -y" don't get mad at me when you find your way back on the internet.  
    """
    raise Exception(readme)


token = args[1]

headers = {
  'Authorization': f'Bearer {token}',
  'Accept': 'application/json'}

plat = platform.system()

# I did this part this way because it was funny to see a friend react to it
# Please don't write case statements like this ffs
# args.extend(['foo', 'bar'])
args.extend(['woof', 'bark', 'doge'])  # the foo/bar paradigm is overrated
pub = Path(args[2]) if num > 2 else Path(r'C:\Users\Public\mod.io\2475') if plat == 'Windows'\
    else Path(r'~/.local/share/Steam/steamapps/compatdata/548430/pfx/drive_c/users/Public/mod.io/2475')
user = Path(args[3]) if num > 2 else Path.home() / r'AppData\Local\mod.io\2475' if plat == 'Windows' \
    else Path(r'~/.local/share/Steam/steamapps/compatdata/548430/pfx/drive_c/users/steamuser/AppData/Local/mod.io/2475')

if args[4].lower() != '-y':
    print(pub.parts)
    assert 'mod.io' in pub.parts
    assert '2475' in pub.parts
    assert 'mod.io' in user.parts
    assert '2475' in user.parts

mods = [mod['id'] for mod in http.get('https://api.mod.io/v1/me/subscribed', params={}, headers=headers).json()['data']]
headers['Content-Type'] = 'application/x-www-form-urlencoded'

with open('modlist.txt', mode='w') as modfile:
    print(mods, file=modfile)

print('UNSUBSCRIBING...')
for mod in mods:
    http.delete(f'https://api.mod.io/v1/games/2475/mods/{mod}/subscribe', params={}, headers=headers)

while 'y' not in pause.lower():
    print('Run DRG and navigate to the "Modding" tab in the menu.')
    print(
        'If you see any mods listed, select "Manage Mods", unsubscribe from anything still there, then close the game.')
    pause = input('Type yessir to confirm.')

print('RE-SUBSCRIBING (STEP 1)')
pause = ''

rmtree(pub)
rmtree(user)

while 'y' not in pause.lower():
    print('Run DRG and navigate to the "Modding" tab in the menu, then close the game.')
    pause = input('Type yessir to confirm.')

print('RE-SUBSCRIBING (STEP 2)')

for mod in mods:
    http.post(f'https://api.mod.io/v1/games/2475/mods/{mod}/subscribe', params={}, headers=headers)

_ = input('HURRAY WE DID IT')
