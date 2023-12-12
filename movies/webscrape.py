from bs4 import BeautifulSoup
import requests


def rotten_tomatoes_rating(movie_name: str):
    movie_name = movie_name.replace("-", " ").replace(":", " ")
    movie_name = "_".join(movie_name.split())

    HTTPS = f"https://www.rottentomatoes.com/m/{movie_name}"

    response = requests.get(HTTPS)
    if response.status_code == 200:
        html = BeautifulSoup(response.content, "html.parser")
        rating = html.find(
            "score-board-deprecated", id="scoreboard").get("tomatometerscore")
        return rating
    else:
        return None


'''IMDB does not allow webscrape and does not provide Public Api'''
# def get_movie_rating(movie_title):
#     # Replace spaces with underscores and make a lowercase version of the title
#     formatted_title = '_'.join(movie_title.split()).lower()

#     # IMDb URL for movie search
#     url = f'https://www.imdb.com/find?q={formatted_title}&s=tt&ttype=ft&ref_=fn_ft'
#     url = "https://www.imdb.com/?ref_=nv_home"
#     # Send an HTTP request to the IMDb URL
#     response = requests.get(url)
#     print(response.status_code)
#     # Check if the request was successful (status code 200)
#     if response.status_code == 200:
#         # Parse the HTML content of the page
#         soup = BeautifulSoup(response.content, 'html.parser')

#         # Find the first search result link
#         result_link = soup.find('td', class_='result_text').a
#         print(result_link)
#         # Extract the IMDb ID from the link
#         imdb_id = result_link['href'].split('/')[2]

#         # IMDb URL for the movie details page
#         movie_url = f'https://www.imdb.com/title/{imdb_id}/'
#         print(movie_url)
#         # Send another HTTP request to the movie details page
#         response_movie = requests.get(movie_url)

#         if response_movie.status_code == 200:
#             # Parse the HTML content of the movie details page
#             soup_movie = BeautifulSoup(
#                 response_movie.content, 'html.parser')

#             # Find the movie rating element
#             rating_element = soup_movie.find(
#                 'span', itemprop='ratingValue')

#             if rating_element:
#                 # Extract the movie rating
#                 movie_rating = rating_element.text
#                 return f"The rating of {movie_title} is {movie_rating}."
