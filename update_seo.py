
import os
import re

# Directory to scan
root_dir = r"c:\Users\tejan\Downloads\Journal Site"
components_dir = os.path.join(root_dir, "components")

# SEO Base Data
journal_name = "International Journal of Advanced Computing and Mechanical Systems"
journal_acronym = "IJACM"
keywords_base = "advanced computing, mechanical systems, engineering research, open access journal, peer reviewed, IJACM"

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Determine Title based on filename or existing title
    filename = os.path.basename(file_path)
    if "index" in filename:
        title = f"Home - {journal_name}"
        desc = f"Welcome to {journal_acronym}, a premier open-access journal publishing research in computing and mechanical engineering."
    elif "about" in filename:
        title = f"About Us - {journal_acronym}"
        desc = f"Learn about {journal_acronym}'s mission, editorial board, and commitment to open-access publishing."
    elif "submit" in filename:
        title = f"Submit Paper - {journal_acronym}"
        desc = "Submit your research paper to IJACM. Review our guidelines and submission process."
    elif "contact" in filename:
        title = f"Contact Us - {journal_acronym}"
        desc = "Contact IJACM editorial office for inquiries regarding submission, fees, or special issues."
    else:
        title = f"{filename.replace('.html', '').replace('-', ' ').title()} - {journal_acronym}"
        desc = f"Read about {filename.replace('.html', '').replace('-', ' ')} at {journal_acronym}."

    # 1. Update <title>
    if "<title>" in content:
        content = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", content)
    else:
        content = content.replace("<head>", f"<head>\n  <title>{title}</title>")

    # 2. Add/Update <meta name="description">
    meta_desc = f'<meta name="description" content="{desc}">'
    if 'name="description"' in content:
        content = re.sub(r'<meta name="description" content=".*?">', meta_desc, content)
    else:
        content = content.replace("</title>", f"</title>\n  {meta_desc}")

    # 3. Add/Update <meta name="keywords">
    meta_kw = f'<meta name="keywords" content="{keywords_base}">'
    if 'name="keywords"' in content:
        content = re.sub(r'<meta name="keywords" content=".*?">', meta_kw, content)
    else:
        content = content.replace("</title>", f"</title>\n  {meta_kw}")

    # 4. Add Viewport if missing
    if '<meta name="viewport"' not in content:
        content = content.replace("</title>", f"</title>\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">")

    # 5. Add Favicon (placeholder)
    # content = content.replace("</title>", f"</title>\n  <link rel=\"icon\" href=\"assets/favicon.ico\" type=\"image/x-icon\">")

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated SEO for {filename}")

# Walk thorough files
for subdir, dirs, files in os.walk(root_dir):
    # Skip components dir
    if components_dir in subdir:
        continue
    for file in files:
        if file.endswith(".html") and "components" not in subdir:
            process_file(os.path.join(subdir, file))
