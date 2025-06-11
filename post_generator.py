from llm_helper import llm
from few_shot import FewShotPosts

few_shot = FewShotPosts()


def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"


def generate_post(length, language, tag):
    prompt = get_prompt(length, language, tag)
    response = llm.invoke(prompt)
    return response.content


def get_prompt(length, language, tag):
    length_str = get_length_str(length)

    prompt = f"""
Generate a {length_str} LinkedIn post using the following instructions. No preamble. Always write in English script.

1) Topic: {tag}
2) Length: {length_str}
3) Language: {language}
If Language is Tanglish, use a natural blend of Tamil and English, but write only in English script.

### Instructions for Long Posts:

Start the post with an engaging greeting like "Hello Connections!" or "Hey LinkedIn fam!" to build connection.

Structure the post into three clear and emotionally engaging paragraphs:

- **Paragraph 1: WHAT** — What was done? Introduce the event/project/achievement and key context.
- **Paragraph 2: WHY & HOW** — Why did you take this up? What was the motivation or challenge? How did you and your team execute it?
- **Paragraph 3: IMPACT** — What was the outcome or achievement? Mention people involved, teamwork, and emotional highlights.

Wrap the post with a short, reflective line (optional) and add **relevant hashtags** at the end. Make it inspiring, personal, and shareable.

"""

    examples = few_shot.get_filtered_posts(length, language, tag)

    if len(examples) > 0:
        prompt += "\nUse the tone and style from the examples below:"

    for i, post in enumerate(examples):
        post_text = post['text']
        prompt += f"\n\nExample {i+1}:\n\n{post_text}"

        if i == 1:
            break

    return prompt



if __name__ == "__main__":
    print(generate_post("Medium", "English", "Mental Health"))