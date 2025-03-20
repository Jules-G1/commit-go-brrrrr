# commit go brrrrr 🔫

Create beautiful emoji patterns with depth and nuance in your GitHub contribution graph using dummy commits!

## Features

- 🎨 Multiple emoji patterns with varying intensities
- 🌈 Support for multiple shades (different numbers of commits per day)
- 🤖 Fully automated with GitHub Actions
- 🔍 Preview patterns before creating them
- ⏰ Customizable start date and intensity
- 🆓 Completely free to use

## 🚀 Setup Instructions

1. **Fork this repository** to your GitHub account

2. **Enable GitHub Actions** in your forked repository if not already enabled:
   - Go to the "Actions" tab in your repository
   - Click "I understand my workflows, go ahead and enable them"

3. **Run the workflow**:
   - Go to the "Actions" tab
   - Select "GitHub Emoji Contributions" workflow
   - Click "Run workflow"
   - Choose your desired emoji pattern and settings
   - Click "Run workflow" button

4. **Check your GitHub profile** after the workflow completes to see your new contribution pattern!

## 📝 Manual Usage

You can also run the script locally:

```bash
# Clone your forked repository
git clone https://github.com/YOUR_USERNAME/commit-go-brrrrr.git
cd commit-go-brrrrr

# List available patterns
python main.py list

# Preview a pattern
python main.py preview --preview heart_3d

# Create a pattern
python main.py heart_3d --intensity 1.5
```

## 🎭 Available Patterns

- `heart` - A heart shape with shading
- `heart_3d` - A 3D heart with depth
- `smile` - A smiley face
- `star` - A star shape
- `thumbsup` - A thumbs up
- `cat` - A cat face
- `fire` - A flame
- `rocket` - A rocket ship

## 🌈 Intensity Levels

The patterns use 5 different intensity levels:

- Level 0: No commits (white squares)
- Level 1: Light intensity (1-2 commits, light green)
- Level 2: Medium intensity (3-5 commits, medium green)
- Level 3: High intensity (6-9 commits, dark green)
- Level 4: Maximum intensity (10+ commits, very dark green)

## ⚙️ Customization

- **Pattern**: Choose from a variety of pre-defined patterns
- **Start Date**: Specify a custom start date in YYYY-MM-DD format
- **Intensity Multiplier**: Adjust the overall intensity of the pattern
  - Use values < 1.0 for lighter patterns
  - Use values > 1.0 for more intense patterns

## 🖼️ Preview Mode

Before creating a pattern, you can preview it in the console:

```bash
python emoji_contributions.py preview --preview heart_3d
```

This will show you a text-based representation of how the pattern will look in your contribution graph.

## 📝 Important Notes

- This repository creates dummy commits which are only meant for fun and visual purposes.
- Keep in mind that creating large numbers of dummy commits might be against GitHub's terms of service if abused.
- Use responsibly and in moderation.

## 🤔 How It Works

The script creates a pattern of commits based on the emoji design you choose. Each "pixel" in the pattern corresponds to a day on your GitHub contribution graph. The intensity of each pixel determines how many commits will be made on that day, resulting in different shades of green in your contribution graph.

## 📋 License

This project is licensed under the MIT License - see the LICENSE file for details.
