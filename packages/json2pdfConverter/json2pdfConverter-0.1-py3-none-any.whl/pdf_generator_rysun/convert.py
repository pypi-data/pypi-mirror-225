import pandas as pd
from jinja2 import Environment, FileSystemLoader
import pdfkit
import time
from PyPDF2 import PdfMerger
import math
import os
import winreg
import sys
import subprocess
import json

# Custom enumerate function for Jinja2
def jinja2_enumerate(iterable, start=0):
    return enumerate(iterable, start=start)

def generate(json_file_path, template_directory_path, template_name, output_html_path, output_pdf_path, options, data_variables):
    print('Running PDF generator')
    
    # System path
    # This section of code deals with managing the system environment variable PATH.
    # It first gets the current working directory and appends the subdirectory 'wkhtmltopdf/bin'
    # to the path_to_add variable, which will be added to the PATH variable.

    current_directory = os.getcwd()

    # Specify the path to add to the user environment variables
    path_to_add = os.path.join(current_directory, 'wkhtmltopdf', 'bin')

    try:
        # Open the registry key for user environment variables
        # Here, the code accesses the Windows registry to open the 'Environment' key,
        # which stores user environment variables. It uses the HKEY_CURRENT_USER constant
        # to specify that the key is located under the current user's hive.
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment', 0, winreg.KEY_ALL_ACCESS)

        # Get the current value of the PATH variable from the registry
        # The code retrieves the current value of the PATH variable stored in the registry
        # and stores it in the path_value variable.
        path_value, _ = winreg.QueryValueEx(key, 'PATH')

        # Split the PATH value by the appropriate separator (semicolon on Windows, colon on Unix-like systems)
        # The PATH variable is a colon-separated string of directories on Unix-like systems (e.g., Linux, macOS)
        # and a semicolon-separated string on Windows. This code checks the OS type using os.name and
        # splits the path_value accordingly, storing the individual directories in the path_list list.

        path_list = path_value.split(';') if os.name == 'nt' else path_value.split(':')

        # Check if the path already exists in the PATH variable
        # The code checks if the path_to_add already exists in the path_list.
        # If it does, it means the path has already been added to the PATH variable,
        # and it prints a message indicating that it is already included.

        if path_to_add in path_list:
            print("The path is already included in the user environment variables.")
        else:
            # Append the new path to the existing value (separated by a semicolon)
            # If the path_to_add is not present in path_list, it means the path is not yet included
            # in the PATH variable. In that case, the code creates a new_path_value by appending
            # path_to_add to the existing path_value, separated by a semicolon (on Windows).
            # This new_path_value will be used to update the PATH variable.

            new_path_value = f'{path_value};{path_to_add}'

            # Update the PATH value in the registry
            # The code updates the PATH variable in the Windows registry using the winreg.SetValueEx function.
            # It sets the new_path_value as the value for the 'PATH' key in the 'Environment' key.

            winreg.SetValueEx(key, 'PATH', 0, winreg.REG_EXPAND_SZ, new_path_value)

            # Print a message indicating that the path has been added to the user environment variables.
            print("The path has been added to the user environment variables.")

            # Update the PATH variable in the current process
            # After updating the PATH in the registry, the code also updates the PATH variable
            # in the current Python process using os.environ['PATH'] to ensure that the updated PATH
            # is immediately available for the current script.

            os.environ['PATH'] = new_path_value

            # Start a new process using the current Python executable
            # To apply the changes immediately, the code starts a new process using subprocess.Popen
            # with the current Python executable (sys.executable) and the command-line arguments (sys.argv).
            # This will create a new process with the updated environment variables.

            subprocess.Popen([sys.executable] + sys.argv)

        # Close the registry key
        # Finally, the code closes the registry key using winreg.CloseKey.

        winreg.CloseKey(key)

    except Exception as e:
        # Exception handling
        # If any error occurs during the process, it will be caught in this block,
        # and the code will print an error message along with the specific error.
        print(f"An error occurred: {str(e)}")       
        
    # Rest of the code...

    # wkhtmltopdf configuration required for pdfkit
    # This section of code sets up the path to the wkhtmltopdf executable, which is required for pdfkit to work.
    # pdfkit is a Python library that converts HTML or URL to PDF using various backends, including wkhtmltopdf.

    # The variable wkhtmltopdf_path is created by joining the current_directory with the subdirectory 'wkhtmltopdf/bin'
    # and the filename 'wkhtmltopdf.exe' (assuming this script runs on Windows, where the extension '.exe' is used for executables).
    # This forms the complete path to the wkhtmltopdf executable, which will be used by pdfkit to convert HTML to PDF.
    
    wkhtmltopdf_path = os.path.join(current_directory, 'wkhtmltopdf', 'bin', 'wkhtmltopdf.exe')

    # Build the full path to the HTML template file by joining the template directory path and the template name
    template_path = os.path.join(template_directory_path, template_name)

    # Create a Jinja2 environment and load the specified HTML template using the FileSystemLoader
    env = Environment(loader=FileSystemLoader(template_directory_path))
    
    # Register the custom enumerate function with the environment
    env.filters['enumerate'] = jinja2_enumerate
        

    # Get the Jinja2 template object corresponding to the specified template file
    template = env.get_template(os.path.basename(template_path))

    # Render the HTML content using the loaded template and the dynamic data from data_variables
    html_content = template.render(**data_variables)

    # Create the full path to the output HTML file
    output_html_path = os.path.join(output_html_path, 'output.html')

    # Open the output HTML file and write the rendered HTML content into it
    with open(output_html_path, 'w', encoding='utf-8') as file:
        file.write(html_content)

    # Print a message confirming the creation of the output HTML file
    print(f'HTML file created: {output_html_path}')

    # Rest of the code...
    # This is where the remaining code for PDF creation is expected to be.

    # Calculate the start time for PDF creation
    start_time = time.time()
    print("PDF Creation Started")

    # Calculate the total number of lines in the HTML content
    # Split the HTML content into lines and count the total number of lines
    total_lines = len(html_content.split('\n'))
    print(f'Total lines: {total_lines}')

    # Define the number of lines per chunk
    # Adjust the number of lines per chunk as needed for processing
    lines_per_chunk = total_lines  # Adjust this value as per your requirement

    # Calculate the number of chunks based on the lines per chunk
    # Calculate the total number of chunks needed for PDF generation
    total_chunks = math.ceil(total_lines / lines_per_chunk)
    print(f'Total chunks: {total_chunks}')

    # Generate PDF for each chunk
    # At this point, the code is expected to loop through each chunk of HTML content
    # and generate separate PDF files for each chunk using the remaining logic.
    
    # Array to store the paths of generated PDF files
    pdf_files = []

    # Iterate through each chunk of HTML content for PDF generation
    for i in range(total_chunks):
        # Calculate the starting and ending line numbers for the current chunk
        start_line = i * lines_per_chunk + 1
        end_line = min((i + 1) * lines_per_chunk, total_lines)

        # Extract the chunk of HTML content for the current PDF chunk
        chunk = html_content.split('\n')[start_line - 1:end_line]
        chunk_html = '\n'.join(chunk)
        
        # Specify the directory to save the PDF files and create it if it doesn't exist
        output_pdf_directory = os.path.join(output_pdf_path, 'pdf')
        os.makedirs(output_pdf_directory, exist_ok=True)

        # Specify the path for the current chunk's PDF file
        pdf_file = os.path.join(output_pdf_directory, f'output_{i}.pdf')

        # Convert the HTML chunk to a PDF file with the specified options
        pdfkit.from_string(chunk_html, pdf_file, options=options, configuration=pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path))

        # Append the path of the generated PDF file to the list
        pdf_files.append(pdf_file)


    # Merge the individual PDF files into a single PDF
    merger = PdfMerger()

    # Iterate through each individual PDF file and append it to the merger
    for pdf_file in pdf_files:
        merger.append(pdf_file)

    # Specify the path for the merged PDF file
    merged_pdf_file = os.path.join(output_pdf_directory, 'merged_output.pdf')

    # Write the merged PDF to the specified path
    merger.write(merged_pdf_file)

    # Close the merger
    merger.close()

    # Calculate the elapsed time for PDF creation
    elapsed_time = time.time() - start_time

    # Print the path of the merged PDF file and the time taken for creation
    print(f'Merged PDF file created: {merged_pdf_file}')
    print(f'PDF creation time: {elapsed_time / 60:.2f} minutes')

    # Optional: Delete the individual PDF files to save space
    for pdf_file in pdf_files:
        os.remove(pdf_file)


