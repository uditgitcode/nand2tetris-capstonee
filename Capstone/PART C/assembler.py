import sys
from pathlib import Path

K = 71

COMP_TABLE = {
    "0":   "0101010", "1":   "0111111", "-1":  "0111010",
    "D":   "0001100", "A":   "0110000", "M":   "1110000",
    "!D":  "0001101", "!A":  "0110001", "!M":  "1110001",
    "-D":  "0001111", "-A":  "0110011", "-M":  "1110011",
    "D+1": "0011111", "A+1": "0110111", "M+1": "1110111",
    "D-1": "0001110", "A-1": "0110010", "M-1": "1110010",
    "D+A": "0000010", "A+D": "0000010",
    "D+M": "1000010", "M+D": "1000010",
    "D-A": "0010011", "D-M": "1010011",
    "A-D": "0000111", "M-D": "1000111",
    "D&A": "0000000", "A&D": "0000000",
    "D&M": "1000000", "M&D": "1000000",
    "D|A": "0010101", "A|D": "0010101",
    "D|M": "1010101", "M|D": "1010101",
}

DEST_TABLE = {
    "":    "000", "M":   "001", "D":   "010", "MD":  "011", "DM": "011",
    "A":   "100", "AM":  "101", "AD":  "110", "AMD": "111",
}

JUMP_TABLE = {
    "":    "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111",
}


def build_symbol_table() -> dict[str, int]:
    symbols = {
        "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
        "SCREEN": 16384, "KBD": 24576,
    }
    for i in range(16):
        symbols[f"R{i}"] = i
    return symbols


def clean_line(line: str) -> str:
    return line.split("//", 1)[0].strip()


def assemble(asm_file: Path) -> None:
    raw_lines = asm_file.read_text(encoding="utf-8").splitlines()
    symbols = build_symbol_table()
    declared_labels: set[str] = set()
    instructions: list[str] = []

    rom_address = 0
    for line_no, raw in enumerate(raw_lines, start=1):
        code = clean_line(raw)
        if not code:
            continue

        if code.startswith("(") and code.endswith(")"):
            label = code[1:-1].strip()
            if K % 3 == 2 and label in declared_labels:
                print(f"Warning (Line {line_no}): Label '{label}' is written more than once.")
            else:
                declared_labels.add(label)
                symbols[label] = rom_address
        else:
            instructions.append(code)
            rom_address += 1

    next_ram_address = 16
    hack_lines: list[str] = []

    for inst in instructions:
        if inst.startswith("@"):
            symbol = inst[1:].strip()
            if symbol.isdigit():
                address = int(symbol)
            else:
                if symbol not in symbols:
                    symbols[symbol] = next_ram_address
                    next_ram_address += 1
                address = symbols[symbol]
            hack_lines.append(f"0{address:015b}")
        else:
            dest, comp, jump = "", inst, ""
            if "=" in comp:
                dest, comp = [part.strip() for part in comp.split("=", 1)]
            if ";" in comp:
                comp, jump = [part.strip() for part in comp.split(";", 1)]

            binary = f"111{COMP_TABLE[comp]}{DEST_TABLE[dest]}{JUMP_TABLE[jump]}"
            hack_lines.append(binary)

    out_file = asm_file.with_suffix(".hack")
    out_file.write_text("\n".join(hack_lines) + "\n", encoding="utf-8")
    print(f"Success: {asm_file.name} -> {out_file.name} ({len(hack_lines)} instructions)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python assembler.py <filename.asm>")
        sys.exit(1)
    assemble(Path(sys.argv[1]))
