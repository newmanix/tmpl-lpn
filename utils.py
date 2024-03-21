import math

def add_emojis(movie_dict):
  for movie in movie_dict:
    if movie['rating'] == 3:
      movie['emoji'] = "😐"
    elif movie['rating'] >= 4:
      movie['emoji'] =  "😊"
    else:
      movie['emoji'] ="☹️"
  return movie_dict


def movie_stars(movie_dict):
  for movie in movie_dict:
    movie['stars'] = add_stars(movie['rating'])
  return movie_dict


def add_stars(rating):
  my_return = ""
  for x in range(math.ceil(rating)):
    x=x+1
    half = "-half" if type(rating) == float and x == math.ceil(rating) else ""
    my_return += f"<span class=\"fa fa-star{half}\"></span>"
  return my_return


