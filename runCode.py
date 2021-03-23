import subprocess

def execute(filename, ext, lang, code):
    with open(f"{filename}.{ext}", "w") as f:
        f.write(code)
    f.close()

    compileError = ''
    output = ''
    runtimeError = ''

    if lang == "python" or lang == "py":
        process = subprocess.Popen(
            ['python', f'{f.name}'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        stdout, stderr = process.communicate()

        output = stdout
        runtimeError = stderr

        return [compileError, output, runtimeError]

    elif lang == "c":
        process = subprocess.Popen(
            ['gcc', '-o', f'{filename}c', f'{f.name}'],
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        stderr = process.communicate()
        compileError = stderr

        if compileError is None:
            process = subprocess.Popen(
                [f'./{filename}c'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            stdout, stderr = process.communicate()
            
            output = stdout
            runtimeError = stderr
        else:
            pass

        return [compileError[1], output, runtimeError]

    elif lang == "cpp" or lang == "c++":
        process = subprocess.Popen(
            ['g++', '-o', f'{filename}cpp', f'{f.name}'],
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        stderr = process.communicate()
        compileError = stderr

        if compileError is None:
            process = subprocess.Popen(
                [f'./{filename}cpp'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            stdout, stderr = process.communicate()
            
            output = stdout
            runtimeError = stderr
        else:
            pass

        return [compileError[1], output, runtimeError]
