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

            command3 = "cat filtered_endpoints.txt | gf xss >> xss_params.txt"
            subprocess.run(command3, shell=True)

            command4 = "cat xss_params.txt | Gxss -p khXSS -o xss_params_reflected.txt"
            subprocess.run(command4, shell=True)

            command5 = "dalfox file xss_params_reflected.txt -o results.txt"
            if headers:
                headers_list = [header.strip() for header in headers.split(",")]
                for header in headers_list:
                    key, value = header.split(":")
                    command5 += f" -H '{key.strip()}: {value.strip()}'"
            subprocess.run(command5, shell=True)

            with open("airixss_output.txt", "r") as f:
                airixss_output = f.read()
                
            airixss_output = re.sub(r'\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]?', '', airixss_output)
            airixss_output = re.sub(r'Not Vulnerable - .*?\n', '', airixss_output)

            with open("kxss_output.txt", "r") as f:
                kxss_output = f.read()

            if output_format == "txt":
                with open("results.txt", "a") as f:
                    f.write("\nAirixss Results:\n")
                    f.write(airixss_output)
                    f.write("\n")
                    f.write("Kxss Results:\n ")
                    f.write(kxss_output)
            elif output_format == "html":
                with open("results.html", "w") as f:
                    f.write("<html><head><style>")
                    f.write("body { font-family: Arial, sans-serif; }")
                    f.write("h2 { color: #00698f; }")
                    f.write("pre { background-color: #f0f0f0; padding: 10px; border: 1px solid #ddd; }")
                    f.write("</style></head><body>")
                    f.write("<h2>Airixss Results:</h2>")
                    f.write("<pre>")
                    f.write(airixss_output)
                    f.write("</pre>")
                    f.write("<h2>Kxss Results:</h2>")
                    f.write("<pre>")
                    f.write(kxss_output)
                    f.write("</pre>")
                    f.write("<h2>Dalfox Results:</h2>")
                    f.write("<pre>")
                    with open("results.txt", "r") as dalfox_file:
                        dalfox_output = dalfox_file.read()
                    f.write(dalfox_output)
                    f.write("</pre>")
                    f.write("</body></html>")
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

        command3 = "cat filtered_endpoints.txt | gf xss >> xss_params.txt"
        subprocess.run(command3, shell=True)

        command4 = "cat xss_params.txt | Gxss -p khXSS -o xss_params_reflected.txt"
        subprocess.run(command4, shell=True)

        command5 = "dalfox file xss_params_reflected.txt -o results.txt"
        if headers:
            headers_list = [header.strip() for header in headers.split(",")]
            for header in headers_list:
                key, value = header.split(":")
                command5 += f" -H '{key.strip()}: {value.strip()}'"
        subprocess.run(command5, shell=True)

        with open("airixss_output.txt", "r") as f:
            airixss_output = f.read()
            
        airixss_output = re.sub(r'\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]?', '', airixss_output)
        airixss_output = re.sub(r'Not Vulnerable - .*?\n', '', airixss_output)

        with open("kxss_output.txt", "r") as f:
            kxss_output = f.read()

        if output_format == "txt":
            with open("results.txt", "a") as f:
                f.write("\nAirixss Results:\n")
                f.write(airixss_output)
                f.write("\n")
                f.write("Kxss Results:\n")
                f.write(kxss_output)
        elif output_format == "html":
            with open("results.html", "w") as f:
                f.write("<html><head><style>")
                f.write("body { font-family: Arial, sans-serif; }")
                f.write("h2 { color: #00698f; }")
                f.write("pre { background-color: #f0f0f0; padding: 10px; border: 1px solid #ddd; }")
                f.write("</style></head><body>")
                f.write("<h2>Airixss Results:</h2>")
                f.write("<pre>")
                f.write(airixss_output)
                f.write("</pre>")
                f.write("<h2>Kxss Results:</h2>")
                f.write("<pre>")
                f.write(kxss_output)
                f.write("</pre>")
                f.write("<h2>Dalfox Results:</h2>")
                f.write("<pre>")
                with open("results.txt", "r") as dalfox_file:
                    dalfox_output = dalfox_file.read()
                f.write(dalfox_output)
                f.write("</pre>")
                f.write("</body></html>")

def clean_up_files():
    try:
        os.remove("endpoints.txt")
        os.remove("filtered_endpoints.txt")
        os.remove("airixss_output.txt")
        os.remove("kxss_output.txt")
        os.remove("xss_params.txt")
        os.remove("xss_params_reflected.txt")
    except FileNotFoundError:
        pass