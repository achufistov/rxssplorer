import subprocess
import os
import re

def remove_duplicates():
    command = "cat endpoints.txt | uro >> filtered_endpoints.txt"
    subprocess.run(command, shell=True)

def crawl_endpoints(host, tool):
    if tool == "waybackurls":
        command = f"echo https://{host} | waybackurls"
    elif tool == "hakrawler":
        command = f"echo https://{host} | hakrawler"
    elif tool == "gau":
        command = f"echo https://{host} | gau --threads 5"
    elif tool == "katana":
        command = f"echo https://{host} | katana -jc"
    subprocess.run(command, shell=True, stdout=open("endpoints.txt", "a"))

def test_endpoints(payload, payload_file=None, output_format="txt", headers="", file=None):
    if payload_file:
        with open(payload_file, "r") as f:
            payloads = [line.strip() for line in f.readlines()]
        airixss_results = []
        kxss_results = []
        for payload in payloads:
            command1 = f"cat filtered_endpoints.txt | qsreplace '{payload}' | airixss -payload '{payload}'"
            if headers:
                headers_list = [header.strip() for header in headers.split(",")]
                for header in headers_list:
                    key, value = header.split(":")
                    command1 += f" -H '{key.strip()}: {value.strip()}'"
            subprocess.run(command1, shell=True, stdout=open("airixss_output.txt", "w"))

            command2 = f"cat filtered_endpoints.txt | qsreplace '{payload}' | kxss"
            subprocess.run(command2, shell=True, stdout=open("kxss_output.txt", "w"))

            with open("airixss_output.txt", "r") as f:
                airixss_output = f.read()
                
            airixss_output = re.sub(r'\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]?', '', airixss_output)
            airixss_output = re.sub(r'Not Vulnerable - .*?\n', '', airixss_output)

            with open("kxss_output.txt", "r") as f:
                kxss_output = f.read()

            airixss_results.append(airixss_output)
            kxss_results.append(kxss_output)

        if output_format == "txt":
            with file as f:
                f.write("\nAirixss Results:\n")
                for result in airixss_results:
                    f.write(result)
                    f.write("\n")
                f.write("Kxss Results:\n")
                for result in kxss_results:
                    f.write(result)
                    f.write("\n")
        elif output_format == "html":
            with file as f:
                f.write("<!DOCTYPE html>\n")
                f.write("<html>\n")
                f.write("  <head>\n")
                f.write("    <style>\n")
                f.write("      body { font-family: Arial, sans-serif; background-color: #f9f9f9; }\n")
                f.write("      h2 { color: #ff0000; }\n")
                f.write("      ul { list-style: none; padding: 0; margin: 0; }\n")
                f.write("      li { padding: 10px; border-bottom: 1px solid #ccc; }\n")
                f.write("      li:last-child { border-bottom: none; }\n")
                f.write("      .success { color: #2ecc71; }\n")
                f.write("      .error { color: #e74c3c; }\n")
                f.write("    </style>\n")
                f.write("  </head>\n")
                f.write("  <body>\n")

                if payload_file:
                    f.write("    <h2>Airixss Results:</h2>\n")
                    f.write("    <ul>\n")
                    for result in airixss_results:
                        for line in result.split('\n'):
                            if line:
                                if "Vulnerable" in line:
                                    f.write(f"      <li class='success'>{line}</li>\n")
                                else:
                                    f.write(f"      <li>{line}</li>\n")
                    f.write("    </ul>\n")
                    f.write("    <h2>Kxss Results:</h2>\n")
                    f.write("    <ul>\n")
                    for result in kxss_results:
                        for line in result.split('\n'):
                            if line:
                                if "Vulnerable" in line:
                                    f.write(f"      <li class='success'>{line}</li>\n")
                                else:
                                    f.write(f"      <li>{line}</li>\n")
                    f.write("    </ul>\n")
                else:
                    f.write("    <h2>Airixss Results:</h2>\n")
                    f.write("    <ul>\n")
                    for line in airixss_output.split('\n'):
                        if line:
                            if "Vulnerable" in line:
                                f.write(f"      <li class='success'>{line}</li>\n")
                            else:
                                f.write(f"      <li>{line}</li>\n")
                    f.write("    </ul>\n")
                    f.write("    <h2>Kxss Results:</h2>\n")
                    f.write("    <ul>\n")
                    for line in kxss_output.split('\n'):
                        if line:
                            if "Vulnerable" in line:
                                f.write(f"      <li class='success'>{line}</li>\n")
                            else:
                                f.write(f"      <li>{line}</li>\n")
                    f.write("    </ul>\n")

                f.write("  </body>\n")
                f.write("</html>\n")
    else:
        command1 = f"cat filtered_endpoints.txt | qsreplace '{payload}' | airixss -payload '{payload}'"
        if headers:
            headers_list = [header.strip() for header in headers.split(",")]
            for header in headers_list:
                key, value = header.split(":")
                command1 += f" -H '{key.strip()}: {value.strip()}'"
        subprocess.run(command1, shell=True, stdout=open("airixss_output.txt", "w"))

        command2 = f"cat filtered_endpoints.txt | qsreplace '{payload}' | kxss"
        subprocess.run(command2, shell=True, stdout=open("kxss_output.txt", "w"))

        with open("airixss_output.txt", "r") as f:
            airixss_output = f.read()
            
        airixss_output = re.sub(r'\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]?', '', airixss_output)
        airixss_output = re.sub(r'Not Vulnerable - .*?\n', '', airixss_output)

        with open("kxss_output.txt", "r") as f:
            kxss_output = f.read()

        if output_format == "txt":
            with file as f:
                f.write("\nAirixss Results:\n")
                f.write(airixss_output)
                f.write("\n")
                f.write("Kxss Results:\n")
                f.write(kxss_output)
                f.write("\n")
        elif output_format == "html":
            with file as f:
                f.write("<!DOCTYPE html>\n")
                f.write("<html>\n")
                f.write("  <head>\n")
                f.write("    <style>\n")
                f.write("      body { font-family: Arial, sans-serif; background-color: #f9f9f9; }\n")
                f.write("      h2 { color: #ff0000; }\n")
                f.write("      ul { list-style: none; padding: 0; margin: 0; }\n")
                f.write("      li { padding: 10px; border-bottom: 1px solid #ccc; }\n")
                f.write("      li:last-child { border-bottom: none; }\n")
                f.write("      .success { color: #2ecc71; }\n")
                f.write("      .error { color: #e74c3c; }\n")
                f.write("    </style>\n")
                f.write("  </head>\n")
                f.write("  <body>\n")

                if payload_file:
                    f.write("    <h2>Airixss Results:</h2>\n")
                    f.write("    <ul>\n")
                    for result in airixss_results:
                        for line in result.split('\n'):
                            if line:
                                if "Vulnerable" in line:
                                    f.write(f"      <li class='success'>{line}</li>\n")
                                else:
                                    f.write(f"      <li>{line}</li>\n")
                    f.write("    </ul>\n")
                    f.write("    <h2>Kxss Results:</h2>\n")
                    f.write("    <ul>\n")
                    for result in kxss_results:
                        for line in result.split('\n'):
                            if line:
                                if "Vulnerable" in line:
                                    f.write(f"      <li class='success'>{line}</li>\n")
                                else:
                                    f.write(f"      <li>{line}</li>\n")
                    f.write("    </ul>\n")
                else:
                    f.write("    <h2>Airixss Results:</h2>\n")
                    f.write("    <ul>\n")
                    for line in airixss_output.split('\n'):
                        if line:
                            if "Vulnerable" in line:
                                f.write(f"      <li class='success'>{line}</li>\n")
                            else:
                                f.write(f"      <li>{line}</li>\n")
                    f.write("    </ul>\n")
                    f.write("    <h2>Kxss Results:</h2>\n")
                    f.write("    <ul>\n")
                    for line in kxss_output.split('\n'):
                        if line:
                            if "Vulnerable" in line:
                                f.write(f"      <li class='success'>{line}</li>\n")
                            else:
                                f.write(f"      <li>{line}</li>\n")
                    f.write("    </ul>\n")

                f.write("  </body>\n")
                f.write("</html>\n")

def clean_up_files():
    files_to_delete = ["endpoints.txt", "filtered_endpoints.txt", "airixss_output.txt", "kxss_output.txt"]
    for file in files_to_delete:
        if os.path.exists(file):
            os.remove(file)