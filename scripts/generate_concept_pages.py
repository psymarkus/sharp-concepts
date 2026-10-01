from html import escape
from pathlib import Path

from rdflib import Graph, Namespace, RDF

SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
DCTERMS = Namespace("http://purl.org/dc/terms/")

# Pfade relativ zum Speicherort dieses Skripts bestimmen
repository = Path(__file__).resolve().parent.parent
ttl_file = repository / "ontology.ttl"
output_directory = repository / "docs" / "concept"

citation_apa = escape(
    "Gödker, M., Richters, C., Chernikova, O., "
    "Holzberger, D., Stadler, M., Bauer, E., Brandl, L., Braun, L., "
    "Cleverley-Kornmayer, A., Fischer, M., Frenzel, A., Gollwitzer, M., "
    "Heitzmann, N., Hofer, S., Koenen, J., Küchemann, S., Lewalter, D., "
    "Michaeli, T., Munk, S., ... Fischer, F. (2026). "
    "SHARP Concepts Ontology (Version 0.2.0) [Computer software]. "
    "https://w3id.org/sharp/ontology"
)

citation_bibtex = """@software{Goedker_SHARP_Concepts_2026,
author = {Gödker, Markus and Richters, Constanze and Chernikova, Olga and Holzberger, Doris and Stadler, Matthias and Bauer, Elisabeth and Brandl, Laura and Braun, Leah and Cleverley-Kornmayer, Anne and Fischer, Martin and Frenzel, Anne and Gollwitzer, Mario and Heitzmann, Nicole and Hofer, Sarah and Koenen, Jenna and Küchemann, Stefan and Lewalter, Doris and Michaeli, Tilman and Munk, Simon and Neuhaus, Birgit and Obersteiner, Andreas and Oezsoy, Melissa and Sailer, Michael and Schmidmaier, Ralf and Schmidt-Hertha, Bernhard and Schneiderbauer, Paul and Traub, Dagmar and Ufer, Stefan and Weiss, Eva and Fischer, Frank},
date = {2026-10-01},
title = {{SHARP Concepts Ontology}},
url = {https://w3id.org/sharp/ontology},
version = {0.2.0}
}"""
citation_footer = f"""
    <footer>
        <h2>Citation</h2>
        <p>{citation_apa}</p>
        <pre>{escape(citation_bibtex)}</pre>
    </footer>
"""

if not ttl_file.exists():
    raise FileNotFoundError(
        f"Die Datei wurde nicht gefunden: {ttl_file}"
    )

output_directory.mkdir(parents=True, exist_ok=True)

graph = Graph()
graph.parse(ttl_file, format="turtle")

# Alle Ressourcen mit rdf:type skos:Concept ermitteln
concepts = sorted(
    set(graph.subjects(RDF.type, SKOS.Concept)),
    key=str
)

print(f"RDF-Tripel geladen: {len(graph)}")
print(f"SKOS-Konzepte gefunden: {len(concepts)}")

created_files = 0
concept_list = []

for concept in concepts:
    identifier_value = graph.value(concept, DCTERMS.identifier)
    label_value = graph.value(concept, SKOS.prefLabel)
    definition_value = graph.value(concept, SKOS.definition)


    # Falls dcterms:identifier fehlt, den letzten Teil der IRI verwenden
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

    html = f"""<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(label)} | SHARP Concept Scheme</title>
</head>
<body>
    <main>
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
    {citation_footer}
</body>
</html>
"""
    
    
    output_file = output_directory / f"{identifier}.html"
    output_file.write_text(html, encoding="utf-8")


    print(f"Erstellt: {output_file.relative_to(repository)}")
    created_files += 1 

concept_list = sorted(concept_list, key=lambda x: x[1])

index_html = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>SHARP Concept Scheme</title>
</head>
<body>
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
""" + citation_footer + """
</body>
</html>
"""

(repository / "docs" / "index.html").write_text(
    index_html,
    encoding="utf-8"
)
  
   


print(f"Fertig. {created_files} HTML-Dateien wurden erstellt.")