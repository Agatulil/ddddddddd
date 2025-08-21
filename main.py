import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("IMDB-Movie-Data.csv")
df = df.dropna(subset=["Genre", "Year", "Director", "Actors", "Rating"])

# === 1: Режиссёры ===
directors_stats = df.groupby("Director").agg(
    Avg_Rating=("Rating", "mean"),
    Film_Count=("Title", "count")
).reset_index()
directors_stats = directors_stats[directors_stats["Film_Count"] >= 5]
directors_stats = directors_stats.sort_values(by="Avg_Rating", ascending=False)

print("=== Топ режиссёров (≥5 фильмов) ===")
print(directors_stats.head(10), "\n")

# Визуализация: топ 10 режиссёров
plt.figure(figsize=(10,5))
top_directors = directors_stats.head(10)
plt.barh(top_directors["Director"], top_directors["Avg_Rating"], color="skyblue")
plt.gca().invert_yaxis()
plt.xlabel("Средний рейтинг")
plt.title("Топ 10 режиссёров (≥5 фильмов)")
plt.show()

# === 2: Актёры ===
actor_ratings = {}
for _, row in df.iterrows():
    actors = [a.strip() for a in row["Actors"].split(",")]
    for actor in actors:
        actor_ratings.setdefault(actor, []).append(row["Rating"])

actor_avg = [
    (actor, sum(ratings) / len(ratings), len(ratings))
    for actor, ratings in actor_ratings.items()
    if len(ratings) >= 5
]
actor_avg_df = pd.DataFrame(actor_avg, columns=["Actor", "Avg_Rating", "Film_Count"])
actor_avg_df = actor_avg_df.sort_values(by="Avg_Rating", ascending=False)

print("=== Топ актёров (≥5 фильмов) ===")
print(actor_avg_df.head(10), "\n")

# Визуализация: топ 10 актёров
plt.figure(figsize=(10,5))
top_actors = actor_avg_df.head(10)
plt.barh(top_actors["Actor"], top_actors["Avg_Rating"], color="lightgreen")
plt.gca().invert_yaxis()
plt.xlabel("Средний рейтинг")
plt.title("Топ 10 актёров (≥5 фильмов)")
plt.show()

# === 3: Жанры по годам ===
genre_ratings = df.groupby(["Genre", "Year"])["Rating"].mean().reset_index()
best_genre_per_year = genre_ratings.loc[genre_ratings.groupby("Year")["Rating"].idxmax()]
print("=== Лучший жанр по годам ===")
print(best_genre_per_year, "\n")

# Визуализация: лучший жанр по годам
plt.figure(figsize=(12,5))
plt.plot(best_genre_per_year["Year"], best_genre_per_year["Rating"], marker="o")
for x, y, g in zip(best_genre_per_year["Year"], best_genre_per_year["Rating"], best_genre_per_year["Genre"]):
    plt.text(x, y+0.02, g, ha="center", fontsize=8)
plt.xlabel("Год")
plt.ylabel("Средний рейтинг")
plt.title("Лучший жанр по каждому году")
plt.show()

# === 4: Топ 1000 фильмов ===
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

top_movies = df.sort_values(by="Rating", ascending=False).head(1000)
print("=== Топ 1000 фильмов по рейтингу ===")
print(top_movies[["Title", "Year", "Genre", "Rating"]].to_string(index=False))

# Визуализация: распределение рейтингов топ-1000
plt.figure(figsize=(8,5))
plt.hist(top_movies["Rating"], bins=20, color="orange", edgecolor="black")
plt.xlabel("Рейтинг")
plt.ylabel("Количество фильмов")
plt.title("Распределение рейтингов (топ-1000 фильмов)")
plt.show()
