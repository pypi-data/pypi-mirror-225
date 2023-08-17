# BranchKey Python Client Application

![BK_logo](https://branchkey.com/wp-content/uploads/elementor/thumbs/branchkeytext-q0lwtzdsb6aaj26q2mj2lpksk47abbz9fd1gndr1l0.png)

This application runs against the BranchKey backend aggregation service for Federated Learning.
It provides a Python interface to login/logout a client, upload files to the system for aggregation,
and download aggregated output files.

# Install

- `pip install branchkey`

# Build Instructions

- To build the dependencies:
  - `make setup`, or
  - `pip install -r requirements.txt`
- To run the tests: `make test`
  - `make test`, or
  - python3 -m unittest -v

# Usage instructions

- To use a client:

  ```python
  import json
  from branchkey.client import Client

  credentials = {"leaf_name": "leaf-1",
                 "leaf_id": "46780841-9787-41e6-ac14-e3ee160e158a",
                 "leaf_session_token": "46780841-9787-41e6-ac14-e3ee160e158a",
                 "response_host":"response.branchkey.com"}

  host = "https://api.branchkey.com"

  proxy_servers = {
        'http': 'http://user:password@proxyserver.com:8080',
        'https': 'http://user:password@proxyserver.com:8080',
        }

  '''initialise the client
  it implicitly authenticates the leaf_session
  and fetches the run_details of the parent branch

  ssl: Whether to verify the SSL certificates of the
  remote host or not. Default it True

  wait_for_run: When trying to upload file, if the
  run is stopped/paused, this parameter decides whether
  to throw exception and stop the process, or wait for
  the run to be started again. Default is False

  run_check_interval_s: if wait_for_run=True, this
  parameter decides the sleeping interval of the
  program until the run status is checked again.
  Default is 30 seconds
  '''
  c = Client(credentials,host, ssl=True, wait_for_run=True, run_check_interval_s=15, proxies=proxy_servers)

  '''
  upload the file to the system
  '''
  c.file_upload("./file/path.npy")

  '''Download a file with the file_id value
  same as the one received from the consumer
  It downloads the files in the ./aggregated_files directory
  '''
  if not c.queue.empty():
        aggregation_id = c.queue.get(block=False)
        c.file_download(aggregation_id)

        '''To push performance analysis metrics for this aggregation:
        mode can be test, train or non-federated
        '''
        data = json.dumps({"key1":"val1","key2":"val2"})
        mode = "test"
        c.send_performance_metrics(aggregation_id, data, mode)
  ```

## File format

Weights file in a numpy `.npy` format:

```python
with open("./test.npy", "wb") as f:
    np.save(f, parameter_array)
[num_samples, [n_d parameter matrix]]
```

```
num_samples - the number of samples that contributed to this update
n_d parameter matrix - parameters
```

### Required file format

The required numpy arrays after exports

```python
[1329, list([array([[[[ 1.71775490e-01,    [[[ 8.74867663e-02,  5.19692302e-02, -1.64664671e-01,,          -2.23452481e-03,  1.11475676e-01],,    [-1.75505821e-02, -1...
```

```python
(1329, [array([[[[ 1.71775490e-01,  3.02851666e-02,  2.90171858e-02,
          -4.27578250e-03,  1.14474617e-01],
         [-8.07138346e-03,  1.44909814e-01, -5.36724664e-02,
          -3.51673253e-02, -1.82426855e-01],
         [ 6.75795972e-02, -1.72839850e-01, -7.25025982e-02,
          -1.59504730e-02,  1.60634145e-01],
         [ 6.62277341e-02, -2.26575769e-02, -1.65369093e-01,
          -8.67117420e-02,  1.80021569e-01],
         [-6.11407161e-02, -1.59245610e-01,  1.45820528e-01,
          -5.40512279e-02, -5.19061387e-02]]],
        ....
         [-1.44068539e-01,  6.15987852e-02,  1.83321223e-01,
          -1.79076958e-02, -1.53445438e-01],
         [-7.76787996e-02,  7.64556080e-02,  9.43044946e-02,
           1.63337544e-01, -1.69042274e-01],
         [-8.55994076e-02, -1.23661250e-01,  1.48442864e-01,
          -1.35983482e-01,  2.05254350e-02]]]], dtype=float32), array([ 0.13065006,  0.12797254, -0.12818147, -0.09621437,  0.04100017,
       -0.07248228,  0.02753541,  0.00476395, -0.11270998,  0.11353076,
       -0.0167569 ,  0.12654744, -0.05019006, -0.07281244,  0.03892357,
       -0.09698197, -0.06845284, -0.04604543, -0.01372138, -0.052395  ,
        0.04833373,  0.16228785,  0.09982517,  0.19556762,  0.10631064,
        0.02496212, -0.14297573, -0.10442089,  0.01970248, -0.1684099 ,
       -0.05076171,  0.19325127], dtype=float32), array([[[[-3.42470817e-02,  8.76816106e-04, -2.13724039e-02,
          -2.62880027e-02, -1.86583996e-02],
         [ 2.56936941e-02, -1.97169576e-02, -3.45735364e-02,
          -4.32738848e-03, -1.22306980e-02],
         [ 8.36322457e-03,  3.26042138e-02, -1.50063485e-02,
          -1.85401291e-02,  2.39207298e-02],
         [-1.15280924e-02, -3.47947963e-02,  2.17274204e-02,
           1.80862695e-02,  2.19682772e-02],
...
etc
```
