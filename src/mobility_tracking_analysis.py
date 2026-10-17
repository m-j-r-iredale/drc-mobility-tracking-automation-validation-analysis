import pandas as pd
import numpy as np


# Configuration

Province = 'North Kivu'
ProvinceFR = 'NORD-KIVU'

previous_Total_IDPs = 2441338
previous_Total_RETs = 1819167


# Load mobility-tracking worksheets
input_file = r'sample_data/OIM_RDC_DTM_MT_Nord-Kivu_2024_2_PUBLIC.xlsx'

df_locations = pd.read_excel(input_file, sheet_name='VILLAGES')
df_cm = pd.read_excel(input_file, sheet_name='SITE_CCCM')
df_ncm = pd.read_excel(input_file, sheet_name='SITE_NON_CCCM')
df_grp_idp = pd.read_excel(input_file, sheet_name='GRP_IDP')
df_grp_ret = pd.read_excel(input_file, sheet_name='GRP_RET')
df_overview = pd.read_excel(input_file, sheet_name='APERCU')


# Standardise column names
df_locations.columns = df_locations.columns.str.strip()
df_grp_idp.columns = df_grp_idp.columns.str.strip()
df_grp_ret.columns = df_grp_ret.columns.str.strip()
df_cm.columns = df_cm.columns.str.strip()
df_ncm.columns = df_ncm.columns.str.strip()
df_overview.columns = df_overview.columns.str.strip()


# Map inconsistent source column names to standardised field names
renaming_Map = {
    'PROVINCE*': 'm0303_meta_adm1_label',
    'PROVINCE': 'm0303_meta_adm1_label',
    'Province': 'm0303_meta_adm1_label',
    'CODE PROVINCE*': 'm0303_meta_adm1_pcode',
    'CODE PROVINCE': 'm0303_meta_adm1_pcode',
    'TERRITOIRE*': 'm0304_meta_adm2_label',
    'TERRITOIRE': 'm0304_meta_adm2_label',
    'Territoire': 'm0304_meta_adm2_label',
    'CODE TERRITOIRE*': 'm0304_meta_adm2_pcode',
    'CODE TERRITOIRE': 'm0304_meta_adm2_pcode',
    'zone de santé': 'm0305_meta_adm3_label',
    'ZONE DE SANTE*': 'm0305_meta_adm3_label',
    'ZONE DE SANTE': 'm0305_meta_adm3_label',
    'CODE ZONE DE SANTE': 'm0305_meta_adm3_pcode',
    'code_ZS': 'm0305_meta_adm3_pcode',
    'INDIVIDUS': 'm0310_loc_num_idp_ind',
    'INDIVIDUS*': 'm0310_loc_num_idp_ind',
    'Individus - IDP': 'm0310_loc_num_idp_ind',
    'MENAGES': 'm0309_loc_num_idp_hh',
    'MENAGES*': 'm0309_loc_num_idp_hh',
    'Menage - IDP': 'm0309_loc_num_idp_hh',
    'Type': 'site_centre',
    'TYPE DE SITE*': 'site_centre',
    'type1': 'site_centre',
    'TYPE DE SITE': 'site_centre',
    'Hommes IDP': 'm2968_loc_num_men_idp',
    'Hommes - IDP': 'm2968_loc_num_men_idp',
    'HOMME': 'm2968_loc_num_men_idp',
    'Femmes - IDP': 'm2969_loc_num_women_idp',
    'FEMME': 'm2969_loc_num_women_idp',
    'Enfants <5 - IDP': 'm2970_loc_num_children_idp',
    'ENFANT': 'm2970_loc_num_children_idp'
}

df_cm = df_cm.rename(columns=lambda x: renaming_Map.get(x, x))
df_ncm = df_ncm.rename(columns=lambda x: renaming_Map.get(x, x))


# Standardise overview-sheet column names
overview_Renaming_Map = {
    'Population 2023 (Estimation de la DPS)': 'Population 2023 (DPS)',
    'Population (DPS 2023)': 'Population 2023 (DPS)',
    'Village connues': 'Villages sur liste',
    'Villages connus (DTM)': 'Villages sur liste',
    'Zone de santé': 'Zone de sante'
}

df_overview = df_overview.rename(
    columns=lambda x: overview_Renaming_Map.get(x, x)
)


# Standardise CCCM and non-CCCM site-type values
CCCM_Non_CCCM_value_renaming_Map = {
    'Centre collectif': 'Collective Centre',
    'Site Spontané': 'Site',
    'Site Spontané ': 'Site',
    'Site Planifié': 'Site',
    'Centre Collectif': 'Collective Centre',
    'CC/ecole': 'Collective Centre',
    'CC/eglise': 'Collective Centre',
    'CC/stade': 'Collective Centre',
    'CC/terrain': 'Collective Centre',
    'CC/autre': 'Collective Centre'
}

df_cm['site_centre'] = df_cm['site_centre'].replace(
    CCCM_Non_CCCM_value_renaming_Map
)
df_ncm['site_centre'] = df_ncm['site_centre'].replace(
    CCCM_Non_CCCM_value_renaming_Map
)


# Validate administrative P-code hierarchies and label/P-code mappings
def BasicChecks(df):
    if Province == 'North Kivu':
        CompD1 = {'NORD-KIVU': 'CD61'}

        CompD2 = {
            'BENI TERRITOIRE (OICHA)': 'CD6107',
            'BENI (Ville)': 'CD6109',
            'BUTEMBO': 'CD6110',
            'GOMA': 'CD6101',
            'LUBERO': 'CD6105',
            'MASISI': 'CD6103',
            'NYIRAGONGO': 'CD6102',
            'RUTSHURU': 'CD6111',
            'WALIKALE': 'CD6104'
        }

        CompD3 = {
            'KALUNGUTA': 'CD6107ZS01',
            'KAMANGO': 'CD6107ZS02',
            'KYONDO': 'CD6107ZS03',
            'MABALAKO': 'CD6107ZS04',
            'MUTWANGA': 'CD6107ZS05',
            'OICHA': 'CD6107ZS06',
            'VUHOVI': 'CD6107ZS07',
            'BENI': 'CD6109ZS01',
            'BUTEMBO': 'CD6110ZS01',
            'KATWA': 'CD6110ZS02',
            'GOMA': 'CD6101ZS01',
            'KARISIMBI': 'CD6101ZS02',
            'ALIMBONGO': 'CD6105ZS01',
            'BIENA': 'CD6105ZS02',
            'KAYINA': 'CD6105ZS03',
            'LUBERO': 'CD6105ZS04',
            'MANGUREDJIPA': 'CD6105ZS05',
            'MASEREKA': 'CD6105ZS06',
            'MUSIENENE': 'CD6105ZS07',
            'KATOYI': 'CD6103ZS01',
            'KIROTSHE': 'CD6103ZS02',
            'MASISI': 'CD6103ZS03',
            'MWESO': 'CD6103ZS04',
            'NYIRAGONGO': 'CD6102ZS01',
            'BAMBO': 'CD6111ZS01',
            'BINZA': 'CD6111ZS02',
            'BIRAMBIZO': 'CD6111ZS03',
            'KIBIRIZI': 'CD6111ZS04',
            'RUTSHURU': 'CD6111ZS05',
            'RWANGUBA': 'CD6111ZS06',
            'ITEBERO': 'CD6104ZS01',
            'KIBUA': 'CD6104ZS02',
            'PINGA': 'CD6104ZS03',
            'WALIKALE': 'CD6104ZS04'
        }

    elif Province == 'Ituri':
        CompD1 = {'ITURI': 'CD54'}

        CompD2 = {
            'ARU': 'CD5409',
            'DJUGU': 'CD5405',
            'IRUMU': 'CD5402',
            'MAHAGI': 'CD5407',
            'MAMBASA': 'CD5403',
            'BUNIA': 'CD5401'
        }

        CompD3 = {
            'BUNIA': 'CD5401ZS01',
            'ADI': 'CD5409ZS01',
            'ADJA': 'CD5409ZS02',
            'ARIWARA': 'CD5409ZS03',
            'ARU': 'CD5409ZS04',
            'BIRINGI': 'CD5409ZS05',
            'LAYBO': 'CD5409ZS06',
            'BAMBU': 'CD5405ZS01',
            'DAMAS': 'CD5405ZS02',
            'DRODRO': 'CD5405ZS03',
            'FATAKI': 'CD5405ZS04',
            'JIBA': 'CD5405ZS05',
            'KILO': 'CD5405ZS06',
            'LINGA': 'CD5405ZS07',
            'LITA': 'CD5405ZS08',
            'MANGALA': 'CD5405ZS09',
            'MONGBALU': 'CD5405ZS10',
            'NIZI': 'CD5405ZS11',
            'RETHY': 'CD5405ZS12',
            'TCHOMIA': 'CD5405ZS13',
            'BOGA': 'CD5402ZS01',
            'GETHY': 'CD5402ZS03',
            'KOMANDA': 'CD5402ZS04',
            'NYAKUNDE': 'CD5402ZS05',
            'RWAMPARA': 'CD5402ZS06',
            'ANGUMU': 'CD5407ZS01',
            'AUNGBA': 'CD5407ZS02',
            'KAMBALA': 'CD5407ZS03',
            'LOGO': 'CD5407ZS04',
            'MAHAGI': 'CD5407ZS05',
            'NYARAMBE': 'CD5407ZS06',
            'RIMBA': 'CD5407ZS07',
            'LOLWA': 'CD5403ZS01',
            'MAMBASA': 'CD5403ZS02',
            'MANDIMA': 'CD5403ZS03',
            'NIA-NIA': 'CD5403ZS04'
        }

    elif Province == 'South Kivu':
        CompD1 = {'SUD-KIVU': 'CD62'}

        CompD2 = {
            'BUKAVU': 'CD6201',
            'FIZI': 'CD6210',
            'IDJWI': 'CD6206',
            'KABARE': 'CD6202',
            'KALEHE': 'CD6205',
            'MWENGA': 'CD6212',
            'SHABUNDA': 'CD6203',
            'UVIRA': 'CD6208',
            'WALUNGU': 'CD6207'
        }

        CompD3 = {
            'BAGIRA': 'CD6201ZS01',
            'IBANDA': 'CD6201ZS02',
            'KADUTU': 'CD6201ZS03',
            'FIZI': 'CD6210ZS01',
            'KIMBI LULENGE': 'CD6210ZS02',
            'MINEMBWE': 'CD6210ZS03',
            'NUNDU': 'CD6210ZS04',
            'IDJWI': 'CD6206ZS01',
            'KABARE': 'CD6202ZS01',
            'KATANA': 'CD6202ZS03',
            'MITI MURHESA': 'CD6202ZS04',
            'NYANTENDE': 'CD6202ZS05',
            'BUNYAKIRI': 'CD6205ZS01',
            'KALEHE': 'CD6205ZS02',
            'KALONGE': 'CD6205ZS03',
            'MINOVA': 'CD6205ZS04',
            'ITOMBWE': 'CD6212ZS01',
            'KAMITUGA': 'CD6212ZS02',
            'KITUTU': 'CD6212ZS03',
            'MWANA': 'CD6212ZS04',
            'MWENGA': 'CD6212ZS05',
            'KALOLE': 'CD6203ZS01',
            'LULINGU': 'CD6203ZS02',
            'MULUNGU': 'CD6203ZS03',
            'SHABUNDA': 'CD6203ZS04',
            'HAUT-PLATEAU': 'CD6208ZS01',
            'LEMERA': 'CD6208ZS02',
            'RUZIZI': 'CD6208ZS03',
            'UVIRA': 'CD6208ZS04',
            'KANIOLA': 'CD6207ZS05',
            'KAZIBA': 'CD6207ZS01',
            'MUBUMBANO': 'CD6207ZS02',
            'NYANGEZI': 'CD6207ZS03',
            'WALUNGU': 'CD6207ZS04'
        }

    elif Province == 'Tanganyika':
        CompD1 = {'TANGANYIKA': 'CD74'}

        CompD2 = {
            'KABALO': 'CD7407',
            'KALEMIE': 'CD7402',
            'KONGOLO': 'CD7409',
            'MANONO': 'CD7406',
            'MOBA': 'CD7404',
            'NYUNZU': 'CD7410'
        }

        CompD3 = {
            'KABALO': 'CD7407ZS01',
            'KALEMIE': 'CD7402ZS01',
            'NYEMBA': 'CD7402ZS02',
            'KONGOLO': 'CD7409ZS01',
            'MBULULA': 'CD7409ZS02',
            'ANKORO': 'CD7406ZS01',
            'KIAMBI': 'CD7406ZS02',
            'MANONO': 'CD7406ZS03',
            'KANSIMBA': 'CD7404ZS01',
            'MOBA': 'CD7404ZS02',
            'NYUNZU': 'CD7410ZS01'
        }

    # Check that each administrative P-code follows the expected hierarchy
    Correct = True

    # Province P-code must match territory P-code prefix
    for index, row in df.iterrows():
        if str(row['m0303_meta_adm1_pcode'])[:4] != str(row['m0304_meta_adm2_pcode'])[:4]:
            print(
                f"Row {index} does not match: "
                f"{row['m0303_meta_adm1_pcode']} -> {row['m0304_meta_adm2_pcode']}"
            )
            Correct = False

    # Province P-code must match health-zone P-code prefix
    for index, row in df.iterrows():
        if str(row['m0303_meta_adm1_pcode'])[:4] != str(row['m0305_meta_adm3_pcode'])[:4]:
            print(
                f"Row {index} does not match: "
                f"{row['m0303_meta_adm1_pcode']} -> {row['m0305_meta_adm3_pcode']}"
            )
            Correct = False

    # Territory P-code must match health-zone P-code prefix
    for index, row in df.iterrows():
        if str(row['m0304_meta_adm2_pcode'])[:6] != str(row['m0305_meta_adm3_pcode'])[:6]:
            print(
                f"Row {index} does not match: "
                f"{row['m0304_meta_adm2_pcode']} -> {row['m0305_meta_adm3_pcode']}"
            )
            Correct = False

    # Validate province label/P-code pairs against reference dictionary
    for index, row in df.iterrows():
        label1 = row['m0303_meta_adm1_label']
        pcode1 = row['m0303_meta_adm1_pcode']
        if CompD1.get(label1) != pcode1:
            print(
                f"This row {index} does not match Province dictionary: "
                f"{label1} -> {pcode1}"
            )
            Correct = False

    # Validate territory label/P-code pairs against reference dictionary
    for index, row in df.iterrows():
        label2 = row['m0304_meta_adm2_label']
        pcode2 = row['m0304_meta_adm2_pcode']
        if CompD2.get(label2) != pcode2:
            print(
                f"This row {index} does not match Territory dictionary: "
                f"{label2} -> {pcode2}"
            )
            Correct = False

    # Validate health-zone label/P-code pairs against reference dictionary
    for index, row in df.iterrows():
        label3 = row['m0305_meta_adm3_label']
        pcode3 = row['m0305_meta_adm3_pcode']
        if CompD3.get(label3) != pcode3:
            print(
                f"This row {index} does not match ZS dictionary: "
                f"{label3} -> {pcode3}"
            )
            Correct = False

    if Correct:
        print("Everything is correct")


# Run P-code validation checks across each relevant worksheet

BasicChecks(df_locations)
print("in the locations tab.\n")

BasicChecks(df_grp_idp)
print("in the grp_idp tab.\n")

BasicChecks(df_grp_ret)
print("in the grp_ret tab.\n")

BasicChecks(df_cm)
print("in the CCCM tab.\n")

BasicChecks(df_ncm)
print("in the Non_CCCM tab.\n")


# Validate CCCM demographic totals using age-band columns when available
try:
    total_Males_CCCM = df_cm[
        ['0 - 5 H', '6 - 17 H', '18 - 59 H', '60 + H']
    ].sum().sum()

    total_Females_CCCM = df_cm[
        ['0 - 5 F', '6 - 17 F', '18 - 59 F', '60 + F']
    ].sum().sum()

    if (
        total_Males_CCCM + total_Females_CCCM
        == df_cm['m0310_loc_num_idp_ind'].sum()
    ):
        print(
            'Correct Age Brackets Method 1: Males plus Females in '
            '"CCCM tab" is equal to the number of individuals.'
        )
        age_Bracket_CCCM = True
    else:
        print(
            'Incorrect Age Brackets Method 1: Males plus Females in '
            '"CCCM tab" is NOT equal to the number of individuals'
        )
        age_Bracket_CCCM = False

    print('\n')

except KeyError:
    print('CCCM Tab is not in the Method 1 "age bracket" format')
    print('\n')


# Validate CCCM demographic totals using aggregate gender columns when available
try:
    if (
        df_cm['m2968_loc_num_men_idp'].sum()
        + df_cm['m2969_loc_num_women_idp'].sum()
        == df_cm['m0310_loc_num_idp_ind'].sum()
    ):
        print(
            'Correct Column Code Method 2: Males plus Females in '
            '"CCCM" is equal to the number of individuals.'
        )
    else:
        print(
            'Incorrect Column Code Method 2: Males plus Females in '
            '"CCCM" is NOT equal to the number of individuals'
        )

    print('\n')

except KeyError:
    print('CCCM Tab is not in the Method 2 "column code" format')
    print('\n')


# Automated reporting analysis

# Page 1: headline mobility indicators

# Assessment date range

print('Top of Page')

try:
    assessment_Date_start = df_locations['m1855_meta_assessment_date'].min()
    assessment_Date_end = df_locations['m1855_meta_assessment_date'].max()
    print(f'Assessment date: {assessment_Date_start} to {assessment_Date_end}, unless otherwise specified.')
except KeyError:
    print('not in date format 1')

try:
    assessment_Date_start = df_locations['m2682_meta_date_auto'].min()
    assessment_Date_end = df_locations['m2682_meta_date_auto'].max()
    print(f'Assessment date: {assessment_Date_start} to {assessment_Date_end}, unless otherwise specified.')
except KeyError:
    print('Not in date format 2')

# Number of assessed villages
number_of_Villages = df_locations['m0306_meta_adm4_label'].count()
print(f'Number of Villages {number_of_Villages}')
# Survey coverage
number_Villages_DPS = df_overview['Villages sur liste'].sum()
coverage = number_of_Villages / number_Villages_DPS *100
print(f'Coverage: {coverage.round(0)}%')
# Number of assessed health zones
number_of_ZS = df_locations['m0305_meta_adm3_pcode'].nunique()
print(f'Number of ZS: {number_of_ZS}')

# Number of key informants
try:
    number_of_KIs = df_locations['m1729_loc_num_ki'].sum()
    print(f'Number of KIs {number_of_KIs}')
except KeyError:
    print('No KI code')

print("\n")

# Displacement summary
print('IDP Box')
# Total IDPs
total_IDPs_Host_Communities = df_grp_idp['x0010_grp_idp_ind'].sum()
total_IDPs_CCCM = df_cm['m0310_loc_num_idp_ind'].sum()
total_IDPs_Non_CCCM = df_ncm['m0310_loc_num_idp_ind'].sum()
total_IDPs = total_IDPs_Host_Communities + total_IDPs_CCCM + total_IDPs_Non_CCCM
total_IDPs = round(total_IDPs)
print(f'Total IDPs: {total_IDPs}')

# Change in total IDPs since the previous reporting round
total_IDP_Change = ((total_IDPs - previous_Total_IDPs)/previous_Total_IDPs) *100
print(f'Total IDP change {total_IDP_Change}%')

# Total IDP households
total_IDPs_Host_Communities_Households = df_grp_idp['x0009_grp_idp_hh'].sum()
total_IDPs_CCCM_Households = df_cm['m0309_loc_num_idp_hh'].sum()
total_IDPs_Non_CCCM_Households = df_ncm['m0309_loc_num_idp_hh'].sum()
total_IDP_Households = total_IDPs_Host_Communities_Households + total_IDPs_CCCM_Households + total_IDPs_Non_CCCM_Households
total_IDP_Households = round(total_IDP_Households)
print(f'Total IDP Households: {total_IDP_Households}')

# Territories hosting the largest numbers of IDPs
majority_IDPs_admin_2_loc = df_grp_idp.groupby(['m0304_meta_adm2_label'])['x0010_grp_idp_ind'].sum()
majority_IDPs_admin_2_loc = majority_IDPs_admin_2_loc.reset_index()
majority_IDPs_admin_2_loc = majority_IDPs_admin_2_loc.rename(columns={'x0010_grp_idp_ind': 'm0310_loc_num_idp_ind'})
majority_IDPs_admin_2_cm = df_cm.groupby(['m0304_meta_adm2_label'])['m0310_loc_num_idp_ind'].sum()
majority_IDPs_admin_2_cm = majority_IDPs_admin_2_cm.reset_index()
majority_IDPs_admin_2_ncm = df_ncm.groupby(['m0304_meta_adm2_label'])['m0310_loc_num_idp_ind'].sum()
majority_IDPs_admin_2_ncm = majority_IDPs_admin_2_ncm.reset_index()
majority_IDPs_admin_2 = pd.concat([majority_IDPs_admin_2_loc, majority_IDPs_admin_2_cm, majority_IDPs_admin_2_ncm])
majority_IDPs_admin_2 = majority_IDPs_admin_2.groupby(['m0304_meta_adm2_label'])['m0310_loc_num_idp_ind'].sum()
majority_IDPs_admin_2 = majority_IDPs_admin_2.sort_values(ascending=False)
print(f'The majority of IDPs found refuge in {majority_IDPs_admin_2.index[0].title()} and {majority_IDPs_admin_2.index[1].title()}')

# IDP demographic breakdown

host_family_Males = df_locations['m2968_loc_num_men_idp'].sum()
host_family_Females = df_locations['m2969_loc_num_women_idp'].sum()
host_family_Children = df_locations['m2970_loc_num_children_idp'].sum()

male_IDPs = host_family_Males / total_IDPs_Host_Communities*100
female_IDPs = host_family_Females / total_IDPs_Host_Communities*100
children_IDPs = host_family_Children / total_IDPs_Host_Communities*100

subtraction = host_family_Children /2
IDP_Men = host_family_Males - subtraction
IDP_Women = host_family_Females - subtraction
IDP_Men = IDP_Men / total_IDPs_Host_Communities*100
IDP_Women = IDP_Women / total_IDPs_Host_Communities*100

print(f'IDPs are {male_IDPs.round(1)}% male and {female_IDPs.round(1)}% female')
print(f'{IDP_Men.round(1)}% are men, {IDP_Women.round(1)}% are women, and {children_IDPs.round(1)}% are under 18 yo')

# IDPs by accommodation setting
print(f'Total IDPs in Host Communities: {total_IDPs_Host_Communities}')
print(f'Total IDPs in CCCM Camps: {total_IDPs_CCCM.round(0)}')
print(f'Total IDPs in Non-CCCM Camps: {total_IDPs_Non_CCCM.round(0)}')
print("\n")

# Returnee summary
print('Returnee Box')
# Total returnees
total_RETs = df_grp_ret['x0034_grp_return_idp_ind'].sum()
print(f'Total Returnees: {total_RETs.round(0)}')

# Change in total returnees since the previous reporting round
total_RET_Change = ((total_RETs - previous_Total_RETs)/previous_Total_RETs) *100
print(f'Total RET change {total_RET_Change}%')

# Total returnee households
total_RET_Households = df_grp_ret['x0033_grp_return_idp_hh'].sum()
print(f'Total RET Households: {total_RET_Households.round(0)}')

# Health zones with the highest returnee shares
majority_RETs_admin_3 = df_grp_ret.groupby(['m0305_meta_adm3_label'])['x0034_grp_return_idp_ind'].sum()
majority_RETs_admin_3 = majority_RETs_admin_3.sort_values(ascending=False)
majority_RETs_admin_3 = majority_RETs_admin_3.reset_index()
total_Population_By_ZS = df_overview.groupby('Zone de sante')['Population 2023 (DPS)'].sum()
total_Population_By_ZS = total_Population_By_ZS.reset_index()
total_Population_By_ZS['Zone de sante'] = total_Population_By_ZS['Zone de sante'].str.upper()
majority_RETs_admin_3 = majority_RETs_admin_3.merge(total_Population_By_ZS, left_on='m0305_meta_adm3_label', right_on='Zone de sante')
majority_RETs_admin_3['Percentage'] = majority_RETs_admin_3['x0034_grp_return_idp_ind'] / majority_RETs_admin_3['Population 2023 (DPS)'] *100
majority_RETs_admin_3 = majority_RETs_admin_3.sort_values('Percentage', ascending=False).round(0)
majority_RETs_admin_3 = majority_RETs_admin_3.reset_index()
print(
    f"Returnees represent the majority of the population in the "
    f"{majority_RETs_admin_3['m0305_meta_adm3_label'][0].title()} {majority_RETs_admin_3['Percentage'][0]}%,"
    f"{majority_RETs_admin_3['m0305_meta_adm3_label'][1].title()} {majority_RETs_admin_3['Percentage'][1]}% "
    f"and {majority_RETs_admin_3['m0305_meta_adm3_label'][2].title()} {majority_RETs_admin_3['Percentage'][2]}% health zones."
    )

# Returnee demographic breakdown

returnee_Males = df_locations['m2971_loc_num_men_return'].sum()
returnee_Females = df_locations['m2972_loc_num_women_return'].sum()
returnee_Children = df_locations['m2973_loc_num_children_return'].sum()

male_RETs = returnee_Males / total_RETs*100
female_RETs = returnee_Females / total_RETs*100
children_RETs = returnee_Children / total_RETs*100

subtraction = returnee_Children /2
RET_Men = returnee_Males - subtraction
RET_Women = returnee_Females - subtraction
RET_Men = RET_Men / total_RETs*100
RET_Women = RET_Women / total_RETs*100

print(f'RETs are {male_RETs.round(1)}% male and {female_RETs.round(1)}% female')
print(f'There are {returnee_Males} male RETs, {returnee_Females} female RETs, and {returnee_Children} are children.')
print(f'{RET_Men.round(1)}% are men, {RET_Women.round(1)}% are women, and {children_RETs.round(1)}% are under 18 yo')
print("\n")

# Percentage of IDPs by accommodation setting
print('Icon Row: Percentage IDPs by Shelter Type ')
total_IDPs_Host_Communities_Percentage = total_IDPs_Host_Communities / total_IDPs *100
print(f'{total_IDPs_Host_Communities_Percentage.round(1)}% of IDPs in Host Communities')
total_IDPs_CCCM_Percentage = total_IDPs_CCCM / total_IDPs *100
print(f'{total_IDPs_CCCM_Percentage.round(1)}% of IDPs in CCCM Camps')
total_IDPs_Non_CCCM_Percentage = total_IDPs_Non_CCCM / total_IDPs *100
print(f'{total_IDPs_Non_CCCM_Percentage.round(1)}% of IDPs in Non-CCCM Camps')



# Page 2: detailed displacement analysis

# IDPs as a share of the provincial population

percent_Total_IDPs = total_IDPs / df_overview['Population 2023 (DPS)'] .sum() *100
number_CCCM_Sites = df_cm['site_centre'].value_counts()
number_Non_CCCM_Sites = df_ncm['site_centre'].value_counts()
print(
    f'IDPs represent {percent_Total_IDPs.round(0)}% of the total population in the province '
    f'a change of {total_IDP_Change}% compared to the previous round.'
    )
print("\n")

# Breakdown of IDPs by CCCM management status

print(
    f'An estimated {total_IDPs_CCCM} IDPs ({total_IDPs_CCCM_Percentage.round(0)}%) were living in sites covered by the CCCM '
    f'{number_CCCM_Sites} \n'
    f'and {total_IDPs_Non_CCCM} IDPs ({total_IDPs_Non_CCCM_Percentage.round(0)}%) were living in sites not covered by the CCCM '
    f'{number_Non_CCCM_Sites}'
)
print("\n")

# IDPs in sites and collective centres regardless of CCCM management

sites_CC_CCCM = df_cm.groupby('site_centre')['m0310_loc_num_idp_ind'].sum()
sites_CC_CCCM = sites_CC_CCCM.reset_index()

sites_CC_Non_CCCM = df_ncm.groupby('site_centre')['m0310_loc_num_idp_ind'].sum()
sites_CC_Non_CCCM = sites_CC_Non_CCCM .reset_index()

sites_CC_Combined = pd.concat([sites_CC_CCCM,sites_CC_Non_CCCM],ignore_index=True)
sites_CC_Combined = sites_CC_Combined.groupby('site_centre')['m0310_loc_num_idp_ind'].sum()
sites_CC_Combined = sites_CC_Combined.reset_index()
sites_CC_Combined['percentage'] = sites_CC_Combined['m0310_loc_num_idp_ind'] / total_IDPs *100

print(f'Irrespective of CCCM management, {sites_CC_Combined}')
print("\n")

# Detailed breakdown of territories hosting the most IDPs

majority_IDPs_admin_2 = majority_IDPs_admin_2.reset_index()
majority_IDPs_admin_2['percentage'] = majority_IDPs_admin_2['m0310_loc_num_idp_ind']/ total_IDPs *100
print(
    f"The majority of IDPs found refuge in {majority_IDPs_admin_2['m0304_meta_adm2_label'][0]} "
    f"({majority_IDPs_admin_2['percentage'][0].round()}%), {majority_IDPs_admin_2['m0304_meta_adm2_label'][1]} "
    f"({majority_IDPs_admin_2['percentage'][1].round()}%), and {majority_IDPs_admin_2['m0304_meta_adm2_label'][2]} "
    f"({majority_IDPs_admin_2['percentage'][2].round()}%)."
)

print("\n")

# Average IDP household size

print(f'Average HH size: {total_IDPs/total_IDP_Households}')
print("\n")

# Reasons for displacement: primary categorisation

displacement_Reasons_One = df_grp_idp.groupby('x0011_grp_idp_reason_disp')['x0010_grp_idp_ind'].sum()
displacement_Reasons_One = displacement_Reasons_One.reset_index()
displacement_Reasons_One['percentage'] = displacement_Reasons_One['x0010_grp_idp_ind'] / displacement_Reasons_One['x0010_grp_idp_ind'].sum() *100
displacement_Reasons_One = displacement_Reasons_One.sort_values(by='percentage', ascending=False)
print(
    f'Displacement is reported to be largely linked to{displacement_Reasons_One}'
)

# Reasons for displacement: detailed categorisation

displacement_Reasons_Two = df_grp_idp.groupby('x0011_grp_idp_reason_disp_detailed')['x0010_grp_idp_ind'].sum()
displacement_Reasons_Two = displacement_Reasons_Two.reset_index()
displacement_Reasons_Two['percentage'] = displacement_Reasons_Two['x0010_grp_idp_ind'] / displacement_Reasons_Two['x0010_grp_idp_ind'].sum() *100
displacement_Reasons_Two = displacement_Reasons_Two.sort_values(by='percentage', ascending=False)
print(f'Displacement breaks down to {displacement_Reasons_Two}')

print("\n")

# IDPs hosted from other provinces

other_Provinces_IDPs = df_grp_idp.groupby('x0013_grp_idp_arrivals_origin_adm1_label')['x0010_grp_idp_ind'].sum()
other_Provinces_IDPs = other_Provinces_IDPs.reset_index()
other_Provinces_IDPs = other_Provinces_IDPs[other_Provinces_IDPs['x0013_grp_idp_arrivals_origin_adm1_label']!=ProvinceFR]
other_Provinces_IDPs_Total = other_Provinces_IDPs['x0010_grp_idp_ind'].sum()
other_Provinces_IDPs['percentage'] = other_Provinces_IDPs['x0010_grp_idp_ind'] / other_Provinces_IDPs_Total *100
print(
    f'According to key informants, {Province} hosts {other_Provinces_IDPs_Total} IDPs from other provinces, '
    f'the vast majority of whom come from: {other_Provinces_IDPs}'
)


# Health-zone displacement flow analysis

flow_ZS_IDPs = df_grp_idp.groupby(['m0305_meta_adm3_pcode', 'm0305_meta_adm3_label'])[['x0010_grp_idp_ind']].sum()
flow_ZS_IDPs = flow_ZS_IDPs.reset_index()

flow_ZS_Arrivals = df_grp_idp.groupby(['x0015_grp_idp_arrivals_origin_ZS','x0015_grp_idp_arrivals_origin_ZS_label'])[['x0010_grp_idp_ind']].sum()
flow_ZS_Arrivals = flow_ZS_Arrivals.reset_index()

flow_Analysis_ZS = flow_ZS_IDPs.merge(flow_ZS_Arrivals, left_on='m0305_meta_adm3_pcode', right_on='x0015_grp_idp_arrivals_origin_ZS', how='inner', suffixes=['_IDP','_Origin'])
flow_Analysis_ZS = flow_Analysis_ZS[['m0305_meta_adm3_label','x0010_grp_idp_ind_IDP','x0010_grp_idp_ind_Origin']]

flow_Analysis_ZS = flow_Analysis_ZS.rename(columns={'m0305_meta_adm3_label': 'Label', 'x0010_grp_idp_ind_IDP' : 'IDPs' , 'x0010_grp_idp_ind_Origin' : 'Origin'})

flow_Province = df_grp_idp.groupby('x0013_grp_idp_arrivals_origin_adm1_label')[['x0010_grp_idp_ind']].sum()
flow_Province = flow_Province.reset_index()
condition_1 = flow_Province['x0013_grp_idp_arrivals_origin_adm1_label']!= ProvinceFR
flow_Province = flow_Province[condition_1]

flow_Province = flow_Province.rename(columns={'x0013_grp_idp_arrivals_origin_adm1_label': 'Label', 'x0010_grp_idp_ind' : 'Origin'})

flow_Analysis = pd.concat([flow_Analysis_ZS, flow_Province], ignore_index=True)

flow_Analysis = flow_Analysis.fillna(0)

flow_Analysis['Flow/Flux'] = flow_Analysis['IDPs'] - flow_Analysis['Origin']
flow_Analysis = flow_Analysis.sort_values(by='Flow/Flux', ascending=False)

flow_Analysis_ZS['Flow/Flux'] = flow_Analysis_ZS['IDPs'] - flow_Analysis_ZS['Origin']
flow_Analysis_ZS = flow_Analysis_ZS.sort_values(by='Flow/Flux', ascending=False)

print(
    f"The largest net zones of origin/net hosts are {flow_Analysis_ZS['Label'].iloc[-1]} {flow_Analysis_ZS['Flow/Flux'].iloc[-1]} IDPs, "
    f"{flow_Analysis_ZS['Label'].iloc[-2]} {flow_Analysis_ZS['Flow/Flux'].iloc[-2]} IDPs, and "
    f"{flow_Analysis_ZS['Label'].iloc[-3]} {flow_Analysis_ZS['Flow/Flux'].iloc[-3]} IDPs."
    )
print("\n")

print(
    f"The health zones hosting the most displaced persons/net sources are {flow_Analysis_ZS['Label'].iloc[0]} {flow_Analysis_ZS['Flow/Flux'].iloc[0]} IDPs, "
    f"{flow_Analysis_ZS['Label'].iloc[1]} {flow_Analysis_ZS['Flow/Flux'].iloc[1]} IDPs, and "
    f"{flow_Analysis_ZS['Label'].iloc[2]} {flow_Analysis_ZS['Flow/Flux'].iloc[2]} IDPs."
    )


# Returnee analysis

# Territories hosting the largest numbers of returnees

majority_RETs_admin_2 = df_grp_ret.groupby(['m0304_meta_adm2_label'])['x0034_grp_return_idp_ind'].sum()
majority_RETs_admin_2 = majority_RETs_admin_2.reset_index()
majority_RETs_admin_2['percentage'] = majority_RETs_admin_2['x0034_grp_return_idp_ind'] / total_RETs *100
majority_RETs_admin_2 = majority_RETs_admin_2.sort_values(by='percentage', ascending=False)
majority_RETs_admin_2 = majority_RETs_admin_2.reset_index()
print(
    f"The majority of Returnees were in {majority_RETs_admin_2['m0304_meta_adm2_label'][0]} ({majority_RETs_admin_2['x0034_grp_return_idp_ind'][0]} "
    f"or {majority_RETs_admin_2['percentage'][0].round(2)}%) and {majority_RETs_admin_2['m0304_meta_adm2_label'][1]} "
    f"({majority_RETs_admin_2['x0034_grp_return_idp_ind'][1]} or {majority_RETs_admin_2['percentage'][1].round(2)}%)"
    )

print("\n")

# Reasons for return
return_Reasons_One = df_grp_ret.groupby('x0035_grp_return_idp_reason_ret')['x0034_grp_return_idp_ind'].sum()
return_Reasons_One = return_Reasons_One.reset_index()
return_Reasons_One['percentage'] = return_Reasons_One['x0034_grp_return_idp_ind'] / return_Reasons_One['x0034_grp_return_idp_ind'].sum() *100
return_Reasons_One = return_Reasons_One.sort_values(by='percentage', ascending=False)
return_Reasons_One = return_Reasons_One.reset_index()
print(
    f"Returns were linked to {return_Reasons_One['x0035_grp_return_idp_reason_ret'][0]}\n "
    f"({return_Reasons_One['percentage'][0].round(2)}%), {return_Reasons_One['x0035_grp_return_idp_reason_ret'][1]} "
    f"({return_Reasons_One['percentage'][1].round(2)}%), and {return_Reasons_One['x0035_grp_return_idp_reason_ret'][2]} "
    f"({return_Reasons_One['percentage'][2].round(2)}%)."
)
print("\n")

print(return_Reasons_One)

print("\n")
# Health zones with the greatest potential for future returns
future_Returns = df_grp_idp.groupby('x0015_grp_idp_arrivals_origin_ZS_label')['x0010_grp_idp_ind'].sum()
future_Returns = future_Returns.sort_values(ascending=False)
future_Returns = future_Returns.reset_index()
print(f'Health Zones with the greatest potential for future returns are {future_Returns.head(10)}')


# Pressure index

all_Flows_1 = df_overview.groupby('Zone de sante', as_index=False)['Population 2023 (DPS)'].sum()
all_Flows_1['Zone de sante'] = all_Flows_1['Zone de sante'].str.upper()
all_Flows_2 = df_overview.groupby('Pcode ZS', as_index=False)['Population 2023 (DPS)'].sum()
all_Flows = all_Flows_1.merge(all_Flows_2, left_on='Population 2023 (DPS)', right_on='Population 2023 (DPS)')

all_Flows=all_Flows.fillna(0)

influx_IDP = df_grp_idp[['m0305_meta_adm3_pcode','m0305_meta_adm3_label', 'x0010_grp_idp_ind','x0015_grp_idp_arrivals_origin_ZS']]
influx_Condition = df_grp_idp['m0305_meta_adm3_pcode'] != df_grp_idp['x0015_grp_idp_arrivals_origin_ZS']
influx_IDP = influx_IDP[influx_Condition]
influx_IDP = influx_IDP.groupby(['m0305_meta_adm3_label'], as_index=False)['x0010_grp_idp_ind'].sum()

all_Flows = all_Flows.merge(influx_IDP, left_on='Zone de sante', right_on='m0305_meta_adm3_label', how='left')
all_Flows=all_Flows.fillna(0)

outflux_IDP = df_grp_idp[['m0305_meta_adm3_pcode','x0010_grp_idp_ind','x0015_grp_idp_arrivals_origin_ZS']]
outflux_Condition = df_grp_idp['m0305_meta_adm3_pcode'] != df_grp_idp['x0015_grp_idp_arrivals_origin_ZS']
outflux_IDP = outflux_IDP[outflux_Condition]
outflux_IDP = outflux_IDP.groupby('x0015_grp_idp_arrivals_origin_ZS', as_index=False)['x0010_grp_idp_ind'].sum()


all_Flows = all_Flows.merge(outflux_IDP, left_on='Pcode ZS', right_on='x0015_grp_idp_arrivals_origin_ZS', how='left')
all_Flows=all_Flows.fillna(0)

all_Flows = all_Flows[['m0305_meta_adm3_label','Pcode ZS','Zone de sante','Population 2023 (DPS)','x0010_grp_idp_ind_x','x0010_grp_idp_ind_y']]

all_Flows = all_Flows.rename(columns={
    'x0010_grp_idp_ind_x' : 'IDP Influx',
    'x0010_grp_idp_ind_y': 'IDPs Outflow'
})

all_Flows['Derived Population Total'] = all_Flows['Population 2023 (DPS)'] + all_Flows['IDP Influx'] - all_Flows['IDPs Outflow']

origin_IDP = df_grp_idp[['m0305_meta_adm3_pcode', 'x0010_grp_idp_ind','x0015_grp_idp_arrivals_origin_ZS']]
origin_Condition = df_grp_idp['m0305_meta_adm3_pcode'] == df_grp_idp['x0015_grp_idp_arrivals_origin_ZS']
origin_IDP = origin_IDP[origin_Condition]
origin_IDP = origin_IDP.groupby('m0305_meta_adm3_pcode', as_index=False)['x0010_grp_idp_ind'].sum()

all_Flows = all_Flows.merge(origin_IDP, left_on='Pcode ZS', right_on='m0305_meta_adm3_pcode', how='outer')
all_Flows = all_Flows.rename(columns={
    'x0010_grp_idp_ind' : 'IDP Origin'
})
all_Flows=all_Flows.fillna(0)

all_Flows = all_Flows[[
    'm0305_meta_adm3_label','Pcode ZS','Zone de sante','Population 2023 (DPS)','IDP Influx',
    'IDPs Outflow','Derived Population Total','IDP Origin']]

flows_CCCM = df_cm.groupby('m0305_meta_adm3_pcode', as_index=False)['m0310_loc_num_idp_ind'].sum()


all_Flows = all_Flows.merge(flows_CCCM, left_on='Pcode ZS', right_on='m0305_meta_adm3_pcode', how='outer')
all_Flows = all_Flows.rename(columns={
    'm0310_loc_num_idp_ind' : 'IDP CCCM'
})

all_Flows = all_Flows[[
    'm0305_meta_adm3_label','Pcode ZS','Zone de sante','Population 2023 (DPS)','IDP Influx','IDPs Outflow',
    'Derived Population Total','IDP Origin','IDP CCCM']]

flows_Non_CCCM = df_ncm.groupby('m0305_meta_adm3_pcode', as_index=False)['m0310_loc_num_idp_ind'].sum()


all_Flows = all_Flows.merge(flows_Non_CCCM, left_on='Pcode ZS', right_on='m0305_meta_adm3_pcode', how='outer')
all_Flows = all_Flows.rename(columns={
    'm0310_loc_num_idp_ind' : 'IDP Non-CCCM'
})

all_Flows = all_Flows.fillna(0)

all_Flows = all_Flows[[
    'm0305_meta_adm3_label','Pcode ZS','Zone de sante','Population 2023 (DPS)','IDP Influx','IDPs Outflow',
    'Derived Population Total','IDP Origin','IDP CCCM','IDP Non-CCCM']]

all_Flows['Total IDP'] = all_Flows['IDP Non-CCCM'] + all_Flows['IDP CCCM'] + all_Flows['IDP Origin']
all_Flows = all_Flows.fillna(0)

flows_RET = df_grp_ret.groupby('m0305_meta_adm3_pcode', as_index=False)['x0034_grp_return_idp_ind'].sum()


all_Flows = all_Flows.merge(flows_RET, left_on='Pcode ZS', right_on='m0305_meta_adm3_pcode',how='left')
all_Flows = all_Flows.rename(columns={
    'x0034_grp_return_idp_ind' : 'Total RET'
})
all_Flows = all_Flows.fillna(0)

all_Flows = all_Flows[[
    'm0305_meta_adm3_label','Pcode ZS','Zone de sante','Population 2023 (DPS)','IDP Influx','IDPs Outflow',
    'Derived Population Total','IDP Origin','IDP CCCM','IDP Non-CCCM','Total IDP',
    'Total RET']]

all_Flows['Not IDP/Returnee'] = all_Flows['Derived Population Total'] - all_Flows['IDP Influx'] - all_Flows['Total IDP'] - all_Flows['Total RET']

all_Flows['IDP Origin Same ZS'] = all_Flows['Total IDP'] / all_Flows['Derived Population Total'] *100
all_Flows['IDP Origin Same ZS'] = all_Flows['IDP Origin Same ZS'].round(2)

all_Flows['IDP Inflow %'] = all_Flows['IDP Influx'] / all_Flows['Derived Population Total'] *100
all_Flows['IDP Inflow %'] = all_Flows['IDP Inflow %'].round(2)

all_Flows['RET Inflow %'] = all_Flows['Total RET'] / all_Flows['Derived Population Total'] *100
all_Flows['RET Inflow %'] = all_Flows['RET Inflow %'].round(2)

all_Flows['Not IDP/RET %'] = all_Flows['Not IDP/Returnee'] / all_Flows['Derived Population Total'] *100
all_Flows['Not IDP/RET %'] = all_Flows['Not IDP/RET %'].round(2)

all_Flows['RET Inflow % 2'] = all_Flows['Total RET'] / all_Flows['Population 2023 (DPS)'] *100
all_Flows['RET Inflow % 2'] = all_Flows['RET Inflow % 2'].round(2)

all_Flows = all_Flows.sort_values(by='RET Inflow %', ascending=False)

print(f'The health zones with the highest percentages of returnees are: {all_Flows[['Zone de sante', 'Derived Population Total', 'Total RET', 'RET Inflow %', 'RET Inflow % 2']]}')



# Mobile network coverage

mobile_Cov = df_locations[['m0304_meta_adm2_label','s1784_loc_mobile_access']].value_counts()
mobile_Cov = mobile_Cov.reset_index()
mob_condition = mobile_Cov['s1784_loc_mobile_access'] == 'yes'
mobile_Cov = mobile_Cov[mob_condition]
mobile_Cov = mobile_Cov[['m0304_meta_adm2_label','count']]

villages_By_Territory = df_locations.groupby('m0304_meta_adm2_label')['m0306_meta_adm4_label'].count()
villages_By_Territory = villages_By_Territory.reset_index()

total_Cov = mobile_Cov['count'].sum()
total_Cov = total_Cov / number_of_Villages *100

mobile_Cov_Admin_2 = mobile_Cov.merge(villages_By_Territory, on='m0304_meta_adm2_label')
mobile_Cov_Admin_2['percentage'] = mobile_Cov_Admin_2['count'] / mobile_Cov_Admin_2['m0306_meta_adm4_label'] *100
mobile_Cov_Admin_2 = mobile_Cov_Admin_2.sort_values(by='percentage', ascending=False)
print(mobile_Cov_Admin_2)

print("\n")

print(
f'Of all the villages surveyed, {total_Cov.round(0)} per cent reported having access to a mobile network. '
f"The territories of {mobile_Cov_Admin_2['m0304_meta_adm2_label'].iloc[0]} and {mobile_Cov_Admin_2['m0304_meta_adm2_label'].iloc[1]} \n"
f"reported the best access to mobile networks. The territories of {mobile_Cov_Admin_2['m0304_meta_adm2_label'].iloc[-1]} "
f"and {mobile_Cov_Admin_2['m0304_meta_adm2_label'].iloc[-2]} reported the lowest percentage of mobile network access."
)



# Priority-needs scoring

df_loc_borda = df_locations[['m0304_meta_adm2_label', 'm0305_meta_adm3_label', 'm1560_loc_first_important_need',
'm1561_loc_second_important_need','m1562_loc_third_important_need', 'm1563_loc_fourth_important_need', 'm1564_loc_fifth_important_need']].copy()
# Ranked need categories: health, NFI, WASH, education, food, employment, transport, protection, shelter, other

# Health
df_loc_borda['Health'] = np.where(df_loc_borda['m1560_loc_first_important_need'] == 'health', 5,
np.where(df_loc_borda['m1561_loc_second_important_need'] == 'health', 4,
np.where(df_loc_borda['m1562_loc_third_important_need'] == 'health', 3,
np.where(df_loc_borda['m1563_loc_fourth_important_need'] == 'health', 2,
np.where(df_loc_borda['m1564_loc_fifth_important_need'] == 'health', 1,0
)))))

# NFI
df_loc_borda['NFI'] = np.where(df_loc_borda['m1560_loc_first_important_need'] == 'nfi', 5,
np.where(df_loc_borda['m1561_loc_second_important_need'] == 'nfi', 4,
np.where(df_loc_borda['m1562_loc_third_important_need'] == 'nfi', 3,
np.where(df_loc_borda['m1563_loc_fourth_important_need'] == 'nfi', 2,
np.where(df_loc_borda['m1564_loc_fifth_important_need'] == 'nfi', 1,0
)))))

# Education
df_loc_borda['Education'] = np.where(df_loc_borda['m1560_loc_first_important_need'] == 'education', 5,
np.where(df_loc_borda['m1561_loc_second_important_need'] == 'education', 4,
np.where(df_loc_borda['m1562_loc_third_important_need'] == 'education', 3,
np.where(df_loc_borda['m1563_loc_fourth_important_need'] == 'education', 2,
np.where(df_loc_borda['m1564_loc_fifth_important_need'] == 'education', 1,0
)))))

df_loc_borda['WASH'] = np.where(df_loc_borda['m1560_loc_first_important_need'] == 'wash', 5,
np.where(df_loc_borda['m1561_loc_second_important_need'] == 'wash', 4,
np.where(df_loc_borda['m1562_loc_third_important_need'] == 'wash', 3,
np.where(df_loc_borda['m1563_loc_fourth_important_need'] == 'wash', 2,
np.where(df_loc_borda['m1564_loc_fifth_important_need'] == 'wash', 1,0
)))))

df_loc_borda['Food'] = np.where(df_loc_borda['m1560_loc_first_important_need'] == 'food', 5,
np.where(df_loc_borda['m1561_loc_second_important_need'] == 'food', 4,
np.where(df_loc_borda['m1562_loc_third_important_need'] == 'food', 3,
np.where(df_loc_borda['m1563_loc_fourth_important_need'] == 'food', 2,
np.where(df_loc_borda['m1564_loc_fifth_important_need'] == 'food', 1,0
)))))

df_loc_borda['Employment'] = np.where(df_loc_borda['m1560_loc_first_important_need'] == 'employment', 5,
np.where(df_loc_borda['m1561_loc_second_important_need'] == 'employment', 4,
np.where(df_loc_borda['m1562_loc_third_important_need'] == 'employment', 3,
np.where(df_loc_borda['m1563_loc_fourth_important_need'] == 'employment', 2,
np.where(df_loc_borda['m1564_loc_fifth_important_need'] == 'employment', 1,0
)))))

df_loc_borda['Protection'] = np.where(df_loc_borda['m1560_loc_first_important_need'] == 'protection', 5,
np.where(df_loc_borda['m1561_loc_second_important_need'] == 'protection', 4,
np.where(df_loc_borda['m1562_loc_third_important_need'] == 'protection', 3,
np.where(df_loc_borda['m1563_loc_fourth_important_need'] == 'protection', 2,
np.where(df_loc_borda['m1564_loc_fifth_important_need'] == 'protection', 1,0
)))))

df_loc_borda['Transport'] = np.where(df_loc_borda['m1560_loc_first_important_need'] == 'transport', 5,
np.where(df_loc_borda['m1561_loc_second_important_need'] == 'transport', 4,
np.where(df_loc_borda['m1562_loc_third_important_need'] == 'transport', 3,
np.where(df_loc_borda['m1563_loc_fourth_important_need'] == 'transport', 2,
np.where(df_loc_borda['m1564_loc_fifth_important_need'] == 'transport', 1,0
)))))

df_loc_borda['Shelter'] = np.where(df_loc_borda['m1560_loc_first_important_need'] == 'shelter', 5,
np.where(df_loc_borda['m1561_loc_second_important_need'] == 'shelter', 4,
np.where(df_loc_borda['m1562_loc_third_important_need'] == 'shelter', 3,
np.where(df_loc_borda['m1563_loc_fourth_important_need'] == 'shelter', 2,
np.where(df_loc_borda['m1564_loc_fifth_important_need'] == 'shelter', 1,0
)))))

df_loc_borda['Other'] = np.where(df_loc_borda['m1560_loc_first_important_need'] == 'other', 5,
np.where(df_loc_borda['m1561_loc_second_important_need'] == 'other', 4,
np.where(df_loc_borda['m1562_loc_third_important_need'] == 'other', 3,
np.where(df_loc_borda['m1563_loc_fourth_important_need'] == 'other', 2,
np.where(df_loc_borda['m1564_loc_fifth_important_need'] == 'other', 1,0
)))))

# Aggregate and rank priority needs

borda_Count = df_loc_borda.groupby(['m0304_meta_adm2_label', 'm0305_meta_adm3_label'])[['Health','NFI','WASH','Education','Food', 'Employment', 'Transport', 'Protection', 'Shelter', 'Other']].mean()
borda_Count = borda_Count.reset_index()
borda_Count = borda_Count.set_index(['m0304_meta_adm2_label', 'm0305_meta_adm3_label'])

borda_Total = df_loc_borda[['m0304_meta_adm2_label', 'm0305_meta_adm3_label','Health','NFI','WASH','Education','Food', 'Employment', 'Transport', 'Protection', 'Shelter', 'Other']]
borda_Total = borda_Total.set_index(['m0304_meta_adm2_label', 'm0305_meta_adm3_label'])
borda_Total = borda_Total.mean()
borda_Count.loc['Grand Total'] = borda_Total

average_Col = borda_Count[['Health','NFI','WASH','Education','Food', 'Employment', 'Transport', 'Protection', 'Shelter']].sum(axis=1)
average_Col = 15 / average_Col

borda_Count_2 = borda_Count[['Health','NFI','WASH','Education','Food', 'Employment', 'Transport', 'Protection', 'Shelter']]
borda_Final = borda_Count_2.multiply(average_Col, axis=0)

ranked = borda_Final.loc['Grand Total']
ranked = ranked.sort_values(ascending=False).index
ranked = borda_Final[ranked]

print(ranked.round(1))