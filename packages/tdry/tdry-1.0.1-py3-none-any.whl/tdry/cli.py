import contextlib
import functools
import glob
#import locale
import sys, os, shutil
from contextlib import contextmanager
from datetime import datetime
from datetime import timedelta
from os.path import isdir
from typing import Tuple

import click
import click_log

from tdry import exceptions
from tdry import formatters
from tdry.configuration import ConfigurationError
from tdry.configuration import load_config
from tdry.interactive import TodoEditor
from tdry.model import Database
from tdry.model import Todo
from tdry.model import cached_property

from tinydb import TinyDB, Query
from tinydb.operations import set as tdb_set

db = TinyDB(os.path.expanduser("~")+"/.config/tdry/db.json")

click_log.basic_config()

from tdry.colors import *

@contextmanager
def handle_error():
    try:
        yield
    except exceptions.tdryError as e:
        click.echo(e)
        sys.exit(e.EXIT_CODE)

def catch_errors(f):
    @functools.wraps(f)
    def wrapper(*a, **kw):
        with handle_error():
            return f(*a, **kw)

    return wrapper

TODO_ID_MIN = 1
with_id_arg = click.argument("id", type=click.IntRange(min=TODO_ID_MIN))

def _validate_lists_param(ctx, param=None, lists=()):
    return [_validate_list_param(ctx, name=list_) for list_ in lists]


def _validate_list_param(ctx, param=None, name=None):
    ctx = ctx.find_object(AppContext)
    if name is None:
        if ctx.config["default_list"]:
            name = ctx.config["default_list"]
        else:
            raise click.BadParameter("You must set `default_list` or use -l.")
    lists = {list_.name: list_ for list_ in ctx.db.lists()}
    fuzzy_matches = [
        list_ for list_ in lists.values() if list_.name.lower() == name.lower()
    ]

    if len(fuzzy_matches) == 1:
        return fuzzy_matches[0]

    # case-insensitive matching collides or does not find a result,
    # use exact matching
    if name in lists:
        return lists[name]
    raise click.BadParameter(
        "{}. Available lists are: {}".format(
            name, ", ".join(list_.name for list_ in lists.values())
        )
    )


def _validate_date_param(ctx, param, val):
    ctx = ctx.find_object(AppContext)
    try:
        return ctx.formatter.parse_datetime(val)
    except ValueError as e:
        raise click.BadParameter(e) from None


def _validate_categories_param(ctx, param, val):
    ctx = ctx.find_object(AppContext)
    return ctx.formatter.parse_categories(val)


def _validate_priority_param(ctx, param, val):
    ctx = ctx.find_object(AppContext)
    try:
        return ctx.formatter.parse_priority(val)
    except ValueError as e:
        raise click.BadParameter(e) from None


def _validate_start_date_param(ctx, param, val) -> Tuple[bool, datetime] | None:
    ctx = ctx.find_object(AppContext)
    if not val:
        return None

    if len(val) != 2 or val[0] not in ["before", "after"]:
        raise click.BadParameter("Format should be '[before|after] [DATE]'")

    is_before = val[0] == "before"

    try:
        dt = ctx.formatter.parse_datetime(val[1])
        return is_before, dt
    except ValueError as e:
        raise click.BadParameter(e) from None


def _validate_startable_param(ctx, param, val):
    ctx = ctx.find_object(AppContext)
    return val or ctx.config["startable"]


def _validate_todos(ctx, param, val):
    ctx = ctx.find_object(AppContext)
    with handle_error():
        return [ctx.db.todo(int(id)) for id in val]


def _sort_callback(ctx, param, val):
    fields = val.split(",") if val else []
    for field in fields:
        if field.startswith("-"):
            field = field[1:]

        if field not in Todo.ALL_SUPPORTED_FIELDS and field != "id":
            raise click.BadParameter(f"Unknown field '{field}'")

    return fields


def validate_status(ctx=None, param=None, val=None) -> str:
    statuses = val.upper().split(",")

    if "ANY" in statuses:
        return ",".join(Todo.VALID_STATUSES)

    for status in statuses:
        if status not in Todo.VALID_STATUSES:
            raise click.BadParameter(
                'Invalid status, "{}", statuses must be one of "{}", or "ANY"'.format(
                    status, ", ".join(Todo.VALID_STATUSES)
                )
            )

    return val

"""
BEGGIN:: rooyca
"""

def time_spend(start_time, end_time):    
    start_time = int(start_time[0])*60+int(start_time[1])
    end_time = int(end_time[0])*60+int(end_time[1])
    return end_time - start_time

"""
END
"""

def _todo_property_options(command):
    click.option(
        "--category",
        "-c",
        multiple=True,
        default=(),
        callback=_validate_categories_param,
        help="Task categories. Can be used multiple times.",
    )(command)
    click.option(
        "--priority",
        default="",
        callback=_validate_priority_param,
        help="Priority for this task",
    )(command)
    click.option("--location", help="The location where this todo takes place.")(
        command
    )
    click.option(
        "--due",
        "-d",
        default="",
        callback=_validate_date_param,
        help=("Due date of the task, in the format specified in the configuration."),
    )(command)
    click.option(
        "--start",
        "-s",
        default="",
        callback=_validate_date_param,
        help="When the task starts.",
    )(command)

    @functools.wraps(command)
    def command_wrap(*a, **kw):
        kw["todo_properties"] = {
            key: kw.pop(key) for key in ("due", "start", "location", "priority")
        }
        # longform is singular since user can pass it multiple times, but
        # in actuality it's plural, so manually changing for #cache.todos.
        kw["todo_properties"]["categories"] = kw.pop("category")

        return command(*a, **kw)

    return command_wrap


class AppContext:
    def __init__(self):
        self.config = None
        self.db = None
        self.formatter_class = None
        self.task_id = None

    @cached_property
    def ui_formatter(self):
        return formatters.DefaultFormatter(
            self.config["date_format"],
            self.config["time_format"],
            self.config["dt_separator"],
        )

    @cached_property
    def formatter(self):
        return self.formatter_class(
            self.config["date_format"],
            self.config["time_format"],
            self.config["dt_separator"],
        )


pass_ctx = click.make_pass_decorator(AppContext)

_interactive_option = click.option(
    "--interactive",
    "-i",
    is_flag=True,
    default=None,
    help="Go into interactive mode before saving the task.",
)


@click.group(invoke_without_command=True)
@click_log.simple_verbosity_option()
@click.option(
    "--colour",
    "--color",
    "colour",
    default=None,
    type=click.Choice(["always", "auto", "never"]),
    help=(
        "By default tdry will disable colored output if stdout "
        "is not a TTY (value `auto`). Set to `never` to disable "
        "colored output entirely, or `always` to enable it "
        "regardless."
    ),
)
@click.option(
    "--porcelain",
    is_flag=True,
    help=(
        "Use a JSON format that will "
        "remain stable regardless of configuration or version."
    ),
)
@click.option(
    "--humanize",
    "-h",
    default=None,
    is_flag=True,
    help="Format all dates and times in a human friendly way",
)
@click.option(
    "--config",
    "-c",
    default=None,
    help="The config file to use.",
    envvar="tdry_CONFIG",
    metavar="PATH",
)
@click.option(
    "--newlist",
    "-nl",
    default=None,
    help="Make a new list with the given name.",
    metavar="TEXT",
)
@click.option(
    "--removelist",
    "-rml",
    default=None,
    help="Delete list with the given name.",
    metavar="TEXT",
)
@click.option(
    "--lists",
    "-sl",
    default=None,
    is_flag=True,
    help="Show all lists",
)
@click.pass_context
@click.version_option(prog_name="tdry")
@catch_errors
def cli(click_ctx, colour, porcelain, humanize, config, newlist, removelist, lists):
    ctx = click_ctx.ensure_object(AppContext)
    try:
        ctx.config = load_config(config)
    except ConfigurationError as e:
        raise click.ClickException(e.args[0]) from None

    _path = ctx.config["path"][:-1]

    try:
        if lists:
            print("="*11+" LISTS "+"="*11)
            print ("= "+" "*25+" =")
            for dir in os.listdir(_path):
                print("= 📁 "+str(dir)+" "*int(22-len(dir))+" =")
            print ("= "+" "*25+" =")
            print("="*29+"\n")
            print("To show tasks from a list use: ")
            print('\033[90m'+"> todo ls LIST\n")
            return
    except:
        pass

    try:
        if newlist:
            os.mkdir(_path +newlist)
            print()
            print("== List "+newlist+" created ==\n")
    except:
        print()
        print("== List "+newlist+" already exists ==\n")

    try:
        if removelist:
            print()
            if click.confirm('[ ☠️ ] Are you sure you want to delete list "'+removelist+'" ?'):
                shutil.rmtree(_path +removelist)
                print()
                print("== List "+removelist+" deleted ==\n")
    except:
        print("== List "+removelist+" does not exist ==")

    del _path

    if porcelain and humanize:
        raise click.ClickException(
            "--porcelain and --humanize cannot be used at the same time."
        )

    if humanize is None:  # False means explicitly disabled
        humanize = ctx.config["humanize"]

    if porcelain:
        ctx.formatter_class = formatters.PorcelainFormatter
    elif humanize:
        ctx.formatter_class = formatters.HumanizedFormatter
    else:
        ctx.formatter_class = formatters.DefaultFormatter

    colour = colour or ctx.config["color"]
    if colour == "always":
        click_ctx.color = True
    elif colour == "never":
        click_ctx.color = False

    paths = [
        path
        for path in glob.iglob(ctx.config["path"])
        if isdir(path) and not path.endswith("__pycache__")
    ]
    if len(paths) == 0:
        raise exceptions.NoListsFoundError(ctx.config["path"])

    ctx.db = Database(paths, ctx.config["cache_path"])

    # Make python actually use LC_TIME, or the user's locale settings
    #
    # I commented this out because it was causing issues with locales on arch
    #
    #locale.setlocale(locale.LC_TIME, "")

    if not click_ctx.invoked_subcommand:
        invoke_command(
            click_ctx,
            ctx.config["default_command"],
        )


def invoke_command(click_ctx, command):
    name, *raw_args = command.split(" ")
    if name not in cli.commands:
        raise click.ClickException("Invalid setting for [default_command]")
    parser = cli.commands[name].make_parser(click_ctx)
    opts, args, param_order = parser.parse_args(raw_args)
    for param in param_order:
        opts[param.name] = param.handle_parse_result(click_ctx, opts, args)[0]
    click_ctx.invoke(cli.commands[name], *args, **opts)


with contextlib.suppress(ImportError):
    import click_repl

    click_repl.register_repl(cli)
    click_repl.register_repl(cli, name="shell")


@cli.command()
@click.argument("summary", nargs=-1)
@click.option(
    "--list",
    "-l",
    callback=_validate_list_param,
    help="List in which the task will be saved.",
)
@click.option(
    "--read-description",
    "-r",
    is_flag=True,
    default=False,
    help="Read task description from stdin.",
)
@_todo_property_options
@_interactive_option
@pass_ctx
@catch_errors
def nw(ctx, summary, list, todo_properties, read_description, interactive):
    """
    Create a new task with SUMMARY.
    """

    todo = Todo(new=True, list=list)

    default_due = ctx.config["default_due"]
    if default_due:
        todo.due = todo.created_at + timedelta(hours=default_due)

    default_priority = ctx.config["default_priority"]
    if default_priority is not None:
        todo.priority = default_priority

    for key, value in todo_properties.items():
        if value is not None:
            setattr(todo, key, value)
    todo.summary = " ".join(summary)

    if read_description:
        todo.description = "\n".join(sys.stdin)

    if interactive or (not summary and interactive is None):
        ui = TodoEditor(todo, ctx.db.lists(), ctx.ui_formatter)
        ui.edit()
        click.echo()  # work around lines going missing after urwid

    if not todo.summary:
        raise click.UsageError("No SUMMARY specified")

    ctx.db.save(todo)
    click.echo(ctx.formatter.detailed(todo))


@cli.command()
@pass_ctx
@click.option(
    "--raw",
    is_flag=True,
    help=(
        "Open the raw file for editing in $EDITOR.\n"
        "Only use this if you REALLY know what you're doing!"
    ),
)
@_todo_property_options
@_interactive_option
@with_id_arg
@catch_errors
def ed(ctx, id, todo_properties, interactive, raw):
    """
    Edit the task with id ID.
    """
    todo = ctx.db.todo(id)
    if raw:
        click.edit(filename=todo.path)
        return
    old_list = todo.list

    changes = False
    for key, value in todo_properties.items():
        if value is not None and value != []:
            changes = True
            setattr(todo, key, value)

    if interactive or (not changes and interactive is None):
        ui = TodoEditor(todo, ctx.db.lists(), ctx.ui_formatter)
        ui.edit()

    # This little dance avoids duplicates when changing the list:
    new_list = todo.list
    todo.list = old_list
    ctx.db.save(todo)
    if old_list != new_list:
        ctx.db.move(todo, new_list=new_list, from_list=old_list)
    click.echo(ctx.formatter.detailed(todo))


@cli.command()
@pass_ctx
@with_id_arg
@catch_errors
def sh(ctx, id):
    """
    Show details about a task.
    """
    todo = ctx.db.todo(id, read_only=True)
    click.echo(ctx.formatter.detailed(todo))


@cli.command()
@pass_ctx
@click.argument(
    "todos",
    nargs=-1,
    required=True,
    type=click.IntRange(0),
    callback=_validate_todos,
)
@catch_errors
def do(ctx, todos):
    """Mark one or more tasks as done."""
    for todo in todos:
        todo.complete()
        ctx.db.save(todo)
        click.echo(ctx.formatter.detailed(todo))


@cli.command()
@pass_ctx
@click.argument(
    "todos",
    nargs=-1,
    required=True,
    type=click.IntRange(0),
    callback=_validate_todos,
)
@catch_errors
def cc(ctx, todos):
    """Cancel one or more tasks."""
    for todo in todos:
        todo.cancel()
        ctx.db.save(todo)
        click.echo(ctx.formatter.detailed(todo))


@cli.command()
@pass_ctx
@click.confirmation_option(prompt="Are you sure you want to delete all done tasks?")
@catch_errors
def fl(ctx):
    """
    Delete done tasks. This will also clear the cache to reset task IDs.
    """
    database = ctx.db
    for todo in database.flush():
        click.echo(ctx.formatter.simple_action("Flushing", todo))


@cli.command()
@pass_ctx
@click.argument("ids", nargs=-1, required=True, type=click.IntRange(0))
@click.option("--yes", is_flag=True, default=False)
@catch_errors
def rm(ctx, ids, yes):
    """
    Delete tasks.

    Permanently deletes one or more task. It is recommended that you use the
    `cancel` command if you wish to remove this from the pending list, but keep
    the actual task around.
    """

    todos = []
    for i in ids:
        todo = ctx.db.todo(i)
        click.echo(ctx.formatter.compact(todo))
        todos.append(todo)

    if not yes:
        click.confirm("Do you want to delete those tasks?", abort=True)

    for todo in todos:
        click.echo(ctx.formatter.simple_action("Deleting", todo))
        ctx.db.delete(todo)


@cli.command()
@pass_ctx
@click.option(
    "--list", "-l", callback=_validate_list_param, help="The list to copy the tasks to."
)
@click.argument("ids", nargs=-1, required=True, type=click.IntRange(0))
@catch_errors
def cp(ctx, list, ids):
    """Copy tasks to another list."""

    for id in ids:
        original = ctx.db.todo(id)
        todo = original.clone()
        todo.list = list
        click.echo(ctx.formatter.compact(todo))
        ctx.db.save(todo)


@cli.command()
@pass_ctx
@click.option(
    "--list", "-l", callback=_validate_list_param, help="The list to move the tasks to."
)
@click.argument("ids", nargs=-1, required=True, type=click.IntRange(0))
@catch_errors
def mv(ctx, list, ids):
    """Move tasks to another list."""

    for id in ids:
        todo = ctx.db.todo(id)
        click.echo(ctx.formatter.compact(todo))
        ctx.db.move(todo, new_list=list, from_list=todo.list)


@cli.command()
@pass_ctx
@click.argument("lists", nargs=-1, callback=_validate_lists_param)
@click.option("--location", help="Only show tasks with location containg TEXT")
@click.option("--grep", help="Only show tasks with message containg TEXT")
@click.option(
    "--sort",
    help=(
        "Sort tasks using fields like : "
        '"start", "due", "priority", "created_at", "percent_complete" etc.'
        "\nFor all fields please refer to: "
        "<https://tdry.readthedocs.io/en/stable/usage.html> "
    ),
    callback=_sort_callback,
)
@click.option(
    "--reverse/--no-reverse",
    default=True,
    help="Sort tasks in reverse order (see --sort). Defaults to true.",
)
@click.option(
    "--due", default=None, help="Only show tasks due in INTEGER hours", type=int
)
@click.option(
    "--category",
    "-c",
    multiple=True,
    default=(),
    help="Only show tasks with specified categories.",
    callback=_validate_categories_param,
)
@click.option(
    "--priority",
    default=None,
    help=(
        "Only show tasks with priority at least as high as TEXT (low, medium or high)."
    ),
    type=str,
    callback=_validate_priority_param,
)
@click.option(
    "--start",
    default=None,
    callback=_validate_start_date_param,
    nargs=2,
    help="Only shows tasks before/after given DATE",
)
@click.option(
    "--startable",
    default=None,
    is_flag=True,
    callback=_validate_startable_param,
    help=(
        "Show only todos which "
        "should can be started today (i.e.: start time is not in the "
        "future)."
    ),
)
@click.option(
    "--status",
    "-s",
    default="NEEDS-ACTION,IN-PROCESS",
    callback=validate_status,
    help=(
        "Show only todos with the "
        "provided comma-separated statuses. Valid statuses are "
        '"NEEDS-ACTION", "CANCELLED", "COMPLETED", "IN-PROCESS" or "ANY"'
    ),
)
@catch_errors
def ls(ctx, *args, **kwargs):
    """
    List tasks (default). Filters any completed or cancelled tasks by default.

    If no arguments are provided, all lists will be displayed, and only
    incomplete tasks are show. Otherwise, only todos for the specified list
    will be displayed.

    eg:
      \b
      - `todo list' shows all unfinished tasks from all lists.
      - `todo list work' shows all unfinished tasks from the list `work`.

    This is the default action when running `todo'.

    The following commands can further filter shown todos, or include those
    omited by default:
    """
    hide_list = (len([_ for _ in ctx.db.lists()]) == 1) or (  # noqa: C416
        len(kwargs["lists"]) == 1
    )

    kwargs["categories"] = kwargs.pop("category")

    todos = ctx.db.todos(**kwargs)
    click.echo(ctx.formatter.compact_multiple(todos, hide_list))

"""
IN THE BENIGIN:: rooyca
"""

@cli.command()
@pass_ctx
@click.argument("task_id", nargs=-1, required=False, type=click.IntRange(0))
@click.option(
    "--all",
    "-a",
    default=None,
    is_flag=True,
    help="Show all todos that are being done.",
)
@catch_errors
def doing(ctx, **kwargs):
    """Show the task that is being done now."""
    try:
        if kwargs["task_id"][0] is not None:
            Task = Query()
            if db.table('done').search(Task.task_id == kwargs["task_id"][0]):
                click.echo("="*(23+int(len(str(kwargs["task_id"][0])))))
                click.echo("== Task ID "+str(kwargs["task_id"][0])+" is done. ==")
                click.echo("="*(23+int(len(str(kwargs["task_id"][0])))))
                return
            r = ctx.db.todo(kwargs["task_id"][0])
            t = ctx.formatter.select_format(r)
            click.echo(" >> "+t)
            doing = db.table("doing") 

            if doing.search(Task.task_id == kwargs["task_id"][0]):
                return

            doing.insert({'task_id': kwargs["task_id"][0],
                          'start_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                          'summary': t,
                          'time_spent': 0,
                          'resume_at': None,
                          'end_time': None,
                          })
            return
    except IndexError:
        pass

    doing = db.table("doing")
    tasks = doing.all()
    if kwargs["all"]:
        color_print = GRAY        
        max_leng = 0
        for t in tasks:
            if max_leng < len(t["summary"]):
                max_leng = len(t["summary"])

        for i, task in enumerate(tasks):
            space = ""
            if i == len(tasks) - 1:
                color_print = GREEN
            if int(task.get('task_id')) <= 9:
                space = " "
            click.echo(color_print+
                       str(task.get('task_id'))+
                       space+
                       "|| "+
                       task.get('summary')+
                       " "*int(max_leng-len(task.get('summary')))+
                       "  >> "+
                       f"({task.get('start_time')})"
                       )
        return
    try:
        task = tasks[-1]
        click.echo(str(task.get('task_id'))+". "+GREEN+task.get('summary')+WHITE+" >> "+f"{CYAN}({task.get('start_time')})")
    except IndexError:
        click.echo("No task is being done now, please use 'todo doing ID' to start a task.")

@cli.command()
@pass_ctx
@click.option(
    "--show",
    "-s",
    default=None,
    is_flag=True,
    help="Show all todos that has been done.",
)
@click.option(
    "--clear",
    "-c",
    default=None,
    is_flag=True,
    help="Clear all todos that has been done.",
)
@catch_errors
def done(ctx, *args, **kwargs):
    """Mark a task as done."""
    done = db.table("done")

    if kwargs["clear"]:
        if click.confirm('[ ☠️ ] Are you sure you want to delete all done tasks?'):
            done.truncate()
            click.echo("-"*35)
            click.echo("All done tasks were deleted.")
        return    

    if not kwargs["show"]:
        try:
            doing = db.table("doing")
            Task = Query()
            if done.search(Task.task_id == doing.all()[-1]['task_id']):
                click.echo("="*(23+int(len(str(doing.all()[-1]['task_id'])))))
                click.echo("== Task ID "+str(doing.all()[-1]['task_id'])+" is done. ==")
                click.echo("="*(23+int(len(str(doing.all()[-1]['task_id'])))))
                doing.remove(Task.task_id == doing.all()[-1]['task_id'])
                return

            doing.update(tdb_set('end_time', datetime.now().strftime("%Y-%m-%d %H:%M:%S")), 
                                                Task.task_id == doing.all()[-1]['task_id'])

            now = datetime.now().strftime("%H:%M:%S").split(":")

            try:
                time_s_resume = time_spend(doing.all()[-1]['resume_at'].split(" ")[1].split(":"), now)
                time_s = time_s_resume
            except:
                time_s = time_spend(doing.all()[-1]['start_time'].split(" ")[1].split(":"), now)

            try:
                time_s_before = int(doing.all()[-1]['time_spent'])
                time_s = time_s_before + time_s
            except:
                pass

            doing.update(tdb_set('time_spent', time_s), Task.task_id == doing.all()[-1]['task_id'])
            done.insert({'task_id': doing.all()[-1]['task_id'],
                         'start_time': doing.all()[-1]['start_time'],
                         'summary': doing.all()[-1]['summary'],
                         'time_spent': doing.all()[-1]['time_spent'],
                         'resume_at': doing.all()[-1]['resume_at'],
                         'end_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
            doing.remove(Task.task_id == doing.all()[-1]['task_id'])
        except IndexError:
            click.echo("There are not tasks being done now.")
            click.echo("-"*35)

    all_done = done.all()
    for i, task in enumerate(all_done):
        click.echo(f"{i+1}. {GREEN}{task.get('summary')}{WHITE} >> {task.get('start_time')} ({task.get('time_spent')} min)")

@cli.command()
@pass_ctx
@catch_errors
def cancel(ctx):
    """Cancel a task that is being done."""
    doing = db.table("doing")
    try:
        doing.remove(doc_ids=[doing.all()[-1]['task_id']])
    except IndexError:
        click.echo("There are not tasks being done now.")

@cli.command()
@pass_ctx
@catch_errors
def pause(ctx):
    """Pause a task that is being done."""
    pause = db.table("pause")
    try:
        doing = db.table("doing")
        Task = Query()
        doing.update(tdb_set('time_spent', 
                    time_spend(doing.all()[-1]['start_time'].split(" ")[1].split(":"),
                    datetime.now().strftime("%H:%M:%S").split(":"))),
                    Task.task_id == doing.all()[-1]['task_id'])
        pause.insert({'task_id': doing.all()[-1]['task_id']})
    except IndexError:
        click.echo("There are not tasks being done now.")

@cli.command()
@pass_ctx
@catch_errors
def resume(ctx):
    """Proceed doing a task that has been paused."""
    pause = db.table("pause")
    doing = db.table("doing")
    Task = Query()
    try:
        doing.update(tdb_set('resume_at', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                                          Task.task_id == doing.all()[-1]['task_id'])
        pause.truncate()
    except IndexError:
        click.echo("There are not tasks being done now.")


"""
END:: rooyca
"""