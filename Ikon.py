import spacy

# Load the spaCy language model
nlp = spacy.load("en_core_web_md")

def brand_score(brand_name: str, tags: list[str], ease_of_saying: float, is_luxury: bool) -> float:
    """
    Calculate a score for a brand based on its name, associated tags, ease of saying, and luxury status.

    Args:
        brand_name (str): The name of the brand.
        tags (list[str]): A list of tags associated with the brand.
        ease_of_saying (float): A score between 0 and 1 indicating how easy the name is to say.
        is_luxury (bool): Whether the product is a luxury product.

    Returns:
        float: A score calculated based on the semantic similarity, ease of saying, and luxury status.
    """
    brand_doc = nlp(brand_name.lower())
    
    score = 0.0
    
    for tag in tags:
        tag_doc = nlp(tag.lower())
        similarity = brand_doc.similarity(tag_doc)
        score += similarity  # Add the similarity score to the total score
    
    if tags:
        score /= len(tags)
    
    score *= 100
    
    score += ease_of_saying * 20
    
    if is_luxury:
        score += 15
    
    return round(score, 2)