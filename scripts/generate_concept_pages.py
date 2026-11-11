from html import escape
from pathlib import Path

from rdflib import Graph, Namespace, RDF

# Define RDF namespaces used later to access SKOS and Dublin Core properties.
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
DCTERMS = Namespace("http://purl.org/dc/terms/")

# Resolve paths relative to this script so the project can be generated
# from any working directory and always target the repository root.
repository = Path(__file__).resolve().parent.parent
ttl_file = repository / "ontology.ttl"
output_directory = repository / "docs" / "concept"
repository_code_url = "https://github.com/psymarkus/sharp-concepts"
repository_code_meta = (
    '<meta name="repository-code" '
    f'content="{repository_code_url}">'
)

# Build the citation block used in every generated HTML page so the dataset is
# attributed consistently in the page footer.
citation_apa = escape(
    "Gödker, M., Richters, C., Chernikova, O., "
    "Holzberger, D., Stadler, M., Bauer, E., Brandl, L., Braun, L., "
    "Cleverley-Kornmayer, A., Fischer, M., Frenzel, A., Gollwitzer, M., "
    "Heitzmann, N., Hofer, S., Koenen, J., Küchemann, S., Lewalter, D., "
    "Michaeli, T., Munk, S., ... Fischer, F. (2026). "
    "SHARP Concepts Ontology (Version 0.2.0) [Computer software]. "
    "https://w3id.org/sharp/"
)

citation_bibtex = """@software{Goedker_SHARP_Concepts_2026,
author = {Gödker, Markus and Richters, Constanze and Chernikova, Olga and Holzberger, Doris and Stadler, Matthias and Bauer, Elisabeth and Brandl, Laura and Braun, Leah and Cleverley-Kornmayer, Anne and Fischer, Martin and Frenzel, Anne and Gollwitzer, Mario and Heitzmann, Nicole and Hofer, Sarah and Koenen, Jenna and Küchemann, Stefan and Lewalter, Doris and Michaeli, Tilman and Munk, Simon and Neuhaus, Birgit and Obersteiner, Andreas and Oezsoy, Melissa and Sailer, Michael and Schmidmaier, Ralf and Schmidt-Hertha, Bernhard and Schneiderbauer, Paul and Traub, Dagmar and Ufer, Stefan and Weiss, Eva and Fischer, Frank},
date = {2026-10-01},
title = {{SHARP Concepts Ontology}},
url = {https://w3id.org/sharp/},
version = {0.2.0}
}"""
citation_footer = f"""
    <footer>
        <h2>Citation</h2>
        <p>Repository: <a href="{repository_code_url}">{repository_code_url}</a></p>
        <p>{citation_apa}</p>
        <pre>{escape(citation_bibtex)}</pre>
    </footer>
"""

# Fail early if the ontology source file is missing so the generator does not
# silently create incomplete output.
if not ttl_file.exists():
    raise FileNotFoundError(
        f"Die Datei wurde nicht gefunden: {ttl_file}"
    )

# Make sure the target folder exists before writing any concept pages.
output_directory.mkdir(parents=True, exist_ok=True)

# Parse the Turtle ontology into an RDF graph so the script can query SKOS
# concepts and their labels, definitions, and alternative labels.
graph = Graph()
graph.parse(ttl_file, format="turtle")

# Collect every resource declared as a SKOS concept, sort them for stable output,
# and print a quick summary for the user.
concepts = sorted(
    set(graph.subjects(RDF.type, SKOS.Concept)),
    key=str
)

print(f"RDF-Tripel geladen: {len(graph)}")
print(f"SKOS-Konzepte gefunden: {len(concepts)}")

# Track created files and the concept metadata needed for the index page.
created_files = 0
concept_list = []

shared_css = """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --primary-color: #387D77;
            --text-color: #000000;
            --font-family: 'Roboto', sans-serif;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        header {
            background-color: var(--primary-color);
            color: white;
            padding: 15px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        header a {
            color: white;
            text-decoration: none;
            font-weight: 700;
            font-size: 1.2rem;
        }

        body {
            font-family: var(--font-family);
            color: var(--text-color);
            line-height: 1.6;
            margin: 0 ;
            padding: 0;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }

        main {
            max-width: 800px;  /* Restricts the text block from getting too wide */
            width: 100%;       /* Ensures it still fits nicely on smaller screens */
            margin: 0 auto;    /* Centers the 800px column on the screen */
            padding: 40px 20px;
            box-sizing: border-box;
            flex: 1;
            text-align: left;  /* Explicitly aligns all text to the left */
        }

        h1, h2 {
            color: var(--primary-color);
            font-weight: 600;
        }

        a {
            color: var(--primary-color);
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        .back-button {
            display: inline-block;
            margin-bottom: 20px;
            padding: 8px 16px;
            background-color: var(--primary-color);
            color: white;
            border-radius: 4px;
        }
        .back-button:hover {
            text-decoration: none;
            opacity: 0.9;
        }
        footer {
            background-color: var(--primary-color); /* Dark teal background */
            color: white;                             /* White text */
            padding: 40px;
            font-size: 0.9rem;
            margin-top: auto;
        }

        footer h2 {
            color: white;
            font-size: 1.2rem;
            margin-bottom: 15px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2); /* Subtle white divider line */
            padding-bottom: 10px;
        }

        footer p {
            color: white;
            margin-bottom: 10px;
        }

        footer a {
            color: #aae0de; /* A lighter pastel teal so links stand out against the dark background */
            text-decoration: underline;
        }
        
        footer a:hover {
            color: white;
        }
        
        footer pre {
            background-color: rgba(0, 0, 0, 0.25); /* Semi-transparent dark box for the BibTeX code */
            color: white;
            padding: 15px;
            border-radius: 4px;
            overflow-x: auto;
            margin-top: 15px;
            font-size: 0.85rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .footer-wrapper {
            background-color: var(--primary-color);
            width: 100%;
            margin-top: auto;
        }
    </style>
"""


# Generate one HTML page per concept using the ontology data.
for concept in concepts:
    identifier_value = graph.value(concept, DCTERMS.identifier)
    label_value = graph.value(concept, SKOS.prefLabel)
    definition_value = graph.value(concept, SKOS.definition)

    # If no explicit identifier exists, fall back to the last segment of the IRI.
    if identifier_value:
        identifier = str(identifier_value)
    else:
        identifier = str(concept).rstrip("/").split("/")[-1]

    label = str(label_value) if label_value else identifier
    definition = (
        str(definition_value)
        if definition_value
        else "No definition available."
    )

    concept_list.append((identifier, label))

    # Aggregate alt labels into HTML list items for display on the page.
    alternative_labels = sorted(
        {str(value) for value in graph.objects(concept, SKOS.altLabel)}
    )

    if alternative_labels:
        alt_label_html = "".join(
            f"<li>{escape(value)}</li>"
            for value in alternative_labels
        )
        alt_label_html = f"<ul>{alt_label_html}</ul>"
    else:
        alt_label_html = "<p>No alternative labels available.</p>"

    # Render the final HTML for this single concept page.
    html = f"""<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    {repository_code_meta}
    <title>{escape(label)} | SHARP Concept Scheme</title>
    {shared_css}
</head>
<body>

    <main>
        <p><a href="../index.html" class="back-button">Back to index</a></p>
        <h1>{escape(label)}</h1>

        <h2>IRI</h2>
        <p>
            <a href="{escape(str(concept), quote=True)}">
                {escape(str(concept))}
            </a>
        </p>

        <h2>Identifier</h2>
        <p>{escape(identifier)}</p>

        <h2>Preferred label</h2>
        <p>{escape(label)}</p>

        <h2>Alternative labels</h2>
        {alt_label_html}

        <h2>Definition</h2>
        <p>{escape(definition)}</p>
    </main>

    <div class="footer-wrapper">
    {citation_footer} 
    </div>
</body>
</html>
"""

    # Save the generated page to the docs/concept folder.
    output_file = output_directory / f"{identifier}.html"
    output_file.write_text(html, encoding="utf-8")

    print(f"Erstellt: {output_file.relative_to(repository)}")
    created_files += 1

# Sort the concept list by label so the index page is alphabetized and easier to
# navigate.
concept_list = sorted(concept_list, key=lambda x: x[1])

# Build the landing page that links to every concept page.
index_html = f"""
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    {repository_code_meta}
    <title>SHARP Concept Scheme</title>
    {shared_css}
</head>
<body>
    <main>
        <h1>SHARP Concept Scheme</h1>

        <ul>
"""

for identifier, label in concept_list:
    index_html += (
        f'<li><a href="concept/{identifier}.html">'
        f'{label} ({identifier})'
        f'</a></li>'
    )

index_html += """
    </ul>
</main>
    <div class="footer-wrapper">
    """ + citation_footer + """
    </div>
</body>
</html>
"""

# Write the generated index file into the docs directory.
(repository / "docs" / "index.html").write_text(
    index_html,
    encoding="utf-8"
)

# Inform the user how many concept pages were generated.
print(f"Fertig. {created_files} HTML-Dateien wurden erstellt.")