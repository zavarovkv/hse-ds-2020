## Film Recommendation: Algorithm
You are tasked with developing a movie recommendation system. You are given a list of movies (their names) and a list of similarities between movies (pairs of movies that are similar). You are also given a list of user's friends and for each friend a list of movies that he has already seen. Your system should recommend one movie with the highest discussability and uniqueness. Discussability is the number of friends of user, who have already seen that movie. Uniqueness is 1 divided by the mean number of similar movies that the user's friends have already seen. So you should return the film with the highest number: F / S, where F = number of friends who have seen this movie, and S = mean of the number of similar movies seen for each friend.

### Preparation of input data
Suppose, we have __N__ movies, __M__ user's friends and __R__ similarities between films.  
Convert list of movies to dictionary with key equals ID of movie and value equals properties of movie. Let's call this dictionary __movies_dict__, example: `{0: 'The Good, the Bad and the Ugly', 1: 'Life Is Beautiful', ...}`.  
Convert list of similarities between movies to adjacency dict. Let's call this dictionary __similarity_dict__, example: `{0: [1, 2, 3], 1: [0, 2, 3], ...}`  
Convert user's friends list to dictionary too, example `{0: [0, 1, 3], 1: [4, 10, 11], ...}`. Let's call this dict like __friends_dict__  
  
  Time estimate for preparation data: O(M) + O(R) + O(N)

### Calculate Discussability
Result of discussability calculations will kepp in __discussability_dict__. 

```python
For each friend in friends_dict
    For each movie in friends_dict[friend]
        discussability_dict[movie]++
```
After that, __discussability_dict__ should contains all movies, which user's friends have ever watched, in other words `len(discussability_dict) ⩽ len(movies_dict)`.  
  
So, max time estimate for discussability is O(M*N).  

### Calculate Uniqueness
Now we need to determine for each movie (like vertex of the graph) the number of the connected component. Will store the connected components in the dictionary __components_dict__. To determine the connectivity component, we will use the depth-first search (DFS) algorithm.  
```python
    components_dict = dict()
    visited = dict()
    num_components = 0

    dfs(v)
        components_dict[v] = num_components
        visited[v] = True
        for w in similarity_dict[v]
            if w not visited
                dfs(w)

    for v in similarity_dict
        if v not visited
            dfs(v)
            num_components++
```
Thus, we can determine the component of connectivity for each movie during the time O(N + R), where N - number of films, R - number of pairs of matches between films.  
  
Now we should calculate final score of discussabilities and choose the largest.  
  
```python

For each film in discussability
    For each friend in friends_dict
        For each friend_film in friends_dict[friend]
            If components_dict[film] == components_dict[friend_film]
                uniqueness[film]++

    film_mean = uniqueness[film] / len(friends_dict)
    coef[film] = discussability[film] / film_mean

return max(coef)
```
  
Time estimation: O(N * M * N) = O(N^2 * M)  
