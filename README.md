
# Postmee Content Migration and SEO Enhancement Script

## Overview

This project is designed to automate the process of migrating and rewriting content from one of our sites, Startdoc, to another, Postmee. The script not only transfers the content but also enhances it, ensuring that it is unique, SEO-friendly, and better aligned with Postmee's branding and guidelines. The script leverages the OpenAI API to rewrite and enrich the content, ensuring that it remains informative, engaging, and distinctly different from the original.

## Features

- **Content Rewriting**: The script generates creative and original rewrites of existing content, avoiding simple paraphrasing by adding at least 140 additional words and reorganizing the structure.
- **SEO Optimization**: The script enhances the SEO value of the content by:
  - Cleaning up the original text, removing unwanted HTML tags and base64 encoded strings.
  - Spinning titles and descriptions to create unique, varied content that appeals to search engines.
  - Maintaining a strict SEO structure with appropriate use of HTML tags such as `<h2>`, `<h3>`, `<h4>`, `<p>`, `<ul>`, and `<li>`.
- **Automated Content Generation**: Using OpenAI's GPT models, the script generates content that is not only unique but also enriched with additional information, ensuring that it is both informative and engaging.

## How to Integrate

### Prerequisites

- **Python 3.8+**: Ensure that you have Python installed on your machine.
- **OpenAI API Key**: You need an API key from OpenAI. Place this key in a file named `api-keys.txt` in the project directory.
- **Required Python Libraries**: Install the necessary Python libraries using the following command:

```bash
pip install pandas openai tiktoken tqdm
```

### Setup Instructions

1. **Clone the Repository**: Begin by cloning the repository to your local machine.

```bash
git clone https://github.com/monsiaz/startdoc_to_postmee.git
```

2. **Configure API Key**: Ensure that your OpenAI API key is correctly placed in a file named `api-keys.txt` in the project directory.

3. **Prepare Your Data**: Place your Excel file containing the Startdoc data in the project directory. The script is currently configured to load from `DB_Startdoc (2).xlsx`.

4. **Run the Script**: Execute the script using Python.

```bash
python migrate_content.py
```

This will start the migration process, rewriting and enhancing the content, and saving the output to `output.json`.

### Understanding the Script Logic

1. **Loading and Cleaning Data**: The script loads content from an Excel file, specifically focusing on `seo_content_text`. It cleans this text to remove unnecessary HTML and base64 strings.

2. **Content Generation**: For each entry, the script generates new content using the OpenAI API. The content is enriched, restructured, and enhanced to meet SEO standards.

3. **Parallel Processing**: The script uses parallel processing to handle multiple entries simultaneously, speeding up the migration process.

4. **Output**: The final output is saved in `output.json`, containing both the original and the rewritten content for Postmee.

### SEO Focus

This script is heavily focused on SEO improvements, ensuring that the migrated content is not just a copy of the original but a significant enhancement. By adding additional information, reorganizing the content, and applying SEO best practices, the script helps improve search engine rankings and drive more traffic to Postmee.

## Conclusion

This script is a powerful tool for migrating and enhancing content between websites. By leveraging AI-driven content generation, it ensures that the new content is both unique and optimized for SEO, helping to maintain and improve search engine visibility for Postmee.

