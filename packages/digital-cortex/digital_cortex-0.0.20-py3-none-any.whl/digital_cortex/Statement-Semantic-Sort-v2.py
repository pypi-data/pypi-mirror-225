from email import header
from operator import index
import tensorflow as tf, datetime
from datetime import datetime
import torch
from pathlib import Path
from textblob import TextBlob
import re
import pandas as pd
import numpy as np, os
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine

pd.set_option('display.max_colwidth', None)
date_today_str = datetime.now()  # to set the date in the csv filename
today = date_today_str.strftime("%Y-%m-%d-%H%M%S")

print("This device is using GPU?", torch.cuda.is_available())
if torch.cuda.is_available() == False:
    print("Using CPU.. \nDEVICE = 'cpu'")
    DEVICE = 'cpu'  # Use 'cpu' if the training has to be done on CPU

else:
    print("Using GPU.. \nDEVICE =  'cuda:0'")
    DEVICE = 'cuda:0'  # Use 'cuda:0' if the training has to be done on GPU

# Make sure to remove duplicates from the phrases.
# This file must have a Header titled "Phrases":

original_path = input(f"Input the Excel/CSV Path of Statements to Sort: ")
if '"' in original_path:
    path1 = original_path.replace('"', "")
else:
    path1 = original_path

filename = os.path.splitext(os.path.basename(path1))[0]
fileextension = os.path.splitext(os.path.basename(path1))[1]

print("Statement Filename:", filename)
print("Statement File Extension:", fileextension)

if fileextension == ".xlsx":
    p = Path(path1)
    input_new_sentences_original = path1
    output_directory_folder = str(p.parent)
    dataframe = pd.read_excel(input_new_sentences_original)
    input_phrases = [*set(input_new_sentences_original)]
    print("Document:\n", dataframe)
    print("\nColumn Header:")
    for col in dataframe.columns:
        print(col)
    document = input("Input header name of the Statements:")
    read_xlsx = dataframe[document].drop_duplicates()
    read_xlsx.dropna(inplace=True)
    input_phrases = read_xlsx.drop_duplicates()
    input_new_sentences_original = list(input_phrases)
elif fileextension == ".csv":
    p = Path(path1)
    input_new_sentences_original = path1
    output_directory_folder = str(p.parent)
    dataframe = pd.read_csv(input_new_sentences_original)
    input_phrases = [*set(input_new_sentences_original)]
    print("Document:\n", dataframe)
    print("\nColumn Header:")
    for col in dataframe.columns:
        print(col)
    document = input("Input header name of the Statements:")
    read_xlsx = dataframe[document].drop_duplicates()
    read_xlsx.dropna(inplace=True)
    input_phrases = read_xlsx.drop_duplicates()
    input_new_sentences_original = list(input_phrases)

# No headers needed all statements should be in column 1.
# If you accidentally load the wrong list, no problem. Just reload the correct one.
input_phrases = [*set(input_new_sentences_original)]
input_new_sentences_cleaned = [x.lower().strip() for x in input_phrases]
unique_input_new_sentences_cleaned = list(set(input_new_sentences_cleaned))

# roberta_model = SentenceTransformer('all-mpnet-base-v2')

# THIS LINE OF CODE BELOW NEEDS TO BE UPDATED TO POINT TO THE LOCAL VERSION OF THIS PRETRAINED MODEL:
path_pretrained = input(f"Input the folder path of your model: ")
if '"' in path_pretrained:
    pre_path = path_pretrained.replace('"', "")
else:
    pre_path = path_pretrained
roberta_model = SentenceTransformer(pre_path, DEVICE)
sentence_embeddings = roberta_model.encode(input_new_sentences_cleaned)
# The speed of this depends on your CPU clock speed, and ignores core count

# This DOES REQUIRE A COLUMN HEADER. The header should be 'New Sentences'
original_path_2 = input(f"\nInput the Excel/CSV Path of New Sentences that you want to sort against: ")
if '"' in original_path_2:
    path2 = original_path_2.replace('"', "")
else:
    path2 = original_path_2
filename_topic = os.path.splitext(os.path.basename(path2))[0]
fileextension_topic = os.path.splitext(os.path.basename(path2))[1]

if fileextension_topic == ".xlsx":
    p = Path(path2)
    input_new_sentences_original = path2
    output_directory_folder = str(p.parent)
    dataframe = pd.read_excel(input_new_sentences_original)
    input_phrases = [*set(input_new_sentences_original)]
    print("Document:\n", dataframe)
    print("\nColumn Header:")
    for col in dataframe.columns:
        print(col)
    document = input("Input the header name that contains your new sentences:")
    read_xlsx = dataframe[document].drop_duplicates()
    topics = list(read_xlsx)
elif fileextension_topic == ".csv":
    p = Path(path2)
    input_new_sentences_original = path2
    output_directory_folder = str(p.parent)
    dataframe = pd.read_csv(input_new_sentences_original)
    input_phrases = [*set(input_new_sentences_original)]
    print("Document:\n", dataframe)
    print("\nColumn Header:")
    for col in dataframe.columns:
        print(col)
    document = input("Input the header name that contains your new sentences:")
    read_xlsx = dataframe[document].drop_duplicates()
    topics = list(read_xlsx)

topic_embeddings = roberta_model.encode(topics)


def get_similar_phrases(phrase, list_of_phrases, phrase_embeddings, original_phrases):
    """
    This function takes in a phrase, list of input phrases to compare against, and then
    a list of embeddings of the input phrases and outputs a sorted dataframe of the
    results.
    """
    phrase_num = list_of_phrases.index(phrase)

    cosine_sims = []

    for i in range(len(list_of_phrases)):
        cosine_sims.append(1 - cosine(phrase_embeddings[phrase_num], phrase_embeddings[i]))

    output = pd.DataFrame(zip(original_phrases, list_of_phrases, cosine_sims),
                          columns=['new_sentences_original', 'new_sentences_cleaned', 'cosine_sim'])

    return output.sort_values('cosine_sim', ascending=False)


def get_similar_phrases_by_topic(topic, list_of_phrases, phrase_embeddings, topic_embedding):
    """
    This function takes in a single phrase (aka "topic"), list of input phrases to compare against, and then
    a list of embeddings of the input phrases and outputs a sorted dataframe of the results.
    """

    cosine_sims = []

    for i in range(len(list_of_phrases)):
        cosine_sims.append(1 - cosine(topic_embedding, phrase_embeddings[i]))

    output = pd.DataFrame(zip(list_of_phrases, cosine_sims),
                          columns=['phrases', 'cosine_sim'])

    return output.sort_values('cosine_sim', ascending=False)


def find_similar_phrases_to_topics(list_of_topics, list_of_phrases, topic_embeddings,
                                   phrase_embeddings, show_scores=True):
    """
    This function will take in a topics list and a phrase list and sort the phrases into
    the topics based on having a similarity score of -0.75 or above.
    """

    print(f"There are {len(list_of_topics)} topics to go through")

    final_df = pd.DataFrame()
    unused_df = pd.DataFrame()

    phrases_used = []

    prog_counter = 1

    for topic, emb in zip(list_of_topics, topic_embeddings):
        sim_phrases = get_similar_phrases_by_topic(topic, list_of_phrases, phrase_embeddings, emb)
        phrases_only = list(sim_phrases[sim_phrases['cosine_sim'] >= -0.75]['phrases'])
        scores_only = list(sim_phrases[sim_phrases['cosine_sim'] >= -0.75]['cosine_sim'])
        # We can change the cutoff from -0.75 to whatever we need.

        phrases_used += phrases_only

        if show_scores:
            sim_phrases_to_attach = pd.DataFrame(zip(phrases_only, scores_only),
                                                 columns=[topic, f"{topic}_cos_scores"])
        else:
            sim_phrases_to_attach = pd.DataFrame(phrases_only, columns=[topic])

        final_df = pd.concat([final_df, sim_phrases_to_attach], axis=1)

        if prog_counter % 10 == 0:
            print(f"____________{prog_counter}/{len(list_of_topics)}")
        prog_counter += 1

    phrases_not_used = [x for x, y in zip(list_of_phrases, phrase_embeddings) if x not in phrases_used]
    not_used_embeddings = [y for x, y in zip(list_of_phrases, phrase_embeddings) if x not in phrases_used]

    print(f"There are {len(phrases_not_used)} phrases that did not get put into a topic.")
    print("Going through each phrase now and calculating the score with each topic.")

    prog_counter = 1

    for phrase, emb in zip(phrases_not_used, not_used_embeddings):
        sim_phrases = get_similar_phrases_by_topic(phrase, list_of_topics, topic_embeddings, emb).reset_index(drop=True)
        unused_df = pd.concat([unused_df, sim_phrases.rename(columns={"phrases": f"{phrase}_topics",
                                                                      "cosine_sim": f"{phrase}_score"})], axis=1)
        if prog_counter % 50 == 0:
            print(f"____________{prog_counter}/{len(phrases_not_used)}")
        prog_counter += 1

    print("Complete.")
    return final_df, unused_df


output, unused_output = find_similar_phrases_to_topics(topics, input_new_sentences_cleaned,
                                                       topic_embeddings, sentence_embeddings,
                                                       show_scores=True)
output_file = f"{output_directory_folder}\{filename}-Pretrained-Scored-{today}.xlsx"
output.to_excel(output_file, index=False)
print("Opening File..")
os.system(output_file)
print("File Closed!")
print("File saved:", output_file)
