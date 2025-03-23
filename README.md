# MCP-Agg: Multi-Channel Platform Aggregator

[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.0-green)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

MCP-Agg is a powerful API service that provides unified access to multiple tools and platforms through a single, consistent interface. It enables seamless integration with various services like GitHub, Slack, and more, simplifying workflow automation and enhancing productivity.

## 🚀 Features

- **Unified Tool Interface**: Access tools from multiple platforms through a standardized API
- **Authentication & Authorization**: Secure access to each integrated service
- **Extensible Architecture**: Easily add new tools and platforms
- **MCP Client Support**: Generate unique URLs for MCP client access
- **Comprehensive Documentation**: Well-documented API with Swagger UI

## 🛠️ Supported Platforms

### GitHub

- List repositories
- Get repository details
- Manage issues and pull requests
- Access user profiles

### Slack

- List channels
- Post messages
- Reply to threads
- Add reactions
- Access channel history
- Retrieve user profiles

## 📋 Requirements

- Python 3.12+
- PostgreSQL database
- uv package manager

## 🔧 Installation

1. Clone the repository:

```bash
git clone https://github.com/moosh3/mcp-agg.git
cd mcp-agg
```

2. Set up a virtual environment and install dependencies using uv:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

3. Create a `.env` file based on the `.env.example` template:

```bash
cp .env.example .env
# Edit .env with your configuration settings
```

4. Run database migrations:

```bash
alembic upgrade head
```

## 🚀 Running the Application

### Development Mode

```bash
uvicorn api.main:app --reload --port 8000
```

### Production Mode

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

### Using Docker

```bash
docker-compose up -d
```

## 📖 API Documentation

Once the application is running, access the interactive API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔌 Using the MCP Client

To access all your tools through an MCP client:

1. Register and log in to the MCP-Agg service
2. Connect your accounts for each supported platform (GitHub, Slack, etc.)
3. Navigate to the MCP URL generator endpoint
4. Use the generated URL in your MCP client configuration

## 🧪 Testing

Run tests using pytest:

```bash
python -m pytest
```

For coverage information:

```bash
python -m pytest --cov=api
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact

Project maintainer: [moosh3](https://github.com/moosh3)

---

Built with ❤️ using FastAPI and Python
