# Digital Pathfinder

Exer is a Python tool for automated path traversal, Vuln testing and digital exploration. It empowers security professionals and developers to identify potential vulnerabilities in web applications by searching for specific strings in URLs and analyzing the response content.

![Exer]

## Features

- **URL Exploration**: Traverse URLs at various depths to uncover potential security loopholes.
- **String Search**: Search for specific strings within URLs to detect sensitive information exposure or path traversal vulnerabilities.
- **Cookie Support**: Ability to provide authentication cookies for exploring authenticated areas of web applications.
- **Verbose Mode**: Enable detailed output to gain deeper insights into the exploration process and matched data.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Zierax/Exer-Vuln-Scanner.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd /Exer-Vuln-Scanner
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

```bash
python main.py --url <URL> --string <STRING> [--cookie <COOKIE>] [--depth <DEPTH>] [--verbose]
--url (-u): Specify the destination URL for exploration.
--string (-s): Provide the string to search for in the URL.
--cookie (-c): (Optional) Provide document cookie if required for authenticated exploration.
--depth (-d): (Optional) Specify the depth of traversal (default is 6).
--verbose (-v): (Optional) Enable verbose mode for detailed output.
Examples
Explore a URL for a specific string:

bash
Copy code
python main.py --url https://example.com --string password
Explore a URL with authentication cookie and verbose output:

bash
Copy code
python main.py -u https://example.com -s admin --cookie "session=123456789" --verbose
Contributing
Contributions are welcome! If you have any ideas for improvements or encounter any issues, feel free to open an issue or submit a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details.
