import os
from google.api_core.client_options import ClientOptions
import googleapiclient.discovery

def predict_json(project, region, model, instances, version=None):
  prefix = "{}-ml".format(region) if region else "ml"
  api_endpoint = "https://{}.googleapis.com".format(prefix)
  client_options = ClientOptions(api_endpoint=api_endpoint)
  service = googleapiclient.discovery.build('ml', 'v1', client_options=client_options)
  name = 'projects/{}/models/{}'.format(project, model)

  if version is not None:
      name += '/versions/{}'.format(version)

  response = service.projects().predict(
      name=name,
      body={'instances': instances}
  ).execute()

  if 'error' in response:
    raise RuntimeError(response['error'])

  return response['predictions']

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "fm-j-league-pack-5c2a2566b71b.json"

instances = [
  [1, 0, 0, 0, 1.43, 29, 0.86, 0]
]
response = predict_json('fm-j-league-pack', 'us-central1', 'regional_league_model', instances, 'regional_league_model_20200523')

print(response)