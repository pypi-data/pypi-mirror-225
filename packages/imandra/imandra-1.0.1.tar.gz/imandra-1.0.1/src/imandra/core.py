import os
import shutil
import urllib.request
import tempfile

def install(auth):
    if os.name == 'nt':
        print("Imandra Core cannot be installed on native Windows.\n\nPlease install the Imandra CLI on Windows Subsystem for Linux (WSL), and re-run this command there.")
        exit(1)

    with urllib.request.urlopen('https://storage.googleapis.com/imandra-installer/install.sh') as fi:
        (fd, path) = tempfile.mkstemp()
        with os.fdopen(fd, 'w') as fo:
            fo.write(fi.read().decode('utf-8'))

    os.execvp('sh', ['sh'] + [path])

def run_repl(auth, args):
    if shutil.which(auth.imandra_repl):
        os.execvp(auth.imandra_repl, [auth.imandra_repl] + args)
    else:
        print("imandra-repl is not installed. Run: 'imandra core install' to install it.")
