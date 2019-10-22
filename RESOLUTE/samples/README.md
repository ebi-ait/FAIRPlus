# Update RESOLUTE samples metadata


### Updates:
1. Extended cell line descriptions
2. Added external links to SRS,SRR.
3. Added license
4. Added cellosaurus IDs

### InFile:
1. sample_template.json
    The template showing the attributes and annotations in the updated metadata
2. accessions_PRJNA545487.txt
    All related accessions, including study accessions, experiment accessions, sequencing run IDs, etc.
3. cellosaurus_data.txt
    Cell line description, generated manually from Cellosaurus website
4. ncbi_sample_ids.xml
    Sample details download from NCBI website.

### OutFile:
- updated_metadata_json/
    All 21 updated metadata.

The outfiles are compatable to EBI biosamples submission JSON schema.

### ToDo 
1. Add link to cellosaurus IDs.
2. Update metadata both in EBI BSD and NCBI BSD.
3. Change "Domain" section when submitting.


