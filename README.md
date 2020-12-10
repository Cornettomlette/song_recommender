# Song Recommendation System
This is a guided project conducted at __Ironhack__.

### Scenario
You have been hired as a Data Analyst for “Gnod”, which is a site that provides recommendations for music based on collaborative filtering algorithms.

You got a task to build a system which would give users two new possibilities when searching for recommendations:

- Songs that are actually similar to the ones they picked from an _acoustic_ point of view.
- Songs that are _popular_ around the world right now, independently from their tastes.

## Approach

- **The dataset**: two sources of song information:
  - The Billboard Hot 100 songs (updated every day)
  - Kaggle dataset of ~160K songs from Spotify with songs' audio features
  
1) **Building the first MVP.** One branch of making a song recommendation would be figuring, if a song is among Bilboard Top 100 and if it is, than recommend a random song from that Hot 100 list. 

2) **Performing K-means clustering and saving the trained clustering model.** The next step would be to deal with a case, when user inputs a song which is not among Hot 100. We approached this problem by building a vast song database, clustered by audio features of songs. The optimal number of clusters after performing K-means clustering was **7**.

3) **Using SpotiPy API wrapper.** Having a song database with clusters, SpotiPy was used to access audio features of the song entered by user. After that the cluster of the entered song can be figured using the saved clustering model.

4) **Putting everything together and wrapping into the Flask application**
  
## Results and Conclusions

The system is able to make basic song recommendations to the user according to the *dichotomous principle*: if a user inputs a popular song, he is recommended with a random popular song, and when the inputted song is not popular, than a random recommendation is made from the same audio-cluster of a song database.

At this point, the recommendations made by the app may not be really appreciated by the user, because there is still a lot of randomness involved in the process of choosing a recommended song. But still the project is a steady POC and a fun way to discover some interesting songs :)

## Presentation of a functionality

To present the work done, we were required to make a short 3 min with a business-oriented presentation of the product.

The link to the video presentation: 

https://youtu.be/OZpNraIWAl0