# 리뷰 인덱스 (movie_data_big.json)
mapping = {
    "movieId": {"type": "integer"},
    "title": {"type": "text"},
    "genres": {"type": "text"},
    "imdbId": {"type": "integer"},
    "tmdbId": {"type": "integer"},
    "userId": {"type": "integer"},
    "rating": {"type": "float"},
    "timestamp": {"type": "date"},
}

# 영화 줄거리 + 임베딩 인덱스 (movies_emb.json)
movie_mapping = {
    "movieId": {"type": "integer"},
    "title": {"type": "text", "analyzer": "english"},
    "genres": {"type": "text"},
    "overview": {"type": "text", "analyzer": "english"},
    "embedding": {
        "type": "dense_vector",
        "dims": 384,
        "index": True,
        "similarity": "cosine",
    },
}