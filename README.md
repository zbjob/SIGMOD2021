EIRES: Efficient Integration of Remote Data in Event Stream Processing
---
This work has been accepted by SIGMOD'21. An extended version of the paper can be found [here](EIRES_extension.pdf).

## Prerequisites to run the code
* The compiler needs to support C++11 or higher. In Makefiles, the default compiler is set as g++.
* Bushfire detection code requires `boost` library, especially `geometry`, to compute intersections of polygons among others. That is to compute overlap of geography boundaries over satellite event streams.  To run bushfire detection code, please configure a boost lib, https://www.boost.org/users/history/version_1_72_0.html.  Edit  `EIRES/src/EIRES_bushfire/Makefile`, update flags `BOOST` and `BOOSTLD` with the path in your machine. 
* All running/configuration scripts are written for linux OS. Windows OS users need to change the paths accordingly (replace "/" with "\\").
* We build parsers to parse query workloads from files. We define query workloads in files ending with `.eql`.  `run/synthetic.eql`, `run/bf-7.7_14.16.eql` and `google_cluster.eql` are query workloads for synthetic, day-time bushfire detection and google cluster monitoring respectively. 

## Download code and data
We also provide compressed archive file for directly downloading. Please find the link [here](https://drive.google.com/file/d/1oC-MjfsoXmcbj7og-ll7L8zOHIa_dU5r/view?usp=sharing).

The size of the archive file, EIRES.tar.gz, is around 1.1GB. The unzipped repo is around 8.7GB.

## Code
Source code is in `src`. Separate directories are built for synthetic data, bushfire detection and google cluster monitoring.

Parameters and their semantics are listed as below:
| parameter      | semantics       |
| :------------- | :--------------:|
| -c | query workload file |
| -q | specific query name |
| -F | stream source file |
| -g | set greedy selection (event consumption policy) |
| -b | configure CEP engine as naive baseline (without caching and fetching) |
| -A | configure prefetch (PFetch) to CEP engine |
| -B | configure lazy evaluation (LzEval) to CEP engine |
| -D | the number of events to process |
| -C | cache capacity |
| -f | number of fetch worker threads |
| -L | transmission latency |
| -u | utility updating frequency |
| -X | utility estimation noise |
| -Y | partial match relax ratio for LzEval |
| -Z | prefetching probability |
| -p | throughput dumping file name |
| -n | latency dumping file name |
| -s | appending timestamps for discarded matches |

#### Synthetic
Directories,  `EIRES_cost_cache` and `EIRES_LRU_cache` are EIRES codebase combined with cost-based cache and LRU cache respectively.
They have similar code structures. Entry points, `main` functions, are defined in `EIRES_cost_cache/cep_match/cep_match.cpp` and `EIRES_LRU_cache/cep_match/cep_match.cpp`.

#### Bushfire detection
Bushfire detection code is in `EIRES_bushfire`. The entry point, `main` function is defined in `EIRES_bushfire/cep/cep_match.cpp`.

#### Cluster monitoring
Google cluster monitoring code is in `EIRES_google_cluster_monitoring`. The `main` function is defined in `EIRES_google_cluster_monitoring/cep_match/cep_match.cpp`




##
## Data
All datasets are in `data` directory. We build separate directories for synthetic datasets, bushfire detection datasets and google cluster monitoring datasets.

#### Synthetic datasets
They are in `data/synthetic_datasets/` with two synthetic data generators implemented by `Uniform_generator.cpp` and `Zipf_generator.cpp`.  As their names suggest, they generate payload value of event streams based on uniform and Zipf distributions respectively. The number of events is configurable. Due to limited capacity, we pushed two sample stream files composed of 500K events, `data/synthetic_datasets/Stream_uniform_500K.csv` and `data/synthetic_datasets/Stream_Zipf_500K.csv`.

#### Bushfire detection datasets
They are in `data/bushfire_datasets/`.
##### Raw satellite data
Imagery information is obtained from the satellite data streams available on Amazon AWS. http://tiny.cc/drt2oz 

The data samples are generated by the Advanced Baseline Imager (ABI) of GOES-16 satellite, which captures Earth’s radiance in 16 spectral bands via a variety of radiance detectors. Basically, they are digital maps of outgoing radiance values at the top of Earth’s atmosphere at visible, infrared, and near-infrared wavelengths. Then, the samples are compressed, packetized, and sent to the ground station, in which they are converted to geo-located and calibrated pixels, covering the whole America continent. The raw image pixels are kept in Network Common Data Form (netCDF) format, which is descriptive, flexible, standardized among large research projects. Each band/channel of an image sample is kept in a separate netCDF file. Detailed information about each band can be found in this [figure](data/bushfire_datasets/bushfire_detection_process.jpg).

##### weather data
Weather datasets are crawled from https://www.wunderground.com

##### Data pre-processing
To leverage GOES-16 satellite, we need pre-processing and generate event streams. In a nutshell, we cluster GOES-16 radiation levels per channel using kMeans and represent each cluster as a Polygon data type (using boost library). The process can be found in this [figure](data/bushfire_datasets/bushfire_detection_process.jpg).

Several visualized results can be found [here](data/bushfire_datasets/visualization.png).


There are four generated stream files.
```
california.csv
woolsey.csv
county.csv
kincade.csv
```
#### Google cluster monitoring datasets
Google cluster monitoring traces are very well defined.
Full datasets and descriptions are publicly available at https://github.com/google/cluster-data/blob/master/ClusterData2011_2.md. Due to limited capacity, we pushed a small sample, `data/google_cluster_monitoring_datasets/sample_event_stream.dat.gz`.

---

## Running scripts
#### configure boost lib
```
cd EIRES
wget https://boostorg.jfrog.io/artifactory/main/release/1.72.0/source/boost_1_72_0.tar.gz
tar zxvf boost_1_72_0.tar.gz
cd boost_1_72_0
./bootstrap.sh
./b2
```
Edit  `EIRES/src/EIRES_bushfire/Makefile`, update flags `BOOST` and `BOOSTLD` with the path in your machine. Assuming the `EIRES` is in `$HOME`, set
```
BOOST = -I $HOME/EIRES/boost_1_72_0
BOOSTLD = -L $HOME/EIRES/boost_1_72_0/stage/lib
```

#### Compile
```
cd EIRES
sh compile.sh
```
#### Running
we prepared scripts to run experiments of synhetic setting, bushfire detection and google cluster monitoring respectively.
Each script runs Baseline1, Baseline2, PFetch, FzEval and Hybrid for related queries and streams for 20 times.
Latency and throughput measurement are monitored and dumped to files for later post analysis.

```
cd run
sh run_all.sh
```
##### run synthetic code and datasets
```
sh run_synthetic.sh
```
##### run bushfire detection code and datasets
```
sh run_bushfire.sh
```
##### run google cluster monitoring code and datasets
```
sh run_google_cluster.sh
```

## Post analysis scripts
We analyse 5th, 25th, 50th, 75th, 95th percentiles latency and throughput. They are realized by `run/process-latency.py` and `run/process-throughput.py`
We prepare scripts to perform all the post analysis.
After running the evaluations. 

```
cd run
sh analyse_all.sh

sh analyse_synthetic.sh
sh analyse_bushfire.sh
sh analyse_google_cluster.sh
```
Following files will be generated. File names are self-explained. They cover latency and throughput for synthetic, bushfire and google cluster monitoring datasets
```
cd run
ls -l *.dat

result_latency_cost_greedy.dat
result_latency_LRU_greedy.dat
result_latency_cost_non_greedy.dat
result_latency_LRU_non_greedy.dat
result_latency_estimation_noise.dat
result_latency_cache_size.dat
result_latency_transmission_latency.dat
result_latency_weight_cache.dat
result_latency_weight_fetch.dat

result_throughput_cost_greedy.dat
result_throughput_LRU_greedy.dat
result_throughput_cost_non_greedy.dat
result_throughput_LRU_non_greedy.dat
result_throughput_estimation_noise.dat
result_throughput_cache_size.dat
result_throughput_transmission_latency.dat

result_latency_bushfire.dat
result_throughput_bushfire.dat

result_latency_google_cluster.dat
result_throughput_google_cluster.dat
```
