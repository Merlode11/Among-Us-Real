from tkinter import Frame, ttk
from tkinter import *
import time
from playsound import playsound


def clear_frame(frame: Frame):
    """
    Clear all entries in a frame
    :param frame: Frame: Frame to clear
    :return: None
    """
    if isinstance(frame, VerticalScrolledFrame):
        frame = frame.inner
    for widget in frame.winfo_children():
        if widget.winfo_class() == "Frame":
            clear_frame(widget)
        widget.destroy()


class VerticalScrolledFrame:
    """
    Code issu du Gist GitHub https://gist.github.com/novel-yet-trivial/3eddfce704db3082e38c84664fc1fdf8?permalink_comment_id=3811531#gistcomment-3811531
    Une Frame verticalement scrollable qui peut être traitée comme n'importe quelle autre Frame
    ie elle a besoin d'un master et d'un layout, et elle peut être un master.
    :width:, :height:, :bg: sont passés au Canvas sous-jacent
    :bg: et tous les autres arguments clé sont passés à la Frame interne
    il faut noter que le widget disposé dans cette frame aura un self.master 3 niveaux plus profonds,
    (outer Frame, Canvas, inner Frame) donc
    si vous sous classez ceci, il n'y a pas de moyen intégré pour que les enfants y accèdent.
    Vous devez fournir le contrôleur séparément.
    """

    def __init__(self, master, **kwargs):
        width = kwargs.pop('width', master.winfo_width())
        height = kwargs.pop('height', master.winfo_height())
        bg = kwargs.pop('bg', kwargs.pop('background', None))
        self.outer = Frame(master, **kwargs)

        self.vsb = Scrollbar(self.outer, orient=VERTICAL)
        self.vsb.pack(fill=Y, side=RIGHT)
        self.canvas = Canvas(self.outer, highlightthickness=0, width=width, height=height, bg=bg)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.canvas.config(yscrollcommand=self.vsb.set)
        # Défilement de la souris ne semble pas fonctionner avec juste "bind"; Vous avez besoin d'utiliser "bind_all". Par conséquent, pour utiliser plusieurs fenêtres, vous devez bind_all dans le widget actuel
        self.canvas.bind("<Enter>", self._bind_mouse)
        self.canvas.bind("<Leave>", self._unbind_mouse)
        self.canvas.addtag_all("all")  # (added) for configuring width
        self.vsb.config(command=self.canvas.yview)

        self.inner = Frame(self.canvas, bg=bg)
        # Installation d'une fenêtre interne dans le Canvas avec le coin supérieur gauche décalé de 4 pixels
        self.canvas.create_window((0, 0), window=self.inner, anchor='nw')
        self.canvas.bind("<Configure>", self._on_frame_configure)  # liaison du canvas au lieu de l'inner

        self.outer_attr = set(dir(Widget))

    def __getattr__(self, item):
        if item in self.outer_attr:
            # Attribus de géométrie, etc. eg pack, destroy, tkraise) sont transmis à self.outer
            return getattr(self.outer, item)
        else:
            # Tous les autres attributs (_w, children, etc.) sont passés à self.inner
            return getattr(self.inner, item)

    def _on_frame_configure(self, event=None):
        x1, y1, x2, y2 = self.canvas.bbox("all")
        height = self.canvas.winfo_height()
        width = self.canvas.winfo_width()
        self.canvas.config(scrollregion=(0, 0, x2, max(y2, height)))
        self.canvas.itemconfigure("all", width=width)

    def _bind_mouse(self, event=None):
        self.canvas.bind_all("<4>", self._on_mousewheel)
        self.canvas.bind_all("<5>", self._on_mousewheel)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mouse(self, event=None):
        self.canvas.unbind_all("<4>")
        self.canvas.unbind_all("<5>")
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        """Linux uses event.num; Windows / Mac uses event.delta"""
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")

    def __str__(self):
        return str(self.outer)


class YesNoButton(Button):
    def __init__(self, master, value=False, **kwargs):
        super().__init__(master, **kwargs)

        self.yes = PhotoImage(file="assets/img/checkbox_yes.png", master=master)
        self.no = PhotoImage(file="assets/img/checkbox_no.png", master=master)

        self.value = value
        self.config(image=self.yes if value else self.no, command=self.toggle)

    def toggle(self):
        self.value = not self.value
        self.config(image=self.yes if self.value else self.no)

    def set_value(self, value):
        self.value = value
        self.config(image=self.yes if value else self.no)

    def get_value(self):
        return self.value


# class IntEntry with validation (only numbers) and a default value and button betweeen the entry to increment or decrement the value by 1
class IntEntry(Frame):
    def __init__(self, master, value: int = 0, minimum: int = 0, maximum: int = 10, **kwargs):
        def _validate(val):
            if val == "":
                return True
            try:
                int(val)
                return True
            except ValueError:
                return False

        super().__init__(master, **kwargs)

        self.value: int = value
        self.minimum: int = minimum
        self.maximum: int = maximum
        self.string_var = StringVar(value=str(value))

        self.button_minus = Button(self, text="-", command=self._decrement)
        self.button_minus.pack(side=LEFT)

        self.entry = Entry(self, width=5, textvariable=self.string_var)
        self.entry.pack(side=LEFT)

        self.entry.bind("<FocusOut>", self._on_focus_out)
        self.entry.bind("<Return>", self._on_focus_out)
        self.entry.config(validate="key", validatecommand=(self.register(_validate), "%P"))

        self.button_plus = Button(self, text="+", command=self._increment)
        self.button_plus.pack(side=LEFT)

    def _increment(self):
        if self.value < self.maximum:
            self.value += 1
            self.string_var.set(str(self.value))

    def _decrement(self):
        if self.value > self.minimum:
            self.value -= 1
            self.string_var.set(str(self.value))

    def _on_focus_out(self, event):
        if self.string_var.get() == "":
            self.string_var.set(str(self.value))
        elif self.string_var.get() == "-":
            self.string_var.set(str(self.value))
        try:
            self.value = int(self.string_var.get())
        except ValueError:
            self.value = 0
        self.string_var.set(str(self.value))
        if self.value > self.maximum:
            self.value = self.maximum
            self.string_var.set(str(self.value))
        elif self.value < self.minimum:
            self.value = self.minimum
            self.string_var.set(str(self.value))

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value
        self.string_var.set(str(self.value))


# class TimerEntry with entry for minutes and seconds
class TimerEntry(Frame):
    def __init__(self, master, minutes: int = 0, seconds: int = 0, **kwargs):
        def _validate(val):
            if val == "":
                return True
            try:
                int(val)
                return True
            except ValueError:
                return False

        super().__init__(master, **kwargs)

        self.minutes: int = minutes
        self.seconds: int = seconds

        self.string_var_minutes = StringVar(value=str(minutes))
        self.string_var_seconds = StringVar(value=str(seconds))

        self.entry_minutes = Entry(self, width=2, textvariable=self.string_var_minutes)
        self.entry_minutes.config(validate="key", validatecommand=(self.register(_validate), "%P"))
        self.entry_minutes.pack(side=LEFT)

        self.entry_minutes.bind("<FocusOut>", self._on_focus_out)
        self.entry_minutes.bind("<Return>", self._on_focus_out)

        self.label_separator = Label(self, text=":")
        self.label_separator.pack(side=LEFT)

        self.entry_seconds = Entry(self, width=2, textvariable=self.string_var_seconds)
        self.entry_seconds.config(validate="key", validatecommand=(self.register(_validate), "%P"))
        self.entry_seconds.pack(side=LEFT)

        self.entry_seconds.bind("<FocusOut>", self._on_focus_out)
        self.entry_seconds.bind("<Return>", self._on_focus_out)

    def _on_focus_out(self, event):
        if event.widget == self.entry_minutes:
            if self.entry_minutes.get() == "":
                self.string_var_minutes.set(str(self.minutes))
            elif self.entry_minutes.get() == "-":
                self.string_var_minutes.set(str(self.minutes))
            try:
                self.minutes = int(self.string_var_minutes.get())
            except ValueError:
                self.minutes = 0
            self.string_var_minutes.set(str(self.minutes))
            if self.minutes > 59:
                self.minutes = 59
                self.string_var_minutes.set(str(self.minutes))
            elif self.minutes < 0:
                self.minutes = 0
                self.string_var_minutes.set(str(self.minutes))
        elif event.widget == self.entry_seconds:
            old_seconds = self.seconds
            if self.entry_seconds.get() == "":
                self.string_var_seconds.set(str(self.seconds))
            elif self.entry_seconds.get() == "-":
                self.string_var_seconds.set(str(self.seconds))
            try:
                self.seconds = int(self.string_var_seconds.get())
            except ValueError:
                self.seconds = 0
            self.string_var_seconds.set(str(self.seconds))
            if self.seconds > 59:
                self.add_seconds(self.seconds)
            elif self.seconds < 0:
                self.seconds = 0
                self.string_var_seconds.set(str(self.seconds))

    def get_value_minutes(self):
        return self.minutes

    def get_value_seconds(self):
        return self.seconds

    def set_value_minutes(self, value):
        self.minutes = value
        self.string_var_minutes.set(str(self.minutes))

    def set_value_seconds(self, value):
        self.seconds = value
        self.string_var_seconds.set(str(self.seconds))

    def get_total_seconds(self):
        return self.minutes * 60 + self.seconds

    def set_total_seconds(self, value):
        self.minutes = value // 60
        self.seconds = value % 60
        self.string_var_minutes.set(str(self.minutes))
        self.string_var_seconds.set(str(self.seconds))

    def add_seconds(self, seconds: int):
        self.set_total_seconds(self.get_total_seconds())


def show_timer(remining: int, title: str):
    root = Tk()
    root.title("Timer")
    root.geometry("200x100")
    root.resizable(True, True)
    root.state("zoomed")

    title = Label(root, text=title, font=("Arial", 100))
    title.pack(fill=BOTH, expand=True, padx=10)

    minutes, seconds = divmod(remining, 60)
    timer = Label(root, text=f"{minutes:02d}:{seconds:02d}", font=("Arial", 120))
    timer.pack(fill=BOTH, expand=True, padx=10)

    while remining > 0:
        remining -= 1
        minutes, seconds = divmod(remining, 60)
        timer.config(text=f"{minutes:02d}:{seconds:02d}")
        root.update()
        time.sleep(1)
    else:
        timer.config(text="00:00")
        root.update()
        playsound("assets/sounds/bip.mp3")
        time.sleep(1)
        root.destroy()

    root.mainloop()


if __name__ == "__main__":
    print(show_timer(10, "Vote"))
