#!/usr/bin/env python3
"""
Codeforces API Integration Script
Fetches user statistics and analyzes problem-solving patterns
"""

import json
import sys
import time
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from collections import Counter

class CodeforcesAPI:
    BASE_URL = "https://codeforces.com/api"
    RATE_LIMIT_DELAY = 2  # seconds between requests

    def __init__(self):
        self.last_request_time = 0

    def _rate_limit(self):
        """Ensure we don't exceed rate limits (1 request per 2 seconds)"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.RATE_LIMIT_DELAY:
            time.sleep(self.RATE_LIMIT_DELAY - time_since_last)
        self.last_request_time = time.time()

    def _make_request(self, endpoint, params=None):
        """Make a request to Codeforces API with rate limiting"""
        self._rate_limit()

        url = f"{self.BASE_URL}/{endpoint}"
        if params:
            param_str = "&".join([f"{k}={v}" for k, v in params.items()])
            url = f"{url}?{param_str}"

        try:
            with urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode())
                if data.get("status") == "OK":
                    return data.get("result")
                else:
                    raise Exception(f"API error: {data.get('comment', 'Unknown error')}")
        except (URLError, HTTPError) as e:
            raise Exception(f"Network error: {str(e)}")

    def get_user_info(self, handle):
        """Get basic user information including rating"""
        result = self._make_request("user.info", {"handles": handle})
        if result and len(result) > 0:
            user = result[0]
            return {
                "handle": user.get("handle"),
                "rating": user.get("rating", 0),
                "maxRating": user.get("maxRating", 0),
                "rank": user.get("rank", "unrated")
            }
        return None

    def get_solved_problems(self, handle):
        """Get list of problems solved by user"""
        submissions = self._make_request("user.status", {"handle": handle})

        # Filter only accepted submissions
        solved_problems = set()
        for sub in submissions:
            if sub.get("verdict") == "OK":
                problem = sub.get("problem", {})
                contest_id = problem.get("contestId")
                index = problem.get("index")
                if contest_id and index:
                    solved_problems.add(f"{contest_id}{index}")

        return list(solved_problems)

    def analyze_user_stats(self, handle):
        """Comprehensive analysis of user's problem-solving patterns"""
        # Get user info
        user_info = self.get_user_info(handle)
        if not user_info:
            raise Exception(f"User '{handle}' not found")

        # Get submissions
        submissions = self._make_request("user.status", {"handle": handle})

        # Analyze solved problems
        solved_problems = {}
        tags_counter = Counter()
        rating_distribution = Counter()

        for sub in submissions:
            if sub.get("verdict") == "OK":
                problem = sub.get("problem", {})
                contest_id = problem.get("contestId")
                index = problem.get("index")

                if contest_id and index:
                    problem_id = f"{contest_id}{index}"

                    # Store unique problems only
                    if problem_id not in solved_problems:
                        solved_problems[problem_id] = problem

                        # Count tags
                        for tag in problem.get("tags", []):
                            tags_counter[tag] += 1

                        # Count rating distribution
                        problem_rating = problem.get("rating", 0)
                        if problem_rating > 0:
                            rating_bucket = (problem_rating // 100) * 100
                            rating_distribution[rating_bucket] += 1

        # Sort tags by frequency
        sorted_tags = sorted(tags_counter.items(), key=lambda x: x[1], reverse=True)

        return {
            "user_info": user_info,
            "solved_count": len(solved_problems),
            "tags_distribution": dict(tags_counter),
            "frequent_tags": [tag for tag, count in sorted_tags[:10]],
            "rare_tags": [tag for tag, count in sorted_tags[-10:] if count < 5],
            "rating_distribution": dict(rating_distribution),
            "analysis_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage: python codeforces_api.py <codeforces_handle>"
        }))
        sys.exit(1)

    handle = sys.argv[1]
    api = CodeforcesAPI()

    try:
        stats = api.analyze_user_stats(handle)
        print(json.dumps(stats, indent=2))
    except Exception as e:
        print(json.dumps({
            "error": str(e)
        }))
        sys.exit(1)

if __name__ == "__main__":
    main()
