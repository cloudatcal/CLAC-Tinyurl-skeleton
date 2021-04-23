# CLAC-TinyURL

## Introduction

This will be the solution repo for a lab aiming to emulate the functionality of tinyurl

We will take inspiration of features from [this](https://www.educative.io/courses/grokking-the-system-design-interview/m2ygV4E81AR#div-stylecolorblack-background-colore2f4c7-border-radius5px-padding5px2-requirements-and-goals-of-the-systemdiv) link, which you can optionally look at if you're interested.

Some important notes and dev links:

- You need a Github and an AWS account for this project.
- We reccomend using an IDE of some kind(PyCharm/VSCode/Atom). As students we get free access to the entire jetbrains toolbox. You can apply
  for a student account [here](https://www.jetbrains.com/shop/eform/students)

- We use the high level api everywhere we can.
  - The [Dynamo Resource API](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html) use resource
    **not** the client api
  - For developing and testing Lambdas we use [SAM](https://aws.amazon.com/serverless/sam/)
  - For questions about Lambda in general refer to the [AWS docs for lambda](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
  - For connecting Lambda to the world see [API Gateway](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Client.create_api_mapping)

The above should be all the documentation you _need_ inorder to contribute/solve to the assignment. Off course, feel
free to use any other resources or tutorials you find helpful :)

Before we get into deployment, we’d like to provide a high-level overview of the whole project. There are multiple components with this:

1. Starting the Home Page, the files for this aspect can be found within the Flask application. Essentially, all this is doing is creating a basic interface for the user to interact with.
2. The Flask application is, in turn, deployed on Elastic Beanstalk. The steps for this deployment will be described later below. Basically, Elastic Beanstalk offers a service to deploy and scale web applications. This can be done in a variety of languages (Java, Python, Node.js). You can read more about this at https://aws.amazon.com/elasticbeanstalk/ .
3. In the IAM roles, we are giving the application Create, Read, Update, and Delete access to the DynamoDB.
4. Then, in the DynamoDB, we are storing the key, value pairs (the key is the hash and the value is the original url inputted by the user).
5. Now, we can look at it from the user perspective. The hash generated creates a tiny url for the user to be able to access the original website. The user, then, creates an HTTP get request on the created tiny url (this is done by simply clicking the URL). This get request is processed in the Amazon API Gateway which, using the tiny url, gets the query_param “hash”.
6. From that, it creates an event in the lambda redirect function. Because this function has Read Access to the DynamoDB, it is able to uncover the original url. Thus, it redirects the tiny url to the original url.
7. At the same time, there is a record of the times in which the tiny url is called within the Amazon CloudWatch logs.

### Installation

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools. When installing the SAM CLI, you will need to create a Free Tier AWS account and set up IAM permissions and configure your local AWS credentials. The first link will guide you through the entire process.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* _OPTIONAL_: Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

## Setup

First, we will configure our AWS credentials. These instructions can be found in step 2 of the SAM CLI install linked above. Just to explicitly explain the steps again, here are the steps to do so:

1. First you want to [create your first IAM admin user and group](https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started_create-admin-group.html). Follow the instructions in the following link.
2. [Create your own IAM access key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey) using the AWS Management Console. Save both the access key ID and the secret access key.
3. Use the AWS CLI in your terminal to [configure your AWS credentials](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started-set-up-credentials.html).


After that, please create a local_constants.py file in the project root folder for all environment variables specific to your project, which are the following:

local_constants.py
```python
 AWS_PROFILE_NAME = '<your_local_profile_name>' # Left as "" if you deploy on the cloud and not locally
 DEPLOYED_GATEWAY = 'the.public.url.of.your.function.' # We will generate this in a later section when we deploy the serverless application
```

**IMPORTANT** Do NOT push your access keys onto Github, as that will expose your security credentials to the Internet and someone could hijack your account and incur a lot of fees on your account. Similarly, when you work with API keys for future personal projects, do not ever push your API keys on Github either.

## Deploying the Serverless Application

This project is located in the sam-app folder, and contains the source code and supporting files for a serverless application that you can deploy with the SAM CLI. It includes the following files and folders.

- redirect_handler/ - Code for the application's Lambda function.
- events/ - Invocation events that you can use to invoke the function.
- tests/ - Unit tests for the application code. **Not fully functional**
- my_layer/ - Creates a layer that allows us to import boto_utils.py in our lambda function. 
- template.yaml - A template that defines the application's AWS resources.

The application uses several AWS resources, including Lambda functions and an API Gateway API. These resources are defined in the `template.yaml` file in this project. You can update the template to add AWS resources through the same deployment process that updates your application code.

### Deployment of sam-app

In this section, we will begin the project by deploying the serveless application onto AWS with the SAM CLI. To build and deploy your application for the first time, make sure you are in the sam-app directory and run the following commands in your shell:

sam-app/
```bash
sam build
sam deploy --guided
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, with a series of prompts: 
Note: Enter yes for every 'y/n' option. It is also fine to press enter without inputting anything, as that will just set the default value, which is displayed inside the brackets.

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modified IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

**IMPORTANT**: You can find your API Gateway Endpoint URL in the output values displayed after deployment. You will put this in your local_constants.py file

### Create an AWS Elastic Beanstalk (EBS) Application for our Front end Flask App

Now that we have deployed the serverless application on AWS, we have finished provisioning several AWS resources for our project, including Lambda functions and an API Gateway API. We will now turn to deploying the front end application on EBS. As a reminder, these resources are defined in the `template.yaml` file in this project, which can be updated to add AWS resources through the same deployment process.

1. Login on the AWS management console (AWS website) and create an application on elastic beanstalk.
2. Give the application any name (Ex. Clacurl) and set the platform as **Python** as flask is a python framework. Set the platform branch as **Python3.8 on 64bit Amazon Linux 2** and the platform version as **3.2.1**.
3. Select **Sample Application** and then finish by selecting **Create Application**. 

### CodePipeline Setup

Now we are onto the coolest part of this project (in our humble opinion), which is setting up the CodePipeline for our front end application. In this section, we will connect our pipeline to our Github repo, which will automate the continuous build, testing, and deployment of our web application after any change in our code. With this tool, anytime we push a new change to our Github repo, the web application will be automatically redeployed so developers can test their changes.

1. After EBS is finished setting up, head to the CodePipeline page and click on **Pipeline** in the sidebar. Press **Create Pipeline**.
2. In the pipeline settings, give it any name (Ex. Clacurl-Github-Pipeline). Leave the rest of the settings at default value and select next.
3. Choose Github Version 2 for our source provider and press **Connect to Github**. Here, we will configure a connection to our Github repo. After you follow the instructions for connecting your Github account, select the repo that you have created for the Clacurl Project, and select the main branch. Leave the other options at default settings.
4. Skip the optional build stage.
5. For the deploy stage, choose AWS Elastic Beanstalk for your deploy provider. Choose the application that you created earlier (we named it Clacurl) and its corresponding environment.

### Set up the DynamoDB Database

Finally, for the last step of our project setup, we will run our migration to create the table in our database that will store the URL mappings between our generated link and the original URL. To do this, go to the project root directory and run the following command in the terminal:

./
```python
python3 boto_utils.py 
```

_Note_: This command will run the last section of the code, which basically tells the program to only run that section of code if the file was directly run as the main program. As you can see, it only calls the migration function, which is exactly what we want the program to do. 

We will have you all fill out these functions for the project assignment.

### Debugging

If you encounter any issues that need to be debugged, you can look at the logs that are generated by the Elastic Beanstalk application. To do this, go to your EBS app and the enviroment that you created. Then go to the logs tab and request the last 100 lines of logs. Much of the logs are gibberish (at least to us haha), but the useful logs will be the logs created by standard output (Check the logs under the title "/var/log/web.stdout.log"). 

## Optional Reading (For building and testing sam-app locally)
Note: Testing the application locally is not thoroughly tested yet, so you may encounter many issues that you will have to debug. However, if you're interested, it may be beneficial to just read along anyways to try and familiarize yourself with how to work more closely with sam-app.

### Use the SAM CLI to build and test locally

Build your application with the `sam build` command.

```bash
sam-app$ sam build
```

The SAM CLI installs dependencies defined in `redirect_handler/requirements.txt`, creates a deployment package, and saves it in the `.aws-sam/build` folder.

Test a single function by invoking it directly with a test event. An event is a JSON document that represents the input that the function receives from the event source. Test events are included in the `events` folder in this project.

Run functions locally and invoke them with the `sam local invoke` command.

```bash
sam-app$ sam local invoke HelloWorldFunction --event events/event.json
```

The SAM CLI can also emulate your application's API. Use the `sam local start-api` to run the API locally on port 3000.

```bash
sam-app$ sam local start-api
sam-app$ curl http://localhost:3000/
```

The SAM CLI reads the application template to determine the API's routes and the functions that they invoke. The `Events` property on each function's definition includes the route and method for each path.

```yaml
      Events:
        HelloWorld:
          Type: Api
          Properties:
            Path: /hello
            Method: get
```

### Add a resource to your application
The application template uses AWS Serverless Application Model (AWS SAM) to define application resources. AWS SAM is an extension of AWS CloudFormation with a simpler syntax for configuring common serverless application resources such as functions, triggers, and APIs. For resources not included in [the SAM specification](https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md), you can use standard [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html) resource types.

### Fetch, tail, and filter Lambda function logs

To simplify troubleshooting, SAM CLI has a command called `sam logs`. `sam logs` lets you fetch logs generated by your deployed Lambda function from the command line. In addition to printing the logs on the terminal, this command has several nifty features to help you quickly find the bug.

`NOTE`: This command works for all AWS Lambda functions; not just the ones you deploy using SAM.

```bash
sam-app$ sam logs -n HelloWorldFunction --stack-name sam-app --tail
```

You can find more information and examples about filtering Lambda function logs in the [SAM CLI Documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-logging.html).

### Tests

Tests are defined in the `tests` folder in this project. Use PIP to install the test dependencies and run tests.

```bash
sam-app$ pip install -r tests/requirements.txt --user
# unit test
sam-app$ python -m pytest tests/unit -v
# integration test, requiring deploying the stack first.
# Create the env variable AWS_SAM_STACK_NAME with the name of the stack we are testing
sam-app$ AWS_SAM_STACK_NAME=<stack-name> python -m pytest tests/integration -v
```

### Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name sam-app
```

### Resources

See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.

Next, you can use AWS Serverless Application Repository to deploy ready to use Apps that go beyond hello world samples and learn how authors developed their applications: [AWS Serverless Application Repository main page](https://aws.amazon.com/serverless/serverlessrepo/)
