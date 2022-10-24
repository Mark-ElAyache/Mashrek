import math
import pandas as pd
def isnan(value):
    try:
        return math.isnan(float(value))
    except:
        return False
data_df = pd.read_csv('Mashrek.csv')
data_df = data_df.loc[data_df['Name'].notnull()]
categories_df = data_df['Category'].unique()
category_list = []
governate_list = []
phone_number_str = ""
phone_number = int
for category in categories_df:
    category_list.append(data_df[data_df['Category'] == category])

with open('index.html', 'w', encoding='utf8') as website:
    # Writing data to a file
    website.write(
        '<!DOCTYPE html>'
        '<html lang="en">'
        '<head>'
            '<meta charset="UTF-8">'
            '<meta http-equiv="X-UA-Compatible" content="IE=edge">'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-Zenh87qX5JnK2Jl0vWa8Ck2rdkQ2Bzep5IDxbcnCeuOxjzrPF/et3URy9Bv1WTRi" crossorigin="anonymous">'
            '<link rel="stylesheet" href="locations.css">'
            '<title>Mashrek Hospitals</title>'
        '</head>'
        '<body>'
        '<a href="https://www.almashrek.com.lb/"><img src="./Mashrek Logo.png" alt=""></a>'
        '<div class="accordion" id="accordionHeading">'
    )
    for category in category_list:
        website.writelines(
        # FOR LOOP FOR CATEGORY
            '<div class="accordion-item">'
                '<h2 class="accordion-header">'
                    f'<button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#{category["Category"].values[0].lower().replace(" ", "_")}">' # adjust data-bs-target {{row[Category].lower()}}
                        f'<h1>{category["Category"].values[0].title().replace(" ", "_")}</h1>' # adjust category {{row[Category].title()}}
                    '</button>'
                '</h2>'
                f'<div id="{category["Category"].values[0].lower().replace(" ", "_")}" class="accordion-collapse collapse" data-bs-parent="#accordionHeading">' #adjust id {{row[Category].lower()}}
                    '<div class="accordion-body">'
                        '<section class="accordion">'
    )
    # FOR LOOP FOR GOVERNATE
        governate_df = category.sort_values(["Governate", "City"]).groupby("Governate", group_keys=False).apply(
            lambda x: [values for values in x.T.to_dict().values()])
        for row in governate_df.values:
            website.writelines(
                            '<div class="accordion-item">'
                                '<h1 class="accordion-header sticky">'
                                    f'<button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#{row[0]["Governate"].lower().replace(" ", "_").replace("/", "_")}_{category["Category"].values[0].lower().replace(" ", "_").replace("/", "_")}">' #adjust aata-bs-target {{row[Governate].lower()}}_{{row[Category].lower()}}
                                        f'<h1>{row[0]["Governate"].title().strip()}</h1>' # ADD GOVERNATE in title letters \{{row[Governate].title()}}
                                    '</button>'
                                '</h1>'
                                f'<div id="{row[0]["Governate"].lower().replace(" ", "_").replace("/", "_")}_{category["Category"].values[0].lower().replace(" ", "_").replace("/", "_")}" class="accordion-collapse collapse"  data-bs-parent="#{category["Category"].values[0].lower().replace(" ", "_").replace("/", "_")}">'  # adjust id {{row[Governate].lower()}}_{{category.lower()}} and data-bs-parent {{row[Category].lower()}}
            )
    # FOR LOOP FOR NAME
            for item in row:
                print(item["Name"])
                website.writelines(
                                    '<div class="accordion-body">'
                                        '<h2>'                    
                                            f'<a{">" if isnan(item["Google Map Location"]) else " href={}>".format(item["Google Map Location"])}' # Google map location of hospital if exists row[Google Map Location]
                                                f'<strong>{item["Name"].strip()}</strong>' # Change Name {{row[Name]}}
                                            '</a><br/>'
            )

                if not(isnan(item["City"])):
                    website.writelines(
                        f'<span>{item["City"].strip()}</span><br/>'  # Location IF exists {{row[City]}}
                        )
                if not (isnan(item["Notes"])):
                    website.writelines(
                        f'<span><em>{item["Notes"].strip()}</em></span><br/>'  # Location IF exists {{row[Notes]}}
                        )
                if not(isnan(item["Phone Number"])):
                    phone_number = int(item["Phone Number"])
                    phone_number_str = str("0" + str(phone_number)) if len(str(phone_number)) == 7 else str(phone_number)
                    website.writelines(
                                            f'<a href="tel:00961{int(item["Phone Number"])}">{phone_number_str[:2] + " " + phone_number_str[2:5] + " " + phone_number_str[5::]}</a>' # change phone number and add IF exists {{row[Phone Number]}}
                    )
                website.writelines(
                                        '</h2>'
                                    '</div>'
                )     # END FOR LOOP FOR NAME
            website.writelines(
                                '</div>'
                            '</div>'
            )
                            # END FOR LOOP FOR GOVERNATE
        website.writelines(
                        '</section>'
                    '</div>'
                '</div>'
            '</div>'
        )
    # END FOR LOOP FOR CATEGORY
    website.writelines(
    '</div>'
    # '<button type="button"><h1>Nearest Hospital</h1></button>'
    '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-OERcA2EqjJCMA+/3y+gxIOqMEjwtxJY7qPCqsdltbNJuaOe923+mo//f6V8Qbsw3" crossorigin="anonymous"></script>'    
    '</body>'
    '</html>'
    )
