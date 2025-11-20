from typing import List
from models.topic import Topic


# Simple topic classifier
class SimpleTopicClassifier:
    def __init__(self):
        self.topic_keywords = {
            "technology": [
                "computer",
                "software",
                "internet",
                "tech",
                "digital",
                "AI",
                "machine learning",
            ],
            "sports": ["sports", "game", "player", "team", "score", "win", "league"],
            "health": [
                "health",
                "medical",
                "disease",
                "doctor",
                "hospital",
                "medicine",
            ],
            "business": [
                "business",
                "company",
                "market",
                "finance",
                "investment",
                "economy",
            ],
            "entertainment": [
                "movie",
                "music",
                "celebrity",
                "film",
                "tv",
                "entertainment",
            ],
            "science": [
                "science",
                "research",
                "scientist",
                "study",
                "physics",
                "chemistry",
            ],
            "education": [
                "education",
                "school",
                "student",
                "teacher",
                "learn",
                "university",
            ],
            "politics": [
                "politics",
                "government",
                "election",
                "law",
                "policy",
                "political",
            ],
        }

    def classify(self, text: str) -> List[Topic]:
        text_lower = text.lower()
        scores = {}
        for topic, keywords in self.topic_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                scores[topic] = score

        total = sum(scores.values())
        if total == 0:
            return []

        # Normalize and return top topics
        topics = [
            Topic(name=topic, confidence=score / total)
            for topic, score in scores.items()
        ]
        topics.sort(key=lambda x: x.confidence, reverse=True)
        return topics[:3]  # Return top 3


classifier = SimpleTopicClassifier()
