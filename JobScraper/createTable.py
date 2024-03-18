from JobScraper import dbFunctions as db

if __name__ == "__main__":
    db.delete_table()
    db.create_table()
