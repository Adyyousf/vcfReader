import vobject
import pandas as pd
import io



# function to read vCard file , extract specfic info and convert to dataframe

def vcf_to_df(vcf_file):

    contact_list = []

    # with open(vcf_file, 'r', encoding='utf-8', errors='replace') as file:
        
        
    for vCard in vobject.readComponents(vcf_file):
        # vCard.prettyPrint()
        # print(vCard)
        contact_dict = {}
        if hasattr(vCard, 'fn'):
            contact_dict['Full Name'] = vCard.fn.value


        if hasattr(vCard, 'tel'):
            contact_dict['Phone'] = vCard.tel.value # "; ".join([tel.value for tel in vCard.tel_list])

        if hasattr(vCard, 'email'):
            contact_dict['Email'] = vCard.email.value #"; ".join([email.value for email in vCard.email_list])
        else:
            contact_dict['Email'] = None
        
        if hasattr(vCard, 'org'):
            contact_dict['Organization'] = vCard.org.value
        contact_list.append(contact_dict)
    return pd.DataFrame(contact_list).fillna('')
        # print(contact_dict)

# function to clean the df
def clean_contacts_df(values):

    out = []

    for value in values:
        if value is None:
            continue

        if isinstance(value, list):
            for v in value:
                element = str(v).strip()
                if element:
                    out.append(element)
        else:
            element = str(value).strip()
            if element:
                out.append(element)
    return sorted(set(out))




# master function call to read vcf and convert to df

def get_cleaned_contacts(vcf_file):

    df = vcf_to_df(vcf_file)

    merged_df = df.groupby('Full Name').agg({
        'Phone': list,
        'Email': list,
        'Organization': list
        }).reset_index()

    merged_df['Phone'] = merged_df['Phone'].apply(clean_contacts_df)
    merged_df['Organization'] = merged_df['Organization'].apply(clean_contacts_df)
    merged_df['Email'] = merged_df['Email'].apply(clean_contacts_df)

    return merged_df

# # print(contact_list)
# df = vcf_to_df('contacts.vcf')


# merged_df = df.groupby('Full Name').agg({
#     'Phone': list,
#     'Email': list,
#     'Organization': list
#     }).reset_index()



# merged_df['Phone'] = merged_df['Phone'].apply(clean_contacts_df)
# merged_df['Organization'] = merged_df['Organization'].apply(clean_contacts_df)
# merged_df['Email'] = merged_df['Email'].apply(clean_contacts_df)

# # print(merged_df.head(20))
# print(merged_df[merged_df['Full Name'] == 'Farheen'])

# merged_df.to_csv('contacts_cleaned.csv', index=False)




# cleaned_df = df.groupby('Full Name')['Phone', 'Email', 'Organization'].agg( 
#     lambda x: '; '.join(sorted(list(x.dropna())))
#     ).reset_index()

# cleaned_df.columns = ['Full Name', 'Phone Numbers']

# print(df[df['Full Name'] == 'Farheen'])

# print(cleaned_df)


# df.to_csv('contacts.csv', index=False)