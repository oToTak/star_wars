import sys

def insert_title(yaml_path, block_path):
    with open(yaml_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    with open(block_path, "r", encoding="utf-8") as f:
        block = f.read()
    if not block.endswith("\n"):
        block += "\n"

    anchor_idx = None
    for i, line in enumerate(lines):
        if line.startswith("evolution_log:"):
            anchor_idx = i
            break

    if anchor_idx is None:
        raise SystemExit("Anchor 'evolution_log:' not found, aborting to avoid corrupting file")

    j = anchor_idx
    while j > 0 and lines[j - 1].strip() == "":
        j -= 1

    new_lines = lines[:j] + [block, "\n"] + lines[j:]

    with open(yaml_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    insert_title(sys.argv[1], sys.argv[2])
