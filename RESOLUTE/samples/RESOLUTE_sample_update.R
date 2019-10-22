library(rjson)
library(XML)

# Output dir
out.dir = "updated_metadata_json/"

##  Load data

# sample template 
sample_template_file = "sample_template.json"
sample_template = fromJSON(file = sample_template_file)

# accession ids from ENA, including sequencing accessions
accession_id_file = "accessions_PRJNA545487.txt"
# The accession file is downloaded from ENA/PRJNAS545487
accession_id = read.table(accession_id_file,sep = ",",stringsAsFactors = FALSE)
colnames(accession_id) = accession_id[1,]
accession_id = accession_id[-1,]

# For accessions, add link
prefix <- "https://www.ebi.ac.uk/ena/data/view/"
accession_id$study_accession <-  paste0(prefix, accession_id$study_accession)
accession_id$experiment_accession <-  paste0(prefix, accession_id$experiment_accession)
accession_id$secondary_sample_accession <-  paste0(prefix, accession_id$secondary_sample_accession)
accession_id$run_accession <- paste0(prefix, accession_id$run_accession)

# sample ids from NCBI, including sample details
#sample_id_file = "../../ncbi_sample_ids.xml"
# this file is downloaded from https://www.ncbi.nlm.nih.gov/biosample?LinkName=bioproject_biosample_all&from_uid=545487
#sample_id = xmlParse(sample_id_file)
#sample_data = xmlToDataFrame(sample_id,stringsAsFactors = FALSE)


# Get cell line annotation.
cell_line_file = "cellosaurus_data.txt"
# The cell line information is manually collected from cellosaurus website. Cell culture information are extracted from internal data release document.
cell_line = read.table(cell_line_file,sep = ",",stringsAsFactors = FALSE)
colnames(cell_line) <- cell_line[1,]
cell_line <- cell_line[-1,]

# Create variables representing every sample
for (i in 1:length(accession_id$sample_name)){
  new_sample = sample_template
  
  # Update submission details
  new_sample$name <- accession_id$sample_name[i]
  new_sample$accession <- accession_id$sample_accession[i]
  new_sample$characteristics$`cell line replicate`[[1]]$text<- strsplit(accession_id$cell_line_name[i],"_")[[1]][2]

  accession_cell_name <- strsplit(accession_id$cell_line_name[i],"_")[[1]][1]
  for (j in 1:nrow(cell_line)){
    # Update cell line metadata
    cellosaurus_cell_name = cell_line$`cell line strain`[j]
    if (accession_cell_name == cellosaurus_cell_name){
      new_sample$characteristics$organism[[1]]$text <- cell_line$organism[j]
      new_sample$characteristics$sex[[1]]$text <- cell_line$sex[j]
      new_sample$characteristics$age[[1]]$text <- cell_line$age[j]
      new_sample$characteristics$tissue[[1]]$text <- cell_line$tissue[j]
      new_sample$characteristics$disease[[1]]$text <- cell_line$disease[j]
      new_sample$characteristics$`cell line strain`[[1]]$text <- cell_line$`cell line strain`[j]
      new_sample$characteristics$`cell line name`[[1]]$text <- paste(cell_line$`cell line strain`[j],new_sample$characteristics$`cell line replicate`[[1]]$text,sep = "_")
      new_sample$characteristics$`cell line ID`[[1]]$text <- cell_line$`cellosaurus ID`[j]
      new_sample$characteristics$`cell line category`[[1]]$text <- cell_line$`cell line category`[j]
      new_sample$characteristics$`cell line source`[[1]]$text <- cell_line$`cell line source`[j]
      new_sample$characteristics$`cell culture`[[1]]$text <- cell_line$`cell culture`[j]
      
      #Add external accession IDs
      for (k in 1:nrow(accession_id)){
        if (new_sample$characteristics$`cell line name`[[1]]$text == accession_id$cell_line_name[k]){
          new_sample$externalReferences[[2]]$url = accession_id$experiment_accession[k]
          new_sample$externalReferences[[3]]$url = accession_id$secondary_sample_accession[k]
          new_sample$externalReferences[[4]]$url = accession_id$run_accession[k]
        }
      }
  }
  }

  assign(accession_id$sample_name[i],new_sample)
  
  out_file = paste0(out.dir,as.name(accession_id$sample_accession[i]),".json")
  file.create(out_file)
  out_data = toJSON(new_sample)
  
  write(out_data, file=out_file)
  
}


