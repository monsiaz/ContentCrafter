import os
import pandas as pd
import json
import tiktoken
import random
import re
import time
from openai import OpenAI
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load the API key from the api-keys.txt file
with open('/Users/simonazoulay/Postmee/api-keys.txt', 'r') as f:
    api_key = f.read().strip()

# Configure OpenAI API with the loaded key
client = OpenAI(api_key=api_key)

# Load the data from the Excel file
file_path = '/Users/simonazoulay/Postmee/DB_Startdoc (2).xlsx'
df = pd.read_excel(file_path, sheet_name=0)  # Load the first sheet

# Vérifier et supprimer les lignes où 'seo_content_text' est NaN
df = df.dropna(subset=['seo_content_text'])

# Define the path for the output JSON file
output_file_path = '/Users/simonazoulay/Postmee/output.json'

# Initialize or load existing results
if os.path.exists(output_file_path):
    with open(output_file_path, 'r', encoding='utf-8') as f:
        results = json.load(f)
else:
    results = []

# Create a set of already processed document IDs
processed_ids = {entry['startdoc_document_id'] for entry in results}

# Function to clean the text from unwanted strings
def clean_text(text):
    # Remove base64 encoded strings
    text = re.sub(r'data:image\/[^;]+;base64,[^"]*', '', text)
    # Remove any remaining image tags or other long, unwanted strings
    text = re.sub(r'<img[^>]*>', '', text)
    return text

# Function to calculate the number of tokens used
def count_tokens(text, model):
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))

# Function to generate content using OpenAI
def generate_content(model, prompt):
    prompt_tokens = count_tokens(prompt, model)
    
    max_tokens_limit = 16384
    remaining_tokens = max_tokens_limit - prompt_tokens - 100  # Safety margin of 100 tokens

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Tu es un expert des démarches administratives et des résiliations par courrier pour le site https://postmee.com/. Quand on te demande de reformuler, tu ne fais pas du simple paraphrase, tu apportes des informations utiles et détaillées."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=remaining_tokens,
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# Function to clean the generated content
def clean_content(content):
    # Remove different types of line breaks and tabs without replacing them with spaces
    content = content.replace('\n\t\t\t', '')
    content = content.replace('\n\n', '')
    content = content.replace('\n', '')
    
    # Ensure there are no multiple spaces introduced (if any other spaces are found)
    content = ' '.join(content.split())
    
    return content

# Function to generate a title with spin
def spin_title(company_name):
    variations = [
        f"Lettre de Résiliation {company_name} | Postmee",
        f"Résilier {company_name} rapidement - Lettre de résiliation | Postmee",
        f"Résiliation de votre abonnement {company_name} | Postmee"
    ]
    return random.choice(variations)

# Function to generate a description with spin
def spin_description(company_name):
    variations = [
        f"Résilier {company_name} en quelques clics. Lettre de résiliation rédigée par des experts (+4,6/5 des clients satisfaits).",
        f"Résiliation de {company_name} facile et rapide. Lettre de résiliation professionnelle (+4,6/5 de satisfaction).",
        f"Résiliez votre service {company_name} en toute simplicité. Nos experts s'occupent de tout (+4,6/5 des clients).",
        f"Résiliation de {company_name} sans stress. Lettre prête en quelques clics (+4,6/5 des clients satisfaits)."
    ]
    return random.choice(variations)

# Process a single row
def process_row(row):
    company_name = row['company_name']

    startdoc_document_id = row['startdoc_document_id']
    postmee_document_id = row['postmee_document_id']

    # Clean the seo_content_text
    cleaned_seo_content_text = clean_text(row['seo_content_text'])

    prompt = (
        f"Réécris le texte suivant de manière créative et originale, en modifiant complètement les structures de phrases et les formulations pour garantir une distinction nette par rapport à l'original : {cleaned_seo_content_text}."
        f"Ajoute au moins 140 mots supplémentaires en incluant de nouvelles informations, des détails complémentaires ou des exemples pertinents pour enrichir le contenu. Le texte doit explorer les idées sous un nouvel angle, sans se limiter à une simple paraphrase."
        f"Réorganise les paragraphes et modifie l'ordre des informations pour offrir une perspective différente, en ajoutant des paragraphes supplémentaires pour approfondir les points clés."
        f"Supprime les liens CTA et internes à Startdoc, ainsi que les ancres et phrases associées. Ne conserve pas les liens de maillage interne vers d'autres services de résiliation, ni les logos et liens vers ceux-ci (exemple : https://media.startdoc.com/)."
        f"Assure-toi que toutes les informations légales, adresses et autres éléments essentiels du texte original soient préservés et intégrés de manière naturelle, tout en restant clairs et faciles à localiser."
        f"Le texte doit être structuré avec des balises HTML comme <p> pour les paragraphes, <ul><li> pour les listes, et <strong> (sauf pour les titres) pour mettre en évidence les points importants. Utilise également des titres <h2>, <h3> et <h4> (sans <h1>), avec au moins deux sous-titres par niveau pour une meilleure organisation et lisibilité. Utilise uniquement du HTML basique sans ajout de fonts ou styles spécifiques."
        f"Assure une structure SEO pertinente, avec une hiérarchie cohérente des titres <h2>, <h3> et <h4> pour refléter les points clés du contenu."
        f"N'utilise pas de balises <p> autour des titres comme <h2>, <h3> et <h4>. Par exemple, préfère <h2>Titre</h2> à <p><h2 style=\"text-align: center;\">Titre</h2></p>."
        f"Ne termine pas le texte par un commentaire sur sa génération (comme 'Ce texte enrichi fournit des détails supplémentaires sur les démarches de résiliation')."
        f"Enfin, remplace systématiquement le terme 'Startdoc' par 'Postmee', et veille à ce que le contenu soit pertinent, informatif, et distinct de l'original, avec une approche plus innovante et engageante."
        f"Si tu trouves (en explorant le web) des informations utiles et complémentaires via les conditions générales de ventes sur le site de {row['company_name']}, n'hésite pas à préciser ces éléments ainsi que les conditions de résiliation ou spécificités du contrat."
        f"Vérifie que le texte généré respecte les critères suivants :"
        f"1. Il comprend bien au moins 140 mots supplémentaires par rapport à l'original."
        f"2. Il explique clairement et de manière structurée comment résilier {row['company_name']} et présente cette entreprise en détail."
        f"3. Il inclut un exemple concret de résiliation pour {row['company_name']}."
        f"4. Il précise clairement les conditions de résiliation, y compris les délais et les textes réglementaires associés."
        f"5. Il ne se termine pas par un commentaire sur la génération du texte."
    )
    
    # Generate the SEO content
    seo_content_text_GPT = generate_content('gpt-4o-mini', prompt)
    
    # Clean the generated content
    seo_content_text_GPT = clean_content(seo_content_text_GPT)

    # Generate the SEO title and description with spin
    seo_title_SPIN = spin_title(company_name)
    seo_description_SPIN = spin_description(company_name)

    # Construct the dictionary for this entry
    result = {
        "company_name": company_name,
        "startdoc_document_id": startdoc_document_id,
        "postmee_document_id": postmee_document_id,
        "Startdoc": {
            "seo_title": row['seo_title'],
            "seo_description": row['seo_description'],
            "seo_content_text": cleaned_seo_content_text
        },
        "Postmee": {
            "seo_title_SPIN": seo_title_SPIN,
            "seo_description_SPIN": seo_description_SPIN,
            "seo_content_text_GPT": seo_content_text_GPT,
        }
    }

    return result

# Parallel processing of rows
with ThreadPoolExecutor(max_workers=9) as executor:
    futures = {}
    for index, row in df.iterrows():
        if row['startdoc_document_id'] not in processed_ids:
            futures[executor.submit(process_row, row)] = row
    
    for future in tqdm(as_completed(futures), total=len(futures), desc="Processing", unit="entries"):
        result = future.result()
        if result:
            results.append(result)
            with open(output_file_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=4)
