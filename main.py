import sys
from PIL import Image
import argparse
import os

# Braille Unicode blocks start at 0x2800
BRAILLE_BASE = 0x2800

# Braille dots: 1 4
#               2 5
#               3 6
#               7 8
BRAILLE_DOTS = [
    (0, 0),  # dot 1
    (0, 1),  # dot 2
    (0, 2),  # dot 3
    (1, 0),  # dot 4
    (1, 1),  # dot 5
    (1, 2),  # dot 6
    (0, 3),  # dot 7
    (1, 3)   # dot 8
]
OUTPUT_IMAGES_DIRECTORY : str = "output_images"


def img_to_braille_ascii(file_path, width=38, height=14, include_newline=False):
    """
    Convert an image to Braille ASCII art of specified width and height.
    Uses a single dot braille (0x2800) for empty space.
    The output is a single, continuous string (no newline characters).
    """
    # Braille cell: 2x4 pixels each
    cell_w, cell_h = 2, 4
    img_w, img_h = width * cell_w, height * cell_h

    # Open and convert image to grayscale
    img = Image.open(file_path)
    img = img.convert('L')
    img = img.resize((img_w, img_h), Image.BILINEAR)

    # Threshold for dot on/off
    threshold = 127

    braille_lines = []
    for y in range(0, img_h, cell_h):
        line = ""
        for x in range(0, img_w, cell_w):
            dots = 0
            for idx, (dx, dy) in enumerate(BRAILLE_DOTS):
                px = x + dx
                py = y + dy
                if px < img_w and py < img_h:
                    val = img.getpixel((px, py))
                    if val < threshold:
                        dots |= (1 << idx)
            braille_char = chr(BRAILLE_BASE + dots)
            line += braille_char
        braille_lines.append(line)
        

    if include_newline == True:
        return "\n".join(braille_lines)
    else:    
        # --- MODIFIED PART ---
        # The original code used "\n".join(braille_lines)
        # This change joins the lines with an empty string ("") instead of "\n"
        return "".join(braille_lines)




Parser : argparse.ArgumentParser
OPTIONS : dict= {
    "include_newline" : "include_newline" 
#   "option_name" : "cli_parameter_namespace_name"
}
'''
CLI AND RUNNING THE PROGRAM FUNCTIONS BELOW
'''
def Parse_CLI_Arguments() -> tuple[argparse.Namespace, list[str]]:
    '''
    Creates an argument parser to handle the CLI side of this program

    Returns a tuple with:
     - Namespace object which contains all the arguments specified by the parser, and their values from running the command. 
         (Namespace object can be converted into a dictionary with vars(obj)) 
     - List of strings which are arguments not specified by the parser
    '''

## Create argument parser
    global Parser
    Parser = argparse.ArgumentParser(description='The command accepts a file path with -f, or a directory path with -d', exit_on_error=False)
    
## Create mutually exclusive group for -f and -d flags
    # Only one of these flags can be present as input to the command. 
    group = Parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-f', '--file', metavar='PATH', 
                      help='Convvert .png or .jpg image at the specified path')
    group.add_argument('-d', '--directory', metavar='PATH',
                      help='Convert images inside a directory at the specified path')
    
## Create option to newline to be included in the output (Not compatible with Minecraft 1.21.10 for some reason)
    Parser.add_argument('-n', "--include_newline", action="store_true",
                        help='Generates the image with newline character included. (Not compatible with Minecraft 1.21.10)')

    ## Parse arguments
    args = Parser.parse_known_args()
    return args
    


def Get_File_Paths_From_Arguments(known_args: argparse.Namespace, unknown_args: list[str]) -> list:
    '''
    Takes in arguments contained in CLI Arguments Namespace object as input 
    (from Parse_CLI_Arguments())

    Returns a list of image file paths to be converted into ascii art
    '''
    args = known_args
    
    ## If the -f (file) flag is specified 
    if args.file:
        file_path = args.file 
        # print(f"File mode selected: {file_path}") #DEBUG
        
        # Validate that the path exists and is a file
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' does not exist", file=sys.stderr)
            sys.exit(1)
        if not os.path.isfile(file_path):
            print(f"Error: '{file_path}' is not a file", file=sys.stderr)
            sys.exit(1)
        # Return the path of the file specified
        return [args.file]

    ## If the -d (directory) flag is specified 
    elif args.directory:
        dir_path = args.directory
        # print(f"Directory mode selected: {dir_path}") #DEBUG
        
        # Validate that the path exists and is a directory
        if not os.path.exists(dir_path):
            print(f"Error: Directory '{dir_path}' does not exist", file=sys.stderr)
            sys.exit(1)
        if not os.path.isdir(dir_path):
            print(f"Error: '{dir_path}' is not a directory", file=sys.stderr)
            sys.exit(1)
            
        # Return paths of the files inside the directory specified
        # print(f"Processing directory: {os.listdir(dir_path)}") #DEBUG
        directory_files = os.listdir(dir_path)
        temp = []
        for file in directory_files:
            temp.append(os.path.join(dir_path, file))
        return (temp)
    
    ## If neither flag was specfied, see if there is a raw file path provided in the unknown arguments list of strings
    else:

        input_determined_invalid = False
        invalid_input_message_response : list[str]= ["\n"]
        file_path = ""
        
        # Check if there is any valid input at all
        if len(unknown_args) < 1:
            input_determined_invalid = True
            invalid_input_message_response.append("Error: No input provided")
        
        # Only try first argument from the list
            # Assume it is a file path
        else:
            file_path = unknown_args[0]

            # Validate that the path exists and is a file
            if not os.path.exists(file_path):
                invalid_input_message_response.append(f"Error: File '{file_path}' does not exist")
            if not os.path.isfile(file_path):
                invalid_input_message_response.append(f"Error: '{file_path}' is not a file")
                input_determined_invalid = True
                

        # Scenario where user failed to provide any file paths or correctly supply any CLI arguments. 
            # Direct user to CLU arguments for guidance. 
        if input_determined_invalid:
            Parser.print_help()

            invalid_input_message_response.append("Error: Please provide a command line argument (-f, -d) or a valid file path")
            for error_message in invalid_input_message_response:
                print(error_message, file=sys.stderr)
            sys.exit(1)
        

        # Found a valid file path
        else:
            return [file_path]

           


def Get_Options_From_Arguments(args: argparse.Namespace) -> dict:
    '''
    Takes in arguments contained in CLI Arguments Namespace object as input 
    (from Parse_CLI_Arguments())

    Returns a dictionary of known options updated input CLI arguments
    '''
    if args:
        args_dict = vars(args)
    else:
        return dict()
    options_dict = dict()

    for option_name in OPTIONS.keys():
        option_value: any
        try: 
            option_value = args_dict[option_name]
        except:
            print(f"Option name: {option_name} is not inside args_dict. This means there is no CLI Argument with that name defined in the argument parser. Check Parse_CLI_Arguments() for argument definitions")
            raise Exception
        
        else:
        # Parse / Santize argument input before adding it to the options dictionary. 
            options_dict[option_name] = args_dict[option_name]

    return options_dict




#MAIN FUNCTION 
if __name__ == "__main__":

## Parse in CLI Arguments 
    parsed_arguments: argparse.Namespace = Parse_CLI_Arguments()[0]
    unknown_extra_arguments: list[str] = Parse_CLI_Arguments()[1] #additional arguments from the command that don't match up with pre-defined argument parser. 
    # print(vars(parsed_arguments)) #DEBUG

## Collect any program parameter options
    options : dict = Get_Options_From_Arguments(parsed_arguments)

##Collect image file paths
    file_paths = Get_File_Paths_From_Arguments(parsed_arguments, unknown_extra_arguments)
    # print(file_paths)    #DEBUG
    # Convert image files
    os.makedirs(OUTPUT_IMAGES_DIRECTORY, exist_ok=True)
    for file in file_paths:
        if (file.endswith(".png")) or (file.endswith(".jpg")): #Only convert the file if it is an image
            
            art = img_to_braille_ascii(file, include_newline=options["include_newline"]) #convert image
            
            output_image_path = OUTPUT_IMAGES_DIRECTORY + "/" + file.split("\\")[-1] + ".txt"
            with open(output_image_path, 'w', encoding='utf-8') as f:
                print(f"Created ascii file: {output_image_path}")
                f.write(art) #write ascii to .txt file



# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("Usage: python braille_ascii_art.py <input_image> [output.txt]")
#         sys.exit(1)
        
#     input_img = sys.argv[1]
#     art = img_to_braille_ascii(input_img)
    
#     if len(sys.argv) > 2:
#         output_file = sys.argv[2]
#         try:
#             with open(output_file, 'w', encoding='utf-8') as f:
#                 f.write(art)
#             print(f"Created single-line ascii file: {output_file}")
#         except IOError as e:
#              print(f"Error writing to file {output_file}: {e}", file=sys.stderr)
#              sys.exit(1)
#     else:
#         # Note: If printed to console, it may wrap based on your terminal window size.
#         print(art)