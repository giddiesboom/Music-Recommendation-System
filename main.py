"""
Main Module
This module launches the Music Recommendation Engine application.
"""

import sys
import os
from load_dataset_module import DatasetLoader
from statistics_module import StatisticsCalculator
from similarity_module import SimilarityCalculator
from user_interface_module import RecommendationUI


def main():
    """
    Main function to initialize and run the recommendation engine
    """
    try:
        print("="*70)
        print("🎵 MUSIC RECOMMENDATION ENGINE 🎵".center(70))
        print("="*70)
        print("\n📦 Initializing application...\n")
        
        # Dataset path - UPDATE THIS to your local path
        dataset_path = "data.csv"  # For local: use "data.csv" in same folder
        
        # Check if file exists
        if not os.path.exists(dataset_path):
            print(f"❌ ERROR: Dataset file not found at: {dataset_path}")
            print("\n📋 Please ensure 'data.csv' is in the same folder as main.py")
            sys.exit(1)
        
        # Load dataset
        print(f"1️⃣  Loading dataset from: {dataset_path}")
        loader = DatasetLoader(dataset_path)
        artist_music = loader.load_data()
        print(f"   ✅ Successfully loaded {len(artist_music)} tracks")
        
        # Display dataset statistics
        num_artists = len(loader.get_all_artists())
        print(f"   📊 Found {num_artists} unique artists\n")
        
        # Initialize statistics calculator
        print("2️⃣  Initializing statistics calculator...")
        stats_calc = StatisticsCalculator()
        print("   ✅ Statistics calculator ready\n")
        
        # Initialize similarity calculator
        print("3️⃣  Initializing similarity calculator...")
        similarity_calc = SimilarityCalculator(artist_music)
        print("   ✅ Similarity calculator ready")
        print("   📐 Available metrics: Euclidean, Cosine, Pearson, Manhattan\n")
        
        # Launch GUI
        print("4️⃣  Launching user interface...")
        print("="*70)
        print("✨ APPLICATION READY ✨".center(70))
        print("="*70)
        print("\n📌 Use the GUI to:")
        print("   - Select comparison type (Track IDs, Artists, or Track Names)")
        print("   - Choose similarity metric")
        print("   - Enter two items to compare")
        print("   - View similarity scores and recommendations")
        print("\n" + "="*70 + "\n")
        
        ui = RecommendationUI(similarity_calc, loader)
        ui.run()
        
    except FileNotFoundError as e:
        print(f"\n❌ ERROR: {e}")
        print("\n📋 Solution:")
        print("   Ensure 'data.csv' is in the same folder as main.py")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
