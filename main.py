import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import ImageGrab

class Sketchpad(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Enhanced Sketchpad with Shapes")
        self.geometry("1000x700")
        self.configure(bg="#f0f0f0") 
        
        self.brush_size = 5
        self.brush_color = "black"
        self.shape = "free"
        self.start_x = None
        self.start_y = None
        self.current_shape = None
        self.eraser_on = False
        self.undo_stack = []
        self.redo_stack = []

        self.canvas = tk.Canvas(self, bg="white", cursor="cross", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)

        control_frame = tk.Frame(self, bg="#d9d9d9", height=50)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        brush_size_label = tk.Label(control_frame, text="Brush Size:", bg="#d9d9d9", fg="black", font=("Arial", 12))
        brush_size_label.pack(side=tk.LEFT, padx=10)

        brush_size_scale = tk.Scale(control_frame, from_=1, to=20, orient=tk.HORIZONTAL, command=self.change_brush_size, bg="#d9d9d9", fg="black", highlightthickness=0)
        brush_size_scale.set(self.brush_size)
        brush_size_scale.pack(side=tk.LEFT, padx=10)

        color_picker_button = tk.Button(control_frame, text="Color Picker", bg="black", fg="white", font=("Arial", 12), command=self.choose_color)
        color_picker_button.pack(side=tk.LEFT, padx=10)

        shape_frame = tk.Frame(control_frame, bg="#d9d9d9")
        shape_frame.pack(side=tk.LEFT, padx=10)

        free_draw_button = tk.Button(shape_frame, text="Free Draw", bg="black", fg="white", font=("Arial", 12), command=lambda: self.set_shape("free"))
        free_draw_button.pack(side=tk.LEFT, padx=5)
        
        line_button = tk.Button(shape_frame, text="Line", bg="black", fg="white", font=("Arial", 12), command=lambda: self.set_shape("line"))
        line_button.pack(side=tk.LEFT, padx=5)
        
        rectangle_button = tk.Button(shape_frame, text="Rectangle", bg="black", fg="white", font=("Arial", 12), command=lambda: self.set_shape("rectangle"))
        rectangle_button.pack(side=tk.LEFT, padx=5)
        
        oval_button = tk.Button(shape_frame, text="Oval", bg="black", fg="white", font=("Arial", 12), command=lambda: self.set_shape("oval"))
        oval_button.pack(side=tk.LEFT, padx=5)

        eraser_button = tk.Button(control_frame, text="Eraser", bg="black", fg="white", font=("Arial", 12), command=self.toggle_eraser)
        eraser_button.pack(side=tk.LEFT, padx=10)

        clear_button = tk.Button(control_frame, text="Clear", bg="black", fg="white", font=("Arial", 12), command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT, padx=10)

        save_button = tk.Button(control_frame, text="Save", bg="black", fg="white", font=("Arial", 12), command=self.save_canvas)
        save_button.pack(side=tk.RIGHT, padx=10)

        undo_button = tk.Button(control_frame, text="Undo", bg="black", fg="white", font=("Arial", 12), command=self.undo)
        undo_button.pack(side=tk.RIGHT, padx=10)

        redo_button = tk.Button(control_frame, text="Redo", bg="black", fg="white", font=("Arial", 12), command=self.redo)
        redo_button.pack(side=tk.RIGHT, padx=10)

    def start_draw(self, event):
        self.start_x, self.start_y = event.x, event.y
        if self.eraser_on:
            self.brush_color_temp = self.brush_color
            self.change_brush_color("white")
        else:
            self.brush_color_temp = None

    def draw(self, event):
        if self.shape == "free":
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, width=self.brush_size, fill=self.brush_color, capstyle=tk.ROUND, smooth=tk.TRUE)
            self.start_x, self.start_y = event.x, event.y
        else:
            if self.current_shape:
                self.canvas.delete(self.current_shape)
            if self.shape == "line":
                self.current_shape = self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, width=self.brush_size, fill=self.brush_color)
            elif self.shape == "rectangle":
                self.current_shape = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, width=self.brush_size, outline=self.brush_color)
            elif self.shape == "oval":
                self.current_shape = self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, width=self.brush_size, outline=self.brush_color)

    def end_draw(self, event):
        self.save_state()
        self.current_shape = None

    def change_brush_size(self, size):
        self.brush_size = int(size)

    def change_brush_color(self, color):
        self.brush_color = color

    def toggle_eraser(self):
        self.eraser_on = not self.eraser_on
        if self.eraser_on:
            self.change_brush_color("white")
        else:
            if self.brush_color_temp:
                self.change_brush_color(self.brush_color_temp)

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose Brush Color")
        if color_code:
            self.change_brush_color(color_code[1])

    def clear_canvas(self):
        self.canvas.delete("all")
        self.save_state(clear_stack=True)

    def save_canvas(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All Files", "*.*")])
        if file_path:
            x = self.canvas.winfo_rootx()
            y = self.canvas.winfo_rooty()
            width = x + self.canvas.winfo_width()
            height = y + self.canvas.winfo_height()
            ImageGrab.grab().crop((x, y, width, height)).save(file_path)
            messagebox.showinfo("Save", f"Image saved as {file_path}")

    def save_state(self, clear_stack=False):
        if clear_stack:
            self.undo_stack = []
        self.redo_stack = []
        self.undo_stack.append(self.canvas_to_image())

    def undo(self):
        if self.undo_stack:
            self.redo_stack.append(self.undo_stack.pop())
            if self.undo_stack:
                self.load_image_to_canvas(self.undo_stack[-1])
            else:
                self.clear_canvas()

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(self.redo_stack.pop())
            self.load_image_to_canvas(self.undo_stack[-1])

    def canvas_to_image(self):
        self.update()
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        width = x + self.canvas.winfo_width()
        height = y + self.canvas.winfo_height()
        return ImageGrab.grab().crop((x, y, width, height))

    def load_image_to_canvas(self, image):
        self.clear_canvas()
        self.canvas.image = tk.PhotoImage(image=image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.canvas.image)

    def set_shape(self, shape_type):
        self.shape = shape_type
        if shape_type == "free":
            self.canvas.config(cursor="cross")
        else:
            self.canvas.config(cursor="arrow")

if __name__ == "__main__":
    app = Sketchpad()
    app.mainloop()
