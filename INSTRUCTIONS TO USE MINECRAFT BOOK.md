INSTRUCTIONS TO USE MINECRAFT BOOK IMAGE GENERATOR:



**FIRST,**

 	Make sure you have python installed *(https://www.python.org/downloads/)*

You can check if you have it installed by typing "python" in Command Prompt.



**SECOND,**

 	Create an image. The image you want to convert into Minecraft book image needs to be in the following file types: **.png, .jpg**

(idk what else works)



**Any size and color works!**

I highly recommend the image to be resized down to **72 x 56** and **white/black** only so you would know what it looks like.

The image will be stretched and distorted a lot being converted from original into ASCII art. Please take note of that!





**THIRD,**

 	Once you have Python and the image ready, open Command Prompt and type "python"

then you can drag or write the path to the "main.py" file into it.

    - python main.py

After that, drag the image you want to convert into the command prompt.
Make sure to leave a space between these 3 parts!

    - python main.py <image_path>

When you press enter, the program will run and generate a text file in the "output_images" folder.
You can then copy text within this file and paste into a Minecraft book.


# Alternative commandline operating modes
There are additional optional commandline flags available for ease of use
-f, --file            : provide this flag with a file path afterwards (default behavior)
    EX. "python main.py -f <file_path>"

-d, --directory       : provide this flag with a directory path. All images inside the directory path will be converted.
    EX. "python main.py -d <dir_path>"
    EX. "python main.py -d ." (converts all images inside the current working directory)
    EX. "python main.py -d ./input_images" (converts all images inside the local folder "input_images")

-n, --include_newline : this flag sets the program to generate the ascii image with the newline character included. This may break the ability to paste the text in some versions of Minecraft (1.21.10) 
    EX. "python main.py -n"

Commandline flags can be combined to convert all images from a directory and convert them with newline included as such:
    EX. "python main.py -n -d ./input_images" 




**Common problems encountered:
Text cannot be pasted into Minecraft book**

That is most likely because your pasted text size is too big.

It will not paste at all if it would go over limit of the Minecraft text.

Also, the script is AI generated that I edited just slightly to make sure it works properly. Please dont blame me if something breaks :(

