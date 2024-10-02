import argparse
import os
import subprocess
import re
from termcolor import colored
from markupsafe import escape
from utils import *

def print_banner():
    banner = """

                                                                                          
    _/      _/    _/_/_/    _/_/_/            _/                                          
     _/  _/    _/        _/        _/_/_/    _/    _/_/    _/  _/_/    _/_/    _/  _/_/   
      _/        _/_/      _/_/    _/    _/  _/  _/    _/  _/_/      _/_/_/_/  _/_/        
   _/  _/          _/        _/  _/    _/  _/  _/    _/  _/        _/        _/           
_/      _/  _/_/_/    _/_/_/    _/_/_/    _/    _/_/    _/          _/_/_/  _/    
                               _/
                              _/

                      _/       _//          _/                                            
 _/      _/        _/_/      _// _/      _/  _/                                           
_/      _/          _/      _/  _/      _/  _/                                            
 _/  _/            _/      _/  _/      _/  _/                                             
  _/    _/        _/  _/    _/    _/    _/                                                
                                                                                          
                                                                                          
                                                           
A Web Application Reflected XSS Scanner
"""
    print(colored(banner, "green", attrs=["bold"]))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="URL to scan", required=False)
    parser.add_argument("-uf", "--urls-file", help="File containing URLs to scan", required=False)
    parser.add_argument("-p", "--payload", help="Payload to use", required=False)
    parser.add_argument("-pf", "--payloads-file", help="File containing payloads to use", required=False)
    parser.add_argument("-o", "--output", help="Output format (txt/html)", choices=["txt", "html"], required=False, default="txt")
    parser.add_argument("-H", "--headers", help="HTTP headers to pass to airixss (e.g., 'header1: value1,header2: value2')", required=False, default="")
    args = parser.parse_args()

    print_banner()

    if args.url:
        hosts = [args.url]
    elif args.urls_file:
        if os.path.isfile(args.urls_file):
            with open(args.urls_file, "r") as f:
                hosts = [line.strip() for line in f.readlines()]
        else:
            print(colored("\nInvalid file path. Please try again.", "red", attrs=["bold"]))
            return
    else:
        print(colored("\nPlease specify a URL or a file containing URLs to scan.", "red", attrs=["bold"]))
        return

    if args.payload:
        payloads = [args.payload]
    elif args.payloads_file:
        if os.path.isfile(args.payloads_file):
            with open(args.payloads_file, "r") as f:
                payloads = [line.strip() for line in f.readlines()]
        else:
            print(colored("\nInvalid file path. Please try again.", "red", attrs=["bold"]))
            return
    else:
        print(colored("\nPlease specify a payload or a file containing payloads to use.", "red", attrs=["bold"]))
        return

    for host in hosts:
        print(colored(f"\nCrawling endpoints for {colored(host, 'light_yellow', attrs=['bold'])}...", "blue", attrs=["bold"]))
        try:
            crawl_endpoints(host, "waybackurls")
            crawl_endpoints(host, "hakrawler")
            crawl_endpoints(host, "gau")
            crawl_endpoints(host, "katana")
        except Exception as e:
            print(colored(f"\nError crawling endpoints for {host}: {str(e)}", "red", attrs=["bold"]))
            continue
        print()

    try:
        remove_duplicates()
    except Exception as e:
        print(colored(f"\nError removing duplicates: {str(e)}", "red", attrs=["bold"]))

    for payload in payloads:
        print(colored(f"\nTesting gathered endpoints using this payload: {colored(payload, 'light_yellow', attrs=['bold'])}", "blue", attrs=["bold"]))
        try:
            with open(f"results.{args.output}", "a") as f:
                if args.output == "html":
                    f.write(f"<h1>Results for {escape(payload)}:</h1>\n")
                else:
                    f.write(f"Results for {escape(payload)}:\n")
                test_endpoints(payload, args.payloads_file, output_format=args.output, headers=args.headers, file=f)
        except Exception as e:
            print(colored(f"\nError testing endpoints: {str(e)}", "red", attrs=["bold"]))

    try:
        clean_up_files()
    except Exception as e:
        print (colored(f"\nError cleaning up files: {str(e)}", "red", attrs=["bold"]))

    print(colored(f"\nThe work is over. You can get acquainted with all vulnerable endpoints here: results.{args.output}", "green", attrs=["bold"]))

if __name__ == "__main__":
    main()