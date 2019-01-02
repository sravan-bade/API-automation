# API-automation

Slack python integration steps:
1. Create a Slack workspace(collaboration tool) if you already don't have one.
2. Create a team and add Incoming WebHooks app to any channel(Can change the channel at runtime).
3. Customise the Incoming WebHook if needed(Name, Icon) and save changes.
4. Copy the Webhook URL.
    eg: Webhook URL = https://hooks.slack.com/services/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
5. Below is the link to post results in Slack using API's.
    slackurl = https://hooks.slack.com/services/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
    requests.post(slackurl, json.dumps(body), headers=self.headers)
      body = {
              "channel": automation,
              "username": "APIBot",
              "attachments": [
                  {
                      "color": "#800000",
                      "title": "Postman API's",
                      "text": textt,
                      "fields": [
                          {
                              "title": "Execution Summary",
                              "value": "Execution count"
                          },
                          {
                              "title": "Test Execution Summary\n",
                              "value": "TestStatus1"+"\n"+"OpenDefects"
                          }
                      ]
                  }
              ]
         }


TestRail python integration steps:
1. Create a trail version of TestRail(Test Management Tool) if you already don't have one.
2. Create TestCases and pull it to TestRun.
3. Navigate to Administrator Tab and click on Site settings link.
4. Click on API tab and save settings by checking Enable API and Enable session authentication for API.
5. Below are the links to get Test cases and Test Run to pull from API's.
    getTestsUrl = "https://sravanbade.testrail.io/index.php?/api/v2/get_tests/{{runid}}"
    postTestUrl = "https://sravanbade.testrail.io/index.php?/api/v2/add_result_for_case/{{runid}}/{{caseid}}"

    requests.get(getTestsUrl, auth=(str(username), str(password)), headers=self.headers, verify=False)
    requests.post(postUrl, body, auth=(str(username), str(password)), headers=self.headers)
      body = '{"status_id":"1"}' #Passed
      body = '{"status_id":"2"}' #Blocked
      body = '{"status_id":"3"}' #Untested
      body = '{"status_id":"4"}' #Retest
      body = '{"status_id":"5"}' #failed

Github Slack integration:
1. Add Github app to your slack.
2. Using slash commands subscribe to your repository
   Format: /github subscribe owner/repository
       eg: /github subscribe sravan-bade/API-Automation
3. Connect to your Github account.
4. These are enabled by default, and can be disabled with the /github unsubscribe owner/repo [feature] command:
      issues - Opened or closed issues
      pulls - New or merged pull requests
      statuses - Statuses on pull requests
      commits - New commits on the default branch (usually master)
      deployments - Updated status on deployments
      public - A repository switching from private to public
      releases - Published releases
5. These are disabled by default, and can be enabled with the /github subscribe owner/repo [feature] command:
      reviews - Pull request reviews
      comments - New comments on issues and pull requests
      branches - Created or deleted branches
      commits:all - All commits pushed to any branch
    eg: /github subscribe sravan-bade/API-automation reviews [For subscribing single feature]
    eg: /github subscribe sravan-bade/API-automation reviews comments branches [For subscribing multiple features]

  For more information please refer to https://github.com/integrations/slack#configuration
6. After performing above steps you will get all github notifications in your slack Github app.
7. To raise a new issue/ pull request or any other action you can use below example:
    /github open sravan-bade/API-automation

Travis Slack integration:
1. Go to any slack channel and add Travis configuration app.
2. Once the configuration is added, click on Add configuration.
3. Select a channel from the drop-down and save settings.
4. You will get .travis.yml notification details from Setup instructions.
   eg: for single default
   notifications:
    slack: automation-sravan:jL4rpMwieMSUfQjqAqy0lnds
   eg: for multiple rooms
   notifications:
    slack:
      rooms:
        - automation-sravan:jL4rpMwieMSUfQjqAqy0lnds
        - automation-sravan:jL4rpMwieMSUfQjqAqy0lnds#general
        - automation-sravan:jL4rpMwieMSUfQjqAqy0lnds#random

Travis Github Deployment integration:
1. Login to Travis using GitHub credentials.
2. Add the repository to perform continuous integration.
3. Get the API key from Github and provide in the Travis environment variable.
    Generate api key from https://github.com/settings/tokens
    In Travis go to repository and click More options -> Settings
    In Environment Variables section add this api key with a variable name.
    eg: Name = api_key and value = xxxxxxxxxx.
4. Add below commands in travis.yml file to deploy the changes and save artifacts in github repository.
    before_deploy:
      Set up git user name and tag this commit
      if ! [[ $TRAVIS_TAG ]]; then
        export TRAVIS_TAG=${TRAVIS_TAG:-$(date +'%Y%m%d%H%M%S')-$(git log --format=%h -1)} &&
        export Release=${TRAVIS_TAG:-$(date +'%Y%m%d%H%M%S')-$(git log --format=%h -1)} &&
        git config --local user.name "sravan-bade" &&
        git config --local user.email "sravan-bade1@gmail.com" &&
        git tag "$TRAVIS_TAG";
      fi
    deploy:
      provider: releases
      api_key: ${api_key}
      file: 
        - "Test_Results.txt"
        - "test_run.log"
        - "test_error.log"
      skip_cleanup: true
      "name": "$(git log --format=%h -1)"
      on:
        all_branches: true 
        
     Use before deploy command only when there are no tags for your release and want to generate dynamic tag name.