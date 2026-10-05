"""Interactive REPL for the Prut programming language."""

import ctypes
import re
import sys

from . import __version__
from .interpreter import Interpreter
from .lexer import Lexer
from .parser import Parser


# ---------------------------------------------------------
# Enable ANSI colours on Windows
# ---------------------------------------------------------

def enable_ansi_colors() -> None:
    """Enable ANSI escape sequences in Windows terminals."""

    if sys.platform != "win32":
        return

    try:
        kernel32 = ctypes.windll.kernel32

        # STD_OUTPUT_HANDLE = -11
        stdout_handle = kernel32.GetStdHandle(-11)

        # Get current console mode.
        mode = ctypes.c_ulong()

        if kernel32.GetConsoleMode(
            stdout_handle,
            ctypes.byref(mode),
        ):
            # ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
            kernel32.SetConsoleMode(
                stdout_handle,
                mode.value | 0x0004,
            )

    except (AttributeError, OSError):
        pass


# ---------------------------------------------------------
# Prut terminal banner
# ---------------------------------------------------------

BANNER = r"""
[size=9px][font=monospace][color=#808080]<span style="color:#808080"> [/color]</span>
[color=#808080][/color][color=#808080]                                                           [/color][color=#647497],[/color]
[color=#808080][/color][color=#808080]         [/color][color=#5c606f]╔[/color][color=#2b3458]▓[/color][color=#2f375a]▓[/color][color=#6c6e76]⌐                                             [/color][color=#1a56d4]╣[/color][color=#1655d7]╣[/color][color=#1655d7]╣[/color]
[color=#808080][/color][color=#808080]         [/color][color=#2b3458]▓[/color][color=#0f1b4b]▓[/color][color=#0f1b4b]▓[/color][color=#474d65]▌                                             [/color][color=#1655d7]╣[/color][color=#1655d7]╣╣[/color]
[color=#808080][/color][color=#808080]         [/color][color=#2b3458]▓[/color][color=#0f1b4b]▓[/color][color=#0f1b4b]▓[/color][color=#474d65]▌   [/color][color=#95716a],[/color][color=#b05e4f]╖[/color][color=#c2523d]@[/color][color=#cb4b34]@[/color][color=#cd4a32]@[/color][color=#c74e38]@[/color][color=#bb5744]╗[/color][color=#a4665b]╖      [/color][color=#a68c59]╓[/color][color=#c0943f]╖[/color][color=#ce9931]╥[/color][color=#d59b2a]H[/color][color=#d39b2c]H[/color][color=#ca9835]╥[/color][color=#b79248]╖[/color][color=#9a8865].     [/color][color=#6d837c],[/color][color=#4c8976]╦[/color][color=#368d72]@[/color][color=#2a8f70]▓[/color][color=#278f6f]▓[/color][color=#2c8e70]▄[/color][color=#398c72]@[/color][color=#518877]╗[/color][color=#4d8976]æ[/color][color=#378c72]@[/color][color=#4b8976]╗    [/color][color=#1655d7]╣[/color][color=#1655d7]╣╣    [/color][color=#9a6d65],[/color][color=#b05e4f]╖[/color][color=#be5441]╗[/color][color=#c2513d]%[/color][color=#c1533e]H[/color][color=#b85947]╗[/color][color=#a66559]╖[/color]
[color=#808080][/color][color=#808080]         [/color][color=#2b3458]▓[/color][color=#0f1b4b]▓[/color][color=#0f1b4b]▓[/color][color=#474d65]▌ [/color][color=#996e66],[/color][color=#d64429]╢[/color][color=#e13c1e]▒[/color][color=#e13c1e]▒[/color][color=#db4024]╣[/color][color=#c94d36]╝[/color][color=#c5503a]╝[/color][color=#d0482f]║[/color][color=#e13c1e]╣[/color][color=#e13c1e]▒[/color][color=#e13c1e]╣[/color][color=#bc5543]╗  [/color][color=#bd9442]╓[/color][color=#eba214]▒[/color][color=#eca314]▒[/color][color=#eba214]▒[/color][color=#da9d25]╨[/color][color=#cd9832]╜[/color][color=#d0992f]╜[/color][color=#e3a01c]║[/color][color=#eca314]▒[/color][color=#eca314]▒[/color][color=#e3a01c]║[/color][color=#a28b5d], [/color][color=#6d837c],[/color][color=#23906e]▓[/color][color=#10946b]▓[/color][color=#10946b]▓[/color][color=#14936b]▓[/color][color=#298f6f]▀[/color][color=#308e71]▀[/color][color=#26906f]▀[/color][color=#11936b]▓[/color][color=#10946b]▓[/color][color=#10946b]▓▓▓    [/color][color=#1655d7]╣[/color][color=#1655d7]╣╣  [/color][color=#b45b4b]╔[/color][color=#df3e20]╣[/color][color=#e13c1e]▒[/color][color=#e13c1e]▒[/color][color=#da4125]╣[/color][color=#d0482f]Ñ[/color][color=#d4452b]Ñ[/color][color=#e03c1f]╣[/color][color=#e13c1e]▒[/color][color=#e13c1e]▒[/color][color=#cc4a33]@[/color]
[color=#808080][/color][color=#808080]         [/color][color=#2b3458]▓[/color][color=#0f1b4b]▓[/color][color=#0f1b4b]▓[/color][color=#474d65]▌ [/color][color=#e13c1e]▒[/color][color=#e13c1e]▒[/color][color=#e03d1f]╣  [/color][color=#474d65]▄[/color][color=#54586b]N[/color][color=#626672]╖ [/color][color=#c4503b]╚[/color][color=#e13c1e]▒[/color][color=#e13c1e]▒[/color][color=#c94d36]@[/color][color=#c89737]║[/color][color=#eca314]▒[/color][color=#eca314]▒[/color][color=#d49b2b]╜ [/color][color=#5e6170]╓[/color][color=#404762]▄[/color][color=#636672]═  [/color][color=#e8a117]╠[/color][color=#eca314]▒[/color][color=#eca314]▒[/color][color=#928760]~[/color][color=#12936b]▓[/color][color=#10946b]▓[/color][color=#10946b]▓[/color][color=#538777]╜     [/color][color=#408b74]▐[/color][color=#10946b]▓[/color][color=#10946b]▓▓    [/color][color=#1655d7]╣[/color][color=#1655d7]╣╣ [/color][color=#c64f39]║[/color][color=#e13c1e]▒[/color][color=#e13c1e]▒[/color][color=#e03d1f]╣[/color][color=#b75948]╖[/color][color=#ab6254]╖[/color][color=#ab6254]╖╖[/color][color=#ac6053]╖[/color][color=#d2462d]║[/color][color=#e13c1e]▒[/color][color=#e13c1e]▒[/color][color=#e03d1f]╣[/color]
[color=#808080][/color][color=#808080]         [/color][color=#2b3458]▓[/color][color=#0f1b4b]▓[/color][color=#0f1b4b]▓[/color][color=#474d65]▌[/color][color=#a76458]][/color][color=#e13c1e]▒[/color][color=#e13c1e]▒[/color][color=#d5442a]╢ [/color][color=#494e66]▐[/color][color=#0f1b4b]▓[/color][color=#1b2651]▓[/color][color=#1b2651]▓ [/color][color=#9c6c63]][/color][color=#e13c1e]▒[/color][color=#e13c1e]▒[/color][color=#de3e21]╣[/color][color=#e4a01b]║[/color][color=#eca314]▒[/color][color=#eca314]▒[/color][color=#a88d57]⌐ [/color][color=#1a2550]▓[/color][color=#0f1b4b]█[/color][color=#212b53]▓[/color][color=#414762]▌ [/color][color=#d99c26]║[/color][color=#eca314]▒[/color][color=#eca314]▒[/color][color=#968b3f]Ü[/color][color=#10946b]▓[/color][color=#10946b]▓▓       ▓▓▓    [/color][color=#1655d7]╣[/color][color=#1655d7]╣╣ [/color][color=#e03c1f]╣[/color][color=#e13c1e]▒[/color][color=#e13c1e]▒▒▒▒▒▒▒▒▒▒[/color][color=#dd3f22]╣[/color][color=#986f67]`[/color]
[color=#7b7b7d][/color][color=#7b7b7d] [/color][color=#4d5268]▄[/color][color=#484e66]▄[/color][color=#6e7077],     [/color][color=#2b3458]▓[/color][color=#0f1b4b]▓[/color][color=#0f1b4b]▓[/color][color=#474d65]▌ [/color][color=#d2472d]║[/color][color=#e13c1e]▒[/color][color=#e13c1e]▒[/color][color=#ca4c35]@[/color][color=#a06960],  [/color][color=#93716b].[/color][color=#b15d4e]╖[/color][color=#de3e21]╣[/color][color=#e13c1e]▒[/color][color=#e13c1e]╣[/color][color=#a4675b]`[/color][color=#a08a5f]'[/color][color=#eba214]▒[/color][color=#eca314]▒[/color][color=#eaa215]▒[/color][color=#ba9245]╖[/color][color=#978768].  [/color][color=#a08a5f],[/color][color=#ce9931]╥[/color][color=#eca314]▒[/color][color=#eca314]▒[/color][color=#df9e20]╝ [/color][color=#2e8e70]▐[/color][color=#10946b]▓[/color][color=#10946b]▓[/color][color=#21906e]▓[/color][color=#558778]╖[/color][color=#6e837c], [/color][color=#6b837c],[/color][color=#4e8876]æ[/color][color=#18926c]▓[/color][color=#10946b]▓[/color][color=#10946b]▓▓    [/color][color=#1655d7]╣[/color][color=#1655d7]╣╣ [/color][color=#b05e4f]╙[/color][color=#e13c1e]▒[/color][color=#e13c1e]▒[/color][color=#da4125]╣[/color][color=#a66559]╖   [/color][color=#967069],[/color][color=#bb5744]╗[/color][color=#c74e38]@[/color][color=#ae5f51]╖[/color]
[color=#555a6c][/color][color=#555a6c]▐[/color][color=#0f1b4b]▓[/color][color=#0f1b4b]▓[/color][color=#1a2550]█     [/color][color=#1d2852]▓[/color][color=#0f1b4b]▓[/color][color=#0f1b4b]▓[/color][color=#505569]P  [/color][color=#a86357]╙[/color][color=#d1472e]║[/color][color=#e13c1e]╢[/color][color=#e13c1e]▒[/color][color=#e13c1e]▒▒▒▒[/color][color=#de3e21]╣[/color][color=#bf5440]╜    [/color][color=#c3953c]╙[/color][color=#e6a119]║[/color][color=#eca314]▒[/color][color=#eca314]▒▒▒▒▒[/color][color=#dd9e22]╝[/color][color=#b1904e]"   [/color][color=#598678]╙[/color][color=#288f6f]▀[/color][color=#10936b]▓[/color][color=#10946b]▓[/color][color=#10946b]▓▓▓▓[/color][color=#11936b]▓▓▓▓    [/color][color=#1956d5]╣[/color][color=#1655d7]╣[/color][color=#1655d7]╣   [/color][color=#cb4b34]╝[/color][color=#e13c1e]╣[/color][color=#e13c1e]▒[/color][color=#e13c1e]▒▒▒▒▒[/color][color=#da4125]╣[/color][color=#b15e4e]╜[/color]
[color=#7f7f7f][/color][color=#7f7f7f] [/color][color=#323a5b]▀[/color][color=#0f1b4b]▓[/color][color=#0f1b4b]▓[/color][color=#15214e]█[/color][color=#373f5e]▄[/color][color=#434963]▄[/color][color=#39405e]▄[/color][color=#17224f]█[/color][color=#0f1b4b]▓[/color][color=#0f1b4b]▓[/color][color=#2d3659]▀                                   [/color][color=#5e8679]`   [/color][color=#10946b]▓[/color][color=#10946b]▓▓             [/color][color=#a4665b]`[/color][color=#a96256]"[/color][color=#a76458]"[/color]
[color=#808080][/color][color=#808080]   [/color][color=#414762]▀[/color][color=#263056]▓[/color][color=#17224f]█[/color][color=#121e4d]█[/color][color=#16224f]█[/color][color=#252f55]▓[/color][color=#3f4661]▀[/color][color=#686b75]`                              [/color][color=#64847a]╒[/color][color=#14936b]▓[/color][color=#10936b]▓[/color][color=#348d71]▄     [/color][color=#388c72]▐[/color][color=#10946b]▓[/color][color=#10946b]▓[/color][color=#1e916d]▓[/color]
[color=#808080][/color][color=#808080]                                          [/color][color=#3f8b73]╚[/color][color=#11936b]▓[/color][color=#10946b]▓[/color][color=#10946b]▓[/color][color=#18926c]▓[/color][color=#22906e]▓[/color][color=#1b926d]▓[/color][color=#10946b]▓[/color][color=#10946b]▓[/color][color=#10936b]▓[/color][color=#388c72]▀[/color]
[color=#808080][/color][color=#808080]                                            [/color][color=#5f8579]`[/color][color=#488975]╙[/color][color=#388c72]▀[/color][color=#348d71]▀[/color][color=#388c72]▀[/color][color=#468a75]╩[/color][color=#5b8679]"[/color]

[/font][/size]
"""


def render_banner(banner: str) -> str:
    """Convert BBCode colour tags into ANSI terminal colours."""

    def replace_color(match):
        color = match.group(1).lstrip("#")

        red = int(color[0:2], 16)
        green = int(color[2:4], 16)
        blue = int(color[4:6], 16)

        return f"\033[38;2;{red};{green};{blue}m"

    # Convert [color=#RRGGBB] to ANSI true-colour.
    banner = re.sub(
        r"\[color=(#[0-9A-Fa-f]{6})\]",
        replace_color,
        banner,
    )

    # Reset colour.
    banner = re.sub(
        r"\[/color\]",
        "\033[0m",
        banner,
    )

    # Remove BBCode formatting tags.
    banner = re.sub(
        r"\[/?(?:size|font)(?:=[^\]]+)?\]",
        "",
        banner,
    )

    # Remove HTML tags.
    banner = re.sub(
        r"<[^>]+>",
        "",
        banner,
    )

    return banner + "\033[0m"


def run_source(source: str, interpreter: Interpreter) -> None:
    """Parse and execute Prut source code."""

    lexer = Lexer(source)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    program = parser.parse()

    interpreter.run(program)


def _needs_more_input(source: str) -> bool:
    """Check whether a Prut block needs more input."""

    depth = 0

    lexer = Lexer(source)

    try:
        tokens = lexer.tokenize()
    except SyntaxError:
        return False

    for token in tokens:
        if token.type.name != "KEYWORD":
            continue

        if token.value == "if":
            depth += 1

        elif token.value == "end":
            depth -= 1

    return depth > 0


def run_repl() -> None:
    """Start the interactive Prut shell."""

    enable_ansi_colors()

    print(render_banner(BANNER))
    print()

    print(f"Prut {__version__}")
    print("Interactive shell")
    print("Type 'exit' or 'quit' to leave.")
    print()

    interpreter = Interpreter()

    while True:
        try:
            source = input(">>> ")

        except EOFError:
            print()
            break

        except KeyboardInterrupt:
            print()
            break

        command = source.strip()

        if not command:
            continue

        if command in {"exit", "quit"}:
            break

        lines = [source]

        while _needs_more_input("\n".join(lines)):
            try:
                line = input("... ")

            except EOFError:
                print()
                return

            except KeyboardInterrupt:
                print()
                break

            if line.strip() in {"exit", "quit"}:
                print("Cannot exit while a block is open.")
                continue

            lines.append(line)

        source = "\n".join(lines)

        try:
            run_source(source, interpreter)

        except (SyntaxError, RuntimeError) as error:
            print(f"Prut error: {error}")


if __name__ == "__main__":
    run_repl()