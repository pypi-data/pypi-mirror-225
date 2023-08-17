
from citros import Citros, __version__ as citros_version
from getpass import getpass
from os import linesep
import git
from pathlib import Path

from InquirerPy import prompt
from prompt_toolkit.validation import Validator, ValidationError


DEFAULT_SIMULATION_TIMEOUT = 10*60  # in seconds

class NumberValidator(Validator):
    """
    small helper class for validating user input during an interactive session.
    """
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(message="Please enter a number",
                                  cursor_position=len(document.text))

############################# Helper functions ################################

#### for dev only
# def dev_test():
#     with Citros() as citros:
#         pass


def print_citros():
    print (f"""
==============================================
 ██████╗██╗████████╗██████╗  ██████╗ ███████╗
██╔════╝██║╚══██╔══╝██╔══██╗██╔═══██╗██╔════╝
██║     ██║   ██║   ██████╔╝██║   ██║███████╗
██║     ██║   ██║   ██╔══██╗██║   ██║╚════██║
╚██████╗██║   ██║   ██║  ██║╚██████╔╝███████║
 ╚═════╝╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
==============================================
CITROS CLI tool for interaction with the CITROS system. V[{citros_version}]
    """)


def generate_question(type, name, message, choices=None, validator=None, filter=None):
    if type not in ["list", "raw_list", "expand", "confirm",
                    "check_box", "input", "password", "editor"]:
        print("question type not supported.")
        return {}

    if type == "list":
        if not choices:
            print("Nothing to choose from.")
            return {}
        return {
            "type": type,
            "name": name,
            "message": message,
            "choices": choices
        }
    elif type == "input":
        return {
            f"type":type,
            f"name":name,
            f"message": message,
            f"validate": validator,
            f"filter": filter
        }
    else:
        raise NotImplementedError()


def is_git_repo(path):
    try:
        _ = git.Repo(path).git_dir
        return True
    except git.InvalidGitRepositoryError:
        return False

############################# CLI implementation ##############################

def init_project(args, argv):
	with Citros(user_proj_dir=args.dir, verbose=args.verbose, debug=args.debug, on_init=True) as citros:
		citros_path = citros.CITROS_REPO_DIR

		if not is_git_repo(citros.USER_PROJ_DIR):
			citros.print(f"The project directory `{citros.USER_PROJ_DIR}` is not a valid git repo.{linesep}" + \
						 f"If you are running inside a devcontainer, make sure the directory " + \
						 f"is not a git submodule.", color='red')
			return

		if citros.check_project(True):
			citros.print(f"The directory {Path(args.dir).resolve()} has already been initialized.", color='yellow')

			# check .git was not corrupted or deleted
			if not is_git_repo(citros_path):
				citros.print(f"The Citros directory {citros_path} is not a valid git repository.", color='red')
				return

			citros_remote = citros.get_citros_remote()
			if citros_remote:
				citros.print(f"working remotely with [{citros_remote}].")
				return

			if not citros.isAuthenticated():
				citros.print("No remotes found and user is not logged in. Working offline.")
			else:
				citros.print(f"You are logged in but have yet to add a remote repo.{linesep}" + \
							 f"To add a remote repo, call the following citros commands:")
				citros.print(f"citros setup-ssh{linesep}citros add-remote", color='cyan')
				citros.print(f"It is also recommended that you than run")
				citros.print(f"citros status", color='cyan')
				citros.print(f"and resolve any conflicts you may have with the remote.")
			
			return

		if not citros.isAuthenticated():
			citros.print("User is not logged in. Initialzing Citros locally.")

			# init repo and work offline
			repo = git.Repo.init(path=citros_path)

			success = citros.internal_sync(True)

			if success:
				citros.try_commit("first commit")
				citros.update_gitignore(citros.USER_PROJ_DIR, ".citros*")
			else:
				# sanity - should never happen.
				citros.print(f"internal_sync on init failed.", color='red')

		else:
			citros.print("Setting up ssh...")
			citros.setup_ssh()

			citros.print("Updating Citros...")
			citros_remote = citros.get_citros_remote_from_api()

			if citros_remote:
				citros.print("Waiting for repo to be ready...")
				
				# it may take a few seconds for the repo to be available on the remote.
				if not citros.wait_till_repo_ready():
					citros.print("Unfortunately something went wrong with the remote repo. " + \
								 "Please try again in a few moments.", color='yellow')
					return

				# if a new repo was created on the remote, an empty repo will be cloned.
				repo = citros.clone_repo(citros_path, citros_remote)

				# write the repo id to file
				with open(citros.REPO_ID_FILE, 'w') as file:
					file.write(citros.repo_id)

				citros.print(f"Citros repo successfully cloned from remote.", color='magenta')

				first_commit = citros.is_repo_empty(repo)

				success = citros.internal_sync(True)

				if success:
					citros.print(f"Citros successfully synched with local project.")

					if first_commit:
						if citros.try_commit("first commit"):
							citros.git_push()
							citros.print(f"All changes committed and pushed to citros.", color='magenta')

							citros.update_gitignore(citros.USER_PROJ_DIR, ".citros*")
					else:
						citros.print(f"You may review your changes via `citros status` " + \
									 f"and commit them via `citros commit`.", color='magenta')
				else:
					citros.print("Failed to sync citros with local project. " + \
								 "Your working directory is likely different than the remote. " + \
								 "Make sure your working directory is clean and that your " + \
								 "local repo is up to date with the remote (e.g. github).", color='red')
			else:
				citros.print(f"Failed to get citros remote url.", color='red')
				return

		citros.print(f"Intialized Citros repository.", color='green')


def setup_ssh(args, argv):
    with Citros(verbose=args.verbose, debug=args.debug) as citros: 
        if not citros.isAuthenticated():
            citros.print(f"Cannot setup ssh while not logged in. Login and try again.", color='red')
            return
        citros.setup_ssh()


def status(args, argv):
	with Citros(user_proj_dir=args.dir, verbose=args.verbose, debug=args.debug) as citros: 
		if not citros.is_initialized:
			citros.print(f"Cannot check status. {args.dir} has not been initialized.", color='red')
			return

		citros.internal_sync()

		citros.print(git.Repo(citros.CITROS_REPO_DIR).git.status())


def add_remote(args, argv):
	with Citros(user_proj_dir=args.dir, verbose=args.verbose, debug=args.debug) as citros: 
		if not citros.is_initialized:
			citros.print(f"Cannot add remote. {args.dir} has not been initialized.", color='red')
			return

		citros_remote = citros.get_citros_remote_from_api()
		if citros_remote:
			citros.add_remote(citros.CITROS_REPO_DIR, 'origin', citros_remote)
			citros.print(f"Successfully added remote [{citros_remote}].", color='magenta')
		else:
			citros.print(f"Failed to get citros remote url.", color='red')


def commit(args, argv):
    with Citros(user_proj_dir=args.dir, verbose=args.verbose, debug=args.debug) as citros: 
        if not citros.is_initialized:
            citros.print(f"Cannot commit. {args.dir} has not been initialized.", color='red')
            return

        citros.try_commit(args.message)
        

def push(args, argv):
    with Citros(user_proj_dir=args.dir, verbose=args.verbose, debug=args.debug) as citros:
        if not citros.is_initialized:
            citros.print(f"Cannot push. {args.dir} has not been initialized.", color='red')
            return

        citros.git_push(args.branch)


def pull(args, argv):
    with Citros(user_proj_dir=args.dir, verbose=args.verbose, debug=args.debug) as citros:
        if not citros.is_initialized:
            citros.print(f"Cannot pull. {args.dir} has not been initialized.", color='red')
            return

        citros.git_pull(args.branch)


def login(args, argv): 
    with Citros(verbose=args.verbose, debug=args.debug) as citros:       
        username, password = args.username, args.password

        if not citros.isAuthenticated() and (args.username is None or args.password is None):        
            username = input("email: ")        
            password = getpass()            
        resp = citros.login(username, password) 
        if resp:
            citros.print("User logged in.", color='green')
        else:
            citros.print("Failed to log in. Please try again.", color='red')

    
def logout(args, argv):
    with Citros(verbose=args.verbose, debug=args.debug) as citros: 
        citros.logout() 
        citros.print("User logged out.")


def list_project(args, argv):
    with Citros(user_proj_dir=args.dir, verbose=args.verbose, debug=args.debug) as citros:
        if not citros.is_initialized:
            citros.print(f"Cannot list. {args.dir} has not been initialized.", color='red')
            return

        simulations = citros.get_simulations()
        i = 1
        for s in simulations:
            citros.print(f"{str(i)}. {s}")
            i = i + 1


def run(args, argv):
	"""
	:param args.dir
	:param args.simulation_name:
	:param args.batch_id:
	:param args.run_id:
	:param args.remote:
	:param args.timeout:
	:param args.completions:
	:param args.debug:
	:param args.batch_name:
	:param args.batch_message:
	:param args.verbose:
    :param args.key:
	"""   
	sim_name, batch_id, run_id = args.simulation_name, args.batch_id, args.run_id
	remote, timeout, completions = args.remote, args.timeout, args.completions
	
	with Citros(user_proj_dir=args.dir, verbose=args.verbose, debug=args.debug) as citros:
		if not citros.is_initialized:
			citros.print(f"Cannot run. {args.dir} has not been initialized.", color='red')
			return
                
		if not Path(citros.USER_PROJ_DIR,'install').exists():
			citros.print(f"Cannot run. `install` directory was not found. " + \
                		 f"Run `colcon build` first.", color='red')
			return

		if args.key:
			citros.set_auth_key(args.key, args.dir)

		loggedin = citros.isAuthenticated()

		if remote and not loggedin:
			citros.print(f"Cannot run remotely - please log in first.", color='red')
			return

		success = citros.internal_sync(False)

		if not success:
			citros.print(f"internal_sync before run failed. Cannot run.{linesep}" + \
						 f"Fix the errors in your project configuration files and try again.", color='red')
			return

		success = citros.set_batch_name_and_message(args.batch_name, args.batch_message)

		if not success:
			citros.print(f"Please try again with all required command parameters.", color='yellow')
			return

		if batch_id:
			if not citros.CITROS_ENVIRONMENT == 'CLUSTER':
				raise ValueError("cannot run batch on non CLUSTER environment.")
			citros.run_simulation_by_k8s(batch_id, run_id, timeout)
		elif sim_name:
			citros.run_simulation(sim_name, completions, timeout, remote)
		else:
			# simulation is chosen by the user 
			run_interactively(citros, completions, timeout, remote)


def run_interactively(citros : Citros, completions, timeout, remote):
    sim_names = citros.get_simulations()
    
    # sanity check - should never happen because internal_sync will fail if there 
    #                isn't at least one simulation file.
    if not sim_names:
        citros.print(f"There are currently no simulations in your {citros.SIMS_DIR} folder. \
                	 Please create at least one simulation for your project.", color='red')
        return
    
    sim_names_q = generate_question("list", "sim_names", 
                                    "Please choose the simulation you wish to run", sim_names )
    #completions_q = generate_question("input", "completions", "Please enter number of completions:",
    #                                  NumberValidator, lambda val: int(val))
    answers = prompt([sim_names_q])  # use default style
    sim_name = answers.get("sim_names")

    citros.run_simulation(sim_name, completions, timeout, remote)


def docker_login(args, argv):
    with Citros(verbose=args.verbose, debug=args.debug) as citros: 
        citros.docker_login()                      


def docker_build(args, argv):
    with Citros(user_proj_dir=args.dir, verbose=args.verbose, debug=args.debug) as citros:
        if not citros.is_initialized:
            citros.print(f"{args.dir} has not been initialized.",color='red')
            return
        
        citros.build_docker_image([f"{args.image_name}:{args.tag}"])


def docker_build_push(args, argv):
    with Citros(user_proj_dir=args.dir, verbose=args.verbose, debug=args.debug) as citros:
        if not citros.is_initialized:
            citros.print(f"{args.dir} has not been initialized.",color='red')
            return

        if not citros.isAuthenticated():
            citros.print(f"Please log in to Citros first.", color='red')
            return
        
        if not citros.is_logged_in_to_docker():
            citros.print("Logging in to docker...")
            citros.docker_login()
        
        success = citros.build_and_push_docker_image(args.image_name)

        if not success:
            citros.print(f"Failed to build or push.", color='red')


#def docker(args, argv):
#    # TODO: login to docker first
#    os.system('docker ' + ' '.join(argv))
 
