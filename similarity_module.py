"""
Similarity Module
This module implements various similarity metrics and recommendation functions.
"""

import math


class SimilarityCalculator:
    """Class for calculating similarity between items"""
    
    def __init__(self, artist_music_dict):
        """
        Initialize SimilarityCalculator with dataset
        
        Args:
            artist_music_dict (dict): Dictionary containing music data
        """
        self.artist_music = artist_music_dict
        # Pre-compute artist features for faster comparison
        self._artist_features_cache = {}
    
    def euclidean_similarity(self, artist_music, item1, item2):
        """Calculate Euclidean distance similarity between two items"""
        try:
            features1 = self._get_features_for_item(artist_music, item1)
            features2 = self._get_features_for_item(artist_music, item2)
            
            if not features1 or not features2:
                return 0.0
            
            squared_diffs = sum((features1[key] - features2[key]) ** 2 
                              for key in features1.keys() if key in features2)
            distance = math.sqrt(squared_diffs)
            return 1 / (1 + distance)
        except Exception:
            return 0.0
    
    def cosine_similarity(self, artist_music, item1, item2):
        """Calculate Cosine similarity between two items"""
        try:
            features1 = self._get_features_for_item(artist_music, item1)
            features2 = self._get_features_for_item(artist_music, item2)
            
            if not features1 or not features2:
                return 0.0
            
            dot_product = sum(features1[key] * features2[key] 
                            for key in features1.keys() if key in features2)
            magnitude1 = math.sqrt(sum(features1[key] ** 2 for key in features1.keys()))
            magnitude2 = math.sqrt(sum(features2[key] ** 2 for key in features2.keys()))
            
            if magnitude1 == 0 or magnitude2 == 0:
                return 0.0
            
            similarity = dot_product / (magnitude1 * magnitude2)
            return (similarity + 1) / 2
        except Exception:
            return 0.0
    
    def pearson_similarity(self, artist_music, item1, item2):
        """Calculate Pearson correlation coefficient between two items"""
        try:
            features1 = self._get_features_for_item(artist_music, item1)
            features2 = self._get_features_for_item(artist_music, item2)
            
            if not features1 or not features2:
                return 0.0
            
            common_keys = [k for k in features1.keys() if k in features2]
            n = len(common_keys)
            
            if n == 0:
                return 0.0
            
            mean1 = sum(features1[k] for k in common_keys) / n
            mean2 = sum(features2[k] for k in common_keys) / n
            
            numerator = sum((features1[k] - mean1) * (features2[k] - mean2) for k in common_keys)
            sum_sq1 = sum((features1[k] - mean1) ** 2 for k in common_keys)
            sum_sq2 = sum((features2[k] - mean2) ** 2 for k in common_keys)
            denominator = math.sqrt(sum_sq1 * sum_sq2)
            
            if denominator == 0:
                return 0.0
            
            correlation = numerator / denominator
            return (correlation + 1) / 2
        except Exception:
            return 0.0
    
    def manhattan_similarity(self, artist_music, item1, item2):
        """Calculate Manhattan distance similarity between two items"""
        try:
            features1 = self._get_features_for_item(artist_music, item1)
            features2 = self._get_features_for_item(artist_music, item2)
            
            if not features1 or not features2:
                return 0.0
            
            distance = sum(abs(features1[key] - features2[key]) 
                         for key in features1.keys() if key in features2)
            return 1 / (1 + distance)
        except Exception:
            return 0.0
    
    def _get_features_for_item(self, artist_music, item_identifier):
        """Get feature vector for an item (track ID, artist, or track name)"""
        # Check if it's a track ID
        if item_identifier in artist_music:
            return artist_music[item_identifier]['features']
        
        # Check cache for artist features
        if item_identifier in self._artist_features_cache:
            return self._artist_features_cache[item_identifier]
        
        # Check if it's an artist name - get average features
        artist_tracks = [data['features'] for track_id, data in artist_music.items() 
                        if item_identifier.lower() in data['artists'].lower()]
        
        if artist_tracks:
            avg_features = {}
            for key in artist_tracks[0].keys():
                avg_features[key] = sum(track[key] for track in artist_tracks) / len(artist_tracks)
            # Cache the result
            self._artist_features_cache[item_identifier] = avg_features
            return avg_features
        
        # Check if it's a track name
        for track_id, data in artist_music.items():
            if item_identifier.lower() in data['name'].lower():
                return data['features']
        
        return None
    
    def track_similarity(self, track1_id, track2_id, similarity_function):
        """Calculate similarity between two tracks"""
        try:
            return similarity_function(self.artist_music, track1_id, track2_id)
        except Exception as e:
            raise ValueError(f"Error: {str(e)}")
    
    def artist_similarity(self, artist1_name, artist2_name, similarity_function):
        """Calculate similarity between two artists"""
        try:
            return similarity_function(self.artist_music, artist1_name, artist2_name)
        except Exception as e:
            raise ValueError(f"Error: {str(e)}")
    
    def get_top_similar(self, item_identifier, similarity_function, n=5, item_type='track'):
        """Get top N similar items (optimized for large datasets)"""
        try:
            similarities = []
            
            if item_type == 'artist':
                # OPTIMIZATION: Only compare against popular artists (those with 3+ tracks)
                # This reduces computation from 112k artists to ~20k artists
                artist_track_counts = {}
                for data in self.artist_music.values():
                    for artist in data['artists'].replace(';', ',').split(','):
                        artist = artist.strip()
                        if artist:
                            artist_track_counts[artist] = artist_track_counts.get(artist, 0) + 1
                
                # Filter to artists with at least 3 tracks (reduces noise and computation)
                significant_artists = {artist for artist, count in artist_track_counts.items() 
                                     if count >= 3 and artist.lower() != item_identifier.lower()}
                
                # Limit to top 500 most prolific artists for faster computation
                if len(significant_artists) > 500:
                    sorted_artists = sorted(significant_artists, 
                                          key=lambda x: artist_track_counts[x], 
                                          reverse=True)
                    significant_artists = set(sorted_artists[:500])
                
                # Calculate similarities
                for artist in significant_artists:
                    try:
                        score = similarity_function(self.artist_music, item_identifier, artist)
                        similarities.append((artist, score))
                    except:
                        continue
            
            else:  # track
                # For tracks, limit to 1000 random tracks for speed
                track_ids = list(self.artist_music.keys())
                
                # If dataset is large, sample for performance
                if len(track_ids) > 1000:
                    import random
                    sample_size = min(1000, len(track_ids))
                    track_ids = random.sample(track_ids, sample_size)
                
                for track_id in track_ids:
                    data = self.artist_music[track_id]
                    # Skip the same track
                    if track_id == item_identifier or data['name'].lower() == item_identifier.lower():
                        continue
                    
                    try:
                        score = similarity_function(self.artist_music, item_identifier, track_id)
                        similarities.append((f"{data['name']} by {data['artists']}", score))
                    except:
                        continue
            
            # Sort by similarity score (descending) and return top N
            similarities.sort(key=lambda x: x[1], reverse=True)
            return similarities[:n]
        except Exception as e:
            raise ValueError(f"Error: {str(e)}")
    
    def get_recommendations(self, item_identifier, similarity_function, n=5, item_type='track'):
        """Generate recommendations based on similarity"""
        try:
            return self.get_top_similar(item_identifier, similarity_function, n, item_type)
        except Exception as e:
            raise ValueError(f"Error: {str(e)}")
