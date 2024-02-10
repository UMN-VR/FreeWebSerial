import gzip
import binascii

import gzip
import re
from bs4 import BeautifulSoup

def read_byte_array_from_header(file_path):
    # Read the content of the webserial_webpage.h file
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Use regular expression to find the byte array
    # This pattern assumes the format is exactly as shown, with curly braces and comma-separated values
    match = re.search(r'const uint8_t WEBSERIAL_HTML\[\] PROGMEM = \{([0-9, \n]+)\};', file_content, re.MULTILINE)
    if match:
        # Extract the matched group and remove newlines and spaces
        byte_array_str = match.group(1).replace('\n', '').replace(' ', '')

        # Convert the string to an actual list of integers
        byte_array = [int(byte) for byte in byte_array_str.split(',') if byte != '']
        return byte_array
    else:
        raise ValueError("Byte array not found in the header file")

def decode_webpage(file_path):
    byte_array = read_byte_array_from_header(file_path)

    # Convert the byte array to binary data
    binary_data = bytearray(byte_array)

    # Decompress the binary data
    decompressed_data = gzip.decompress(binary_data)

    soup = BeautifulSoup(decompressed_data, 'html.parser')

    pretty_html = soup.prettify()

    # Write the decompressed data to an HTML file
    with open('webpage.html', 'wb') as f:
        f.write(pretty_html.encode('utf-8'))




# Part 2: Encoding
def encode_webpage():
    # Read the modified HTML file
    with open('webpage_min.html', 'rb') as f:
        html_content = f.read()

    # Compress the HTML content
    compressed_data = gzip.compress(html_content)

    # Convert the compressed data to a byte array
    byte_array = [b for b in compressed_data]

    # Format the byte array for C header
    formatted_array = ','.join([str(b) for b in byte_array])

    # Update the size variable
    size_variable = f"const uint32_t WEBSERIAL_HTML_SIZE = {len(byte_array)};"

    # Prepare the final header content
    header_content = f"""//webserial_webpage.h
            #ifndef _webserial_webpage_h
            #define _webserial_webpage_h

            {size_variable}
            const uint8_t WEBSERIAL_HTML[] PROGMEM = {{
            {formatted_array}
            }};

            #endif
"""

    # Write the header content to a new file
    with open('webserial_webpage_updated.h', 'w') as f:
        f.write(header_content)



# Example usage
header_file_path = 'webserial_webpage.h'
#decode_webpage(header_file_path)
# Run the functions
# Modify the webpage.html as needed before running the encoding part
encode_webpage()
