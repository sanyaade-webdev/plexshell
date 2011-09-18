# plexshell (psh)

<http://github.com/jkp/plexshell>

A shell to interact with the Plex Media Server

# What does it do?

psh is a command-line interface to interact with Plex Media Server instances.  It is primarily aimed at Plex plugin authors who would like a lightweight way to interact with PMS whilst developing their plugins.

It provides the following functionality at present:

* Directory navigation (cd, pwd).
* Directory listing (ls).
* Fetch arbitary resources and dump the XML (get).
* Perform searches when plugins support it.
* Get and set preferences for plugins.
* Restart a plugin (restart).
* Initiate plugin auto-update (update).
* Run a user-provided script non-interactively (very useful for testing specific functionality repeatedly in development).

# Where is the documentation?

You're looking at it!  Further help can be obtained by issuing the help command from the shell prompt or using the --help switch on the command-line.

# License

Open Source MIT License.
