import json
from llm_helper import llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException


def clean_text(text):
    return text.encode('utf-8', 'replace').decode('utf-8', 'replace')


def process_posts(raw_file_path, processed_file_path=None):
    with open(raw_file_path, encoding='utf-8') as file:
        posts = json.load(file)
        enriched_posts = []

        for post in posts:
            cleaned_text = clean_text(post['text'])
            metadata = extract_metadata(cleaned_text)

            post_with_metadata = post | metadata

            # Clean all string fields in post_with_metadata
            safe_post = {
                k: clean_text(str(v)) if isinstance(v, str) else v
                for k, v in post_with_metadata.items()
            }

            enriched_posts.append(safe_post)

    unified_tags = get_unified_tags(enriched_posts)

    for post in enriched_posts:
        current_tags = post['tags']
        new_tags = {unified_tags.get(tag, tag) for tag in current_tags}
        post['tags'] = list(new_tags)

    # Final sanitization before writing
    safe_posts = json.loads(clean_text(json.dumps(enriched_posts)))

    with open(processed_file_path, encoding='utf-8', mode="w") as outfile:
        json.dump(safe_posts, outfile, indent=4, ensure_ascii=False)



def get_unified_tags(posts_with_metadata):
    unique_tags = set()
    for post in posts_with_metadata:
        unique_tags.update(post['tags'])  

    unique_tags_list = ','.join(unique_tags)

    template = '''I will give you a list of tags. You need to unify tags with the following requirements,
    1. Tags are unified and merged to create a shorter list. 
       Example 1: "Jobseekers", "Job Hunting" can be all merged into a single tag "Job Search". 
       Example 2: "Motivation", "Inspiration", "Drive" can be mapped to "Motivation"
       Example 3: "Personal Growth", "Personal Development", "Self Improvement" can be mapped to "Self Improvement"
       Example 4: "Scam Alert", "Job Scam" etc. can be mapped to "Scams"
        Example 5: "Job Search", "Job Seekers", "Job Hunting" can be mapped to "Job Search"
        Example 6: "Job Opportunities", "Job Openings" can be mapped to "Job Opportunities"
        Example 7: "Job Seekers", "Job Search" can be mapped to "Job Search"
        Example 8: "Job Search", "Job Opportunities" can be mapped to "Job Search"
        Example 9: "Job Search", "Job Seekers" can be mapped to "Job Search"
        Example 10: "Job Search", "Job Opportunities" can be mapped to "Job Search"
    2. Each tag should be follow title case convention. example: "Motivation", "Job Search"
    3. Output should be a JSON object, No preamble
    3. Output should have mapping of original tag and the unified tag. 
       For example: {{"Jobseekers": "Job Search",  "Job Hunting": "Job Search", "Motivation": "Motivation}}

    
    Here is the list of tags: 
    {tags}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"tags": clean_text(unique_tags_list)})
    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        print("⚠️ Skipping post due to parsing error.")
        return {
            "line_count": 0,
            "language": "Unknown",
            "tags": []
        }
    return res

def extract_metadata(post):
    template = '''
      You are given a LinkedIn post. You need to extract number of lines, language of the post and tags.
      1. Return a valid JSON. No preamble. 
      2. JSON object should have exactly three keys: line_count, language and tags. 
      3. tags is an array of text tags. Extract maximum two tags.
      4. Language should be English or Tanglish (Tanglish means tamil + english)
      
      Here is the actual post on which you need to perform this task:  
      {post}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"post": clean_text(post)})
    
    json_parser = JsonOutputParser()
    try:
        res = json_parser.parse(response.content)
        return res
    except OutputParserException:
        print("⚠️ Skipping post due to parsing error.")
        return {
            "line_count": 0,
            "language": "Unknown",
            "tags": []
        }



if __name__ == "__main__":
  process_posts("data/raw_posts.json", "data/processed_posts.json")