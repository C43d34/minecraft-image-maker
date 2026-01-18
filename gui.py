import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import main as BrailleConverter
import gui_components

class GUIComponent:
    def __init__(self, parent_container):
        self.SetupStuff(parent_container)
        return

    def SetupStuff(self, parent_container):
        """Setup the image drop zone tab"""
        # Title
        title = tk.Label(
            parent_container, 
            text="Drag & Drop Images Here", 
            font=("Arial", 16, "bold"),
            bg="#f0f0f0"
        )
        title.pack(pady=10)
        
        # Drop zone frame
        self.drop_frame = tk.Frame(
            parent_container, 
            bg="white", 
            highlightbackground="#4a90e2",
            highlightthickness=2,
            relief=tk.SUNKEN
        )
        self.drop_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # Instructions label
        self.instruction_label = tk.Label(
            self.drop_frame,
            text="📁 Drop image files here\n\nSupported: PNG, JPG, JPEG, GIF, BMP",
            font=("Arial", 12),
            bg="white",
            fg="#888888"
        )
        self.instruction_label.pack(expand=True)
        
        # Image display label (hidden initially)
        self.image_label = tk.Label(self.drop_frame, bg="white")
        
        # Info label
        self.info_label = tk.Label(
            parent_container,
            text="No images loaded",
            font=("Arial", 10),
            bg="#f0f0f0"
        )
        self.info_label.pack(pady=5)
    


class BrailleAsciiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Drop Zone & Text Viewer")
        self.root.configure(bg="#f0f0f0")

        # Set minimum window size
        self.root.minsize(700, 700)
        
        # Allow window to be resizable
        self.root.resizable(True, True)
        
        # Update window to calculate required size
        self.root.update_idletasks()

        self.images = []
        self.current_image = None
        
        self.main_window = tk.Frame(self.root, bg="#C43d34")
        # Create notebook (tabbed interface)
        # self.notebook = ttk.Notebook(root)
        # self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        # # Create tabs
        # self.image_tab = tk.Frame(self.notebook, bg="#f0f0f0")
        # self.text_tab = tk.Frame(self.notebook, bg="#2f3382")
        # self.notebook.add(self.image_tab, text="Image Drop Zone")
        # self.notebook.add(self.text_tab, text="Text File Preview")

        # Setup image tab
        # self.setup_image_tab()
        # GUIComponent(self.image_tab)
        
        # Setup text tab
        # self.setup_text_tab()

        self.setup_gui_framework()

    def setup_gui_framework(self):

    ## Define containers for Image display, ASCII text display, and ASCII conversion parameter controls
        ascii_display_container = tk.Frame(self.main_window, bg="#07981c")

        #Sidebar contains image display and controls 
        right_sidebar_container = tk.Frame(self.main_window)
        ascii_parameter_controls_container = tk.Frame(right_sidebar_container, bg="#08269D")
        image_display_container = tk.Frame(right_sidebar_container, bg="#c7a52d")


    ## Pack containers into main window
        #Initialize main window
        self.main_window.pack(fill=tk.BOTH, expand=True)

        #Container for where ASCII is displayed
        ascii_display_container.pack(side=tk.LEFT,padx=20, pady=10, fill=tk.BOTH, expand=True)

        #Container for the original image preview and ascii controls
        right_sidebar_container.pack(side=tk.LEFT, fill=tk.Y, expand=False)
        image_display_container.pack(side=tk.TOP, fill=tk.BOTH, expand=False)
        ascii_parameter_controls_container.pack(fill=tk.BOTH, expand=True)


    ## Populate containers with stuff
        self.image_display_component = gui_components.ImageDisplayZone(image_display_container)
        self.ASCII_art_display_component = gui_components.ASCIIArtDisplay(ascii_display_container)
        self.ASCII_parameter_controls_component = gui_components.ASCIIArtParameterControls(ascii_parameter_controls_container)
        
        # Register a function to trigger when controls change inside ASCII controll component
        self.ASCII_parameter_controls_component.register_listener_on_control_updates(self.do_on_ascii_controls_update)
       

    ## Enable drag and drop functionality
        self.setup_drag_drop()


    def setup_drag_drop(self):
        """Setup drag and drop functionality"""
        self.main_window.drop_target_register('DND_Files')
        self.main_window.dnd_bind('<<Drop>>', self.on_drop)
        self.main_window.dnd_bind('<<DragEnter>>', self.on_drag_enter)
        self.main_window.dnd_bind('<<DragLeave>>', self.on_drag_leave)
        
    def on_drag_enter(self, event):
        """Visual feedback when dragging over drop zone"""
        self.main_window.configure(highlightbackground="#2ecc71", highlightthickness=3)
        
    def on_drag_leave(self, event):
        """Reset visual feedback when leaving drop zone"""
        self.main_window.configure(highlightbackground="#4a90e2", highlightthickness=2)
        
    def on_drop(self, event):
        """Handle dropped files"""
        self.main_window.configure(highlightbackground="#4a90e2", highlightthickness=2)
        
        files =  self.main_window.tk.splitlist(event.data)
        valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
        
        for file_path in files:
            file_path = file_path.strip('{}')
            if os.path.isfile(file_path) and file_path.lower().endswith(valid_extensions):
                # self.load_image(file_path)
                self.image_display_component.load_image(file_path) #load image into image display component
                ascii_text = BrailleConverter.img_file_to_braille_ascii(file_path, include_newline=True) #load image into braille converter (loading image twice maybe a waste of resources?)
                self.ASCII_art_display_component.load_text_file(ascii_text)
                self.current_image = Image.open(file_path)


    def do_on_ascii_controls_update(self):
        # print(f"WAZ {self.ASCII_parameter_controls_component.threshold_value}") # DEBUG
        
    ## Get Control parameter values
        threshold = self.ASCII_parameter_controls_component.threshold_value
        threshold_spread = self.ASCII_parameter_controls_component.threshold_spread_value
        skew_factor = self.ASCII_parameter_controls_component.skew_factor

        if self.current_image: #check to make sure not NONE
            ascii_text = BrailleConverter.img_to_braille_ascii(self.current_image, threshold, threshold_spread, skew_factor=skew_factor, include_newline=True) #load image into braille converter (loading image twice maybe a waste of resources?)
            self.ASCII_art_display_component.load_text_file(ascii_text)
        else:
            print("NO IMAGE SET")
        return       

        
def main():
    try:
        from tkinterdnd2 import TkinterDnD, DND_FILES
        root = TkinterDnD.Tk()
    except ImportError:
        print("Error: tkinterdnd2 is not installed.")
        print("Install it using: pip install tkinterdnd2")
        return
    
    app = BrailleAsciiGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()