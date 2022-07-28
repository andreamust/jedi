# Empirical Ontology Inference

Infer an ontology from a Knowledge Graph in `csv`-based triple format.

## Quickstart 

0. Run `mkdir properties_per_subject property_usage_hierarchy subjects_per_property`. Intermediate results will be stored here for reload on subsequent runs.
1. Install following dependencies:
   - npm: `$apt-get install npm`
   - graphviz: `$apt-get install graphviz`
2. Install node modules from `package.json` via `$npm install` in the projects directory.
3. Place your file in the `./data` directory. **The file has to have the `.csv` file extension!**
4. Run `$node your_files_name > hierarchy.dot` **without the file extension!**
   - Intermediate results and mappings will be saved in the given other directories in this repository to save processing time on subsequent runs of the program.
5. OPTIONAL: Run `$sfdp -x -Goverlap=scale -Tpdf hierarchy.dot > hierarchy.pdf` to retrieve a visualization of the class hierarchy.

