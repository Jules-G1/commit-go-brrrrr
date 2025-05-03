import os
import sys
import datetime
import random
import subprocess
from pathlib import Path

# Dictionary of emoji patterns with intensity levels - ROTATED 90° CLOCKWISE
# Each pattern is now defined with days of week (Sun-Sat) as rows and weeks as columns
# 0: No commits (white)
# 1: Light intensity (1-2 commits)
# 2: Medium intensity (3-5 commits)
# 3: High intensity (6-9 commits)
# 4: Maximum intensity (10+ commits)
EMOJI_PATTERNS = {
    "diamond": [
        "0004000",
        "0044400",
        "0444440",
        "4444444",
        "0444440",
        "0044400",
        "0004000"
    ],
    "heart": [
        "0404040",
        "4444444",
        "4444444",
        "0444440",
        "0044400",
        "0004000",
        "0000000",
    ],
    "arrow_right": [
        "0001000",
        "0001100",
        "0001110",
        "1111111",
        "0001110",
        "0001100",
        "0001000",
    ],
    "smiley": [
        "0000000",
        "0040400",
        "0040400",
        "0000000",
        "4000004",
        "0400040",
        "0044400",
    ],
    "star": [
        "0004000",
        "0044400",
        "0444440",
        "4444444",
        "0044400",
        "0044400",
        "0044400",
    ],
    "letter_A": [
        "0004000",
        "0044400",
        "0440440",
        "4444444",
        "4400044",
        "4400044",
        "0000000",
    ],
    "wave": [
        "0000000",
        "0004400",
        "0444000",
        "4400000",
        "0044000",
        "0000440",
        "0000044",
    ],
    "x_shape": [
        "4000004",
        "0400040",
        "0040400",
        "0004000",
        "0040400",
        "0400040",
        "4000004",
    ],
    "checkmark": [
        "0000001",
        "0000011",
        "0000110",
        "0001100",
        "0110000",
        "1100000",
        "1000000",
    ],
    "box": [
        "4444444",
        "4000004",
        "4000004",
        "4000004",
        "4000004",
        "4000004",
        "4444444",
    ],
    "triangle_up": [
        "0004000",
        "0044400",
        "0444440",
        "4444444",
        "0000000",
        "0000000",
        "0000000",
    ],
    "triangle_down": [
        "0000000",
        "0000000",
        "0000000",
        "4444444",
        "0444440",
        "0044400",
        "0004000",
    ]
}

def create_commit(date):
    """Create a dummy commit on the specified date"""
    # Create or update a dummy file with a random change
    random_str = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8))
    with open('dummy.txt', 'a') as f:
        f.write(f'Dummy commit on {date.isoformat()} - {random_str}\n')
    
    # Commit with the specified date
    env = os.environ.copy()
    env['GIT_AUTHOR_DATE'] = date.isoformat()
    env['GIT_COMMITTER_DATE'] = date.isoformat()
    
    subprocess.run(['git', 'add', 'dummy.txt'], check=True)
    subprocess.run(['git', 'commit', '-m', f'Dummy commit for {date.isoformat()} - {random_str}'], env=env, check=True)

def get_commits_for_intensity(intensity):
    """Return number of commits for a given intensity level"""
    if intensity == 0:
        return 0
    elif intensity == 1:
        return random.randint(1, 2)
    elif intensity == 2:
        return random.randint(3, 5)
    elif intensity == 3:
        return random.randint(6, 9)
    elif intensity == 4:
        return random.randint(10, 15)
    else:
        return int(intensity)  # Support for custom intensity numbers

def calculate_dates(pattern_name, start_date=None):
    """Calculate dates and commit counts for the pattern"""
    if start_date is None:
        # Default to starting from the current date, aligned to Sunday
        start_date = datetime.datetime.now().date()
        # Align to previous Sunday
        start_date = start_date - datetime.timedelta(days=start_date.weekday() + 1)
    
    pattern = EMOJI_PATTERNS.get(pattern_name)
    if not pattern:
        print(f"Pattern '{pattern_name}' not found. Available patterns: {', '.join(EMOJI_PATTERNS.keys())}")
        sys.exit(1)
    
    commit_plan = []
    for day_idx, day_pattern in enumerate(pattern):
        for week_idx, intensity in enumerate(day_pattern):
            if intensity != '0':
                commit_date = start_date + datetime.timedelta(weeks=week_idx, days=day_idx)
                commit_count = get_commits_for_intensity(int(intensity))
                if commit_count > 0:
                    commit_plan.append((commit_date, commit_count))
    
    return commit_plan

def create_pattern(pattern_name, start_date=None, intensity_multiplier=1):
    """Create commits for the specified pattern"""
    commit_plan = calculate_dates(pattern_name, start_date)
    
    total_commits = 0
    for date, commit_count in commit_plan:
        # Apply intensity multiplier (can be used to increase overall intensity)
        adjusted_count = max(1, int(commit_count * intensity_multiplier))
        total_commits += adjusted_count
        
        print(f"Creating {adjusted_count} commits for {date}")
        for _ in range(adjusted_count):
            # Add some randomness to the time
            hour = random.randint(9, 17)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            commit_datetime = datetime.datetime.combine(
                date, 
                datetime.time(hour, minute, second)
            )
            create_commit(commit_datetime)
    
    print(f"Pattern '{pattern_name}' created successfully with {total_commits} commits!")

def preview_pattern(pattern_name):
    """Show a preview of the pattern in the console"""
    pattern = EMOJI_PATTERNS.get(pattern_name)
    if not pattern:
        print(f"Pattern '{pattern_name}' not found. Available patterns: {', '.join(EMOJI_PATTERNS.keys())}")
        sys.exit(1)
    
    print(f"Preview of '{pattern_name}':")
    
    max_weeks = max(len(day_pattern) for day_pattern in pattern)
    
    print("    ", end="")
    for week_idx in range(max_weeks):
        print(f"W{week_idx+1}", end=" ")
    print()
    
    # Print each row (day of week)
    days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    for day_idx, day_pattern in enumerate(pattern):
        if day_idx < len(days):  # Only print for valid days
            print(f"{days[day_idx]}: ", end="")
            
            # Print intensity for each week in this day
            for week_idx in range(max_weeks):
                if week_idx < len(day_pattern):
                    intensity = day_pattern[week_idx]
                    if intensity == '0':
                        print("⬜", end=" ")
                    elif intensity == '1':
                        print("🟩", end=" ")
                    elif intensity == '2':
                        print("🟨", end=" ")
                    elif intensity == '3':
                        print("🟧", end=" ")
                    elif intensity == '4':
                        print("🟥", end=" ")
                    else:
                        print("⬛", end=" ")
                else:
                    print("⬜", end=" ")  # Empty for missing data
            print()

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Create GitHub contribution patterns to make you look busy')
    parser.add_argument('pattern', choices=list(EMOJI_PATTERNS.keys()) + ['list', 'preview'], 
                        help='Pattern to create or "list" to show available patterns or "preview" to preview a pattern')
    parser.add_argument('--preview', help='Pattern to preview (with --pattern preview)')
    parser.add_argument('--start-date', help='Start date in YYYY-MM-DD format (defaults to aligned previous Sunday)')
    parser.add_argument('--intensity', type=float, default=1.0, help='Intensity multiplier (default: 1.0)')
    
    args = parser.parse_args()
    
    if args.pattern == 'list':
        print("Available patterns:")
        for pattern in EMOJI_PATTERNS.keys():
            print(f"- {pattern}")
        return
    
    if args.pattern == 'preview':
        if not args.preview:
            print("Please specify a pattern to preview with --preview")
            return
        preview_pattern(args.preview)
        return
    
    start_date = None
    if args.start_date:
        start_date = datetime.datetime.strptime(args.start_date, '%Y-%m-%d').date()
    
    create_pattern(args.pattern, start_date, args.intensity)

if __name__ == "__main__":
    main()