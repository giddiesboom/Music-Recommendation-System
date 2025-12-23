"""
User Interface Module
This module creates a GUI for the recommendation system using tkinter.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext


class RecommendationUI:
    """Class for creating and managing the user interface"""
    
    def __init__(self, similarity_calculator, dataset_loader):
        """
        Initialize the UI with required components
        
        Args:
            similarity_calculator: SimilarityCalculator instance
            dataset_loader: DatasetLoader instance
        """
        self.similarity_calc = similarity_calculator
        self.dataset_loader = dataset_loader
        self.root = tk.Tk()
        self.root.title("Music Recommendation Engine")
        self.root.geometry("900x750")
        
        # Similarity function mapping
        self.similarity_functions = {
            'Euclidean': self.similarity_calc.euclidean_similarity,
            'Cosine': self.similarity_calc.cosine_similarity,
            'Pearson': self.similarity_calc.pearson_similarity,
            'Manhattan': self.similarity_calc.manhattan_similarity
        }
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create all UI widgets"""
        
        # Title
        title_label = tk.Label(
            self.root, 
            text="🎵 Music Recommendation System 🎵", 
            font=("Arial", 18, "bold"),
            fg="#2E86AB",
            pady=10
        )
        title_label.pack()
        
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Comparison type selection
        type_frame = ttk.LabelFrame(main_frame, text="Select Comparison Type", padding="10")
        type_frame.pack(fill=tk.X, pady=5)
        
        self.comparison_type = tk.StringVar(value="track_id")
        ttk.Radiobutton(
            type_frame, 
            text="Compare Track IDs", 
            variable=self.comparison_type, 
            value="track_id"
        ).pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(
            type_frame, 
            text="Compare Artists", 
            variable=self.comparison_type, 
            value="artist"
        ).pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(
            type_frame, 
            text="Compare Track Names", 
            variable=self.comparison_type, 
            value="track_name"
        ).pack(anchor=tk.W, pady=2)
        
        # Similarity metric selection
        metric_frame = ttk.LabelFrame(main_frame, text="Select Similarity Metric", padding="10")
        metric_frame.pack(fill=tk.X, pady=5)
        
        self.similarity_metric = tk.StringVar(value="Euclidean")
        for metric in self.similarity_functions.keys():
            ttk.Radiobutton(
                metric_frame, 
                text=metric, 
                variable=self.similarity_metric, 
                value=metric
            ).pack(anchor=tk.W, pady=2)
        
        # Input frame
        input_frame = ttk.LabelFrame(main_frame, text="Enter Items to Compare", padding="10")
        input_frame.pack(fill=tk.X, pady=5)
        
        # Item 1
        ttk.Label(input_frame, text="First Item:", font=("Arial", 10)).grid(
            row=0, column=0, sticky=tk.W, pady=5, padx=5
        )
        self.item1_entry = ttk.Entry(input_frame, width=50, font=("Arial", 10))
        self.item1_entry.grid(row=0, column=1, pady=5, padx=5, sticky=tk.EW)
        
        # Item 2
        ttk.Label(input_frame, text="Second Item:", font=("Arial", 10)).grid(
            row=1, column=0, sticky=tk.W, pady=5, padx=5
        )
        self.item2_entry = ttk.Entry(input_frame, width=50, font=("Arial", 10))
        self.item2_entry.grid(row=1, column=1, pady=5, padx=5, sticky=tk.EW)
        
        input_frame.columnconfigure(1, weight=1)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        calculate_btn = ttk.Button(
            button_frame, 
            text="Calculate Similarity", 
            command=self.calculate_similarity,
            width=20
        )
        calculate_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = ttk.Button(
            button_frame, 
            text="Clear Results", 
            command=self.clear_results,
            width=20
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        quit_btn = ttk.Button(
            button_frame, 
            text="Quit", 
            command=self.quit_application,
            width=20
        )
        quit_btn.pack(side=tk.LEFT, padx=5)
        
        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Scrolled text for results
        self.results_text = scrolledtext.ScrolledText(
            results_frame, 
            wrap=tk.WORD, 
            width=80, 
            height=20,
            font=("Consolas", 9)
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for styling
        self.results_text.tag_configure("header", font=("Arial", 12, "bold"), foreground="#2E86AB")
        self.results_text.tag_configure("subheader", font=("Arial", 10, "bold"), foreground="#0066CC")
        self.results_text.tag_configure("error", foreground="red", font=("Arial", 10, "bold"))
        self.results_text.tag_configure("success", foreground="green")
    
    def calculate_similarity(self):
        """Calculate and display similarity results"""
        try:
            # Get inputs
            item1 = self.item1_entry.get().strip()
            item2 = self.item2_entry.get().strip()
            comp_type = self.comparison_type.get()
            metric = self.similarity_metric.get()
            
            # Validate inputs
            if not item1 or not item2:
                messagebox.showerror("Input Error", "Please enter both items to compare")
                return
            
            # Get similarity function
            similarity_func = self.similarity_functions[metric]
            
            # Clear previous results
            self.results_text.delete(1.0, tk.END)
            
            # Display header
            self.results_text.insert(tk.END, "="*80 + "\n")
            self.results_text.insert(tk.END, "SIMILARITY ANALYSIS RESULTS\n", "header")
            self.results_text.insert(tk.END, "="*80 + "\n\n")
            
            # Calculate similarity based on type
            if comp_type == "track_id":
                self._calculate_track_id_similarity(item1, item2, metric, similarity_func)
            elif comp_type == "artist":
                self._calculate_artist_similarity(item1, item2, metric, similarity_func)
            elif comp_type == "track_name":
                self._calculate_track_name_similarity(item1, item2, metric, similarity_func)
            
        except Exception as e:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"Error: {str(e)}\n", "error")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def _calculate_track_id_similarity(self, item1, item2, metric, similarity_func):
        """Calculate similarity for track IDs"""
        # Validate track IDs exist
        if item1 not in self.dataset_loader.artist_music:
            messagebox.showerror("Error", f"Track ID '{item1}' not found in dataset")
            return
        if item2 not in self.dataset_loader.artist_music:
            messagebox.showerror("Error", f"Track ID '{item2}' not found in dataset")
            return
        
        score = self.similarity_calc.track_similarity(item1, item2, similarity_func)
        
        track1_info = self.dataset_loader.artist_music[item1]
        track2_info = self.dataset_loader.artist_music[item2]
        
        # Display results
        self.results_text.insert(tk.END, f"Comparison Type: Track IDs\n")
        self.results_text.insert(tk.END, f"Similarity Metric: {metric}\n\n")
        self.results_text.insert(tk.END, f"Track 1: {track1_info['name']} by {track1_info['artists']}\n")
        self.results_text.insert(tk.END, f"Track 2: {track2_info['name']} by {track2_info['artists']}\n\n")
        self.results_text.insert(tk.END, f"Similarity Score: {score:.4f}\n\n", "success")
        
        # Get top 5 similar tracks for each
        self.results_text.insert(tk.END, "-"*80 + "\n")
        self.results_text.insert(tk.END, f"Top 5 Similar Tracks for '{track1_info['name']}':\n", "subheader")
        self.results_text.insert(tk.END, "-"*80 + "\n")
        similar1 = self.similarity_calc.get_top_similar(item1, similarity_func, 5, 'track')
        for i, (track, sim_score) in enumerate(similar1, 1):
            self.results_text.insert(tk.END, f"{i}. {track} (Score: {sim_score:.4f})\n")
        
        self.results_text.insert(tk.END, "\n" + "-"*80 + "\n")
        self.results_text.insert(tk.END, f"Top 5 Similar Tracks for '{track2_info['name']}':\n", "subheader")
        self.results_text.insert(tk.END, "-"*80 + "\n")
        similar2 = self.similarity_calc.get_top_similar(item2, similarity_func, 5, 'track')
        for i, (track, sim_score) in enumerate(similar2, 1):
            self.results_text.insert(tk.END, f"{i}. {track} (Score: {sim_score:.4f})\n")
    
    def _calculate_artist_similarity(self, item1, item2, metric, similarity_func):
        """Calculate similarity for artists"""
        score = self.similarity_calc.artist_similarity(item1, item2, similarity_func)
        
        self.results_text.insert(tk.END, f"Comparison Type: Artists\n")
        self.results_text.insert(tk.END, f"Similarity Metric: {metric}\n\n")
        self.results_text.insert(tk.END, f"Artist 1: {item1}\n")
        self.results_text.insert(tk.END, f"Artist 2: {item2}\n\n")
        self.results_text.insert(tk.END, f"Similarity Score: {score:.4f}\n\n", "success")
        
        # Get top 5 similar artists for each
        self.results_text.insert(tk.END, "-"*80 + "\n")
        self.results_text.insert(tk.END, f"Top 5 Similar Artists to '{item1}':\n", "subheader")
        self.results_text.insert(tk.END, "-"*80 + "\n")
        similar1 = self.similarity_calc.get_top_similar(item1, similarity_func, 5, 'artist')
        for i, (artist, sim_score) in enumerate(similar1, 1):
            self.results_text.insert(tk.END, f"{i}. {artist} (Score: {sim_score:.4f})\n")
        
        self.results_text.insert(tk.END, "\n" + "-"*80 + "\n")
        self.results_text.insert(tk.END, f"Top 5 Similar Artists to '{item2}':\n", "subheader")
        self.results_text.insert(tk.END, "-"*80 + "\n")
        similar2 = self.similarity_calc.get_top_similar(item2, similarity_func, 5, 'artist')
        for i, (artist, sim_score) in enumerate(similar2, 1):
            self.results_text.insert(tk.END, f"{i}. {artist} (Score: {sim_score:.4f})\n")
    
    def _calculate_track_name_similarity(self, item1, item2, metric, similarity_func):
        """Calculate similarity for track names"""
        # Find tracks by name
        tracks1 = self.dataset_loader.get_track_by_name(item1)
        tracks2 = self.dataset_loader.get_track_by_name(item2)
        
        if not tracks1:
            messagebox.showerror("Error", f"Track name '{item1}' not found")
            return
        if not tracks2:
            messagebox.showerror("Error", f"Track name '{item2}' not found")
            return
        
        # Use first matching track
        track1_id = list(tracks1.keys())[0]
        track2_id = list(tracks2.keys())[0]
        
        score = self.similarity_calc.track_similarity(track1_id, track2_id, similarity_func)
        
        track1_info = self.dataset_loader.artist_music[track1_id]
        track2_info = self.dataset_loader.artist_music[track2_id]
        
        self.results_text.insert(tk.END, f"Comparison Type: Track Names\n")
        self.results_text.insert(tk.END, f"Similarity Metric: {metric}\n\n")
        self.results_text.insert(tk.END, f"Track 1: {track1_info['name']} by {track1_info['artists']}\n")
        self.results_text.insert(tk.END, f"Track 2: {track2_info['name']} by {track2_info['artists']}\n\n")
        self.results_text.insert(tk.END, f"Similarity Score: {score:.4f}\n\n", "success")
        
        # Get top 5 similar tracks for each
        self.results_text.insert(tk.END, "-"*80 + "\n")
        self.results_text.insert(tk.END, f"Top 5 Similar Tracks for '{track1_info['name']}':\n", "subheader")
        self.results_text.insert(tk.END, "-"*80 + "\n")
        similar1 = self.similarity_calc.get_top_similar(track1_id, similarity_func, 5, 'track')
        for i, (track, sim_score) in enumerate(similar1, 1):
            self.results_text.insert(tk.END, f"{i}. {track} (Score: {sim_score:.4f})\n")
        
        self.results_text.insert(tk.END, "\n" + "-"*80 + "\n")
        self.results_text.insert(tk.END, f"Top 5 Similar Tracks for '{track2_info['name']}':\n", "subheader")
        self.results_text.insert(tk.END, "-"*80 + "\n")
        similar2 = self.similarity_calc.get_top_similar(track2_id, similarity_func, 5, 'track')
        for i, (track, sim_score) in enumerate(similar2, 1):
            self.results_text.insert(tk.END, f"{i}. {track} (Score: {sim_score:.4f})\n")
    
    def clear_results(self):
        """Clear all input fields and results"""
        self.item1_entry.delete(0, tk.END)
        self.item2_entry.delete(0, tk.END)
        self.results_text.delete(1.0, tk.END)
    
    def quit_application(self):
        """Quit the application"""
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            self.root.quit()
            self.root.destroy()
    
    def run(self):
        """Start the GUI main loop"""
        self.root.mainloop()
