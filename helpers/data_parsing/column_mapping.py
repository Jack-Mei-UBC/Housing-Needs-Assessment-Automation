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
    "Total - Aboriginal": "total aboriginal",
    "Total - Immigrant": "total immigrant",
    "family type of the primary": "total family type of PHM",
    "immigration of the prim": "total immigration of PHM",
    "Sex of the prim": "total sex of PHM",
    "Total - Visible minority ho": "total visible minority",
    "Total - Visible minority st": "total minority of PHM",
    "by age group": "total age of PHM",
    "85 years and over": "85+",
    "female lone": "single mom",
    "recent immigrant": "immigrant",
    "is female": "female",
    "Aboriginal household": "aboriginal",
    "between 65 years and over": "65+",
    "under 24 years": "under 24",
    "Black": "black",
    "minority household": "minority",
    "Owner": "owner",
    "Renter": "renter",
    "1 person": "1 person",
    "2 persons": "2 persons",
    "3 persons": "3 persons",
    "4 persons": "4 persons",
    "5 or more persons": "5+ persons",
    "Household size": "total by household size",
    "tenure and mortgage": "total by ownership",
    "income 20% or": "very low income",
    "income 121% or": "very high income",
    "income 21% to 50%": "low income",
    "income 51% to 80%": "moderate income",
    "income 81% to 120%": "high income",
    "shelter cost 0.5%": "very low shelter cost",
    "shelter cost 0.6% to 1.25%": "low shelter cost",
    "shelter cost 1.26% to 2%": "moderate shelter cost",
    "shelter cost 2.01% to 3%": "high shelter cost",
    "shelter cost 3.1% or": "very high shelter cost",
    "by household income proportion to AMHI": "total by household income",
    "by shelter cost proportion to AMHI": "total by shelter cost",
    "in core housing need": "CHN",
    "examined for core housing need": "examined for CHN",
}