"""Allow an API Wrapper for the CLI"""
from typing import Union
from os import getenv


from wsgiref import simple_server
from click import Group, Command
from flask import Flask, render_template_string
from flask_rebar import Rebar
from flask_restx import Api


from regscale import __version__
from regscale.core.server.helpers import create_view_func, generate_parameters_model
from regscale.regscale import cli

app = Flask(__name__)
# setup swagger
api = Api(
    app,
    version=__version__,
    title="RegScale-CLI REST API Wrapper",
    description="A REST API wrapper support GET and POST requests for the RegScale-CLI.",
    doc="/swagger/",
    default="RegScale-CLI REST API",
    default_label="RegScale-CLI REST API Operations",
)
# setup redoc
rebar = Rebar()
registry = rebar.create_handler_registry()


# recursive function to generate routes from a click group
def generate_routes(api_instance: Api, group: Union[Group, Command], path: str = ""):
    """Generate routes for the app, recursively
    since group is assumed to be a click.Group, we get the command_name and command for all of those items.
    an endpoint_path is created. if the command is found to be a click.Group it is called on itself until we have a
    click command.
    :param Api api_instance: the flask_restx.Api instance
    :param group: A Group or Command from click
    :param path: str a representation of the endpoint path
    """
    for command_name, command in group.commands.items():
        endpoint_path = f"{path}/{command_name}"
        if command.name in {
            "encrypt",
            "decrypt",
            "change_passkey",
            "catalog",
            "assessments",
            "control_editor",
        }:
            continue
        if isinstance(command, Group) and command.name in {"issues"}:
            continue
        if isinstance(command, Group):
            # Generate routes for nested group
            generate_routes(api_instance, command, endpoint_path)
        else:
            # generate the CommandResource class
            resource_class = create_view_func(command)
            # if command has params, generate the parameters model for that command
            if command.params:
                # generate the parameters model
                parameters_model = generate_parameters_model(api_instance, command)
                resource_class.post = api.expect(parameters_model)(resource_class.post)
            api.add_resource(resource_class, endpoint_path)


# generate all the routes dynamically from the click information
generate_routes(api, cli)


@app.route("/redoc/")
def redoc():
    return render_template_string(
        """
        <!DOCTYPE html>
        <html>
        <head>
            <title>ReDoc</title>
            <meta charset="utf-8"/>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
            <style>
                body, html { margin: 0; padding: 0; }
                #redoc { width: 100vw; height: 100vw; position: sticky; }
            </style>
        </head>
        <body>
            <div id="redoc"></div>
            <script src="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"> </script>
            <script>
                Redoc.init('/swagger.json', {}, document.getElementById('redoc'))
            </script>
        </body>
        </html>
    """
    )


def run_app(
    port: int = int(getenv("REGSCALE_FLASK_PORT", "5555")), debug: bool = False
):
    """Run the CLI as a flask app
    :param int port: the port to serve flask on
    :param bool debug: should it be run in debug mode
    """
    server = simple_server.make_server("0.0.0.0", port, app)
    server.serve_forever()


def run_app_old(
    port=int(getenv("REGSCALE_FLASK_PORT", "5555")),
    host=getenv("REGSCALE_FLASK_HOST", "localhost"),
    debug=bool(getenv("REGSCALE_FLASK_DEBUG", "False")),
):
    """Entrypoint for running the flask app
    :param int port: port to run the app on, defaults to 5555
    :param host: the host the app should run on
    :param bool debug: should the app be run with debug.
    """
    from werkzeug.serving import run_simple

    run_simple(
        host,
        port,
        app,
        threaded=False,
        processes=1,
        use_debugger=debug,
        use_reloader=debug,
    )
