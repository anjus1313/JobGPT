from JobScraper import dbFunctions as db, scraperFunctions as scraper
import multiprocessing


class JobSites:
    site_url = None
    site_type = None

    def __init__(self, site_url, site_type):
        self.site_url = site_url
        self.site_type = site_type


def load_data(job):
    job.content = scraper.scrape_simplify(job.link)
    job.clean_up()
    job.convert_date()
    db.load_table(job)


if __name__ == "__main__":
    job_sites = []
    job_site1 = JobSites("https://github.com/SimplifyJobs/Summer2024-Internships", "Intern")
    job_site2 = JobSites("https://github.com/SimplifyJobs/New-Grad-Positions", "FTE")
    job_sites.append(job_site1)
    job_sites.append(job_site2)
    for job_site in job_sites:
        jobs = scraper.scrape_github(job_site.site_url, job_site.site_type)
        total_jobs = len(jobs)
        batch = 10
        start = 0
        while start < total_jobs:
            end = min(total_jobs, start + batch)
            professions = jobs[start:end]
            processes = []
            for profession in professions:
                process = multiprocessing.Process(target=load_data, args=(profession,))
                processes.append(process)

            for process in processes:
                process.start()

            for process in processes:
                process.join(timeout=10)
                if process.is_alive():
                    process.terminate()
                    print(f"Process {process.pid} timed out. Terminated.")
            start += batch
            print("Batch " + str(int(start / batch)) + " Ended")
    db.display_table_rows()
