from reviews.models import (Category,
                            Comment,
                            Genre,
                            GenreTitle,
                            Review,
                            Title)


#TODO:
model_by_filename = {
    'category': Category,
    'genre': Genre,
    'titles': Title,
    'genre_title': GenreTitle,
    #'users': User,
    'review': Review,
    'comments': Comment,
}
