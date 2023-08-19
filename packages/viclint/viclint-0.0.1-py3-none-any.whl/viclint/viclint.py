import click
import os

INDENTED_STATEMENTS = [
    "If",
    "In",
    "UseCamera",
]

DEDENT_STATEMENTS = [
    "End",
    "Endin",
    "EndCamera",
]

@click.command()
@click.argument('path', default=".")
def main(path):
    files = []

    if os.path.isfile(path):
        files.append(path)
    else:
        for file in os.listdir(path):
            # if file doesn't end in .vic, skip
            if not file.lower().endswith(".vic"):
                continue

            files.append(os.path.join(path, file))

    for file in files:
        try:
            print(f"🪄 Linting {file}...")
            with open(file, 'r') as f:
                lines = f.readlines()

            result = []

            is_in_indented_context = 0

            for i, line in enumerate(lines):
                current_line = line.rstrip("\n")
                
                # if last line starts with any indented statement
                if current_line.startswith(tuple(INDENTED_STATEMENTS)):
                    is_in_indented_context = is_in_indented_context + 1
                    result.append(current_line + "\n")
                    continue

                if current_line.startswith(tuple(DEDENT_STATEMENTS)):
                    is_in_indented_context = is_in_indented_context - 1

                if not current_line.startswith("    ") and is_in_indented_context:
                    # add indent
                    current_line = "    " * is_in_indented_context + current_line

                result.append(current_line + "\n")

            contents = "".join(result)

            with open(file, 'w+') as f:
                f.write(contents)

            print(f"✨ {file} is now prettier! ✨")
        except:
            print(f"🚨 {file} failed to lint.")

if __name__ == '__main__':
    main()