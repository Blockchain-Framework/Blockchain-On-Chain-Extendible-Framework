Below is a template for your `README.md` file written in Markdown format, tailored for your GodSight framework. This template includes instructions on installation, setting up the `.env` file, and using the framework's commands.

```markdown
# GodSight

GodSight is an extendable framework designed for on-chain analysis, offering a range of tools and functionalities to streamline the analysis of blockchain data.

## Installation

To get started with GodSight, follow these steps to install the framework on your system.

### Prerequisites

Ensure you have Python installed on your system. GodSight requires Python 3.10 or newer.

### Setting up the Virtual Environment

It's recommended to use a virtual environment for Python projects. To set up a virtual environment in the project directory, run:

```bash
python -m venv venv
```

Activate the virtual environment:

- On Windows:
    ```bash
    .\venv\Scripts\activate
    ```

- On macOS/Linux:
    ```bash
    source venv/bin/activate
    ```

### Installing GodSight

With the virtual environment activated, navigate to the root directory of GodSight and run:

```bash
pip install -e .
```

This command installs the GodSight framework in editable mode, allowing you to modify the framework and see changes without reinstalling.

## Configuration

Before running GodSight, you need to configure the environment variables. Navigate to the `GodSight/config` directory and create a `.env` file with the following structure:

```plaintext
DB_HOST=localhost
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_PORT=5432
EXTRACT_PATH=path/to/extract
MAPPER_PATH=path/to/mapper
META_PATH=path/to/meta
METRIC_PATH=path/to/metric
```

Replace the placeholders with your actual database configuration and paths.

## Usage

GodSight supports several commands to interact with the framework.

### Starting the API Server

To start the API server, run:

```bash
GodSight start api
```

This command launches the GodSight API server, making it accessible for API requests.

### Adding Blockchain Data

To add blockchain data to your analysis, use the `add-blockchain` command followed by the path to your JSON file containing blockchain data:

```bash
GodSight add-blockchain path/to/file.json
```

### Displaying Framework Information

To display information about the GodSight framework, run:

```bash
GodSight info
```

### Checking the Version

To check the current version of the GodSight framework installed, run:

```bash
GodSight --version
```

## Support

For support and further inquiries, please contact [your email or support channel].

```

Make sure to replace placeholders like `[your email or support channel]` with actual contact information or support channels you have for your project. This README provides a basic guide for users to get started with your framework, including installation, configuration, and basic usage commands.