# Data Engineering showcase

Simple project showcasing my data engineering skills. It downloads data
from [Czech Police](https://kriminalita.policie.cz/) using [Dagster](https://dagster.io), cleans them up, processes them
and provide simple visualization using [Streamlit](https://streamlit.io).

## Requirements

- [Docker](https://docker.com)

## Running

First you need to build the application image using:

```bash
docker build -t data-engineering .
```

And then run:

```bash
docker run --rm -it -p 8501:8501 data-engineering
```

What happens first is Dagster will load the and process the necessary data and store them in `/tmp/criminality.pqt` (
using `/tmp` is just for convenience here). You should see a lot of debug logs from Dagster telling you how its
progressing. Then when data is prepared Streamlit is started, and you can access it either using the local URL you see
in docker logs or at `http://0.0.0.0:8501`.

## Author

- Hynek
  Davídek [hynek.davidek@gmail.com](mailto:hynek.davidek@gmail.com), [LinkedIn](https://www.linkedin.com/in/hynek-dav%C3%ADdek-77765511/)

## License

[MIT](https://choosealicense.com/licenses/mit/)