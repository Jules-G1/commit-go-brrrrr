import os
import sys
import datetime
import random
import subprocess
from pathlib import Path

# Dictionary of emoji patterns with intensity levels
# 0: No commits (white)
# 1: Light intensity (1-2 commits)
# 2: Medium intensity (3-5 commits)
# 3: High intensity (6-9 commits)
# 4: Maximum intensity (10+ commits)
EMOJI_PATTERNS = {
    "heart": [
        "0220220",
        "2343432",
        "2444442",
        "1344431",
        "0233320",
        "0022200",
        "0001000",
    ],
    "smile": [
        "0033300",
        "0244420",
        "3000043",
        "4000004",
        "3200023",
        "0244420",
        "0033300",
    ],
    "star": [
        "0004000",
        "0024200",
        "2344432",
        "3444443",
        "0233320",
        "0022200",
        "0001000",
    ],
    "thumbsup": [
        "0033300",
        "0044400",
        "0044400",
        "2044400",
        "3444400",
        "0442000",
        "0230000",
    ],
    "cat": [
        "3000003",
        "4200024",
        "4004004",
        "4000004",
        "3022203",
        "0244420",
        "0033300",
    ],
    "heart_3d": [
        "0110110",
        "1331331",
        "3443443",
        "3444443",
        "0344430",
        "0033300",
        "0001000",
    ],
    "fire": [
        "0001000",
        "0012100",
        "0123210",
        "1234321",
        "2344432",
        "3444443",
        "0333330",
    ],
    "rocket": [
        "0001000",
        "0012100",
        "0123210",
        "0004000",
        "0044400",
        "0344430",
        "3000003",
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
    for week_idx, week in enumerate(pattern):
        for day_idx, intensity in enumerate(week):
            if intensity != '0':
                commit_date = start_date + datetime.timedelta(weeks=week_idx, days=day_idx)
                commit_count = get_commits_for_intensity(int(intensity))
                if commit_count > 0:
                    commit_plan.append((commit_date, commit_count))
    
    return commit_plan

def create_pattern(pattern_name, start_date=None, intensity_multiplier=1):
    """Create commits for the specified pattern"""
    setup_repo()
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
    print("  Su Mo Tu We Th Fr Sa")
    for week_idx, week in enumerate(pattern):
        print(f"W{week_idx+1}", end=" ")
        for day_idx, intensity in enumerate(week):
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
        print()

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Create GitHub contribution patterns')
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
