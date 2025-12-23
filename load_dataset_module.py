"""
Load Dataset Module
This module handles loading and parsing of the music dataset.
"""

import csv


class DatasetLoader:
    """Class for loading and managing music dataset"""
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.artist_music = {}
    
    def load_data(self):
        """Load data from CSV file and return structured dictionary"""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                required_features = [
                    'acousticness', 'artists', 'danceability', 'energy',
                    'id', 'liveness', 'loudness', 'name', 'popularity',
                    'speechiness', 'tempo', 'valence'
                ]
                
                for row in reader:
                    try:
                        track_id = row.get('id', '').strip()
                        if not track_id:
                            continue
                        
                        artists = row.get('artists', '').strip()
                        if not artists:
                            continue
                        
                        track_name = row.get('name', '').strip()
                        
                        features = {}
                        for feature in required_features:
                            if feature not in ['id', 'artists', 'name']:
                                try:
                                    value = row.get(feature, '0')
                                    features[feature] = float(value) if value else 0.0
                                except (ValueError, TypeError):
                                    features[feature] = 0.0
                        
                        self.artist_music[track_id] = {
                            'artists': artists,
                            'name': track_name,
                            'features': features
                        }
                        
                    except Exception:
                        continue
                
                if not self.artist_music:
                    raise ValueError("No valid data loaded from dataset")
                
                return self.artist_music
                
        except FileNotFoundError:
            raise FileNotFoundError(f"Dataset file not found: {self.filepath}")
        except Exception as e:
            raise Exception(f"Error loading dataset: {str(e)}")
    
    def get_track_by_id(self, track_id):
        return self.artist_music.get(track_id)
    
    def get_tracks_by_artist(self, artist_name):
        tracks = {}
        artist_lower = artist_name.lower()
        for track_id, data in self.artist_music.items():
            if artist_lower in data['artists'].lower():
                tracks[track_id] = data
        return tracks
    
    def get_track_by_name(self, track_name):
        tracks = {}
        name_lower = track_name.lower()
        for track_id, data in self.artist_music.items():
            if name_lower in data['name'].lower():
                tracks[track_id] = data
        return tracks
    
    def get_all_artists(self):
        artists_set = set()
        for data in self.artist_music.values():
            artist_list = data['artists'].replace(';', ',').split(',')
            for artist in artist_list:
                artist = artist.strip()
                if artist:
                    artists_set.add(artist)
        return sorted(list(artists_set))
    
    def get_all_track_names(self):
        return [data['name'] for data in self.artist_music.values()]
    
    def get_all_track_ids(self):
        return list(self.artist_music.keys())
