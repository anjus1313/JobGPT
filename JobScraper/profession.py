from datetime import datetime


class Profession:
    title = None
    company = None
    location = None
    date = 'Jan 01 2022'
    date_object = None
    content = None
    link = None
    platform = 'Simplify'
    type = None

    def clean_up(self):
        attributes = ['title', 'company', 'location', 'date', 'content', 'link', 'platform', 'type']
        for attribute in attributes:
            if getattr(self, attribute):
                cleaned_value = getattr(self, attribute).strip().lower()
                encoded_string = cleaned_value.encode("ascii", "ignore")
                cleaned_value = encoded_string.decode()
                setattr(self, attribute, cleaned_value)

    def convert_date(self):
        default_year = datetime.now().year
        default_date = "01"
        if len(self.date.split()[1]) == 2:
            try:
                self.date_object = datetime.strptime(self.date + ' ' + str(default_year), '%b %d %Y')
            except ValueError:
                self.date_object = datetime.strptime('Jan 01 2022', '%b %d %Y')
        elif len(self.date.split()[1]) == 4:
            try:
                self.date_object = datetime.strptime(
                    self.date.split()[0] + ' ' + default_date + ' ' + self.date.split()[1], '%b %d %Y')
            except ValueError:
                self.date_object = datetime.strptime('Jan 01 2022', '%b %d %Y')
        else:
            self.date_object = datetime.strptime('Jan 01 2022', '%b %d %Y')
