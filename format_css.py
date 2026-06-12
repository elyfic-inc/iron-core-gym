import re

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# I will write a simple python script to extract specific blocks from the css
# and then combine them in the correct order.

def extract_block(css, start_marker, end_marker=None, include_end=False):
    start_idx = css.find(start_marker)
    if start_idx == -1: return ""
    
    if end_marker:
        end_idx = css.find(end_marker, start_idx + len(start_marker))
        if end_idx == -1: end_idx = len(css)
        if include_end: end_idx += len(end_marker)
    else:
        end_idx = len(css)
        
    return css[start_idx:end_idx].strip()

# We will split the file by the standard section comment:
pattern = r'/\* =========================================\n\s*.*?\n========================================= \*/'
sections_raw = re.split(pattern, css)
headers_raw = re.findall(pattern, css)

# Combine them
blocks = {}
for i in range(len(headers_raw)):
    header = headers_raw[i]
    content = sections_raw[i+1].strip()
    
    # Extract name from header
    match = re.search(r'/\* =========================================\n\s*(.*?)\n========================================= \*/', header)
    name = match.group(1).strip()
    
    blocks[name] = {
        'header': header,
        'content': content
    }

# Handle the messy 'Features' block which currently contains Marquee and Feature-card
features_content = blocks['Features (BEM Block: features & feature-card)']['content']

# Split features_content into: cases-slider/case-card, marquee, feature-card
idx_marquee = features_content.find('.marquee-container {')
idx_features = features_content.find('.features .section__inner {')
idx_feature_card = features_content.find('.feature-card {')

cases_content = features_content[:idx_marquee].strip()
marquee_content = features_content[idx_marquee:idx_features].strip()
# wait, .features .section__inner is before .feature-card
feature_card_content = features_content[idx_feature_card:].strip()
features_main_content = features_content[idx_features:idx_feature_card].strip()

# Now reassemble everything in the correct order:

ordered_names = [
    'Reset & Base Styles',
    'Typography & Utilities',
    'Buttons (BEM Block: btn)',
    'Hero (BEM Block: hero)',
    'Benefits Bar (BEM Block: benefits-bar)',
    'Troubles (BEM Block: troubles)',
    'Solutions (BEM Block: solutions & solution-card)'
]

new_css = []
# 1. Add everything up to Solutions
for name in ordered_names:
    new_css.append(blocks[name]['header'])
    new_css.append(blocks[name]['content'] + '\n')

# 2. Add feature-card to Solutions
new_css.append(feature_card_content + '\n')

# 3. Add Concept
new_css.append(blocks['Concept (BEM Block: concept)']['header'])
new_css.append(blocks['Concept (BEM Block: concept)']['content'] + '\n')

# 4. Add Locations
new_css.append(blocks['Locations (BEM Block: locations)']['header'])
new_css.append(blocks['Locations (BEM Block: locations)']['content'] + '\n')

# 5. Add Marquee
new_css.append("/* =========================================\n   Marquee (BEM Block: marquee)\n========================================= */")
new_css.append(marquee_content + '\n')

# 6. Add Features (cases-slider, case-card)
new_css.append("/* =========================================\n   Features / Cases (BEM Block: features & case-card)\n========================================= */")
new_css.append(features_main_content)
new_css.append(cases_content + '\n')

# 7. Add Banner CTA
new_css.append(blocks['Banner CTA (BEM Block: banner-cta)']['header'])
new_css.append(blocks['Banner CTA (BEM Block: banner-cta)']['content'] + '\n')

# 8. Add Pricing
new_css.append(blocks['Pricing (BEM Block: pricing & price-card)']['header'])
new_css.append(blocks['Pricing (BEM Block: pricing & price-card)']['content'] + '\n')

# 9. Add FAQ
new_css.append(blocks['FAQ (BEM Block: faq)']['header'])
new_css.append(blocks['FAQ (BEM Block: faq)']['content'] + '\n')

# 10. Add Sticky CTA
new_css.append(blocks['Sticky CTA (BEM Block: sticky-cta)']['header'])
new_css.append(blocks['Sticky CTA (BEM Block: sticky-cta)']['content'] + '\n')

# 11. Add Modal
new_css.append(blocks['ELYFiC Modal (BEM Block: elyfic-modal)']['header'])
new_css.append(blocks['ELYFiC Modal (BEM Block: elyfic-modal)']['content'] + '\n')

# 12. Add Animations
new_css.append(blocks['Animations']['header'])
new_css.append(blocks['Animations']['content'] + '\n')

with open('style.css', 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_css))

print("CSS Reordered Successfully")
