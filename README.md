
# Postmee Content Migration Script

## Overview

This script is designed to facilitate the migration or duplication of documents from the `https://www.startdoc.fr/` website to `https://postmee.com/` while ensuring that no duplicate content is generated. The primary goal is to avoid SEO penalties due to duplicate content by generating unique, extended content for each document.

## Features

- **API Integration**: Utilizes OpenAI's `gpt-4o-mini` model to generate unique content based on existing documents.
- **Token Management**: Carefully manages token usage to stay within API limits while ensuring comprehensive content generation.
- **Custom Content**: Generates customized titles and meta descriptions using a "spin" technique to ensure uniqueness.
- **HTML Comparison**: Produces a comparison HTML file that visually compares the original content from Startdoc with the newly generated content for Postmee.
- **JSON Output**: Saves the results in a JSON file for easy review and further processing.

## Prerequisites

- Python 3.x
- Install the required packages:
  ```bash
  pip install pandas openai tiktoken
  ```

## Configuration

1. **API Key Setup**:
   - Ensure your OpenAI API key is stored in a file named `api-keys.txt` in the root directory of your project.
   - The script reads the API key from this file to authenticate requests to the OpenAI API.

2. **Input Data**:
   - The script reads data from a TSV (Tab-Separated Values) file named `DB_Startdoc - Feuille 1.tsv`. This file should be located in the `/Users/simonazoulay/Postmee/` directory or update the script with your path.
   - Ensure the TSV file contains columns such as `company_name`, `startdoc_document_id`, `postmee_document_id`, `seo_title`, `seo_description`, and `seo_content_text`.

3. **Output Configuration**:
   - The script generates several outputs:
     - A JSON file `output.json` storing all generated content and metadata.
     - An HTML file `comparison_all.html` that visually compares the content from Startdoc and Postmee, including token usage details.
   - The output files are saved in the `/Users/simonazoulay/Postmee/` directory.

## Usage

1. **Run the Script**:
   - Execute the script using Python:
   ```bash
   python script_name.py
   ```
   - The script processes the first five entries from the TSV file, generates unique content for Postmee, and saves the results.

2. **Review the Output**:
   - Open the `comparison_all.html` file in a web browser to visually inspect the original and generated content side by side.
   - The JSON file can be opened with any text editor or parsed programmatically for further processing.

## Error Handling

- The script includes error handling for token limits and API response issues. In case of an error, the script will print a detailed message, including the number of tokens used and available, to help diagnose the issue.

## Future Enhancements

- **Batch Processing**: Extend the script to process a larger batch of documents.
- **Enhanced Error Handling**: Improve the granularity of error messages and automate retries for recoverable errors.
- **Custom Model Selection**: Allow users to select different models or configurations for content generation.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Author

This script was developed by [Your Name]. Contributions and improvements are welcome.
# startdoc_to_postmee
