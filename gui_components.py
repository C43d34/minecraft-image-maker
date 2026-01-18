'''
Contains the components used in GUI design. 
'''
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import main as BrailleConverter

class ImageDisplayZone:
    '''
    Builds component that loads and displays an image when triggered using "load_image" method. 
    '''

## COMPONENTS 
    images = [] #Can use to store image and file path 
    current_image = None

## METHODS

    def __init__(self, parent):
        self.root = parent
        self.setup_image_dropzone(parent)
        return

    def setup_image_dropzone(self, parent_container):
        """Setup the image drop zone tab"""

        # Title
        self.title = tk.Label(
            parent_container, 
            text="Original Image", 
            font=("Arial", 16, "bold"),
            bg="#f0f0f0"
        )
        # self.title.pack(pady=10)
        
        # Drop zone frame
        self.drop_frame = tk.Frame(
            parent_container, 
            bg="white", 
            highlightbackground="#4a90e2",
            highlightthickness=2,
            relief=tk.SUNKEN
        )   
        # self.drop_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        
        # Image display label (hidden initially)
        blank_image = tk.PhotoImage()
        self.image_label = tk.Label(
            parent_container,
            image=blank_image, 
            bg="white",
            width=240,
            height=240,
        )
        self.image_label.pack(padx=10, pady=10)
        
        # Info label
        self.info_label = tk.Label(
            parent_container,
            text="No images loaded",
            font=("Arial", 10),
            bg="#f0f0f0",
            wraplength=200,
        )
        self.info_label.pack(pady=5)


    def load_image(self, file_path):
        """Load and display an image"""
        try:
            img = Image.open(file_path)
            self.images.append({'path': file_path, 'image': img}) #Can store the image and file path if we want 
            
            self.image_label.pack(expand=True)
            
            # Display the image
            self.display_image(img, file_path)

        except Exception as e:
            self.info_label.config(text=f"Error loading image: {str(e)}")
            

    def display_image(self, img, file_path):
        """
        Display image inside the frame's dimension but maintain the same aspect ratio.
        Assume the frame's dimensions are fixed and don't expand when the image is added ._.
        """
        
        # Get frame dimensions
        frame_width = self.image_label.winfo_width()
        frame_height = self.image_label.winfo_height()
        
        # Use default size if frame not yet rendered
        if frame_width <= 1:
            frame_width = 200
            frame_height = 200
        
        # Calculate scaling to fit image in frame
        img_width, img_height = img.size
        scale = min(frame_width / img_width, frame_height / img_height, 1.0)
        
        new_width = int(img_width * scale * 0.9)
        new_height = int(img_height * scale * 0.9)
        
        #DEBUGGING
        print(f"frame height and width: {frame_height}, {frame_width}") 
        print(f"original image width {img_width}, new image width {new_width}")
        print(f"original image height {img_height}, new image width {new_height}")
        #DEBUGGING

        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img_resized)
        
        self.image_label.config(image=photo)
        self.image_label.image = photo
        
        # Update info
        filename = os.path.basename(file_path)
        self.info_label.config(
            text=f"Loaded: {filename} | Size: {img_width}x{img_height} | Total images: {len(self.images)}"
        )


class ASCIIArtDisplay:
    '''
    Builds component to display text generated as ASCII art
    '''
    def __init__(self, parent):
        self.setup_ascii_display_zone(parent)
        return
          
    def setup_ascii_display_zone(self, parent_container):
        """Setup the text file preview tab"""
        # Title
        title = tk.Label(
            parent_container, 
            text="Text File Preview", 
            font=("Arial", 16, "bold"),
            bg="#24bebe"
        )
        title.pack(pady=10)
        
        # Path label
        self.path_label = tk.Label(
            parent_container,
            text="File: ./text_file_path",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#666666"
        )
        self.path_label.pack(pady=5)
        
        # Main content frame
        # content_frame = tk.Frame(parent_container, bg="#63b962", width=65)
        # content_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # Text widget with scrollbar (left side)
        text_frame = tk.Frame(parent_container)
        text_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(text_frame)
        # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_widget = tk.Text(
            text_frame,
            wrap=tk.WORD,
            font=("Courier", 10),
            yscrollcommand=scrollbar.set,
            bg="white",
            relief=tk.SUNKEN,
            borderwidth=2,
            width=50,
            height=1
        )
        # self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_widget.yview)
        

        # Instructions label
        self.instruction_label = tk.Label(
            text_frame,
            text="📁 Drop image files here\n\nSupported: PNG, JPG, JPEG, GIF, BMP",
            font=("Arial", 10),
            bg="white",
            fg="#888888",
            borderwidth=2,
            width=50
        )
        self.instruction_label.pack(fill=tk.BOTH, expand=True)


        # Reload button
        reload_btn = tk.Button(
            parent_container,
            text="Reload File",
            command=self.reload_button,
            bg="#4a90e2",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=5,
            cursor="hand2"
        )
        reload_btn.pack(side=tk.BOTTOM, pady=10)
        
        # self.load_text_file()


    def reload_button(self):

        #DEBUG
        # self.text_widget.configure(width=50)
        print(self.text_widget.winfo_width())
        print(self.instruction_label.winfo_width())
        return

    def load_text_file(self, *text):
        """Load and display the text file"""
        file_path = "./text_file_path"
        
        #make sure text widget is visible
        self.instruction_label.pack_forget()
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Clear existing content
        self.text_widget.delete(1.0, tk.END)
        
        if(text == None or len(text) == 0):

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.text_widget.insert(1.0, content)
                    self.path_label.config(text=f"File: {file_path} ✓", fg="#2ecc71")
            except FileNotFoundError:
                error_msg = f"Error: File not found at '{file_path}'\n\n"
                error_msg += "Please ensure the file exists at this location."
                self.text_widget.insert(1.0, error_msg)
                self.path_label.config(text=f"File: {file_path} ✗", fg="#e74c3c")
            except Exception as e:
                error_msg = f"Error reading file: {str(e)}"
                self.text_widget.insert(1.0, error_msg)
                self.path_label.config(text=f"File: {file_path} ✗", fg="#e74c3c")
        else:
            #check text tuple for any text
            text_string = text[0]
            self.text_widget.insert(1.0, text_string)
            self.path_label.config(text=f"Text from converted image {{image path goes here}} ✓", fg="#2ecc71")



class ASCIIArtParameterControls:
    '''
    Builds component that houses controls and parameters which feed input to the ASCII Art generation algorithm. 
    '''

    threshold_value: int = 0
    threshold_spread_value: int = 0
    skew_factor: float = 1.0
    listener_function_handles: list = [] #contains a list of functions that will be activated whenever the state of this component's controls change. 


    def __init__(self, parent):
        self.setup_parameter_controls(parent)
        return
    
    def setup_parameter_controls(self, parent_container):

        # Slider frame (right side)
        slider_frame = tk.Frame(parent_container, bg="#e913db")
        slider_frame.pack(fill=tk.BOTH, padx=(10, 0), expand=True)
        
        # Slider 1
        slider1_container = tk.Frame(slider_frame, bg="#f0f0f0")
        slider1_container.pack( pady=10, padx=10)
        
        self.slider1_label = tk.Label(
            slider1_container,
            text="Threshold: 0",
            font=("Arial", 10, "bold"),
            bg="#f0f0f0",
            width=20
        )
        self.slider1_label.pack()
        
        self.slider1 = tk.Scale(
            slider1_container,
            from_=0,
            to=255,
            orient=tk.HORIZONTAL,
            command=self.update_slider1_label,
            length=200,
            bg="#f0f0f0",
            highlightthickness=0
        )
        self.slider1.pack(pady=5)
        
        # Slider 2
        slider2_container = tk.Frame(slider_frame, bg="#f0f0f0")
        slider2_container.pack(pady=10, padx=10)
        
        self.slider2_label = tk.Label(
            slider2_container,
            text="Threshold Spread: 0",
            font=("Arial", 10, "bold"),
            bg="#f0f0f0",
            width=20
        )
        self.slider2_label.pack()
        
        self.slider2 = tk.Scale(
            slider2_container,
            from_=0,
            to=255,
            orient=tk.HORIZONTAL,
            command=self.update_slider2_label,
            length=200,
            bg="#f0f0f0",
            highlightthickness=0
        )
        self.slider2.pack(pady=5)


        # Slider 3
        slider3_container = tk.Frame(slider_frame, bg="#f0f0f0")
        slider3_container.pack(pady=10, padx=10)


        self.slider3_label = tk.Label(
            slider3_container,
            text="Skew Factor: 1.0",
            font=("Arial", 10, "bold"),
            bg="#f0f0f0",
            width=20
        )
        self.slider3_label.pack()
        
        self.slider3 = tk.Scale(
            slider3_container,
            from_=0.25,
            to=2.0,
            resolution=0.05,
            orient=tk.HORIZONTAL,
            command=self.update_slider3_label,
            length=200,
            bg="#f0f0f0",
            highlightthickness=0
        )
        self.slider3.set(1.0)
        self.slider3.pack(pady=5)
        

    def update_slider1_label(self, value: str):
        """Update slider 1 label with current value"""
        self.slider1_label.config(text=f"Threshold {value}")
        self.threshold_value = int(value)

        '''
        When Threshold changes, Threshold Spread range can only be equal to 255-Threshold (max value of a pixel cell - threshold at which a pixel will be treated as black dot)
        There is no point setting Threshold Spread to anything greater than this value. 
            For example, If threshold is 250. Then spread must be <= 5 (255-250). If spread is 10, then it would treated cells with average value up to 260 to be at or below the threshold of 250. But we know there are no cells that can average a value at 260 (255 is the cap). Therefore, we clamp Threshold spread to max out at 5. 
        This adjustment is simply for clarity. It has no physical bearing on the Braille algorithm if Threshold spread is set "too high"  
        '''
        maximum_threshold_spread_value = 255 - int(value)
        self.slider2.config(to=maximum_threshold_spread_value)
        
        self.notify_listener_functions()
    

    def update_slider2_label(self, value):
        """Update slider 2 label with current value"""
        self.slider2_label.config(text=f"Threshold Spread: {value}")
        self.threshold_spread_value = int(value)
        self.notify_listener_functions()

    
    def update_slider3_label(self, value):
        """Update slider 3 label with current value"""
        self.slider3_label.config(text=f"Skew Factor: {value}")
        self.skew_factor = float(value)
        self.notify_listener_functions()


    def register_listener_on_control_updates(self, function_triggered_on_update):
        '''
        Add a function to be triggered whenever the state of this component's controls change. Such as a slider changing value

        :param function_triggered_on_update: Function signature to be triggered on update. ( I don't know how to work with signatures with parameters just yet )
        '''
        self.listener_function_handles.append(function_triggered_on_update)
        return
    
    
    def notify_listener_functions(self):
        '''
        Call this function whenever state of the component's controls change so that we can notify any functions registered to listen for changes. 
        '''
        for function_handle in self.listener_function_handles:
            function_handle()
        
        return