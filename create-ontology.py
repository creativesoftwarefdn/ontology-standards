#!/usr/bin/env python
import optparse
import validators
import os
import json

# Based on: https://github.com/creativesoftwarefdn/weaviate/blob/develop/docs/en/use/ontology-schema.md
COMPLETEONTOLOGY = {
    "@context": "",
    "version": "",
    "type": "",
    "name": "",
    "maintainer": "",
    "classes": []
}
SCHEMADIR = "./schemas"

def kill(i, m):
  print(i + " can not be unset " + m + ". Use --help to see all arguments")
  exit(1)

def validate():
  if OPTIONS.context == "UNSET" or validators.url(OPTIONS.context) != True: kill("context", "and needs to be formatted as URL")
  if OPTIONS.type == "UNSET" or OPTIONS.type != "thing" and OPTIONS.type != "action": kill("type", "and needs to be 'thing' or 'action'")
  if OPTIONS.name == "UNSET": kill("name", "and should be a CamelCase string")
  if OPTIONS.merge == "UNSET": kill("merge", "should be comma intended (e.g., companies,vehicles")

def main():

  global OPTIONS
  args = optparse.OptionParser()

  # Get the arguments
  args.add_option('--context', default="UNSET", help="What is the context in URL format?")
  args.add_option('--version', default="0.0.1", help="What is the SEMVER version number?")
  args.add_option('--type', default="UNSET", help="What is the type? Thing or Action?")
  args.add_option('--name', default="UNSET", help="What is the name of this schema?")
  args.add_option('--maintainer', default="hello@creativesoftwarefdn.org", help="What is the maintainer email address?")
  args.add_option('--merge', default="UNSET", help="Which ontologies need to be merged?")
  args.add_option('--mergeList', default="UNSET", help="Show a list of available ontologies and ignores other arguments", action="store_true")

  OPTIONS, arguments = args.parse_args()

  # Show available schemas
  if OPTIONS.mergeList == True:
    for filename in os.listdir(SCHEMADIR):
      if filename.endswith(".json"): 
        with open(os.path.join(SCHEMADIR + "/" + filename)) as f:
          weaviateOntologyFile = json.load(f)
        print("\tmergeTag: " + filename.replace(".json", ""))
        print("\tname: " + weaviateOntologyFile["name"])
        print("\ttype: " + weaviateOntologyFile["type"])
        print("\t---")
        continue
      else:
          continue
    exit(0)

  # check if unset arguments need to be set?
  validate()

  # add meta info
  COMPLETEONTOLOGY["name"] = OPTIONS.name
  COMPLETEONTOLOGY["version"] = OPTIONS.version
  COMPLETEONTOLOGY["@context"] = OPTIONS.context
  COMPLETEONTOLOGY["maintainer"] = OPTIONS.maintainer
  COMPLETEONTOLOGY["type"] = OPTIONS.type

  # add the data
  PARSEDMERGEFILES = OPTIONS.merge.split(",")
  for filename in os.listdir(SCHEMADIR):
      if filename.endswith(".json"):
        if filename.replace(".json", "") in PARSEDMERGEFILES :
          with open(os.path.join(SCHEMADIR + "/" + filename)) as f:
            weaviateOntologyFile = json.load(f)
            COMPLETEONTOLOGY["classes"].append(weaviateOntologyFile["classes"])

  # Output the result
  print(json.dumps(COMPLETEONTOLOGY, indent=4, sort_keys=True))

if __name__ == '__main__':
  main()