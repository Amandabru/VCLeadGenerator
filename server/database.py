import sqlite3


# We move all the ugly database calls here to be able to see what's going on in the scraper
class Database:

    def __init__(self, db):

        self.con = sqlite3.connect(db + ".db")

        # BE CAREFUL W THESE
        # self.con.execute("DROP TABLE profile")
        # self.con.execute("DROP TABLE company")
        # self.con.execute("DROP TABLE experience")

        self.con.execute("CREATE TABLE IF NOT EXISTS profile(profile_id TEXT UNIQUE, saved BOOLEAN)")
        self.con.execute(
            "CREATE TABLE IF NOT EXISTS company(company_id TEXT,name TEXT, description TEXT, website_url TEXT, saved BOOLEAN)")
        self.con.execute(
            "CREATE TABLE IF NOT EXISTS experience(profile_id TEXT, company_id TEXT, role TEXT, start_date DATE, end_date DATE)")
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

    def add_company(self, company_id, ):
        # Todo expand to allow company data to be inserted
        if company_id not in self.saved_companies and company_id not in self.potential_companies:
            self.potential_companies.add(company_id)
            self.con.execute(
                f"INSERT INTO company (company_id, saved) VALUES ('{company_id}', false) ON CONFLICT DO NOTHING")

    def add_profile(self, profile_id, saved):
        self.con.execute(f"INSERT OR REPLACE INTO profile (profile_id, saved) VALUES ('{profile_id}', {saved})")
        if saved:
            self.saved_profiles.add(profile_id)
            if profile_id in self.potential_profiles:
                self.potential_profiles.remove(profile_id)
        else:
            if profile_id not in self.saved_profiles:
                self.potential_profiles.add(profile_id)

    def add_experience(self, profile_id, company_id, role, start_date, end_date):
        self.con.execute(
            f"INSERT INTO experience (profile_id, company_id, role, start_date, end_date) VALUES ('{profile_id}', '{company_id}', '{role}', '{start_date}', '{end_date}')")

    def commit(self):
        self.con.commit()
