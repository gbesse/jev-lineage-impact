# Jev OpenLineage Impact

## Français

**But.** Comparer deux versions d'un schéma OpenLineage avec des usages aval documentés. Jev classe l'effet plausible en `impact`, `low` ou `review` ; la suppression d'un champ ou un changement de type force une revue humaine. Les chemins exacts des champs concernés figurent dans le résultat. Aucun déploiement ni schéma n'est modifié.

**Entrée.** Un JSON `{"before":<RunEvent>,"after":<RunEvent>,"consumers":[{"name":"...","purpose":"...","columns":["..."]}]}`. Chaque événement doit contenir exactement un jeu de données dans `outputs`, avec `facets.schema.fields`. La [spécification OpenLineage](https://openlineage.io/docs/spec/object-model/) documente les événements et la [facette schema](https://openlineage.io/docs/spec/facets/dataset-facets/). Les usages aval sont fournis explicitement : ce prototype ne découvre pas automatiquement tous les consommateurs. Jev ne reçoit aucune ligne de données, seulement les définitions des champs modifiés et les usages déclarés.

**Utilisation.** Installez `python3 -m pip install -r requirements.txt`, puis lancez `python3 app.py --demo`. Pour une revue réelle, chargez `TYPESAFE_API_KEY` dans l'environnement et lancez `python3 app.py --input chemin/vers/dossier.json`. Tests : `python3 -m unittest discover -s tests -v`. Les descriptions de champs peuvent être sensibles ; vérifiez les métadonnées avant transmission. Ce livrable traite un jeu de données par dossier.

## English

**Purpose.** Compare two OpenLineage schema versions against documented downstream uses. Jev classifies plausible impact as `impact`, `low`, or `review`; removing a field or changing its type forces human review. The result contains exact paths for affected fields. It changes no deployment or schema.

**Input.** A JSON `{"before":<RunEvent>,"after":<RunEvent>,"consumers":[{"name":"...","purpose":"...","columns":["..."]}]}`. Each event must contain exactly one dataset in `outputs` with `facets.schema.fields`. See the [OpenLineage event model](https://openlineage.io/docs/spec/object-model/) and [schema facet](https://openlineage.io/docs/spec/facets/dataset-facets/). Downstream uses are supplied explicitly: this prototype does not discover every consumer automatically. Jev receives no data rows, only changed field definitions and declared uses.

**Run.** Install `python3 -m pip install -r requirements.txt`, then run `python3 app.py --demo`. For a real review, load `TYPESAFE_API_KEY` into the environment and run `python3 app.py --input path/to/case.json`. Tests: `python3 -m unittest discover -s tests -v`. Field descriptions may be sensitive; inspect metadata before transmission. This release handles one dataset per case.

## Español

**Objetivo.** Comparar dos versiones de un esquema OpenLineage con usos posteriores documentados. Jev clasifica el posible impacto como `impact`, `low` o `review`; eliminar un campo o cambiar su tipo exige revisión humana. El resultado incluye rutas exactas de los campos afectados. No modifica despliegues ni esquemas.

**Entrada.** Un JSON `{"before":<RunEvent>,"after":<RunEvent>,"consumers":[{"name":"...","purpose":"...","columns":["..."]}]}`. Cada evento debe contener exactamente un conjunto de datos en `outputs` con `facets.schema.fields`. Consulte el [modelo de eventos OpenLineage](https://openlineage.io/docs/spec/object-model/) y la [faceta de esquema](https://openlineage.io/docs/spec/facets/dataset-facets/). Los usos posteriores se indican explícitamente: este prototipo no descubre automáticamente a todos los consumidores. Jev no recibe filas de datos, solo definiciones de campos modificados y usos declarados.

**Uso.** Instale `python3 -m pip install -r requirements.txt` y ejecute `python3 app.py --demo`. Para una revisión real, cargue `TYPESAFE_API_KEY` en el entorno y ejecute `python3 app.py --input ruta/al/caso.json`. Pruebas: `python3 -m unittest discover -s tests -v`. Las descripciones de campos pueden ser sensibles; revise los metadatos antes de enviarlos. Esta versión procesa un conjunto de datos por caso.

MIT · v0.1.0
