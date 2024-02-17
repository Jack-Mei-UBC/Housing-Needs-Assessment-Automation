# Matching things 1-1 is hell, so we just do a "contains key" search
# Strictest matchings first, then looser comes later
class Comparable:
    def __init__(self, value):
        self.value = value
    def compare(self, input):
        if isinstance(self.value, str):
            return input in self.value
        elif isinstance(self.value, list):
            return any([i in input for i in self.value])


col_map = {
    "female lone": "single mom",
    'PHM is a recent immigrant (immigrated between 2011 and 2016)': "recent immigrant",
    'Visible Minority households': "visible minority",
    "PHM immigrated with a refugee status": "refugee immigrant",
    "PHM is a female lone-parent": "single mom",
    "PHM is female": "female PHM",
    "Aboriginal household status": "aboriginal",
    'PHM is between 65 years and over': "PHM 65+",
    'PHM is between 85 years and over': "PHM 85+",
    'PHM is under 24 years': "under 24",
    "PHM is Black": "black",
    "minority household": "minority",
    "Minority household": "minority",
    "Household has at least one person who had at least one or of combined activity limitations reported for Q11a, Q11b, Q11c or Q11f": "disabled",
    "Household has at least one person with activity limitations reported for Q11d and Q11e or combined Q11d and Q11e health issues": "health issues",
    "Owner": "owner",
    "Renter": "renter",
    "Not subsidized housing": "unsubsidized",
    "Subsidized housing": "subsidized",
    "85 years and over": "85 years+",
    '75 years and over': '75 years+',
}

fuzzy_col_mapping = {
    "Total - Aboriginal": "total by aboriginal",
    'Total - Private households by Aboriginal household status': "total by aboriginal 2",
    "Total - Private households by visible minority ho": "total by minority",
    'Total - Visible minority status of the primary household maintainer (PHM)': "total by minority PHM",
    "Total - Immigrant": "total by immigrant",
    "Total \x96 Immigrant status and admission category of the primary household maintainer (PHM)": "total by immigrant PHM",
    'Total - Private households by immigrant status and period of immigration of the primary household maintainer (PHM)': "total by immigrant PHM 2",
    "Immigrant status and admission category of the primary household maintainer (PHM)": "total by immigrant PHM 3",
    "Total - Private households by presence of at least one or of the combined activity limitations (Q11a, Q11b, Q11c or Q11f or combined)": "total by disability",
    'Total \x96 Private households by presence of at least one or of the combined activity limitations (Q11d or Q11e or combined)': "total by disability 2",
    "Private households by presence of at least one or of the combined activity limitations (Q11d or Q11e or combined)": "total by disability 3",
    "Total - Private households by tenure including presence of mortgage payments and subsidized housing": "total by subsidized housing",
    'Total - Private households by household family type of the primary household maintainer (PHM)': "total by PHM",
    "tenure and mortgage": "total by ownership",
    'Total - Sex of the primary household maintainer (PHM)': "total by gender PHM",
    "by household income proportion to AMHI": "total by income",
    "by shelter cost proportion to AMHI": "total by shelter cost",
    "by core housing need": "total by CHN",
    'Total - Sex': 'total by gender',  # Technically wrong but right in the context of data
    'Total - Gender': 'total by gender',
    'Total - Age': 'total by age',
    'Total - Age groups of primary household maintainer': 'total by age of PHM',
    'Total - Period of construction': 'total by construction period',
    'Total - Structural type of dwelling': 'total by structural type',
    
    "1 person": "1 person",
    "2 persons": "2 persons",
    "3 persons": "3 persons",
    "4 persons": "4 persons",
    "5 or more persons household": "5+ persons",
    "income 20% or": "very low income",
    "income 121% or": "very high income",
    "income 21% to 50%": "low income",
    "income 51%": "moderate income",
    "income 81% to 120%": "high income",
    "shelter cost 0.5%": "very low shelter cost",
    "shelter cost 0.6% to 1.25%": "low shelter cost",
    "shelter cost 1.26% to 2%": "moderate shelter cost",
    "shelter cost 2.1% to 3%": "high shelter cost",
    "shelter cost 3.1% or": "very high shelter cost",
    "in core housing need": "CHN",
    "examined for core housing need": "examined for CHN",
    'Under 25 years': 'under 25 years',
    '0 to 4 years': '0 to 4 years',
    '5 to 9 years': '5 to 9 years',
    '10 to 14 years': '10 to 14 years',
    '15 to 19 years': '15 to 19 years',
    '20 to 24 years': '20 to 24 years',
    '25 to 29 years': '25 to 29 years',
    '30 to 34 years': '30 to 34 years',
    '35 to 39 years': '35 to 39 years',
    '40 to 44 years': '40 to 44 years',
    '45 to 49 years': '45 to 49 years',
    '50 to 54 years': '50 to 54 years',
    '55 to 59 years': '55 to 59 years',
    '60 to 64 years': '60 to 64 years',
    '65 to 69 years': '65 to 69 years',
    '70 to 74 years': '70 to 74 years',
    '75 to 79 years': '75 to 79 years',
    '80 to 84 years': '80 to 84 years',
    '85 to 89 years': '85 to 89 years',
    '90 to 94 years': '90 to 94 years',
    '95 to 99 years': '95 to 99 years',
    '100 years': '100 years+',
    'Population, ': 'population',
    'Median age': 'median age',
}
key_list = list(fuzzy_col_mapping.keys())
for key in key_list:
    fuzzy_col_mapping['.*'+key+'.*'] = fuzzy_col_mapping.pop(key)