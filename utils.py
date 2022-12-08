from tkinter import *
import time
from playsound import playsound


def clear_frame(frame: Widget):
    """
    Clear all entries in a frame
    :param frame: Frame: Frame to clear
    :return: None
    """
    if isinstance(frame, VerticalScrolledFrame or HorizontalScrolledFrame):
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


class HorizontalScrolledFrame:
    """
    Code issu du Gist GitHub https://gist.github.com/novel-yet-trivial/3eddfce704db3082e38c84664fc1fdf8?permalink_comment_id=3811531#gistcomment-3811531
    Une Frame horizontalement scrollable qui peut être traitée comme n'importe quelle autre Frame
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

        self.vsb = Scrollbar(self.outer, orient=HORIZONTAL)
        self.vsb.pack(fill=X, side=BOTTOM)
        self.canvas = Canvas(self.outer, highlightthickness=0, width=width, height=height, bg=bg)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.canvas.config(yscrollcommand=self.vsb.set)
        # Défilement de la souris ne semble pas fonctionner avec juste "bind"; Vous avez besoin d'utiliser "bind_all". Par conséquent, pour utiliser plusieurs fenêtres, vous devez bind_all dans le widget actuel
        self.canvas.bind("<Enter>", self._bind_mouse)
        self.canvas.bind("<Leave>", self._unbind_mouse)
        self.canvas.addtag_all("all")  # (added) for configuring width
        self.vsb.config(command=self.canvas.yview)

        self.inner = Frame(self.canvas, bg=bg)
        self.inner.pack(side=TOP, fill=BOTH, expand=True)
        # Installation d'une fenêtre interne dans le Canvas avec le coin supérieur gauche décalé de 4 pixels
        self.canvas.create_window((0, 0), window=self.inner, anchor='nw')
        self.canvas.bind("<Configure>", self._on_frame_configure)  # liaison du canvas au lieu de l'inner

        self.outer_attr = set(dir(Widget))

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


class IntEntry(Frame):
    def __init__(self, master, value: int = 0, min_value: int = 0, max_value: int = 10, **kwargs):
        def _validate(val):
            if val == "":
                return True
            try:
                int(val)
                return True
            except ValueError:
                return False

        # **kwargs without value, min_value and max_value
        kwargs.pop("value", None)
        kwargs.pop("min_value", None)
        kwargs.pop("max_value", None)
        super().__init__(master, **kwargs)
        super().__init__(master, **kwargs)

        self.value: int = value
        self.min_value: int = min_value
        self.max_value: int = max_value
        self.string_var = StringVar(value=str(value))

        self.button_minus = Button(self, text="-", command=self._decrement)
        self.button_minus.pack(side=LEFT)

        self.entry = Entry(self, width=5, textvariable=self.string_var)
        self.entry.pack(side=LEFT)
        self.set_value(value)

        self.entry.bind("<FocusOut>", self._on_focus_out)
        self.entry.bind("<Return>", self._on_focus_out)
        self.entry.config(validate="key", validatecommand=(self.register(_validate), "%P"))

        self.button_plus = Button(self, text="+", command=self._increment)
        self.button_plus.pack(side=LEFT)

    def _increment(self):
        if self.value < self.max_value:
            self.set_value(self.value + 1)

    def _decrement(self):
        if self.value > self.min_value:
            self.set_value(self.value - 1)

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
        if self.value > self.max_value:
            self.set_value(self.max_value)

        elif self.value < self.min_value:
            self.set_value(self.min_value)

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value
        self.string_var.set(str(self.value))
        self.entry.delete(0, END)
        self.entry.insert(0, str(self.value))


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
        self.entry_minutes.delete(0, END)
        self.entry_minutes.insert(0, str(minutes))

        self.entry_minutes.bind("<FocusOut>", self._on_focus_out)
        self.entry_minutes.bind("<Return>", self._on_focus_out)

        self.label_separator = Label(self, text=":")
        self.label_separator.pack(side=LEFT)

        self.entry_seconds = Entry(self, width=2, textvariable=self.string_var_seconds)
        self.entry_seconds.config(validate="key", validatecommand=(self.register(_validate), "%P"))
        self.entry_seconds.pack(side=LEFT)
        self.entry_seconds.delete(0, END)
        self.entry_seconds.insert(0, str(seconds))

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
        self.entry_minutes.delete(0, END)
        self.entry_minutes.insert(0, str(self.minutes))

    def set_value_seconds(self, value):
        self.seconds = value
        self.string_var_seconds.set(str(self.seconds))
        self.entry_seconds.delete(0, END)
        self.entry_seconds.insert(0, str(self.seconds))

    def get_total_seconds(self):
        return self.minutes * 60 + self.seconds

    def set_total_seconds(self, value):
        self.minutes = value // 60
        self.seconds = value % 60
        self.string_var_minutes.set(str(self.minutes))
        self.string_var_seconds.set(str(self.seconds))
        self.entry_minutes.delete(0, END)
        self.entry_minutes.insert(0, str(self.minutes))
        self.entry_seconds.delete(0, END)
        self.entry_seconds.insert(0, str(self.seconds))

    def add_seconds(self, seconds: int):
        self.set_total_seconds(self.get_total_seconds())


class TagsEntry(Frame):
    """
    A Frame with an Entry and a Button to add tags to a list. Each tag is a button that can be clicked to remove it.
    The tags are displayed in a HorizontalScrobleFrame that can be scrolled horizontally if there are too many tags.
    """
    def __init__(self, master, tags: list = None, **kwargs):
        super().__init__(master, **kwargs)

        self.tags = tags if tags is not None else []

        self.string_var = StringVar()
        self.entry = Entry(self, textvariable=self.string_var)
        self.entry.pack(side=LEFT)
        self.entry.bind("<Return>", self._add_tag)

        self.button_add = Button(self, text="Add", command=self._add_tag)
        self.button_add.pack(side=LEFT)
        
        self.frame_tags = HorizontalScrolledFrame(self, width=200, height=40)
        self.frame_tags.pack(side=BOTTOM, fill=BOTH, expand=True)

        self._update_tags()
        
    def _add_tag(self, event=None):
        tag = self.entry.get()
        if tag not in self.tags and tag != "":
            self.tags.append(tag)
            self.entry.delete(0, END)
            self._update_tags()

    def _remove_tag(self, tag):
        self.tags.remove(tag)
        self._update_tags()
        
    def _update_tags(self):
        clear_frame(self.frame_tags.inner)
        for tag in self.tags:
            button = Button(self.frame_tags.inner, text=tag + " ⨂", command=lambda tag=tag: self._remove_tag(tag))
            button.pack(side=LEFT)

    def _on_click(self, event):
        widget = event.widget
        index = widget.curselection()[0]
        tag = widget.get(index)
        self._remove_tag(tag)



class Timer:
    def __init__(self, remining: int, title: str, game):
        self.game = game
        approx_time = remining // 5
        self.root = root = Tk()
        root.title("Timer")
        root.geometry("200x100")
        root.resizable(False, False)
        root.state("zoomed")
        root.iconbitmap("assets/img/amongus.ico")

        timer_frame = Frame(root)

        title = Label(timer_frame, text=title, font=("Arial", 50))
        title.pack(fill=BOTH, expand=True, padx=10)

        minutes, seconds = divmod(remining, 60)
        timer = Label(timer_frame, text=f"{minutes:02d}:{seconds:02d}", font=("Arial", 55))
        timer.pack(fill=BOTH, expand=True, padx=10)

        timer_frame.pack(fill=BOTH, expand=True)

        self.players_frame = players_frame = VerticalScrolledFrame(root)
        players_frame.pack(fill=BOTH, expand=True)

        self.show_players()

        while remining > 0:
            remining -= 1
            minutes, seconds = divmod(remining, 60)
            timer.config(text=f"{minutes:02d}:{seconds:02d}")
            if remining <= approx_time:
                if remining == approx_time:
                    playsound(r"assets/sounds/mid_time.mp3", block=False)
                if remining % 2 == 0:
                    timer.config(fg="red")
                else:
                    timer.config(fg="black")
            root.update()
            time.sleep(1)
        else:
            timer.config(text="00:00")
            root.update()
            playsound(r"assets/sounds/time_end.mp3")
            time.sleep(1)
            root.destroy()
            return

        root.mainloop()

    def show_players(self):
        players_frame = self.players_frame
        game = self.game
        # show players in a grid adapted to the number of players
        players = game.players
        for i, player in enumerate(players):
            # set a border around the player frame
            player_frame = Frame(players_frame, borderwidth=2, relief="groove")
            player_frame.grid(row=i // 2, column=i % 2, padx=10, pady=10)
            player_name = Label(player_frame, text=player.get_str(game), font=("Arial", 20))
            if game.meeting == "vote" and player.id in game.meeting_votes.keys():
                player_name.config(fg="red")
            player_name.pack(fill=BOTH, expand=True)



if __name__ == "__main__":
    # print recommended impostors
    # for i in range(4, 20):
    #    print(f"{i} players: {recommanded_impostors(i)} impostors")
    Timer(60, "Test", [])
    print("Done")
