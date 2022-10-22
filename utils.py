from tkinter import Frame


def clear_frame(frame: Frame):
    """
    Clear all entries in a frame
    :param frame: Frame: Frame to clear
    :return: None
    """
    for widget in frame.winfo_children():
        if widget.winfo_class() == "Frame":
            clear_frame(widget)
        widget.destroy()
