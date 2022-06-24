from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Movie, Critic, Review, Rating, TopCritics
from django.contrib.auth import get_user_model
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import minmax_scale
from itertools import chain
import pandas as pd
import numpy as np

User = get_user_model()

class MovieListView(ListView):
    model = Movie
    paginate_by = 25
    ordering = ['title']
    context_object_name = 'movie_list'
    template_name = 'movies/movie_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        sort_by = self.request.GET.get('sortBy') if self.request.GET.get('sortBy') else 'title'
        if query:
            object_list = self.model.objects.filter(title__icontains=query).order_by(sort_by)
        else:
            object_list = self.model.objects.all().order_by(sort_by)
        return object_list

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if not self.request.user.is_anonymous:
            ratings = Rating.objects.filter(user=self.request.user)
        else:
            return data

        data['ratings'] = {rating.movie.id: rating.score for rating in ratings}
        
        top_critics = TopCritics.objects.filter(user=self.request.user)[:5]
        personalized_ratings, count = {}, {}
        for critic_obj in top_critics:
            reviews = critic_obj.critic.review_set.all()

            for review in reviews:
                if review.movie.title not in personalized_ratings:
                    count[review.movie.title] = 1
                    personalized_ratings[review.movie.title] = review.normalized_score
                else:
                    personalized_ratings[review.movie.title] += review.normalized_score
                    count[review.movie.title] += 1
        data['personalized_ratings'] = {x: personalized_ratings[x] / count[x] for x in count.keys()}
        return data

class MovieDetailView(DetailView):
    model = Movie
    context_object_name = 'movie'
    template_name = 'movies/movie_detail.html'

class CriticListView(ListView):
    model = Critic
    paginate_by = 25
    ordering = ['name']
    context_object_name = 'critic_list'
    template_name = 'movies/critic_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        # sort_by = self.request.GET.get('sortBy') if self.request.GET.get('sortBy') else 'name'

        if query:
            object_list = self.model.objects.filter(name__icontains=query).order_by('name')
        else:
            object_list = self.model.objects.all().order_by('name')
        
        '''
        if sort_by == 'match' or sort_by == '-match':
            top_critics = TopCritics.objects.filter(user=self.request.user).order_by(sort_by)

            if sort_by == 'match':
                object_list = list(chain(top_critics, object_list))
            else:
                object_list = list(chain(object_list, top_critics))
        '''
        return object_list

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if not self.request.user.is_anonymous:
            top_critics = TopCritics.objects.filter(user=self.request.user)
            data['top_critics'] = {critic.critic.name: critic.match for critic in top_critics}
        return data

class CriticDetailView(DetailView):
    model = Critic
    context_object_name = 'critic'
    template_name = 'movies/critic_detail.html'

class TopCriticsView(ListView):
    model = TopCritics
    paginate_by = 25
    context_object_name = 'top_critics'
    template_name = 'movies/top_critics_list.html'

class RateMovieView(DetailView):
    def post(self, request, *args, **kwargs):
        name, value, id = request.POST['name'], request.POST['value'], request.POST['id']

        # Update/create user rating for movie
        user = User.objects.get(username=request.user)
        movie = Movie.objects.get(title=name, id=id[:id.find('-rating')])

        rating, created = Rating.objects.get_or_create(
            user=user,
            movie=movie
        )

        rating.score = value
        rating.save()

        recommender_engine = Recommender(user)
        recommender_engine.update_db()
        
        return JsonResponse({"instance": request.POST}, status=200)
        

class Recommender:
    def __init__(self, user):
        self.user = user
        self.user_id = str(user.id)

    def get_similar_critics(self):
        user_ratings = self.get_user_ratings()
        critic_ratings = self.get_critic_ratings()

        ratings = critic_ratings.append(user_ratings)
        normalized_ratings = self.normalize_ratings(ratings)

        similarity_matrix = self.build_similarity_matrix(normalized_ratings)

        # Find 100 closest neighbors with similar ratings
        sim_50_matrix = self.find_n_neighbours(similarity_matrix, 100)
        similar_critics = sim_50_matrix[sim_50_matrix.index.str.fullmatch(self.user_id)].values
        similar_critics = similar_critics.squeeze().tolist()

        # Get correlation
        match = [similarity_matrix.loc[x, self.user_id] for x in similar_critics]

        # Add the min and max values to normalize the data
        match.extend([0, match[0] + 0.01])
        match = self.normalize_list_numpy(match)[:-2]

        # Create similarity dictionary
        similar_critics = dict(zip(similar_critics, match))

        return similar_critics

    def update_db(self):
        similar_critics = self.get_similar_critics()
        self.update_top_critics(similar_critics)
    
    def get_user_ratings(self):
        '''
            Store all movie ratings by a user in a pandas dataframe and nomralize the score to a range of 1-10.
        '''
        user_ratings_list = list(Rating.objects.filter(user=self.user).values('user__id', 'movie__id', 'score'))

        user_ratings = pd.DataFrame(user_ratings_list)
        user_ratings.rename(columns={'user__id': 'critic__id', 'score': 'normalized_score'}, inplace=True)
        user_ratings["normalized_score"] = 10 * user_ratings["normalized_score"]

        return user_ratings

    def get_critic_ratings(self):
        '''
            Returns a pandas dataframe containing all critic ratings
        '''
        return pd.DataFrame(list(Review.objects.all().values('critic__id', 'movie__id', 'normalized_score')))

    def normalize_ratings(self, ratings):
        '''
            Normalize ratings to account for differences critics/users rate movies. 
        '''
        ratings['critic__id'] = ratings['critic__id'].astype(str)

        # Get average rating given by critic
        critic_avg_rating = ratings.groupby(by="critic__id",as_index=False)['normalized_score'].mean()  
        critic_avg_rating.columns = critic_avg_rating.columns.map(str)

        # Get rating variance by subtracting the critics rating by their average rating
        rating_avg = pd.merge(ratings, critic_avg_rating, on='critic__id')
        rating_avg['rating_variance'] = pd.to_numeric(rating_avg['normalized_score_x']) - rating_avg['normalized_score_y']

        return rating_avg

    def build_similarity_matrix(self, ratings):
        # Create pivot table of ratings
        ratings_pivot_table = pd.pivot_table(ratings, values='rating_variance', index='critic__id', columns='movie__id')

        # Fill in NaN values with critic average
        critics = ratings_pivot_table.apply(lambda row: row.fillna(row.mean()), axis=1)
        critics.columns = critics.columns.map(str)

        # Calculate similarity usisng cosine similarity
        cosine = cosine_similarity(critics)
        np.fill_diagonal(cosine, 0)
        similarity_matrix = pd.DataFrame(cosine, index=critics.index)
        similarity_matrix.columns = critics.index

        return similarity_matrix

    def find_n_neighbours(self, df, n):
        order = np.argsort(df.values, axis=1)[:, :n]
        df = df.apply(lambda x: pd.Series(x.sort_values(ascending=False)
            .iloc[:n].index, 
            index=['top{}'.format(i) for i in range(1, n+1)]), axis=1)
        return df
    
    def normalize_list_numpy(self, list_numpy):
        normalized_list = minmax_scale(list_numpy)
        return normalized_list

    def update_top_critics(self, critics):
        '''
            Update db with similar critics and their correlation
        '''
        # Delete previous top matching critics
        TopCritics.objects.all().delete()

        for critic_id, score in critics.items():
            critic = Critic.objects.get(id=critic_id)

            top_critic, created = TopCritics.objects.get_or_create(
                user=self.user,
                critic=critic,
            )

            top_critic.match = score * 100
            top_critic.save()
    

