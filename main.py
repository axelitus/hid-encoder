import customtkinter
from h10301 import H10301


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        self.geometry("500x480")
        self.title("HID Encoder")

        self.validate_facility = self.register(self.validation_facility)
        self.validate_card = self.register(self.validation_card)

        self.frame = customtkinter.CTkFrame(master=self)
        self.frame.pack(pady=20, padx=30, fill="both", expand=True)

        self.lbl_facility = customtkinter.CTkLabel(
            master=self.frame,
            font=("Ubuntu", 24),
            text="Facility Code (0 - {}):".format(H10301.FACILITY_MAX_VALUE)
        )
        self.lbl_facility.pack(pady=10, padx=10)

        self.ent_facility = customtkinter.CTkEntry(
            master=self.frame,
            width=200,
            height=32,
            font=("Ubuntu", 24),
            validate="key", validatecommand=(self.validate_facility, "%P")
        )
        self.ent_facility.pack(pady=10, padx=10)
        self.ent_facility.bind("<Tab>", self.focus_next_widget)
        self.ent_facility.bind("<KeyRelease>", self.clear_flipper)

        self.lbl_card = customtkinter.CTkLabel(
            master=self.frame,
            font=("Ubuntu", 24),
            text="Card Code (0 - {}):".format(H10301.CARD_MAX_VALUE)
        )
        self.lbl_card.pack(pady=10, padx=10)

        self.ent_card = customtkinter.CTkEntry(
            master=self.frame,
            width=200,
            height=32,
            font=("Ubuntu", 24),
            placeholder_text="",
            validate="key", validatecommand=(self.validate_card, "%P")
        )
        self.ent_card.pack(pady=10, padx=10)
        self.ent_card.bind("<Tab>", self.focus_next_widget)
        self.ent_card.bind("<KeyRelease>", self.clear_flipper)

        self.btn_encode = customtkinter.CTkButton(
            master=self.frame,
            height=32,
            text="Encode",
            font=("Ubuntu", 20),
            command=self.encode
        )
        self.btn_encode.pack(pady=20, padx=10, anchor=customtkinter.CENTER)

        self.txt_flipper = customtkinter.CTkTextbox(
            master=self.frame,
            width=350,
            height=132,
            font=("Ubuntu", 20),
            state="disabled"
        )
        self.txt_flipper.pack(pady=10, padx=10)

        self.ent_facility.focus()

    @staticmethod
    def focus_next_widget(event):
        event.widget.tk_focusNext().focus()
        return "break"

    @staticmethod
    def validation_facility(text):
        if text != "" and not text.isdigit():
            return False

        if text != "" and int(text) > H10301.FACILITY_MAX_VALUE:
            return False

        return True

    @staticmethod
    def validation_card(text):
        if text != "" and not text.isdigit():
            return False

        if text != "" and int(text) > H10301.CARD_MAX_VALUE:
            return False

        return True

    def clear_flipper(self, event):
        if self.txt_flipper.get("0.0", customtkinter.END) != "":
            self.txt_flipper.configure(state="normal")
            self.txt_flipper.delete("0.0", customtkinter.END)
            self.txt_flipper.configure(state="disabled")

    def encode(self):
        facility = int(self.ent_facility.get()) if self.ent_facility.get() != "" else 0
        card = int(self.ent_card.get()) if self.ent_card.get() != "" else 0
        hid = H10301(facility, card)

        self.txt_flipper.configure(state="normal")
        self.txt_flipper.delete("0.0", customtkinter.END)
        self.txt_flipper.insert("0.0", hid.flipper())
        self.txt_flipper.configure(state="disabled")


if __name__ == "__main__":
    app = App()
    app.mainloop()
