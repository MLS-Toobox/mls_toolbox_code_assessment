import os
import subprocess
import json

from .code_assess import CodeAssess

class PyLintTest(CodeAssess):

    def __init__(self, session_id, local_path, **options):
        super().__init__(session_id, local_path)
        self.options = options
        self.my_id = "PyLint"

    def rate_app(self):
        files = os.listdir(self.local_path)
        json_output = {}
        pre_dir = os.getcwd()
        for file in files:
            # check file is folder
            if os.path.isdir(os.path.join(self.local_path, file)):
                current_dir = os.path.join(pre_dir, self.session_id, file)
                try:
                    os.chdir(current_dir)
                    subprocess.check_output(
                        ["pylint", "--recursive", "y", "--output-format", "json2",
                         "--disable", "E0401", "--clear-cache-post-run", "y", '.'])
                except subprocess.CalledProcessError as e:
                    json_output = json.loads(str(e.output, "utf-8"))

        self.result = {
            "score": json_output["statistics"]["score"],
            "message_count": json_output["statistics"]["messageTypeCount"],
            "module_count": json_output["statistics"]["modulesLinted"]
        }
        os.chdir(pre_dir)

    def run_report(self):
        files = os.listdir(self.local_path)
        readable_output = None

        pre_dir = os.getcwd()
        for file in files:
            # check file is folder
            if os.path.isdir(os.path.join(self.local_path, file)):
                current_dir = os.path.join(pre_dir, self.session_id, file)
                try:
                    os.chdir(current_dir)
                    subprocess.check_output(
                        ["pylint", "--recursive", "y", "--score","n", "--reports", "y",
                         "--disable", "E0401", "--clear-cache-post-run", "y", '.'])
                except subprocess.CalledProcessError as e:
                    readable_output = e.output
        self.full_report = readable_output
        os.chdir(pre_dir)
        