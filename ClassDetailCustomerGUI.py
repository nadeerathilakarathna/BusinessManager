import customtkinter
import ClassGUI




class DetailCustomer:
    def screen(invoice):
        def a():
            screen.destroy()
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        screen = customtkinter.CTk()

        width = 1000  # Width
        height = 750  # Height

        screen_width = screen.winfo_screenwidth()  # Width of the screen
        screen_height = screen.winfo_screenheight()  # Height of the screen

        # Calculate Starting X and Y coordinates for Window
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)

        b = customtkinter.CTkButton(master=screen,command=a)
        b.pack()

        screen.geometry('%dx%d+%d+%d' % (width, height, x + 50, y - 40))

        screen.mainloop()