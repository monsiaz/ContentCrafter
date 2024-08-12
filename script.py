import os
import pandas as pd
import json
import tiktoken 
import random 
from openai import OpenAI

# Load the API key from the api-keys.txt file
print("Loading API key...")
with open('/Users/simonazoulay/Postmee/api-keys.txt', 'r') as f:
    api_key = f.read().strip()

# Configure OpenAI API with the loaded key
client = OpenAI(api_key=api_key)
print("API key loaded and OpenAI configured.")

# Load the data from the TSV file
print("Loading data from the TSV file...")
file_path = '/Users/simonazoulay/Postmee/DB_Startdoc - Feuille 1.tsv'
df = pd.read_csv(file_path, sep='\t')

# Verify the structure of the loaded dataframe
print("Verifying the loaded dataframe:")
print(df.head())

# Select the first 5 entries for processing
df = df.head(5)
print("Selected the first 5 entries.")

# Define the path for the output JSON file
output_file_path = '/Users/simonazoulay/Postmee/output.json'

# Initialize or load existing results
print("Loading existing results if available...")
if os.path.exists(output_file_path):
    with open(output_file_path, 'r', encoding='utf-8') as f:
        results = json.load(f)
    print("Existing results loaded.")
else:
    results = []
    print("No existing results found, initializing a new list.")

# Function to calculate the number of tokens used
def count_tokens(text, model):
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))

# Function to generate content using OpenAI
def generate_content(model, prompt):
    print(f"Calling the OpenAI API with the model {model}...")
    
    # Calculate the number of tokens in the prompt
    prompt_tokens = count_tokens(prompt, model)
    print(f"Number of tokens in the prompt: {prompt_tokens}")

    # Determine the token limit based on the model
    max_tokens_limit = 16384  # Fixed token limit for gpt-4o-mini

    # Calculate the number of tokens available for the response, leaving a safety margin
    remaining_tokens = max_tokens_limit - prompt_tokens - 100  # Safety margin of 100 tokens
    print(f"Number of tokens available for the response: {remaining_tokens}")

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Tu es un expert des démarches administratives et des résiliations par courrier pour le site https://www.startdoc.fr/.Quand on te demande de reformuler, tu ne fais pas du simple paraphrase, tu fais mieux que l'original et tu apportes ton savoir."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=remaining_tokens,  # Adjusted limit to leave space for generated text
            temperature=0.3   # Temperature for text generation
        )
        generated_text = response.choices[0].message.content.strip()
        
        # Remove unwanted code formatting if present
        if generated_text.startswith("```html"):
            generated_text = generated_text[len("```html"):].strip()
        if generated_text.endswith("```"):
            generated_text = generated_text[:-len("```")].strip()

        generated_tokens = count_tokens(generated_text, model)
        print(f"Number of tokens generated: {generated_tokens}")
        print(f"Total tokens used (prompt + response): {prompt_tokens + generated_tokens}")

        return generated_text
    except Exception as e:
        print(f"Error during OpenAI API call: {e}")
        return f"Error: {e}"

# Function to generate a title with spin
def spin_title(company_name):
    print(f"Generating the title for {company_name}...")
    variations = [
        f"Résiliation {company_name} | Postmee",
        f"Résilier {company_name} rapidement | Postmee",
        f"Résiliation service {company_name} | Postmee"
    ]
    return random.choice(variations)

# Function to generate a description with spin
def spin_description(company_name):
    print(f"Generating the description for {company_name}...")
    variations = [
        f"Résilier {company_name} en quelques clics. Lettre de résiliation rédigée par des experts (+4,6/5 des clients satisfaits).",
        f"Résiliation de {company_name} facile et rapide. Lettre de résiliation professionnelle (+4,6/5 de satisfaction).",
        f"Résiliez votre service {company_name} en toute simplicité. Nos experts s'occupent de tout (+4,6/5 des clients).",
        f"Résiliation de {company_name} sans stress. Lettre prête en quelques clics (+4,6/5 des clients satisfaits)."
    ]
    return random.choice(variations)

# Create a directory to store the HTML comparison files
print("Creating directory to store the HTML files...")
html_output_dir = '/Users/simonazoulay/Postmee/comparisons/'
os.makedirs(html_output_dir, exist_ok=True)

# Prepare the global HTML content for the combined page
global_html_content = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comparaison de Résiliation - STARTDOC vs POSTMEE</title>
    <style>
        body { font-family: Arial, sans-serif; }
        .container { display: flex; }
        .section { flex: 1; padding: 20px; border-right: 2px solid #000; }
        .section:last-child { border-right: none; }
        .comparison-container { margin-bottom: 50px; }
        .postmee-logo-container {
            position: relative;
            width: 181px;
            height: 24px;
            background-color: #222148;
        }
        .postmee-logo-container img {
            position: relative;
            z-index: 1;
        }
    </style>
</head>
<body>
    <h1>Comparaison des résiliations - STARTDOC vs POSTMEE</h1>
"""

# Loop over the entries in the dataframe
print("Starting the loop over the dataframe entries...")
for index, row in df.iterrows():
    print(f"Processing entry {index + 1}/{len(df)} for {row['company_name']}...")

    # Generate the specific prompt for each entry
    company_name = row['company_name']
    startdoc_document_id = row['startdoc_document_id']
    postmee_document_id = row['postmee_document_id']

    prompt = (
        f"Reformule entièrement le texte suivant en utilisant un style d'écriture différent et en changeant les formulations pour éviter toute similarité avec l'original : {row['seo_content_text']}."
        f"Le texte doit impérativement être enrichi de 600 mots supplémentaires, en apportant de nouvelles informations ou en développant des aspects non abordés dans la version originale."
        f"Assure-toi que chaque phrase est distincte et que les concepts sont abordés sous un nouvel angle, en évitant strictement les répétitions ou paraphrases directes."
        f"Tu devras également introduire des paragraphes supplémentaires, non présents dans l'original, pour étendre les idées présentées."
        f"Le texte doit être complet et structuré avec des balises HTML appropriées, telles que <p> pour les paragraphes, <ul><li> pour les listes à puces. Par ailleurs tu mettras en <strong> les points importants ainsi que des tables si cela est nécessaire. Enfin tu pourras utiliser des H2, H3,H4 pour les titres (ils vont par 2 au minimum)."
        f"Le mot Startdoc doit être systématiquement remplacé par Postmee, et le texte doit être écrit de manière à se distinguer totalement de l'original tout en restant pertinent pour le sujet abordé."
    )
    
    print(f"Generated prompt:\n{prompt}")

    # Use the fixed model gpt-4o-mini
    model = 'gpt-4o-mini'
    print(f"Model selected: {model}")
    
    # Calculate the number of tokens in the prompt
    prompt_tokens = count_tokens(prompt, model)
    remaining_tokens = 16384 - prompt_tokens - 100  # Subtract 100 tokens as a safety margin
    print(f"Number of tokens in the prompt: {prompt_tokens}")
    print(f"Number of tokens available for the response: {remaining_tokens}")

    # Generate the SEO content
    seo_content_text_GPT = generate_content(model, prompt)
    print("SEO content generated.")

    # Generate the SEO title and description with spin
    seo_title_SPIN = spin_title(company_name)
    seo_description_SPIN = spin_description(company_name)
    print(f"Generated SEO title and description for Postmee:\nTitle: {seo_title_SPIN}\nDescription: {seo_description_SPIN}")

    # Construct the dictionary for this entry
    result = {
        "company_name": company_name,
        "startdoc_document_id": startdoc_document_id,
        "postmee_document_id": postmee_document_id,
        "Startdoc": {
            "seo_title": row['seo_title'],
            "seo_description": row['seo_description'],
            "seo_content_text": row['seo_content_text']
        },
        "Postmee": {
            "seo_title_SPIN": seo_title_SPIN,
            "seo_description_SPIN": seo_description_SPIN,
            "seo_content_text_GPT": seo_content_text_GPT,
            "model_used": model,  # Add the model used
            "tokens_used": {
                "input_tokens": prompt_tokens,
                "output_tokens": count_tokens(seo_content_text_GPT, model),
                "total_tokens": prompt_tokens + count_tokens(seo_content_text_GPT, model)
            }
        }
    }

    # Add the result to the list
    results.append(result)
    print(f"Result for {company_name} added to the list.")

    # Add the HTML comparison content for this company to the global content
    global_html_content += f"""
    <div class="comparison-container">
        <h2>Comparaison pour {company_name}</h2>
        <div class="container">
            <div class="section">
                <img src="https://cdn.startdoc.com/img/logo-startdoc.svg" alt="Startdoc" width="163" height="24">
                <p><strong>Titre :</strong> {row['seo_title']}</p>
                <p><strong>Méta Description :</strong> {row['seo_description']}</p>
                <hr>
                {row['seo_content_text']}
            </div>
            <div class="section">
                <div class="postmee-logo-container">
                    <img src="https://cdn.postmee.com/images/logo-postmee-light.svg?v=undefined" alt="Postmee" width="181" height="24">
                </div>
                <p><strong>Titre :</strong> {seo_title_SPIN}</p>
                <p><strong>Méta Description :</strong> {seo_description_SPIN}</p>
                <hr>
                {seo_content_text_GPT}
                <hr>
                <p><strong>Modèle utilisé :</strong> {model}</p>
                <p><strong>Tokens utilisés :</strong></p>
                <ul>
                    <li><strong>Input Tokens :</strong> {prompt_tokens}</li>
                    <li><strong>Output Tokens :</strong> {count_tokens(seo_content_text_GPT, model)}</li>
                    <li><strong>Total Tokens :</strong> {prompt_tokens + count_tokens(seo_content_text_GPT, model)}</li>
                </ul>
            </div>
        </div>
    </div>
    """

# Finalize the global HTML content
global_html_content += """
</body>
</html>
"""
print("Global HTML content generated.")

# Save the global HTML file
html_output_path = os.path.join(html_output_dir, 'comparison_all.html')
with open(html_output_path, 'w', encoding='utf-8') as f:
    f.write(global_html_content)
print(f"Global HTML file saved at {html_output_path}.")

# Save the updated JSON
with open(output_file_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)
print(f"JSON saved at {output_file_path}.")

print("Processing complete. JSON and global HTML file generated.")
