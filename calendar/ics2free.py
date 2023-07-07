import os
import re
import argparse

def process_ics(input_file, output_directory, detailed_log):
    # Construct the output file name
    output_file = os.path.join(output_directory, os.path.basename(input_file).replace('.ics', '.free.ics'))

    try:
        with open(input_file, 'r') as f:
            lines = f.readlines()

        in_event = False
        add_transp = True
        add_busy_status = True
        new_content = []

        # Iterate over each line in the file
        for line in lines:
            if detailed_log:
                print(f"Processing line: {line.strip()}")

            # Check if we are inside a VEVENT block
            if re.search('BEGIN:VEVENT', line):
                in_event = True
            elif re.search('END:VEVENT', line):
                in_event = False

                # Add TRANSP and BUSYSTATUS properties if they are not already present
                if add_transp:
                    new_content.append('TRANSP:TRANSPARENT\n')
                if add_busy_status:
                    new_content.append('X-MICROSOFT-CDO-BUSYSTATUS:FREE\n')

                # Reset flags for the next VEVENT
                add_transp = True
                add_busy_status = True

            # Check if TRANSP or BUSYSTATUS properties already exist
            if re.search('TRANSP:TRANSPARENT', line):
                add_transp = False
            elif re.search('X-MICROSOFT-CDO-BUSYSTATUS:FREE', line):
                add_busy_status = False

            new_content.append(line)

        # Write new content to the output file
        with open(output_file, 'w') as f:
            f.writelines(new_content)

        if detailed_log:
            print(f"File written to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Create the parser
parser = argparse.ArgumentParser(description="Process an ics file.")

# Add the arguments
parser.add_argument('inputIcsFile', type=str, help='The input ics file')
parser.add_argument('--outputDirectory', type=str, default=os.getcwd(), help='The output directory (default: current directory)')
parser.add_argument('--detailedLog', action='store_true', help='Enable detailed log')

# Parse the arguments
args = parser.parse_args()

# Call the function with parsed arguments
process_ics(args.inputIcsFile, args.outputDirectory, args.detailedLog)
