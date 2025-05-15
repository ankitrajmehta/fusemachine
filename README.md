# Sentiment Converter

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Analyze and convert the sentiment of any text message, power by Llama 3.3, hosted on Groq

# SET UP

1. **Clone the repository**
    ```bash
    # Clone the repository
    git clone https://github.com/ankitrajmehta/fusemachine.git

    # Navigate to the project directory
    cd chat_app
    ```
2. **Configure Environment Variables**
   - Copy or rename `.env.example` to `.env`, and fill in your Groq API key (https://console.groq.com/keys).

# TO RUN

```bash
docker compose build
```

```bash
docker compose up
```


- The site will be available at: [http://localhost/](http://localhost/)
- API documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

--------

#### TO CLEAN CONTAINERS AND VOLUME
```docker compose down -v```
