############################################################
# For informatics site, 12.23
# This generates the file "index.md" for the about page
############################################################

import sys, os
import json

############################################################

def getCardMargins(people_left, cards_per_row):
    if people_left < cards_per_row:
        return "7";
    else:
        return "1";
# This function gets the margins for the side of the current row, depending
# on how many cards are in the row
# NOTE: if we change the number of cards_per_row from 2, this will need to be updated

def getAlumCardMargins(people_left, cards_per_row):
    if people_left < cards_per_row and people_left == 2:
        return ["7", "2"];
        # [outer row margin, inner margin]
    elif people_left < cards_per_row and people_left == 1:
        return ["9", "0"];
        # [outer row margin, inner margin]
    else:
        return ["0", "1"];
        # [outer row margin, inner margin]

############################################################

print("-" * 20);
print("RUNNING scripts/about_generatory.py TO GENERATE PROFILE CARDS")

md_template_file = "templates/about_template.md";
# Markdown templates

json_file = "data/people/people.json";
# JSON file with profiles

md_output_file = "docs/about/index.md";
# The output file for the about page

####################

print("READING TEMPLATES");
md_template = open(md_template_file, 'r').read();
#tag_template = open(tag_template_file, 'r').read();
# Read the templates

print("READING PEOPLE JSON");
with open(json_file, 'r') as json_file_stream:
    json_data = json.load(json_file_stream)
# Read the primary JSON file to get all the profiles

####################

print("GENERATING PROFILE CARDS");
with open(md_output_file, 'w') as md_output:

    cards_table = "";
    cards_per_row = 2;
    card_width = "10";
    inner_margin = "2"
    # Initialize variables for the card table
    # Some of these control the width of the cards and the space between them
    # NOTE: that some margins depend on the number of cards in the row, and are set later on

    for section in json_data:
        cards_table += "\n\n## " + section + "\n";
        # Write the section header

        for sub_section in json_data[section]:
            first_row = True;
            # cards_table += "\n\n### " + sub_section + "\n";
            # Write the sub-section header

            people_list = sorted(list(json_data[section][sub_section].keys()));
            people_list = [ person for person in people_list if json_data[section][sub_section][person]['status'] == "active" ];
            people_left = len(people_list);
            # Get the list of active people in the current sub-section and the number of people

            for person in people_list:
                person_data = json_data[section][sub_section][person];
                # Get the profile data for the current person

                if first_row:
                    cur_card_num = 1;

                    row_margin = getCardMargins(people_left, cards_per_row);
                    # Get the row margin for the current row depending on how many cards are in the row

                    cards_table += '\n<div class="row card-row">\n';
                    cards_table += '\n<div class="col-' + row_margin + '-24 card-margin-outer"></div>\n';
                    first_row = False;
                ## Get the margins and add a div for the first row

                if cur_card_num > cards_per_row:
                    cards_table += '\n<div class="col-' + row_margin + '-24 card-margin-outer"></div>\n';
                    cards_table += '</div>\n';
                    # Close the current row

                    cards_table += '\n<div class="card-sep-div"></div>\n';
                    # Put a vertical space between the two rows
                    
                    row_margin = getCardMargins(people_left, cards_per_row);
                    # Get the row margins for the next row depending on how many cards are left

                    cards_table += '\n<div class="row card-row">\n';
                    cards_table += '\n<div class="col-' + row_margin + '-24 card-margin-outer"></div>\n';
                    cur_card_num = 1;
                    # Add the new row divs
                ## If the current row is full, close it and add a new one

                cards_table += '\n<div class="col-' + card_width + '-24 card-container">\n';
                
                cards_table += '\t<div class="row card-name-container">\n';
                ## The card container div

                cards_table += '\t\t<div class="col-6-24 card-margin"></div>\n';
                cards_table += '\t\t<div class="col-12-24 card-name">\n';

                if person_data['link'] != "":
                    cards_table += '\t\t\t<b><a href="' + person_data['link'] + '" target="_blank">' + person_data['name'] + ', Ph.D.</a></b><br>\n\n';
                else:
                    cards_table += '\t\t\t<b>' + person_data['name'] + ', Ph.D.</b><br>\n\n';
                # Add the person name with or without a link                

                cards_table += '\t\t</div>\n';
                cards_table += '\t\t<div class="col-6-24 card-margin"></div>\n';
                cards_table += '\t</div>\n';
                # The card name header div

                cards_table += '\t<div class="row card-content-container">\n';
                cards_table += '\t\t<div class="col-1-24 card-margin"></div>\n';

                cards_table += '\t\t<div class="col-8-24 card-img-container">\n';
                if person_data['link'] != "":
                    cards_table += '\t\t\t<a href="' + person_data['link'] + '" target="_blank">\n';
                    cards_table += '\t\t\t\t<img class="card-img" src="../' + person_data['img'] + '" alt="' + person_data['name'] + '">\n';
                    cards_table += '\t\t\t</a>\n';
                else:
                    cards_table += '\t\t\t<img class="card-img" src="../' + person_data['img'] + '" alt="' + person_data['name'] + '">\n';
                cards_table += '\t\t</div>\n';
                # Profile image

                cards_table += '\t\t<div class="col-1-24 card-margin"></div>\n';
                cards_table += '\t\t<div class="col-13-24 card-content">\n';
                cards_table += '\t\t\t' + person_data['email'] + '<br>\n';
                cards_table += '\t\t\t Northwest Labs, ' + person_data['office'] + '<br>\n';
                cards_table += '\t\t\t<p>' + person_data['profile'] + '</p>\n';
                cards_table += '\t\t</div>\n';
                # Contact info and profile

                cards_table += '\t\t<div class="col-1-24 card-margin"></div>\n';
                cards_table += '\t</div>\n';
                ## The card content (image, contact, profile)

                cards_table += '\t<div class="sep-div"></div>\n';
                # Add a horizontal space between the content and the links     

                link_types = ['link', 'pubs', 'github'];
                links = { link_type : person_data[link_type] for link_type in link_types if person_data[link_type] != "" };
                num_links = len(links);
                # Get the links for the current person

                if num_links > 0:
                    if num_links == 3:
                        links_outer_margin = "2";
                        links_inner_margin = "2";
                    elif num_links == 2:
                        links_outer_margin = "6";
                        links_inner_margin = "2";
                    elif num_links == 1:
                        links_outer_margin = "10";
                        links_inner_margin = "0";
                    # Set the margins for the link row depending on the number of links in the profile

                    cards_table += '\t<div class="row card-link-row">\n\n';
                    cards_table += '\t\t<div class="col-' + links_outer_margin + '-24 card-margin"></div>\n\n';
                    # The link row div and outer margin

                    if 'link' in links:
                        cards_table += '\t\t<div class="col-4-24 card-link-container">\n\n';
                        cards_table += '\t\t\t<div class="icon-link-container">\n';
                        cards_table += '\t\t\t\t<a class="icon-link" href="' + person_data['link'] + '" target="_blank">\n';
                        cards_table += '\t\t\t\t\t<div class="icon-container">\n';
                        cards_table += '\t\t\t\t\t\t<img class="icon" src="../img/icons/website-logo-black.png">\n';
                        cards_table += '\t\t\t\t\t</div>\n';
                        cards_table += '\t\t\t\t\t<span>Website</span>\n';
                        cards_table += '\t\t\t\t</a>\n';
                        cards_table += '\t\t\t</div>\n';
                        cards_table += '\t\t</div>\n\n';
                
                        if num_links > 1:
                            cards_table += '\t\t<div class="col-' + links_inner_margin + '-24 card-margin"></div>\n\n';
                    ## End website link block
                
                    if 'pubs' in links:
                        cards_table += '\t\t<div class="col-4-24 card-link-container">\n\n';
                        cards_table += '\t\t\t<div class="icon-link-container">\n';
                        cards_table += '\t\t\t\t<a class="icon-link" href="' + person_data['pubs'] + '" target="_blank">\n';
                        cards_table += '\t\t\t\t\t<div class="icon-container">\n';
                        cards_table += '\t\t\t\t\t\t<img class="icon" src="../img/icons/scholar-logo-black.png">\n';
                        cards_table += '\t\t\t\t\t</div>\n';
                        cards_table += '\t\t\t\t\t<span>Scholar</span>\n';
                        cards_table += '\t\t\t\t</a>\n';
                        cards_table += '\t\t\t</div>\n';
                        cards_table += '\t\t</div>\n\n';
                
                        if num_links > 2:
                            cards_table += '\t\t<div class="col-' + links_inner_margin + '-24 card-margin"></div>\n\n';
                    ## End scholar link block
                
                    if 'github' in links:
                        cards_table += '\t\t<div class="col-4-24 card-link-container">\n\n';
                        cards_table += '\t\t\t<div class="icon-link-container">\n';
                        cards_table += '\t\t\t\t<a class="icon-link" href="' + person_data['github'] + '" target="_blank">\n';
                        cards_table += '\t\t\t\t\t<div class="icon-container">\n';
                        cards_table += '\t\t\t\t\t\t<img class="icon" src="../img/icons/github-logo-black.png">\n';
                        cards_table += '\t\t\t\t\t</div>\n';
                        cards_table += '\t\t\t\t\t<span>GitHub</span>\n';
                        cards_table += '\t\t\t\t</a>\n';
                        cards_table += '\t\t\t</div>\n';
                        cards_table += '\t\t</div>\n\n';
                    ## End github link block
                
                    cards_table += '\t\t<div class="col-' + links_outer_margin + '-24 card-margin"></div>\n\n';
                    cards_table += '\t</div>\n\n';
                    # Add the end margin and close the link row div
                ## End links block

                cards_table += '</div>\n';
                ## Close the card container div

                if cur_card_num != cards_per_row and people_left != 1:
                    cards_table += '<div class="col-' + inner_margin + '-24 card-margin-inner"></div>\n'; 
                # Add the inner margin if the current card isn't the last one in the row

                cur_card_num += 1;
                people_left -= 1;
                # Increment the card number and decrement the number of people left
            ## End person loop

            cards_table += '\n<div class="col-' + row_margin + '-24 card-margin-outer"></div>\n';
            cards_table += "</div>\n";
            # Add the outer margin and close the last row

            cards_table += '\n<div class="card-sep-div"></div>\n';
            # Put a vertical space between the sections
        ## End sub-section loop
        

    ## End section loop

####################

    print("GENERATING ALUMNI CARDS");
    cards_table += "\n\n## Group Alumni\n";

    cards_per_row = 3;
    cur_card_num = 1;
    alum_width = "6";
    people_left = 0;
    # Initialize variables for the alumni card table
    # Some of these control the width of the cards and the space between them
    # NOTE: that some margins depend on the number of cards in the row, and are set later on

    for section in json_data:
        for sub_section in json_data[section]:
            people_left += len([ person for person in json_data[section][sub_section] if json_data[section][sub_section][person]['status'] != "active" ]);
    ## Since the alumni cards will be in one table, we need to count the total number of people instead of doing it by section like above 

    first_row = True;
    # Since this is one table, we don't need to reset the first row variable for each section

    for section in json_data:
        for sub_section in json_data[section]:
            for person in json_data[section][sub_section]:
                
                person_data = json_data[section][sub_section][person];
                # Lookup the profile data for the current person

                if person_data['status'] == "active":
                    continue;
                # Skip the current person if they are active

                if first_row:
                    row_margin, alum_inner_margin = getAlumCardMargins(people_left, cards_per_row);
                    # Get the row margins for the current row depending on how many cards are in the row

                    cards_table += '\n<div class="row alum-card-row">\n';
                    cards_table += '\n<div class="col-' + row_margin + '-24 card-margin-outer"></div>\n';
                    first_row = False;
                ## Get the margins and add a div for the first row

                if cur_card_num > cards_per_row:
                    cards_table += '\n<div class="col-' + row_margin + '-24 card-margin-outer"></div>\n';
                    cards_table += '</div>\n';
                    # Close the current row

                    cards_table += '\n<div class="card-sep-div"></div>\n';
                    # Put a vertical space between the two rows
                    
                    row_margin, alum_inner_margin = getAlumCardMargins(people_left, cards_per_row);
                    # Get the row margins for the current row depending on how many cards are in the row

                    cards_table += '\n<div class="row alum-card-row">\n';
                    cards_table += '\n<div class="col-' + row_margin + '-24 card-margin-outer"></div>\n';
                    cur_card_num = 1;
                    # Add the new row divs
                ## If the current row is full, close it and add a new one

                cards_table += '\n<div class="col-' + alum_width + '-24 card-container alum-card-container">\n';
                ## The card container div 

                if person_data['link'] != "":
                    cards_table += '\t\t<b><a href="' + person_data['link'] + '" target="_blank">' + person_data['name'] + '</a></b><br>\n\n';
                else:
                    cards_table += '\t\t<b>' + person_data['name'] + '</b><br>\n\n';
                # Add the person name with or without a link
                
                if person_data['date-joined'] != "" and person_data['date-left'] != "":
                    start_year = person_data['date-joined'].split("-")[2];
                    end_year = person_data['date-left'].split("-")[2];

                    if start_year == end_year:
                        cards_table += '\t\t(' + start_year + ')<br>\n\n';
                    else:
                        cards_table += '\t\t(' + start_year + '-' + end_year + ')<br>\n\n';
                # Lookup the start and end years for the current person and add them to the card if they are available

                if person_data['profile'] != "":
                    cards_table += '\t\t<p>' + person_data['profile'] + '</p>\n';
                # Add the person profile if it is available

                cards_table += '</div>\n';
                ## Close the card container div

                if cur_card_num != cards_per_row and people_left != 1:
                    cards_table += '<div class="col-' + alum_inner_margin + '-24 card-margin-inner"></div>\n';
                # Add the inner margin if the current card isn't the last one in the row

                cur_card_num += 1;
                people_left -= 1;
                # Increment the card number and decrement the number of people left
            ## End person loop
        ## End sub-section loop

    cards_table += '\n<div class="col-' + row_margin + '-24 card-margin-outer"></div>\n';
    cards_table += "</div>\n";        
    # Add the outer margin and close the last row
    ## End section loop

####################

    md_output.write(md_template.format(profile_cards_table=cards_table));
    # Write the resources page using the template
## Close the resources output file

print("-" * 20);

############################################################


