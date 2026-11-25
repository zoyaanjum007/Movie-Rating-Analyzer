import pandas as pd
import matplotlib.pyplot as plt

try:
    df = pd.read_csv("movies.csv")
except FileNotFoundError:
    print("Error: movies.csv file not found.")
    exit()

valid_rows = []

for index, row in df.iterrows():
    row_number = index + 1

    if pd.isna(row["Movie"]) or pd.isna(row["Genre"]) or pd.isna(row["Rating"]):
        print("Row", row_number, "skipped: Missing value.")
        continue

    try:
        rating = float(row["Rating"])
    except (ValueError, TypeError):
        print("Row", row_number, "skipped: invalid Rating '" + str(row["Rating"]) + "'.")
        continue

    if rating < 0 or rating > 10:
        print("Row", row_number, "skipped: Rating", rating, "must be between 0 and 10.")
        continue

    valid_rows.append({
        "Movie": row["Movie"],
        "Genre": row["Genre"],
        "Rating": rating
    })

df = pd.DataFrame(valid_rows)

old_count = len(df)
df = df.drop_duplicates()
duplicate_count = old_count - len(df)

if duplicate_count > 0:
    print("Duplicate rows skipped:", duplicate_count)

print("Valid rows:", len(df))
if df.empty:
    print("No valid movie records found.")
    exit()

while True:
    print("\nMOVIE RATING ANALYZER")
    print("---------------------")
    print("1. Movie Rating Statistics")
    print("2. Genre-wise Analysis")
    print("3. Display Charts")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        average_rating = df["Rating"].mean()
        highest_rating = df["Rating"].max()
        lowest_rating = df["Rating"].min()

        top_movie = df.loc[df["Rating"].idxmax()]
        lowest_movie = df.loc[df["Rating"].idxmin()]

        print("\nMOVIE RATING STATISTICS")
        print("-----------------------")
        print("Average Rating:", round(average_rating, 2))
        print("Highest Rating:", highest_rating)
        print("Lowest Rating:", lowest_rating)

        print("\nTOP AND LOWEST RATED MOVIES")
        print("---------------------------")
        print("Top rated:", top_movie["Movie"], "(", top_movie["Rating"], ")")
        print("Lowest rated:", lowest_movie["Movie"], "(", lowest_movie["Rating"], ")")

    elif choice == "2":
        genre_average = df.groupby("Genre")["Rating"].mean()

        print("\nGENRE-WISE AVERAGE RATINGS")
        print("--------------------------")
        print(genre_average.round(2))

        best_genre = genre_average.idxmax()
        highest_average = genre_average.max()

        print("\nBEST GENRE:", best_genre)
        print("Average Rating:", round(highest_average, 2))

        plt.figure(figsize=(8, 5))
        plt.bar(genre_average.index, genre_average.values)
        plt.title("Genre-wise Average Movie Ratings")
        plt.xlabel("Genre")
        plt.ylabel("Average Rating")
        plt.ylim(0, 10)
        plt.savefig("genre_ratings.png")
        plt.show()

    elif choice == "3":
        
        plt.figure(figsize=(8, 5))
        plt.hist(df["Rating"], bins=5, edgecolor="black")
        plt.title("Distribution of Movie Ratings")
        plt.xlabel("Movie Rating")
        plt.ylabel("Number of Movies")
        plt.savefig("rating_distribution.png")
        plt.show()

    elif choice == "4":
        print("Thank you for using Movie Rating Analyzer!")
        break

    else:
        print("Invalid choice. Please try again.")
