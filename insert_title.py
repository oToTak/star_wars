import re
import sys


def insert_title(yaml_path, block_path, not_watched_path=None):
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

    if not_watched_path:
        remove_watched_titles(not_watched_path, block)


def _normalize(s):
    return re.sub(r"[^a-zа-яіїєґ0-9]+", "", s.lower())


def remove_watched_titles(not_watched_path, block):
    titles = re.findall(r'title:\s*"([^"]+)"', block)
    if not titles:
        return

    try:
        with open(not_watched_path, "r", encoding="utf-8") as f:
            md_lines = f.readlines()
    except FileNotFoundError:
        return

    norm_titles = [_normalize(t) for t in titles]

    removed = []
    kept_lines = []
    for line in md_lines:
        stripped = line.strip()
        if stripped.startswith("- "):
            item = stripped[2:].strip()
            norm_item = _normalize(item)
            match = norm_item and any(
                norm_item in nt or nt in norm_item for nt in norm_titles
            )
            if match:
                removed.append(item)
                continue
        kept_lines.append(line)

    if removed:
        with open(not_watched_path, "w", encoding="utf-8") as f:
            f.writelines(kept_lines)
        print("Removed from not_watched_yet.md: " + ", ".join(removed))


if __name__ == "__main__":
    yaml_arg = sys.argv[1]
    block_arg = sys.argv[2]
    not_watched_arg = sys.argv[3] if len(sys.argv) > 3 else None
    insert_title(yaml_arg, block_arg, not_watched_arg)
