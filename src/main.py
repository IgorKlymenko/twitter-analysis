import get_leads
import get_posts
import filter

DATAFILE = "../data/leads.csv"

def main():
    print("Collecting Leads...")
    get_leads.main(DATAFILE = DATAFILE, count = 10)

    print("Collecting Posts...")
    get_posts.main(months = 2)

    print("Filtering...")
    filter.main()

if __name__ == "__main__":
    main()
