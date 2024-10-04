import PyPDF2
from sentence_transformers import SentenceTransformer
import numpy as np


# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
    return text


# Function to split text into a specified number of batches
def split_text_into_batches(text, num_batches):
    # Remove any extra whitespaces and split into sentences
    sentences = text.split('. ')
    batch_size = len(sentences) // num_batches
    batches = []

    # Create batches based on the number of specified batches
    for i in range(num_batches):
        start_index = i * batch_size
        end_index = (i + 1) * batch_size if i != num_batches - 1 else len(sentences)
        batch_text = ". ".join(sentences[start_index:end_index])
        batches.append(batch_text)
    return batches


# Function to create embeddings for each batch
def create_embeddings_for_batches(batches, model_name='all-MiniLM-L6-v2'):
    model = SentenceTransformer(model_name)
    embeddings = [model.encode(batch) for batch in batches]
    return embeddings, batches


# Main script
def create_embeddings(pdf_path, num_batches):
    # Step 1: Extract text from PDF
    text = extract_text_from_pdf(pdf_path)

    # Step 2: Split text into batches
    batches = split_text_into_batches(text, num_batches)

    # Step 3: Create embeddings for each batch
    embeddings, batches = create_embeddings_for_batches(batches)

    # Step 4: Print or save embeddings
    for i, embedding in enumerate(embeddings):
        print(f"Embedding for Batch {i + 1}:\n{embedding}\n")

    return embeddings, batches


# Specify the PDF file path and number of batches
pdf_file = 'test.pdf'  # Replace with the path to your PDF file
number_of_batches = 600  # Adjust as needed
# Run the main script
embeddings, batches = create_embeddings(pdf_file, number_of_batches)
len(batches[0])

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline


# Function to create embeddings for a question
def get_question_embedding(question, model):
    return model.encode(question)


# Function to calculate cosine similarity and retrieve the top 5 most similar batches
def get_top_similar_batches(question_embedding, embeddings, contexts, top_n=2):
    # Compute cosine similarity between question embedding and each batch embedding
    similarities = cosine_similarity([question_embedding], embeddings)[0]

    # Get the indices of the top_n most similar batches
    top_indices = similarities.argsort()[-top_n:][::-1]  # Sort in descending order

    # Retrieve top_n similar contexts and their similarity scores
    top_similar_contexts = [(contexts[idx], similarities[idx]) for idx in top_indices]
    return top_similar_contexts


# Function to generate an answer based on similar contexts
def generate_answer(question, similar_contexts, model_name='distilbert-base-uncased-distilled-squad'):
    # Concatenate the similar contexts into a single context string
    combined_context = " ".join([context for context, _ in similar_contexts])
    initial_prompt = "You read a book about python, based on provided {context}, try to answer question, read this context carefully please answer me in at least 2 senteces. Context is as follows"
    # Load a pre-trained question-answering pipeline

    final_prompt = initial_prompt+combined_context
    print(f"Final content {final_prompt}")
    qa_pipeline = pipeline("question-answering", model=model_name)

    # Create input for the model
    qa_input = {
        'question': question,
        'context': final_prompt
    }

    # Generate the answer using the QA model
    answer = qa_pipeline(qa_input)
    return answer['answer']


from transformers import AutoModelForCausalLM, AutoTokenizer


def generate_text(prompt, model_name='gpt2', temperature=0.7, top_k=50, top_p=0.9):
    """
    Generates text using a specified LLM model based on the provided prompt.

    Parameters:
    - prompt (str): The input prompt to generate text from.
    - model_name (str): The name of the pre-trained language model to use.
    - max_length (int): The maximum length of the generated text (in tokens).
    - temperature (float): Controls randomness in generation. Lower values make the output more focused.
    - top_k (int): Limits the sampling pool to top_k tokens for diversity.
    - top_p (float): Nucleus sampling: cumulative probability for limiting token pool.

    Returns:
    - generated_text (str): The text generated by the model based on the input prompt.
    """
    # Load the pre-trained model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    # Encode the prompt text and generate tokens
    input_ids = tokenizer.encode(prompt, return_tensors='pt')

    # Generate text based on the prompt
    output = model.generate(
        input_ids,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        do_sample=True,
        num_return_sequences=1
    )

    # Decode the generated tokens to text
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

    return generated_text


# Example: Main function to demonstrate question answering based on context
def rag(question, pdf_embeddings, batch_contexts, embedding_model_name='all-MiniLM-L6-v2',
         qa_model_name='distilbert-base-uncased-distilled-squad'):
    # Load the pre-trained sentence transformer model
    embedding_model = SentenceTransformer(embedding_model_name)

    # Step 1: Create an embedding for the provided question
    question_embedding = get_question_embedding(question, embedding_model)

    # Step 2: Get the top 5 most similar batches based on cosine similarity
    top_similar_batches = get_top_similar_batches(question_embedding, pdf_embeddings, batch_contexts)
    combined_context = " ".join([context for context, _ in top_similar_batches])
    prompt_text = "Based on provided {context}, please try to answer on following {question}. Context is as follows: {context}, Question is as follows: {question}"
    prompt_text = prompt_text.replace('{context}', top_similar_batches[0][0]).replace("{question}", question)
    # Generate text using the model

    print(prompt_text)
    generated_output = generate_text(prompt_text, model_name='gpt2', max_length=150)

    # Print the generated text
    # Step 3: Generate an answer based on the top similar contexts
    #answer = generate_answer(question, top_similar_batches, model_name=qa_model_name)

    # # Step 4: Display the results
    # print(f"Question: {question}\n")
    # print(f"Answer: {answer}\n")
    # print("Top 5 Similar Contexts:\n")
    # for i, (context, similarity) in enumerate(top_similar_batches):
    #     print(f"Top {i + 1} Similar Context (Cosine Similarity: {similarity:.4f}):\n{context}\n")
    return generated_output

# Example inputs (replace these with actual embeddings and contexts)
#embeddings = np.random.rand(5, 384)  # Dummy embeddings for illustration purposes


# Sample question
question = "For what I can use loop?"

# Run the main function with example inputs
answer = rag(question, embeddings, batches)
