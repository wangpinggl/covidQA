import json
class Utility:
    def __init__(self):
        self.day_dict = {'1st': '01', '2nd': '02', '3rd': '03', '4th': '04', '5th': '05', '6th': '06', '7th': '07', '8th': '08',
                '9th': '09', '10th': 10, '11th': 11, '12th': 12, '13th': 13, '14th': 14, '15th': 15, '16th': 16,
                '17th': 17, '18th': 18, '19th': 19, '20th': 20, '21st': 21, '22nd': 22, '23rd': 23, '24th': 24,
                '25th': 25, '26th': 26, '27th': 27, '28th': 28}
        self.month_dict = {'January' : "01", 'February' : "02", 'March' : "03", 'April' : "04", 'May' : "05", 'June' : "06", 'July' : "07" , 'August' : "08", 'September' : "09", 'October' : "10", 'November' : "11", 'December' : "12"}

        self.month_dict6 = {'January' : "Jan", 'February' : "Feb", 'March' : "Mar", 'April' : "Apr", 'May' : "May", 'June' : "Jun", 'July' : "Jul" , 'August' : "Aug", 'September' : "Sep", 'October' : "Oct", 'November' : "Nov", 'December' : "Dec"}

        self.state_dict = {'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'}
        self.case_entity = ['cases', 'confirmed cases', 'deaths']
        
        self.demographic_entity = ['sex', 'race', 'age', 'age group', 'race and ethnicity', 'ethnicity', 'gender']

        self.entities = ['Demographic Entity', 'Value Entity', 'Amount Entity', 'Case Entity']
        
        self.amount_entity = ['number of', 'percentage of']