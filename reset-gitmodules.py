import subprocess

'''
Sorry, no error checking. Assuming we have a valid .gitmodules file.
'''

submodules = []
out, err = subprocess.Popen("git config -f .gitmodules --get-regexp '^submodule\..*\.(path|url)$'", shell=True, stdout=subprocess.PIPE).communicate() 
out = out.splitlines()

urls = out[1::2]
paths = out[::2]

# build the array of {url, path} hashes
for idx, val in enumerate(urls):
    url = val.split()[1]
    path = paths[idx].split()[1]
    submodules.append({
      "url": url,
      "path": path
    })

# rm, add and sync gitmodules
for submodule in submodules:
    rmCall = "git rm --cached %(path)s" % submodule
    addCall = "git submodule add --force %(url)s %(path)s" % submodule
    subprocess.call(rmCall, shell=True)
    subprocess.call(addCall, shell=True)

subprocess.call("git submodule sync", shell=True)
