<div align="center">
    <h1 align="center">🎵 Serving Bark with BentoML</h1>
</div>

[Bark](https://github.com/suno-ai/bark) is a transformer-based text-to-audio model created by Suno. Bark can generate highly realistic, multilingual speech as well as other audio - including music, background noise and simple sound effects.

This is a BentoML example project, demonstrating how to build an audio generation API server using Bark. See [here](https://github.com/bentoml/BentoML?tab=readme-ov-file#%EF%B8%8F-what-you-can-build-with-bentoml) for a full list of BentoML example projects.

## Prerequisites

- You have installed Python 3.8+ and `pip`. See the [Python downloads page](https://www.python.org/downloads/) to learn more.
- You have a basic understanding of key concepts in BentoML, such as Services. We recommend you read [Quickstart](https://docs.bentoml.com/en/1.2/get-started/quickstart.html) first.
- (Optional) We recommend you create a virtual environment for dependency isolation for this project. See the [Conda documentation](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) or the [Python documentation](https://docs.python.org/3/library/venv.html) for details.

## Install dependencies

```bash
git clone https://github.com/bentoml/BentoBark.git
cd BentoBark
pip install -r requirements.txt
```

## Run the BentoML Service

We have defined a BentoML Service in `service.py`. Run `bentoml serve` in your project directory to start the Service.

```bash
$ bentoml serve service:SunoBark

2024-04-03T04:21:20+0000 [WARNING] [cli] Converting 'SunoBark' to lowercase: 'sunobark'.
2024-04-03T04:21:20+0000 [INFO] [cli] Starting production HTTP BentoServer from "service:SunoBark" listening on http://localhost:3000 (Press CTRL+C to quit)
```

The server is now active at [http://localhost:3000](http://localhost:3000/). You can interact with it using the Swagger UI or in other different ways. Note that you can set `voice_preset` to simulate your desired voice. See the [Bark Speaker Library](https://suno-ai.notion.site/8b8e8749ed514b0cbf3f699013548683?v=bc67cff786b04b50b3ceb756fd05f68c) for details (use the value in the Prompt Name column).

CURL

```bash
curl -X 'POST' \
  'http://localhost:3000/generate' \
  -H 'accept: audio/*' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "♪ In the jungle, the mighty jungle, the lion barks tonight ♪",
  "voice_preset": null
}'
```

Python client

```python
import bentoml

with bentoml.SyncHTTPClient("http://localhost:3000") as client:
    result = client.generate(
        text="♪ In the jungle, the mighty jungle, the lion barks tonight ♪",
        voice_preset="",
    )
```

Expected output:

[output-music](/assets/output-bark.wav)

## Deploy to BentoCloud

After the Service is ready, you can deploy the application to BentoCloud for better management and scalability. [Sign up](https://www.bentoml.com/) if you haven't got a BentoCloud account.

Make sure you have [logged in to BentoCloud](https://docs.bentoml.com/en/latest/bentocloud/how-tos/manage-access-token.html), then run the following command to deploy it.

```bash
bentoml deploy .
```

Once the application is up and running on BentoCloud, you can access it via the exposed URL.

**Note**: For custom deployment in your own infrastructure, use [BentoML to generate an OCI-compliant image](https://docs.bentoml.com/en/latest/guides/containerization.html).
