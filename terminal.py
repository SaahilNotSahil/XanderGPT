import subprocess

def run(comm):
    commandAndArguments = comm.split()

    process = subprocess.Popen(
        commandAndArguments, 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        universal_newlines=True
    )

    stdout, stderr = process.communicate()

    output = stdout
    error = stderr

    return [output, error]
