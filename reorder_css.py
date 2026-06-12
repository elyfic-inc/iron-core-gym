import re

with open('style.css', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the blocks manually based on the current style.css lines
# (Since the line numbers are known, it's safer to extract by string index or split)

# 1. Reset - Hero
# 2. Benefits
# 3. Troubles
# 4. Solutions
# 5. Concept
# 6. Locations
# 7. Features (cases-slider, case-card)
# 8. Marquee
# 9. feature-card
# 10. Banner CTA
# 11. Pricing - end

# Let's write a python script to extract sections using regex on the header comments

pattern = r'(/\* =========================================\n\s*(.*?)\n========================================= \*/)'
matches = list(re.finditer(pattern, content))

sections = []
for i in range(len(matches)):
    start = matches[i].start()
    end = matches[i+1].start() if i + 1 < len(matches) else len(content)
    
    header = matches[i].group(1)
    name = matches[i].group(2).strip()
    body = content[start+len(header):end].strip()
    
    sections.append({
        'name': name,
        'header': header,
        'body': body
    })

# Special handling: The Features section currently contains:
# - .features
# - .cases-slider
# - .case-card
# - .marquee-container (no header)
# - .feature-card (belongs to Solutions)
# Let's just fix it by string manipulation since we know the exact text.

# 1. Extract feature-card block
feature_card_match = re.search(r'(\.feature-card \{.*?\n\n)', content, re.DOTALL)
feature_card_full = re.search(r'(\.feature-card \{.*?\n\n.*?\.feature-card__text \{.*?\}\n)', content, re.DOTALL)

# Easier approach: rewrite the file sequentially by matching known classes

