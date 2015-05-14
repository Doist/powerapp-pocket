The getpocket.com integration
-----------------------------

This app creates a new project in your Todoist account and starts
monitoring tasks in it. As soon as you create a task there
(or move the task from other projects), URLs from it will be extracted and added to your
pocket account.


Installation instructions for Heroku installation
-------------------------------------------------

1. Log in to your getpocket account and create a new application here:
   http://getpocket.com/developer/apps/new . Notice the "consumer key"
   created for you. It will be required to identify your PowerApp installation
   on getpocket.

   .. image:: powerapp_pocket/static/powerapp_pocket/getpocket_consumer_key.png

2. Extend your configuration with two variables. `POWERAPP_SERVICES` has to be
   extended with the git URL of the repository: `git@github.com:Doist/powerapp-pocket.git`.
   Create a new variable with this name if it doesn't exist yet.
   Then create a `POCKET_CONSUMER_KEY` key with a variable copied from your
   Pocket settings.

   It can be done either from command line::

        heroku config:set POWERAPP_SERVICES=git@github.com:Doist/powerapp-pocket.git
        heroku config:set POCKET_CONSUMER_KEY=XXXXX-XXXXXXXXXXXXXXXXX

   Or from Heroku web interface:

    .. image:: powerapp_pocket/static/powerapp_pocket/heroku_config_variables.png



Installation instructions for local of self-hosted installation
---------------------------------------------------------------

1. Log in to your getpocket account and create a new application here:
   http://getpocket.com/developer/apps/new

2. Copy the "consumer key" value from your application and create a new key
   `POCKET_CONSUMER_KEY` holding this value.

   .. image:: powerapp_pocket/static/powerapp_pocket/getpocket_consumer_key.png

   For local installations extend your `.env` file with a string like::

        POCKET_CONSUMER_KEY=XXXXX-XXXXXXXXXXXXXXXXX

   For Heroku installation, update the settings of your installation, either
   from the command line::

        heroku config:set POCKET_CONSUMER_KEY=XXXXX-XXXXXXXXXXXXXXXXX

   Or from their web interface. Just add variables and apply your changes.

    .. image:: powerapp_pocket/static/powerapp_pocket/heroku_config_variables.png
