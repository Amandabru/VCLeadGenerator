import sqlite3


# We move all the ugly database calls here to be able to see what's going on in the scraper
class Database:

    def __init__(self, db):

        self.con = sqlite3.connect(db + ".db")

        # BE CAREFUL W THESE
        # self.con.execute("DROP TABLE profile")
        # self.con.execute("DROP TABLE company")
        # self.con.execute("DROP TABLE experience")
        # self.con.execute("DROP TABLE education")

        self.con.execute("CREATE TABLE IF NOT EXISTS profile(profile_id TEXT UNIQUE, name TEXT, saved BOOLEAN)")
        self.con.execute(
            "CREATE TABLE IF NOT EXISTS company(company_id TEXT UNIQUE, name TEXT, industry TEXT, size INTEGER, description TEXT, business_summary TEXT, founder_summary TEXT, website TEXT, saved BOOLEAN)")
        self.con.execute(
            "CREATE TABLE IF NOT EXISTS experience(profile_id TEXT, company_id TEXT, role TEXT, start_date DATE, end_date DATE)")
        self.con.execute(
            "CREATE TABLE IF NOT EXISTS education(profile_id TEXT, school_name TEXT, degree TEXT)")
        self.con.commit()
        self.cursor = self.con.cursor()

        self.saved_profiles = set()
        self.potential_profiles = set()
        self.saved_companies = set()
        self.potential_companies = set()

        for row in self.cursor.execute("SELECT profile_id, saved FROM profile").fetchall():
            profile_id, saved = row[0], row[1]
            if saved:
                self.saved_profiles.add(profile_id)
            else:
                self.potential_profiles.add(profile_id)

        for row in self.cursor.execute("SELECT company_id, saved FROM company").fetchall():
            company_id, saved = row[0], row[1]
            if saved:
                self.saved_companies.add(company_id)
            else:
                self.potential_companies.add(company_id)

    def add_company(self, company_id, company_info=None):
        if company_id not in self.saved_companies and company_id not in self.potential_companies:
            self.potential_companies.add(company_id)
            self.con.execute(
                f"INSERT INTO company (company_id, saved) VALUES ('{company_id}', false) ON CONFLICT DO NOTHING")
        if company_info:
            company_name = company_info["name"]
            company_industry = company_info["industry"]
            company_size = int(company_info["size"])
            company_description = company_info["description"]  # Reason for crash is quoutes in desc
            company_website = company_info["website"]
            self.con.execute(
                "INSERT OR REPLACE INTO company (company_id, name, industry, size, description, website, saved) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (company_id, company_name, company_industry, company_size, company_description, company_website, 1)
            )
            if company_id in self.potential_companies:
                self.potential_companies.remove(company_id)
            self.saved_companies.add(company_id)

    def add_company_summaries(self, company_id, business, founders):
        if business and founders:
            self.con.execute(
                "UPDATE company SET business_summary=?, founder_summary=? WHERE company_id=?",
                (business, founders, company_id)
            )
        elif business:
            self.con.execute(
                "UPDATE company SET business_summary=? WHERE company_id=?",
                (business, company_id)
            )

    def get_employee_info(self, company_id):  # What info do we need here - the employees and all of their experience
        employees = {}
        for row in self.cursor.execute(f"SELECT profile_id FROM experience WHERE company_id='{company_id}'").fetchall():
            profile_id = row[0]
            if profile_id not in employees:
                employees[profile_id] = []
        for profile_id in employees:
            employee_string = ""
            profile_row = self.cursor.execute(f"SELECT name FROM profile WHERE profile_id='{profile_id}'").fetchone()
            if profile_row and profile_row[0]:
                employee_string += "Name: " + profile_row[0]
            employees[profile_id].append(employee_string)

            for row in self.cursor.execute(f"SELECT * FROM experience WHERE profile_id='{profile_id}'").fetchall():
                experience_string = "Experience:  "
                if row[1]:
                    experience_string += "Company: " + row[1] + " "
                if row[2]:
                    experience_string += "Role: " + row[2] + " "
                if row[3]:
                    experience_string += "Started: " + row[3] + " "
                if row[4]:
                    experience_string += "Ended: " + row[4] + " "
                employees[profile_id].append(experience_string)
            for row in self.cursor.execute(f"SELECT * FROM education WHERE profile_id='{profile_id}'").fetchall():
                experience_string = "Education:  "
                if row[1]:
                    experience_string += "School: " + row[1] + " "
                if row[2]:
                    experience_string += "Degree: " + row[2] + " "
                employees[profile_id].append(experience_string)
        return employees

    def add_profile(self, profile_id, saved, name=None):
        # First query
        self.con.execute(
            "INSERT OR REPLACE INTO profile (profile_id, saved) VALUES (?, ?)",
            (profile_id, saved)
        )

        # Second query
        if saved and name:
            self.con.execute(
                "INSERT OR REPLACE INTO profile (profile_id, name, saved) VALUES (?, ?, ?)",
                (profile_id, name, saved)
            )
            self.saved_profiles.add(profile_id)
            if profile_id in self.potential_profiles:
                self.potential_profiles.remove(profile_id)
        else:
            self.con.execute(
                "INSERT OR REPLACE INTO profile (profile_id, saved) VALUES (?, ?)",
                (profile_id, saved)
            )
            if profile_id not in self.saved_profiles:
                self.potential_profiles.add(profile_id)

    def add_experience(self, profile_id, company_id, role, start_date, end_date):

        # First case
        if not start_date or not end_date:
            self.con.execute(
                "INSERT INTO experience (profile_id, company_id, role) VALUES (?, ?, ?)",
                (profile_id, company_id, role)
            )

        # Second case
        elif not end_date:
            self.con.execute(
                "INSERT INTO experience (profile_id, company_id, role, start_date) VALUES (?, ?, ?, ?)",
                (profile_id, company_id, role, start_date)
            )

        # Third case
        else:
            self.con.execute(
                "INSERT INTO experience (profile_id, company_id, role, start_date, end_date) VALUES (?, ?, ?, ?, ?)",
                (profile_id, company_id, role, start_date, end_date)
            )

    def add_education(self, profile_id, school_name, degree):
        self.con.execute(
            "INSERT INTO education (profile_id, school_name, degree) VALUES (?, ?, ?)",
            (profile_id, school_name, degree)
        )

    def commit(self):
        self.con.commit()

    def rollback(self):
        self.con.rollback()
