import xml.etree.ElementTree as Et
import os
import json


class LmChallenge:
    def __init__(self, list_of_xml_file):
        """
        Sets the initialization for the class
        :param list_of_xml_file: List of all .xml files in the directory
        """
        self.list_of_xml_file = list_of_xml_file
        self.output = {}

    def parse_xml(self):
        """
        Parses all xml files found and places them into a dictionary to later be exported to a text file.
        Uses key words used in every document to find the plaintiff and the defendants.
        :return: None
        """
        # loop to iterate through all xmls
        for xml_file in self.list_of_xml_file:
            # creates the fame for the xml
            tree = Et.parse(xml_file)
            plaintiff = ''
            trigger = False
            defendant_trigger = True
            defendant = ''
            # the next two for loops deep dive into different branches on the tree.
            for element in tree.iter():
                for child in element:
                    # Flag to check we found what we are looking for, so we dont waste time iterating through everything
                    if defendant_trigger:
                        # I only wanted to pull string files.
                        if isinstance(child.text, str) and child.text != '\n':
                            # checks if the defendant data has been found then quits out.
                            if "Defendant" in child.text:
                                defendant_trigger = False
                                break
                            # indicates that the next value is data we are looking for.
                            if trigger:
                                if len(plaintiff) == 0:
                                    plaintiff = child.text
                                    trigger = False
                                else:
                                    word = child.text.strip()
                                    defendant += word
                            if "COUNTY OF" in child.text:
                                trigger = True
                            if ("v." in child.text or "vs." in child.text) and defendant_trigger:
                                trigger = True
                        # Because the data we are looking for is stored on the left half of the pdf we do not need to
                        # iterate over all child nodes in the element. so a break is used to stop once we have the data.
                        break
            # the data is stored in a dictionary to be later exported.
            self.output[xml_file] = {'Plaintiff': plaintiff,
                                     'Defendants': defendant}

    def write_to_text(self):
        """
        opens a text file to export the desired data. the text file is current set to update, instead of replace.
        :return: None
        """
        with open("Results.txt", "a") as results:
            json.dump(self.output, results, indent=4)
            results.write('\n')
            results.close()


def get_file():
    """
    Pulls all .xml files from the current directory.
    :return: List of all .xml files in the directory
    """
    list_of_xmls = []
    path = os.path.dirname(os.path.abspath(__file__))
    for filename in os.listdir(path):
        if filename.endswith(".xml"):
            list_of_xmls.append(filename)
    if len(list_of_xmls) == 0:
        print("No XML files found")
        exit()
    return list_of_xmls


list_of_xml = get_file()
o = LmChallenge(list_of_xml)
o.parse_xml()
o.write_to_text()
