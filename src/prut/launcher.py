"""Graphical launcher for the Prut programming language."""

import contextlib
import io
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext

from .interpreter import Interpreter
from .lexer import Lexer
from .parser import Parser


def resource_path(filename: str) -> Path:
    """Return the path to a bundled application resource."""

    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / filename

    return Path(__file__).resolve().parents[2] / filename


def run_program(source: str) -> str:
    """Run Prut source code and return its output."""

    output = io.StringIO()

    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        program = parser.parse()

        interpreter = Interpreter()

        with contextlib.redirect_stdout(output):
            interpreter.run(program)

    except SyntaxError as error:
        return f"Prut syntax error: {error}"

    except RuntimeError as error:
        return f"Prut runtime error: {error}"

    except Exception as error:
        return f"Prut error: {error}"

    return output.getvalue()


def main() -> None:
    """Start the Prut graphical launcher."""

    root = tk.Tk()

    # ---------------------------------------------------------
    # Window
    # ---------------------------------------------------------

    root.title("Prut")
    root.geometry("1200x700")
    root.minsize(750, 450)

    # ---------------------------------------------------------
    # Application icon
    # ---------------------------------------------------------

    icon_path = resource_path("prutlog.ico")

    if icon_path.exists():
        try:
            root.iconbitmap(str(icon_path))
        except tk.TclError:
            pass

    # ---------------------------------------------------------
    # Theme
    # ---------------------------------------------------------

    background = "#0f172a"
    panel = "#111827"
    panel_light = "#172033"
    border = "#263244"
    text = "#e5e7eb"
    muted = "#94a3b8"
    accent = "#3b82f6"
    accent_hover = "#2563eb"
    output_text = "#dbeafe"

    root.configure(bg=background)

    # ---------------------------------------------------------
    # Fonts
    # ---------------------------------------------------------

    title_font = ("Segoe UI", 15, "bold")
    label_font = ("Segoe UI", 10, "bold")
    normal_font = ("Segoe UI", 10)
    code_font = ("Cascadia Mono", 11)

    # ---------------------------------------------------------
    # Configure resizing
    # ---------------------------------------------------------

    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # ---------------------------------------------------------
    # Top toolbar
    # ---------------------------------------------------------

    toolbar = tk.Frame(
        root,
        bg=background,
        height=52,
    )

    toolbar.grid(
        row=0,
        column=0,
        sticky="ew",
        padx=12,
        pady=(10, 6),
    )

    toolbar.grid_columnconfigure(1, weight=1)

    title = tk.Label(
        toolbar,
        text="Prut",
        bg=background,
        fg=text,
        font=title_font,
    )

    title.grid(
        row=0,
        column=0,
        padx=(4, 20),
        sticky="w",
    )

    # ---------------------------------------------------------
    # Buttons
    # ---------------------------------------------------------

    def make_button(parent, label, command, primary=False):
        button = tk.Button(
            parent,
            text=label,
            command=command,
            font=normal_font,
            relief="flat",
            borderwidth=0,
            padx=12,
            pady=6,
            cursor="hand2",
            bg=accent if primary else panel_light,
            fg="white",
            activebackground=accent_hover if primary else border,
            activeforeground="white",
        )

        return button

    # ---------------------------------------------------------
    # Main content
    # ---------------------------------------------------------

    main = tk.Frame(
        root,
        bg=background,
    )

    main.grid(
        row=1,
        column=0,
        sticky="nsew",
        padx=12,
        pady=(0, 8),
    )

    main.grid_rowconfigure(0, weight=1)

    # Equal-width panels.
    main.grid_columnconfigure(
        0,
        weight=1,
        uniform="panels",
    )

    main.grid_columnconfigure(
        1,
        weight=1,
        uniform="panels",
    )

    # ---------------------------------------------------------
    # Editor panel
    # ---------------------------------------------------------

    editor_panel = tk.Frame(
        main,
        bg=panel,
        highlightbackground=border,
        highlightthickness=1,
    )

    editor_panel.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=(0, 3),
    )

    editor_panel.grid_rowconfigure(1, weight=1)
    editor_panel.grid_columnconfigure(0, weight=1)

    editor_label = tk.Label(
        editor_panel,
        text="SOURCE",
        bg=panel,
        fg=muted,
        font=label_font,
    )

    editor_label.grid(
        row=0,
        column=0,
        sticky="w",
        padx=14,
        pady=(12, 8),
    )

    editor = scrolledtext.ScrolledText(
        editor_panel,
        wrap=tk.NONE,
        undo=True,
        font=code_font,
        bg="#0b1220",
        fg=text,
        insertbackground="white",
        selectbackground="#1d4ed8",
        selectforeground="white",
        relief="flat",
        borderwidth=0,
        padx=12,
        pady=12,
    )

    editor.grid(
        row=1,
        column=0,
        sticky="nsew",
        padx=8,
        pady=(0, 8),
    )

    editor.insert(
        "1.0",
        'say "Hello from Prut!"\n\n'
        'set name = "Jed"\n'
        "say name\n\n"
        "set number = 10\n"
        "say number + 5\n\n"
        "if number >= 10\n"
        '    say "Number is 10 or greater."\n'
        "else\n"
        '    say "Number is less than 10."\n'
        "end\n",
    )

    # ---------------------------------------------------------
    # Output panel
    # ---------------------------------------------------------

    output_panel = tk.Frame(
        main,
        bg=panel,
        highlightbackground=border,
        highlightthickness=1,
    )

    output_panel.grid(
        row=0,
        column=1,
        sticky="nsew",
        padx=(3, 0),
    )

    output_panel.grid_rowconfigure(1, weight=1)
    output_panel.grid_columnconfigure(0, weight=1)

    output_label = tk.Label(
        output_panel,
        text="OUTPUT",
        bg=panel,
        fg=muted,
        font=label_font,
    )

    output_label.grid(
        row=0,
        column=0,
        sticky="w",
        padx=14,
        pady=(12, 8),
    )

    output = scrolledtext.ScrolledText(
        output_panel,
        wrap=tk.NONE,
        font=code_font,
        bg="#080d17",
        fg=output_text,
        insertbackground="white",
        selectbackground="#1d4ed8",
        selectforeground="white",
        relief="flat",
        borderwidth=0,
        padx=12,
        pady=12,
        state="disabled",
    )

    output.grid(
        row=1,
        column=0,
        sticky="nsew",
        padx=8,
        pady=(0, 8),
    )

    # ---------------------------------------------------------
    # Status bar
    # ---------------------------------------------------------

    status = tk.Label(
        root,
        text="Ready",
        bg=background,
        fg=muted,
        font=("Segoe UI", 9),
        anchor="w",
    )

    status.grid(
        row=2,
        column=0,
        sticky="ew",
        padx=16,
        pady=(0, 8),
    )

    # ---------------------------------------------------------
    # Functions
    # ---------------------------------------------------------

    def set_output(value: str) -> None:
        """Replace the output panel contents."""

        output.configure(state="normal")
        output.delete("1.0", tk.END)
        output.insert("1.0", value)
        output.configure(state="disabled")

    def run() -> None:
        """Run the code currently in the editor."""

        source = editor.get("1.0", tk.END).rstrip()

        if not source.strip():
            set_output("")
            status.configure(text="Nothing to run")
            return

        result = run_program(source)

        set_output(result)

        if result.startswith("Prut syntax error"):
            status.configure(text="Syntax error")

        elif result.startswith("Prut runtime error"):
            status.configure(text="Runtime error")

        elif result.startswith("Prut error"):
            status.configure(text="Error")

        else:
            status.configure(text="Program finished")

    def new_file() -> None:
        """Create a new empty Prut program."""

        if editor.get("1.0", tk.END).strip():
            answer = messagebox.askyesno(
                "New Program",
                "Clear the current program?",
            )

            if not answer:
                return

        editor.delete("1.0", tk.END)
        editor.insert("1.0", "")
        set_output("")
        status.configure(text="New program")

    def open_file() -> None:
        """Open a Prut source file."""

        filename = filedialog.askopenfilename(
            title="Open Prut Program",
            filetypes=[
                ("Prut files", "*.prut"),
                ("All files", "*.*"),
            ],
        )

        if not filename:
            return

        try:
            source = Path(filename).read_text(
                encoding="utf-8"
            )

            editor.delete("1.0", tk.END)
            editor.insert("1.0", source)

            set_output("")
            status.configure(
                text=f"Opened {Path(filename).name}"
            )

        except OSError as error:
            messagebox.showerror(
                "Open Error",
                str(error),
            )

    def save_file() -> None:
        """Save the current program."""

        filename = filedialog.asksaveasfilename(
            title="Save Prut Program",
            defaultextension=".prut",
            filetypes=[
                ("Prut files", "*.prut"),
                ("All files", "*.*"),
            ],
        )

        if not filename:
            return

        try:
            source = editor.get("1.0", tk.END)

            Path(filename).write_text(
                source,
                encoding="utf-8",
            )

            status.configure(
                text=f"Saved {Path(filename).name}"
            )

        except OSError as error:
            messagebox.showerror(
                "Save Error",
                str(error),
            )

    def clear_output() -> None:
        """Clear the output panel."""

        set_output("")
        status.configure(text="Output cleared")

    # ---------------------------------------------------------
    # Toolbar buttons
    # ---------------------------------------------------------

    new_button = make_button(
        toolbar,
        "New",
        new_file,
    )

    new_button.grid(
        row=0,
        column=2,
        padx=3,
    )

    open_button = make_button(
        toolbar,
        "Open",
        open_file,
    )

    open_button.grid(
        row=0,
        column=3,
        padx=3,
    )

    save_button = make_button(
        toolbar,
        "Save",
        save_file,
    )

    save_button.grid(
        row=0,
        column=4,
        padx=3,
    )

    clear_button = make_button(
        toolbar,
        "Clear",
        clear_output,
    )

    clear_button.grid(
        row=0,
        column=5,
        padx=3,
    )

    run_button = make_button(
        toolbar,
        "Run",
        run,
        primary=True,
    )

    run_button.grid(
        row=0,
        column=6,
        padx=(8, 3),
    )

    # ---------------------------------------------------------
    # Keyboard shortcuts
    # ---------------------------------------------------------

    root.bind(
        "<Control-r>",
        lambda event: run(),
    )

    root.bind(
        "<Control-s>",
        lambda event: save_file(),
    )

    root.bind(
        "<Control-o>",
        lambda event: open_file(),
    )

    root.bind(
        "<Control-n>",
        lambda event: new_file(),
    )

    # ---------------------------------------------------------
    # Start application
    # ---------------------------------------------------------

    editor.focus_set()

    root.mainloop()


if __name__ == "__main__":
    main()