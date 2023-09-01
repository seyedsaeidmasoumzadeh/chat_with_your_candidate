"""Prompts"""

from langchain import PromptTemplate


def get_prompt_template(type: str) -> str:
    if type == "question_answering":
        template = """As a job candidate, you will be asked by hiring manager to answer questions. Please use the context provided for you below as a part of your resume.


                context as a part of your resume: {context}
                hiring manager question: {question}

                Please just consider the context to answer the question and dont make up the answer.

                your answer:
                """
        prompt = PromptTemplate(
            template=template, input_variables=["context", "question"]
        )
    elif type == "cv_to_markdown":
        template = """Your task is to convert the provided context into Markdown format. The context to be included in the Markdown format should cover the following sections:

                Name
                Contact Information
                About Me
                Skills
                Experiences
                Education

                Please follow these guidelines for each section:

                1. About Me: Provide a concise summary of the entire resume in one paragraph.
                2. Skills: Include both soft skills (e.g., Leadership) and hard skills (e.g., Deep Learning, Python).
                3. Experience: Mention the companies or organizations where the person gained experience, along with detailed explanations of their responsibilities and notable achievements.
                4. Education: Specify the degree level and field of study, and mention any relevant projects or thesis titles related to the field.    

                context: {context}
                context in markdown format:

                """
        prompt = PromptTemplate(template=template, input_variables=["context"])

    else:
        raise ValueError("type is not valid")

    return prompt
