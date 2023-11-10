from flask import Flask, render_template, request
import subprocess
import zipfile
import os
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compile', methods=['POST'])
def compile_code():
    code = request.files['code']
    testcase = request.files['testcase']
    code.save('main.cpp')
    testcase.save('testcases.zip')

    with zipfile.ZipFile('testcases.zip', 'r') as zip_ref:
        zip_ref.extractall('testcase')

    input_files = sorted([f for f in os.listdir('testcase') if f.startswith('input')])
    output_files = sorted([f for f in os.listdir('testcase') if f.startswith('output')])

    execution_times = {}  

    for input_file, output_file in zip(input_files, output_files):
        input_path = os.path.join('testcase', input_file)
        output_path = os.path.join('testcase', output_file)

        with open(input_path, 'r') as f:
            input_data = f.read().strip()

        with open(output_path, 'r') as f:
            expected_output = f.read().strip()

        start_time = time.time()  

        program_output = subprocess.getoutput(f'./program < {input_path}').strip()

        end_time = time.time()  
        execution_time = end_time - start_time

        if program_output == expected_output:
            execution_times[input_file] = {
                'execution_time': execution_time,
                'status': 'Passed'
            }
        else:
            execution_times[input_file] = {
                'execution_time': execution_time,
                'status': 'Failed'
            }

    return render_template('result.html', execution_times=execution_times)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6776)