import json
import os
from datetime import datetime


class LeaderboardManager:
    def __init__(self):
        """Initialize leaderboard manager"""
        # Get path relative to this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        self.leaderboard_file = os.path.join(project_root, "leaderboard.json")
        
        # Load existing leaderboard or create new
        self.leaderboard = self.load_leaderboard()
    
    def load_leaderboard(self):
        """Load leaderboard from file"""
        if os.path.exists(self.leaderboard_file):
            try:
                with open(self.leaderboard_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self.create_default_leaderboard()
        else:
            return self.create_default_leaderboard()
    
    def create_default_leaderboard(self):
        """Create default leaderboard structure"""
        return {
            "easy": [],
            "medium": [],
            "hard": []
        }
    
    def save_leaderboard(self):
        """Save leaderboard to file"""
        try:
            with open(self.leaderboard_file, 'w', encoding='utf-8') as f:
                json.dump(self.leaderboard, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving leaderboard: {e}")
    
    def add_score(self, difficulty, score, player_name="Player"):
        """Add a new score to leaderboard"""
        entry = {
            "name": player_name,
            "score": score,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        # Add to appropriate difficulty list
        self.leaderboard[difficulty].append(entry)
        
        # Sort by score (descending)
        self.leaderboard[difficulty].sort(key=lambda x: x["score"], reverse=True)
        
        # Keep only top 10
        self.leaderboard[difficulty] = self.leaderboard[difficulty][:10]
        
        # Save to file
        self.save_leaderboard()
        
        # Return rank (1-based)
        rank = next((i + 1 for i, e in enumerate(self.leaderboard[difficulty]) 
                    if e["score"] == score and e["name"] == player_name), None)
        return rank
    
    def get_top_scores(self, difficulty, limit=10):
        """Get top scores for a difficulty"""
        return self.leaderboard.get(difficulty, [])[:limit]
    
    def is_high_score(self, difficulty, score):
        """Check if score qualifies for leaderboard"""
        scores = self.leaderboard.get(difficulty, [])
        if len(scores) < 10:
            return True
        return score > scores[-1]["score"]
