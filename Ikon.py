import spacy
import pronouncing
import re
import random

nlp = spacy.load("en_core_web_md")

STOP_WORDS = {"the", "a", "an", "and", "of", "in", "on", "at", "for", "with"}

def brand_score(brand_name: str, tags: list[str], ease_of_saying: float, is_luxury: bool) -> float:
    if not brand_name or not isinstance(brand_name, str):
        return 0.0
    
    brand_doc = nlp(brand_name.lower())
    
    score = 0.0
    
    for tag in tags:
        try:
            tag_doc = nlp(tag.lower())
            similarity = brand_doc.similarity(tag_doc)
            score += similarity
        except Exception as e:
            score += 0.1
    if tags:
        score /= len(tags)
    score *= 100
    
    # Alliteration check
    words = [word for word in brand_name.split() if word.lower() not in STOP_WORDS]
    if len(words) > 1 and all(word[0].lower() == words[0][0].lower() for word in words):
        score += 10
    
    # Non-luxury penalty for hard-to-say names
    if not is_luxury and ease_of_saying < 0.5:
        score -= 15
    
    try:
        phones = pronouncing.phones_for_word(brand_name.lower())
        if phones:
            syllables = pronouncing.syllable_count(phones[0])
            if 2 <= syllables <= 3:
                score += 5
    except:
        pass

    # skip length check if the brand name is a luxury brand
    if not is_luxury:
        if 5 <= len(brand_name) <= 10:
            score += 8
        elif len(brand_name) < 5:
            score += 3
        else:
            score -= min(10, (len(brand_name) - 10) * 0.5)
    if not is_luxury:
        score += ease_of_saying * 20
    else:
        score = score + 20 * (1 - ease_of_saying)

    
    vowel_patterns = re.findall(r'[aeiou]{2,}', brand_name.lower())
    if vowel_patterns:
        score += 3
    
    name_lower = brand_name.lower()
    if any(pattern in name_lower and name_lower.count(pattern) > 1 
           for pattern in ["ca", "co", "ma", "mi", "pa", "po"]):
        score += 5
    
    problematic_combos = ["th", "sch", "zh", "rr", "tl", "xh"]
    if any(combo in brand_name.lower() for combo in problematic_combos):
        score -= 5
    
    # Make sure score is non-negative before applying the power operations

    
    if not is_luxury and ease_of_saying < 0.5:
        score -= 15

    if score < 0:
        return 0
    
    score = (score ** 0.5) * 10
    score = (score ** 0.5) * 10


    return round(score, 2)

import random

def generate_brand_names(industry, descriptors):
    """
    Generate a list of potential brand names based on the industry and descriptors.

    Args:
        industry (str): The industry for which the brand name is being generated.
        descriptors (list of str): Words describing the brand.

    Returns:
        list of str: A list of generated brand names.
    """
    brand_names = []

    for descriptor in descriptors:
        # Create meaningful combinations that reflect the descriptor's essence
        if "luxury" in descriptor.lower():
            brand_names.append(f"{descriptor.capitalize()} {industry.capitalize()}")
        elif "tech" in descriptor.lower():
            brand_names.append(f"{industry.capitalize()} {descriptor.capitalize()}")
        elif "eco" in descriptor.lower() or "green" in descriptor.lower():
            brand_names.append(f"Eco{industry.capitalize()}")
        else:
            brand_names.append(f"{descriptor.capitalize()} {industry.capitalize()}")

    # Add some creative combinations
    for _ in range(5):
        random_descriptor = random.choice(descriptors).capitalize()
        brand_names.append(f"{random_descriptor}{industry.capitalize()}")

    return list(set(brand_names))  # Remove duplicates