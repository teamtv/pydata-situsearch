# SituSearch

Sam Allardyce walks into the video analysis room.. “Morning, I was watching the last Arsenal match and there were a few situations I saw that I thought they would hurt us on Saturday. I want you to find me all of these situations from their last 5 games and find the times in our last 5 matches that we have faced similar situations. Let me have it this afternoon. Thanks” …….“Gaffer, that is going…” Big Sam slams the door “… to take hours… of work”.



### Installation

#### Clone the repository
To get started with this repository make sure you clone it using `git clone https://github.com/teamtv/pydata-situsearch.git`.

#### Install requirements
After making a local clone you it's preferred to create a virtual environment to keep you machine clean.

Then run:
```shell script
pip install -r requirements.txt
pip install -r requirements-local.txt
```

#### Getting tracking data
For this demo we use open tracking data provided by Metrica Sports. You can find more information about their datasets here: https://github.com/metrica-sports/sample-data

```shell script
cd data/raw
wget "https://github.com/metrica-sports/sample-data/blob/master/data/Sample_Game_1/Sample_Game_1_RawTrackingData_Home_Team.csv?raw=true" -O sample1_home.csv
wget "https://github.com/metrica-sports/sample-data/blob/master/data/Sample_Game_1/Sample_Game_1_RawTrackingData_Away_Team.csv?raw=true" -O sample1_away.csv
```


### Run it on your local machine
This project is able to run on your local machine without any additional dependencies like servers, daemons, brokers, etc.

#### Fill your local repository
You can fill your local repository using the command line tool. The tool will parse the Metrica files and write the serialized files on your local disk.
```shell script
cd src
python cmdline.py fill-local-repository
```

#### Select the right repository
Open `src/flask_api/__init__.py` and make sure you use the local repository.

#### Start the server
You can either use gunicorn or debug werkzeug server. To start the debug werkzeug server run:
```shell script
cd src
python run_app.py
```


## Diving in the code
Learn more about the code itself

### 1. Domain models
In favor of sharing knowledge about the domain between developers and domain experts, we create domain models. These models helps us to have a common language.

We try to use names that teach others about the domain. In the case of SituSearch we can identity three core tracking models:
1. [TrackingDataset](https://github.com/teamtv/pydata-situsearch/blob/master/src/domain/models/tracking.py#L34)
2. [Frame](https://github.com/teamtv/pydata-situsearch/blob/master/src/domain/models/tracking.py#L25)
3. [Point](https://github.com/teamtv/pydata-situsearch/blob/master/src/domain/models/tracking.py#L9)

For the search domain there are two models:
1. [ResultSet](https://github.com/teamtv/pydata-situsearch/blob/master/src/domain/models/search.py#L16)
2. [Result](https://github.com/teamtv/pydata-situsearch/blob/master/src/domain/models/search.py#L6)

### 2. Domain services
Next to the models there are domain services. These services provide the core of application.

In the tracking domain we have some interfaces:
1. [Matcher](https://github.com/teamtv/pydata-situsearch/blob/master/src/domain/services/matchers/base.py#L6)
2. [ReferenceMatcher](https://github.com/teamtv/pydata-situsearch/blob/master/src/domain/services/matchers/base.py#L12)
And one implementation: [MunkresMatcher](https://github.com/teamtv/pydata-situsearch/blob/master/src/domain/services/matchers/munkres.py#L17)

The search domain contains one service: [SearchEngine](https://github.com/teamtv/pydata-situsearch/blob/master/src/domain/services/search_engine.py#L6)

### 3. + 4. Application and Infrastructure layer
To make it possible to interact with the outside world we need an application layer. This layer provides an easy way to use the domain layers.
In this project we only have a [SearchApplicationService](https://github.com/teamtv/pydata-situsearch/blob/master/src/application/search.py#L7). 

Next to the application layer there is the infrastructure layer. This layer makes it possible to connect to external systems like database or file systems.
The infrastructure layer contains some more types of components.

For parsing Metrica data we can use the [MetricaParser](https://github.com/teamtv/pydata-situsearch/blob/master/src/infrastructure/parsers/metrica_parser.py#L7)

For converting a TrackingDataset to json (to send to the client) we can use the [DatasetToJson](https://github.com/teamtv/pydata-situsearch/blob/master/src/infrastructure/serializers/__init__.py#L6).

There are two repositories in this project:
1. [LocalRepository](https://github.com/teamtv/pydata-situsearch/blob/master/src/infrastructure/repositories/local.py#L7)
2. [S3Repository](https://github.com/teamtv/pydata-situsearch/blob/master/src/infrastructure/repositories/s3.py#L7)
Both implement the same [Repository](https://github.com/teamtv/pydata-situsearch/blob/master/src/domain/repository.py#L6) interface

### 5. Add a flask api
We would like to expose the frames of dataset, and the search results to the outside world. We use flask to do so.

The flask app can be found [here](https://github.com/teamtv/pydata-situsearch/blob/master/src/flask_api/__init__.py)

### 6. Deploy to heroku
Make sure you have an heroku account. You can sign up for free [here](https://signup.heroku.com/)

Install the [heroku toolbelt](https://devcenter.heroku.com/articles/heroku-cli) to use their CLI. [Read more](https://devcenter.heroku.com/articles/git) about how to link your local repository with their build platform.

To deploy the application just do
`git push heroku master`

Checkout the logging:
`heroku logs --tail`

Validate you api is working:
`curl https://pydata-situsearch.herokuapp.com/datasets/test/frames | less`

Make sure you have configured your aws keys: `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`

### 7. Add a React frontend
Normally a React frontend requires a lot of building tools. For this project we decides to do use babel within the browser. This makes the deployment way easier. Keep in mind you should use a tool like [create-react-app](https://reactjs.org/docs/create-a-new-react-app.html) when you want to build a real application.

The entire frontend can be [found here](https://github.com/teamtv/pydata-situsearch/blob/master/src/flask_api/index.html).