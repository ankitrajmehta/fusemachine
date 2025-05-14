# Sentiment Converter

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Analyze and convert the sentiment of any text message, power by Llama 3.3, hosted on Groq

# SET UP
create ```mongodb\.env``` exactly as in ```mongodb\.env.example``` (Can simply rename it as well)

create ```chat_app_backend\.env``` like ```chat_app_backend\.env.example```, by filing in the Groq api from https://console.groq.com/keys

# TO RUN

```docker compose build```

```docker compose up```

### Site will be hosted at: http://localhost/

### Docs at: http://localhost:8000/docs
--------

#### TO CLEAN CONTAINERS AND VOLUME
```docker compose down -v```
