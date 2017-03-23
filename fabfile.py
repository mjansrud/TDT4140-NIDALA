from fabric.api import env, run, cd

env.hosts = ['beta.nidala.no']
root_folder = '/srv/'
website_folder = 'TDT4140-NIDALA'
projects = {
        'beta': {
            'repo_folder': 'beta.nidala.no'
        },
        'nidala': {
            'repo_folder': 'nidala.no'
        }
}

def deploy(project='beta', ref='master'):
    with cd(root_folder + projects[project]['repo_folder'] + '/' + website_folder):
        run('git fetch --all')
        run('git checkout {0}'.format(ref))
        run('git reset --hard origin/{0}'.format(ref))
    with cd(root_folder + projects[project]['repo_folder']):
        run('./startserver.sh', pty=False)
